import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import time

start_time=time.time()
df=pd.read_excel("Datasets/doubled_dataset.xlsx")

x=df[["Glucose","Blood pressure","Skin thickness","Insulin","Body mass index","Diabetes pedigree function","Age"]]
y=df["Outcome"]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)

model=GradientBoostingClassifier(n_estimators=350,random_state=42,max_depth=2,learning_rate=0.5)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

end_time=time.time()
accuracy=accuracy_score(y_test,y_pred)
print(accuracy*100)
print("Time Taken: ",end_time-start_time,"seconds")

# To Save The Model
# joblib.dump(model,"ImprovedDiabetesModel.pkl")

