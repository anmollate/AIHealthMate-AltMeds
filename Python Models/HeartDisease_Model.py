import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import joblib
import time

df=pd.read_csv("Datasets/heart.csv")

start_time=time.time()

x=df[["Age","ChestPainType","RestingBP","Cholesterol","FastingBS","Re1ingECG","MaxHR","ExerciseAngina","Oldpeak","ST_Slope"]]
y=df["HeartDisease"]

x_train,x_test,y_train,y_test=train_test_split(x,y,random_state=42,test_size=0.2)
model=GradientBoostingClassifier(n_estimators=50,random_state=42,learning_rate=0.2,max_depth=2)
model.fit(x_train,y_train)

y_pred=model.predict(x_test)

end_time=time.time()

accuracy=accuracy_score(y_test,y_pred)
print("Accuracy:",accuracy*100,"Time Required:",end_time-start_time)

joblib.dump(model,"HeartDisease_Model.pkl")