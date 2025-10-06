import pandas as pd
import joblib
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import numpy as np
import re
from PIL import Image
import pytesseract
import cv2
import io
import os

app = Flask(__name__)
CORS(app)

# Load the saved model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "Models")

# Load all models with absolute paths
Diabetesmodel = joblib.load(os.path.join(MODELS_DIR, "ImprovedDiabetesModel.pkl"))
Anemiamodel = joblib.load(os.path.join(MODELS_DIR, "Anemia_Model.pkl"))
KidneyDiseaseModel = joblib.load(os.path.join(MODELS_DIR, "KidneyDisease_Model.pkl"))
LiverDiseaseModel = joblib.load(os.path.join(MODELS_DIR, "Liver_Disease_Model.pkl"))
HeartDiseaseModel = joblib.load(os.path.join(MODELS_DIR, "HeartDisease_Model.pkl"))

pattern = r"([A-Za-z ()]+)[^\d]*([\d]+\.?\d*)[^\d]+([\d]+\.?\d*)-([\d]+\.?\d*)"

def extract_vitals_from_image_bytes(image_bytes):
    # Open image from bytes, convert to grayscale using OpenCV for better OCR
    image_stream = io.BytesIO(image_bytes)
    pil_img = Image.open(image_stream).convert("RGB")
    cv_img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)

    # Optional preprocessing for better OCR:
    # gray = cv2.medianBlur(gray, 3)
    # _, gray = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)

    pil_for_ocr = Image.fromarray(gray)

    # Run pytesseract
    text = pytesseract.image_to_string(pil_for_ocr, config='--psm 6')

    vitals_found = {}
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.search(pattern, line)
        if match:
            vital_name = match.group(1).strip()
            try:
                value = float(match.group(2))
                lower = float(match.group(3))
                upper = float(match.group(4))
            except ValueError:
                continue

            vitals_found[vital_name] = {
                "value": value,
                "lower": lower,
                "upper": upper,
                "raw_line": line
            }

    return vitals_found, text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/medicines')
def medicines():
    return render_template('medicines.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/disease')
def disease():
    return render_template('disease.html')

@app.route('/ReportAnalyzer')
def Report():
    return render_template('ReportAnalyzer.html')


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

@app.route("/api/ocr", methods=["POST"])
def ocr():
    if "image" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    try:
        image_bytes = file.read()
        vitals, raw_text = extract_vitals_from_image_bytes(image_bytes)
        return jsonify({"vitals": vitals, "raw_text": raw_text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500



if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0", port=5000)
