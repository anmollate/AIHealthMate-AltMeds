import pandas as pd

df=pd.read_excel('Medicine Dataset.xlsx')

MedName=input("Enter The Name Of Medicine: ")

row_matched=df[df['Product Name'].str.lower()==MedName.lower()]

if not row_matched.empty:
    salt_composition=row_matched.iloc[0]['salt_composition']
    print("Contents: ",salt_composition)
    usage=row_matched.iloc[0]['primary_use']
    print("Primary Usage: ",usage)

    similar_meds=df[df['salt_composition'].str.lower()==salt_composition.lower()]

    if not similar_meds.empty and len(similar_meds)!=1:
        for _,row in similar_meds.iterrows():
            print("Alternate Medicines: ",row['Product Name'],"     Contents: ",row['salt_composition'])
    else:
        print("No Alternatives Availabel At The Moment !")


else:
    print("Med Not Found!")