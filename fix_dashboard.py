import re

with open("templates/dashboard.html", "r") as f:
    html = f.read()

# 1. Fix Material Symbols Font
html = html.replace("</style>", """
        .material-symbols-outlined {
            font-family: 'Material Symbols Outlined' !important;
            font-size: 24px;
            font-weight: normal;
            font-style: normal;
            line-height: 1;
            letter-spacing: normal;
            text-transform: none;
            display: inline-block;
            white-space: nowrap;
            word-wrap: normal;
            direction: ltr;
        }
    </style>
""")

# 2. Fix Initial Dropzone State
html = html.replace('<h3 class="font-headline-md text-headline-md text-on-surface mb-xs">Red Herring Prospectus.docx</h3>', '<h3 class="font-headline-md text-2xl font-bold text-on-surface mb-xs" id="dropzone-title">Click or Drag & Drop Document Here</h3>')
html = html.replace('<p class="font-body-sm text-body-sm text-on-surface-variant mb-md">4.2 MB • Uploaded Today, 09:41 AM</p>', '<p class="font-body-sm text-sm text-on-surface-variant mb-md" id="dropzone-subtitle">Supported formats: .docx</p>')

# 3. Fix KPI cards overlapping text (reduce font sizes and add flex)
html = html.replace('font-display-lg text-display-lg', 'text-4xl font-bold whitespace-nowrap')

# 4. Hide download button until upload is complete, and fix its initial state
html = html.replace('pointer-events: none; opacity: 0.5;', 'pointer-events: none; opacity: 0.5; display: none;')
html = html.replace('btn.style.opacity = "1";', 'btn.style.opacity = "1"; btn.style.display = "inline-block";')

with open("templates/dashboard.html", "w") as f:
    f.write(html)
