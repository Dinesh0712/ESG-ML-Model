import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, HistGradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

#File contains all required data and esg score
ML_df = pd.read_csv('Fund_other_data.csv')
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

RFC = RandomForestClassifier()
HGBC = HistGradientBoostingClassifier()
DTC = DecisionTreeClassifier()

for i in [RFC, HGBC, DTC]:
    i.fit(X_train, y_train)
    y_pred = i.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(i, accuracy)