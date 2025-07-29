import pandas as pd
import streamlit as st

# Load data
df = pd.read_excel('Medicine.xlsx')

# Title
st.markdown("## 💊Search For Your Desired Medicines")

# Input field
MedName = st.text_input("🔍 Enter the name of the medicine:")

# Process if user enters input
if MedName:
    row_matched = df[df['Name'].str.lower() == MedName.lower()]

    if not row_matched.empty:
        st.success("✅ Medicine Found!")

        # Display primary info
        imagepath="images/"+row_matched.iloc[0]['Image']
        st.image(imagepath, caption=row_matched.iloc[0]['Image'], width=250)
        st.markdown(f"**🏭 Marketer:** {row_matched.iloc[0]['Marketer']}")
        st.markdown(f"**🧪 Contents:** {row_matched.iloc[0]['Contents']}")
        st.markdown(f"**📌 Primary Usage:** {row_matched.iloc[0]['Primary Usage']}")
        st.markdown(f"**💵 Price: ₹** {row_matched.iloc[0]['Mrp']} **/-**")

        # Search for alternatives
        salt = row_matched.iloc[0]['Contents'].lower()
        similar_meds = df[(df['Contents'].str.lower() == salt) & (df['Name'].str.lower() != MedName.lower())]

        # Display alternatives
        if not similar_meds.empty:
            st.markdown("### 🔁 Alternative Medicines:")
            for _, row in similar_meds.iterrows():
                imagepath="images/"+row['Image']
                st.image(imagepath, caption=row['Name'], width=250)
                st.markdown(f"- **{row['Name']}** &nbsp;&nbsp; _({row['Contents']})_")
        else:
            st.warning("⚠️ No alternative medicines available at the moment.")
    else:
        st.error("❌ Medicine not found!")
