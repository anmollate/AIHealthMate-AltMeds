import pandas as pd
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

app = Flask(__name__)
CORS(app)

# Load the saved model
Diabetesmodel = joblib.load("Models/ImprovedDiabetesModel.pkl")
Anemiamodel= joblib.load("Models/Anemia_Model.pkl")
KidneyDiseaseModel=joblib.load("Models/KidneyDisease_Model.pkl")
LiverDiseaseModel=joblib.load("Models/Liver_Disease_Model.pkl")
HeartDiseaseModel=joblib.load("Models/HeartDisease_Model.pkl")

@app.route("/DiabetesPredict", methods=["POST"])
def predict_diabetes():
    data = request.json  # Get JSON data from frontend

    # Extract and convert to float
    glucose = float(data.get("Glucose"))
    bp = float(data.get("BP"))
    st = float(data.get("ST"))
    ins = float(data.get("INS"))
    bmi = float(data.get("BMI"))
    dpf = float(data.get("DPF"))
    age = float(data.get("Age"))

    # Prepare features in correct order
    vitals = np.array([[glucose, bp, st, ins, bmi, dpf, age]])

    # Make prediction
    prediction = Diabetesmodel.predict(vitals)[0]  

    return prediction

@app.route("/AnemiaPredict", methods=["POST"])
def predict_anemia():
    data=request.json

    hemoglobin=float(data.get("hemoglobin"))
    hematocrit=float(data.get("hematocrit"))
    MCV=float(data.get("MCV"))
    MCH=float(data.get("MCH"))
    RDW=float(data.get("RDW"))

    vitals=np.array([[hemoglobin,hematocrit,MCV,MCH,RDW]])

    prediction=Anemiamodel.predict(vitals)[0]

    return prediction

@app.route("/KidneyDiseasePredict", methods=["POST"])
def predict_KidneyDisease():
    data=request.json    
    Creatinine=float(data.get("Creatinine"))
    BUN=float(data.get("BUN"))
    eGFR=float(data.get("eGFR"))
    Potassium=float(data.get("Potassium"))
    Bicarbonate=float(data.get("Bicarbonate"))


    vitals=np.array([[Creatinine,BUN,eGFR,Potassium,Bicarbonate]])

    prediction=KidneyDiseaseModel.predict(vitals)[0]

    return prediction

@app.route("/LiverDiseasePredict",methods=["POST"])
def predict_LiverDisease():
    data=request.json
    Age=float(data.get("Age"))
    Total_Bilirubin=float(data.get("Total_Bilirubin"))
    Direct_Bilirubin=float(data.get("Direct_Bilirubin"))
    Alkaline_Phosphatase=float(data.get("Alkaline_Phosphatase"))
    Alanine_Aminotransferase=float(data.get("Alanine_Aminotransferase"))
    Aspartate_Aminotransferase=float(data.get("Aspartate_Aminotransferase"))
    Total_Proteins=float(data.get("Total_Proteins"))
    Albumin=float(data.get("Albumin"))
    Albumin_And_Globulin_Ratio=float(data.get("Albumin_And_Globulin_Ratio"))

    vitals=np.array([[Age,Total_Bilirubin,Direct_Bilirubin,Alkaline_Phosphatase,Alanine_Aminotransferase,Aspartate_Aminotransferase,Total_Proteins,Albumin,Albumin_And_Globulin_Ratio]])

    prediction=LiverDiseaseModel.predict(vitals)[0]
    return str(prediction)

@app.route("/HeartDiseasePredict",methods=["POST"])
def predict_HeartDisease():
    data=request.json
    Age=float(data.get("Age"))
    ChestPainType=float(data.get("ChestPainType"))
    RestingBP=float(data.get("RestingBP"))
    Cholesterol=float(data.get("Cholesterol"))
    FastingBS=float(data.get("FastingBS"))
    RelingECG=float(data.get("RelingECG"))
    MaxHR=float(data.get("MaxHR"))
    ExerciseAngina=float(data.get("ExerciseAngina"))
    Oldpeak=float(data.get("Oldpeak"))
    ST_Slope=float(data.get("ST_Slope"))

    vitals=np.array([[Age,ChestPainType,RestingBP,Cholesterol,FastingBS,RelingECG,MaxHR,ExerciseAngina,Oldpeak,ST_Slope]])

    prediction=HeartDiseaseModel.predict(vitals)[0]

    return str(prediction)



if __name__ == "__main__":
    app.run(debug=True)
