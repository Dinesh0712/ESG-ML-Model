import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

#File contains all required data and esg score
ML_df = pd.read_csv('Fund_Datas.csv')
ML_df.dropna(subset=['esg_score'], inplace=True)
ML_df.value_counts()

# get the test and training datas
y = ML_df['grade']
#y.head() #comment out when testing data
X = ML_df.drop(['esg_score','grade'], axis=1)
#X.head() #comment out when testing data

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2
)

model = RandomForestClassifier()

model.fit(X_train, y_train)
y_pred = model.predict(X_test)
# accuracy = accuracy_score(y_test, y_pred)
# print(accuracy) #comment out when not training

#Exporting model
ref_cols = list(X.columns)
target = 'grade'

joblib.dump(value=[model,ref_cols,target], filename='../../ESG_ML_Model/model.pkl')
