import pandas as pd
import numpy as np
import os 
import directories as d
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error,r2_score,mean_squared_error


def main():
    fname = os.path.join(d.data_dir, "MPs_in_all_snapshots.xlsx")
    df = pd.read_excel(fname)
    df = df.drop('id', axis=1)
    
    arr = df.to_numpy()
    array = np.zeros(shape=(3940, 11))
    
    x = 0
    for row in range(197):
        for i in range(20):
            y = 0
            for j in range(11):
                array[x][y] = arr[row][i+j]
                y += 1
            x += 1
    array = array.astype(int)
    
    df = pd.DataFrame(array)
    
    feature_cols = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    X = df[feature_cols]
    y = df[10]
    
    scaler = preprocessing.StandardScaler().fit(X)
    X_scaled = scaler.transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.25, random_state=1)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_pred = np.round(y_pred).astype(int)
    
    fname = os.path.join(d.tables_dir, "regression_evluation.csv")
    with open(fname, mode='a') as f:
        f.write(f"R^2, {r2_score(y_test, y_pred)}\n")
        f.write(f"MAE, {mean_absolute_error(y_test, y_pred)}\n")
        f.write(f"RMSE, {np.sqrt(mean_squared_error(y_test, y_pred))}")
        # print("R^2 : ", r2_score(y_test, y_pred))
        # print("MAE :", mean_absolute_error(y_test,y_pred))
        # print("RMSE:",np.sqrt(mean_squared_error(y_test, y_pred)))
    

if __name__ == "__main__":
    main()