import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
import dill as pickle
from sklearn.model_selection import train_test_split

def make_model(df):
    X = df.drop("Force_Level", axis=1)
    y = df.Force_Level
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=659)
    
    
    gbc3 = GradientBoostingClassifier(loss='deviance', learning_rate=0.1, n_estimators=1000,
                                random_state=659, verbose=1)
    
    gbc3.fit(X_train, y_train)
    
    with open('gbc3test.pkl', 'wb') as my_pickle:
        pickle.dump(gbc3, my_pickle)
    
    

    
    
if __name__ == "__main__":
    sampleall = pd.read_pickle("X.pkl")
    gbc3 = make_model(sampleall)

   