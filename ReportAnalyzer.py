import re
import pytesseract
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import cv2
import numpy as np

st.subheader("HEALTH REPORT ANALYZER🩺📊")
image=st.file_uploader("Upload Your Blood Report Image:",type=["png","jpg","jpeg","webp"])
if image is not None:
    img_cv=Image.open(image)
    gray=cv2.cvtColor(np.array(img_cv),cv2.COLOR_BGR2GRAY)
    img=Image.fromarray(gray)

    # image_path='cbc-report-format.png'
    # img=Image.open(image_path)
    vitals_found = {}
    text=pytesseract.image_to_string(img,config='--psm 6')
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

    # print(vitals_found)

    for vital,data in vitals_found.items():
        value=data['value']
        lower=data['lower']
        upper=data['upper']

        st.title(f'{vital} Level')
        fig,ax=plt.subplots(figsize=(6,4))

        ax.fill_between([0,1],lower,upper,color='lightgreen',alpha=0.5,label=f"Normal {vital} Level")

        ax.plot([0,1],[value,value],'r-',linewidth=2,label='Observed Value')
        ax.text(0.5,value,f'{value}',va='center',color='black')

        ax.set_xticks([])
        ax.set_ylabel(vital)
        ax.set_title(f"{vital} Level")
        ax.legend()

        # Show plot in Streamlit
        st.pyplot(fig)
        st.write(f"{vital} Analysis:")
        if value < lower:
            st.write(f"⚠️ {vital} is **below the normal range** ({lower}-{upper})")
        elif value > upper:
            st.write(f"⚠️ {vital} is **above the normal range** ({lower}-{upper})")
        else:
            st.write(f"✅ {vital} is **within the normal range** ({lower}-{upper})")




