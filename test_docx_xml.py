from docx import Document
from docx.text.paragraph import Paragraph
import docx

doc = Document()
doc.add_paragraph("Test")
print("Paragraph added")
for p in doc.element.xpath('.//w:p'):
    para = Paragraph(p, doc)
    print(para.text)

print("Imports worked")
