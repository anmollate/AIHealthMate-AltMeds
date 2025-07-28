import pandas as pd
import streamlit as st

df=pd.read_excel('Medicine Dataset.xlsx')

st.subheader("Search Medicines🔍💊")
MedName=st.text_input("Enter The Name Of Medicine: ")

row_matched=df[df['Product Name'].str.lower()==MedName.lower()]

if not row_matched.empty:
    salt_composition=row_matched.iloc[0]['salt_composition']
    st.write("Contents: ",salt_composition)
    usage=row_matched.iloc[0]['primary_use']
    st.write("Primary Usage: ",usage)

    similar_meds=df[df['salt_composition'].str.lower()==salt_composition.lower()]

    if not similar_meds.empty and len(similar_meds)!=1:
        for _,row in similar_meds.iterrows():
            st.write("Alternate Medicines: ",row['Product Name'],"     Contents: ",row['salt_composition'])
    else:
        st.write("No Alternatives Availabel At The Moment !")
else:
    st.write("Med Not Found!")