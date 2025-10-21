import re
import pytesseract
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import cv2
import numpy as np
import fitz  # PyMuPDF
import io

st.subheader("HEALTH REPORT ANALYZER 🩺📊")

# Accept both image and PDF files
uploaded_file = st.file_uploader("Upload Your Blood Report (Image or PDF):", type=["png", "jpg", "jpeg", "webp", "pdf"])

if uploaded_file is not None:
    images = []

    # ✅ If PDF, convert pages to images using PyMuPDF (no Poppler needed)
    if uploaded_file.type == "application/pdf":
        pdf_bytes = uploaded_file.read()
        pdf_doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        for page in pdf_doc:
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            images.append(img)
    else:
        # ✅ If image, just read it
        img = Image.open(uploaded_file)
        images = [img]

    vitals_found = {}
    summary_analysis = []  # To store summary of all vitals

    # Process each image/page
    for img_cv in images:
        gray = cv2.cvtColor(np.array(img_cv), cv2.COLOR_BGR2GRAY)
        img = Image.fromarray(gray)

        text = pytesseract.image_to_string(img, config='--psm 6')
        pattern = r"([A-Za-z ()]+)[^\d]*([\d]+\.?\d*)[^\d]+([\d]+\.?\d*)-([\d]+\.?\d*)"

        for line in text.splitlines():
            match = re.search(pattern, line)
            if match:
                vital_name = match.group(1).strip()
                value = float(match.group(2))
                lower = float(match.group(3))
                upper = float(match.group(4))

                vitals_found[vital_name] = {
                    "value": value,
                    "lower": lower,
                    "upper": upper
                }

    # Display extracted results and create summary
    for vital, data in vitals_found.items():
        value = data['value']
        lower = data['lower']
        upper = data['upper']

        st.title(f'{vital} Level')
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.fill_between([0, 1], lower, upper, color='lightgreen', alpha=0.5, label=f"Normal {vital} Level")
        ax.plot([0, 1], [value, value], 'r-', linewidth=2, label='Observed Value')
        ax.text(0.5, value, f'{value}', va='center', color='black')
        ax.set_xticks([])
        ax.set_ylabel(vital)
        ax.set_title(f"{vital} Level")
        ax.legend()

        st.pyplot(fig)

        # Individual analysis
        if value < lower:
            analysis = f"⚠️ {vital} is below the normal range ({lower}-{upper})"
        elif value > upper:
            analysis = f"⚠️ {vital} is above the normal range ({lower}-{upper})"
        else:
            analysis = f"✅ {vital} is within the normal range ({lower}-{upper})"
        
        st.write(f"{vital} Analysis:")
        st.write(analysis)

        # Add to summary
        # summary_analysis.append(f"{vital}: {analysis}")
        if "below" in analysis.lower() or "above" in analysis.lower():
            summary_analysis.append(f"{vital}: {analysis}")

    # Display summary at the end
    if summary_analysis:
        st.subheader("📋 Summary of All Vitals")
        for item in summary_analysis:
            st.write(item)
