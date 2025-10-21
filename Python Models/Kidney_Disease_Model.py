from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pandas as pd
import joblib
import time

df=pd.read_csv("Datasets/kidney_disease_balanced_6000.csv")
start_time=time.time()
x=df[["Creatinine (mg/dL)","BUN (mg/dL)","eGFR","Potassium (mmol/L)","Bicarbonate (mmol/L)"]]
y=df["Kidney_Stage"]

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)

model=GradientBoostingClassifier(n_estimators=50,random_state=42,max_depth=2,learning_rate=0.5)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

end_time=time.time()
accuracy=accuracy_score(y_test,y_pred)
print(accuracy*100)
print("Time Required: ",end_time-start_time,"Seconds")

# joblib.dump(model,"KidneyDisease_Model.pkl")