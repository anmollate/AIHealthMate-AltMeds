import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import joblib
from sklearn.model_selection import train_test_split
import time

start_time=time.time()
df=pd.read_csv("Datasets/anemia_diagnosis_5000.csv")

x=df[["Hemoglobin (g/dL)","Hematocrit (%)","MCV (fL)","MCH (pg)","RDW (%)"]]
y=df["Diagnosis"]

x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.2,random_state=42)

model=GradientBoostingClassifier(n_estimators=125,random_state=42,max_depth=2,learning_rate=0.5)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

end_time=time.time()
accurracy=accuracy_score(y_test,y_pred)
print("Accurracy: ",accurracy*100)
print("Time Taken: ",end_time-start_time)

# Saving The Model
# joblib.dump(model,"Anemia_Model.pkl")

