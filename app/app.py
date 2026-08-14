import reflex as rx
import os
import json
import asyncio
from typing import List, Dict, Any

# Import the existing redaction pipeline logic
from redact_pii import process_document

class State(rx.State):
    """The app state."""
    
    # State variables
    recall: str = "0.0"
    precision: str = "0.0"
    accuracy: str = "0.0"
    total_redacted: str = "0"
    
    audit_data: List[Dict[str, str]] = []
    
    processing: bool = False
    download_ready: bool = False
    output_file_path: str = ""
    
    @rx.background
    async def handle_upload(self, files: List[rx.UploadFile]):
        """Handle the file upload and trigger processing in the background."""
        async with self:
            self.processing = True
            self.download_ready = False
        
        # Get the uploaded file
        if not files:
            async with self:
                self.processing = False
            return
            
        file = files[0]
        upload_data = await file.read()
        
        # Save to upload dir
        upload_dir = rx.get_upload_dir()
        os.makedirs(upload_dir, exist_ok=True)
        
        input_path = os.path.join(upload_dir, file.filename)
        with open(input_path, "wb") as f:
            f.write(upload_data)
            
        # Trigger redaction script in a separate thread to avoid freezing the UI
        loop = asyncio.get_event_loop()
        raw_output_path = await loop.run_in_executor(None, process_document, input_path)
        
        # Move it to assets so it can be downloaded via URL
        assets_dir = os.path.join(os.getcwd(), "assets")
        os.makedirs(assets_dir, exist_ok=True)
        final_output_path = os.path.join(assets_dir, "redacted_document.docx")
        
        import shutil
        shutil.copy(raw_output_path, final_output_path)
        
        async with self:
            self.output_file_path = "/redacted_document.docx"
            # Update metrics after processing
            self.update_metrics()
            self.processing = False
            self.download_ready = True
        
    def update_metrics(self):
        """Read the output metrics and mapping data."""
        # Read from EVALUATION_REPORT.md for metrics
        try:
            with open("EVALUATION_REPORT.md", "r") as f:
                content = f.read()
                # Parse metrics from markdown
                for line in content.split('\\n'):
                    if "Recall:" in line:
                        self.recall = line.split(":")[-1].strip().replace("%", "")
                    elif "Precision:" in line:
                        self.precision = line.split(":")[-1].strip().replace("%", "")
                    elif "Accuracy:" in line:
                        self.accuracy = line.split(":")[-1].strip().replace("%", "")
        except FileNotFoundError:
            pass
            
        # Read audit data from JSON
        try:
            with open("pii_mapping.json", "r") as f:
                data = json.load(f)
                self.audit_data = [{"original": k, "fake": v} for k, v in data.items()]
                self.total_redacted = str(len(self.audit_data))
        except FileNotFoundError:
            pass

    @rx.var
    def get_audit_data(self) -> List[List[str]]:
        return [[item["original"], item["fake"]] for item in self.audit_data]

def index() -> rx.Component:
    return rx.center(
        rx.vstack(
            # Header
            rx.hstack(
                rx.heading("Presidio Vault", size="8", color="indigo"),
                rx.badge("Reflex UI Active", color_scheme="green", variant="solid"),
                justify="between",
                width="100%",
                padding_y="4",
                border_bottom="1px solid #334155"
            ),
            
            # Main Layout
            rx.hstack(
                # Dropzone
                rx.vstack(
                    rx.upload(
                        rx.vstack(
                            rx.button("Select .docx File", color_scheme="indigo"),
                            rx.text("Drag and drop files here or click to select files"),
                            align="center"
                        ),
                        id="upload_file",
                        border="2px dashed #475569",
                        padding="10",
                        width="100%",
                        border_radius="md",
                        multiple=False,
                        accept={
                            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
                        },
                        on_drop=State.handle_upload(rx.upload_files(upload_id="upload_file")),
                    ),
                    rx.cond(
                        State.processing,
                        rx.spinner(color="indigo", size="3"),
                        rx.text("Ready to process.")
                    ),
                    width="40%",
                    height="100%",
                    justify="start"
                ),
                
                # Metrics
                rx.vstack(
                    rx.hstack(
                        rx.card(rx.vstack(rx.text("Recall"), rx.heading(State.recall + "%", size="6", color="indigo")), width="100%"),
                        rx.card(rx.vstack(rx.text("Precision"), rx.heading(State.precision + "%", size="6", color="indigo")), width="100%"),
                    ),
                    rx.hstack(
                        rx.card(rx.vstack(rx.text("Accuracy"), rx.heading(State.accuracy + "%", size="6", color="indigo")), width="100%"),
                        rx.card(rx.vstack(rx.text("Entities Redacted"), rx.heading(State.total_redacted, size="6", color="indigo")), width="100%"),
                    ),
                    width="60%",
                    spacing="4"
                ),
                width="100%",
                spacing="6",
                padding_y="6"
            ),
            
            # Audit Table
            rx.heading("Anonymization Audit Log", size="6", padding_y="4"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Original Text"),
                        rx.table.column_header_cell("Anonymized Alternative"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.get_audit_data,
                        lambda row: rx.table.row(
                            rx.table.cell(row[0]),
                            rx.table.cell(row[1]),
                        )
                    )
                ),
                width="100%",
            ),
            
            # Action Panel
            rx.cond(
                State.download_ready,
                rx.button(
                    "Download Redacted .docx",
                    on_click=rx.download(
                        url=State.output_file_path,
                        filename="redacted_document.docx"
                    ),
                    color_scheme="green",
                    size="3",
                    margin_top="6"
                )
            ),
            width="80%",
            max_width="1200px",
            align="stretch"
        ),
        width="100vw",
        min_height="100vh",
        background_color="#0f172a",
        color="white",
        padding="6"
    )

app = rx.App(theme=rx.theme(appearance="dark", radius="large"))
app.add_page(index)
