#!/home/ur10pc/anaconda3/bin/python

from sklearn.decomposition import FastICA, PCA
from sklearn.ensemble import AdaBoostRegressor, ExtraTreesRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline, make_union
#from tpot.builtins import StackingEstimator
#from tpot.export_utils import set_param_recursive
import pandas as pd
import numpy as np
import pickle
import sys


def model(angle):

    # Construct dummy data frame to house
    dataw = pd.DataFrame([[angle, 20, 16, 40]], columns=['angle', 'hole', 'hose', 'force'])

    # Data has added synthetic data
    data0 = pd.read_csv('/home/ur10pc/Desktop/robot_data/un_normalised_data.csv', delimiter=',')
    data0 = pd.DataFrame(data0)
    data0.drop(data0.tail(1).index,inplace=True) # drop last n rows

    # Append new data-point to existing data for regularisation
    data0 = data0.append(dataw, ignore_index = True)

    # Regularisation over data including new datapoint.
    from sklearn.preprocessing import StandardScaler
    data = data0.drop('force', axis=1)
    scaler = StandardScaler()
    scaler.fit(data)
    data2 = scaler.transform(data)
    data2 = pd.DataFrame(data2)
    data2.columns= ['angle', 'hole', 'hose']

    # Concat regularised data (data2), back with target feature 'force' from data0.
    df2 = pd.concat([data2, data0['force']], axis=1)


    ###################################################################################

    # Train-Test-Split Data
    features = df2.drop('force', axis=1)
    training_features, testing_features, training_target, testing_target = \
                train_test_split(features, data0['force'], random_state=42)


    ###################################################################################
    ###################################################################################


    # Load Saved Model
    with open('/home/ur10pc/Desktop/robot_data/pickle/simple_model2.pkl','rb') as f:
        pipeline = pickle.load(f)

    ##################################################################################

     # Make New Prediction On New datapoint

    sample = features[-1:]

    result = pipeline.predict(sample)
    result = result[0]
    #print('hello',result)



    print(result)
    return result


if __name__ == "__main__":
    a = sys.argv[1]
    a = float(a)
    print(a)
    model(a)
