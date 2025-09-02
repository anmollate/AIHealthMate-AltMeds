import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import time

df=pd.read_csv("Datasets/Liver_Disease_Dataset.csv")
start_time=time.time()

x=df[["Age","Total_Bilirubin","Direct_Bilirubin","Alkaline_Phosphatase","Alanine_Aminotransferase","Aspartate_Aminotransferase","Total_Proteins","Albumin","Albumin_and_Globulin_Ratio"]]
y=df["Result"]

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42,)
model=GradientBoostingClassifier(random_state=42,max_depth=3,n_estimators=50,learning_rate=0.2)
model.fit(x_train,y_train)
y_pred=model.predict(x_test)

end_time=time.time()
accuracy=accuracy_score(y_test,y_pred)
print("Accuracy: ",accuracy*100)
print("Time Required: ",end_time-start_time)

# joblib.dump(model,"Liver_Disease_Model.pkl")