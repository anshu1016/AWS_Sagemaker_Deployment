

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,precision_score
import sklearn
import joblib
import boto3
from io import StringIO
import argparse  
import os
import numpy as np  
import pandas as pd  

def model_fn(model_dir):
    clf = joblib.load(os.path.join(model_dir,'model.joblib'))
    return clf
if __name__=='__main__':
    print('[Info] Extracting arguments')
    parser = argparse.ArgumentParser()

    # Hyperparameters
    parser.add_argument('--n_estimators',type=int,default=100)
    parser.add_argument('--random_state',type=int,default=10)

    # Provide Data, Model and Output Directory
    parser.add_argument('--model-dir',type=str,default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train',type=str,default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test',type=str,default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--train-file',type=str,default='train-V-1.csv')
    parser.add_argument('--test-file',type=str,default='test-V-1.csv')


    args,_ = parser.parse_known_args()
    print('SKLearn version: ',sklearn.__version__)
    print('Joblib Version: ',joblib.__version__)

    print('[INFO] Reading Data')
    print()
    train_df = pd.read_csv(os.path.join(args.train,args.train_file))
    test_df = pd.read_csv(os.path.join(args.test,args.test_file))

    features= list(train_df.columns)
    label = features.pop(-1)
    
    print('Building Training and Testing Datasets')
    print()

    X_train = train_df[features]
    X_test = test_df[features]
    y_train = train_df[label]
    y_test = test_df[label]

    print("column Order: ")
    print(features)
    print()

    print('Label Column is : ',label)
    print()

    print('Data Schape: ')
    print()
    print('---- Shape of trainng Data(80%)----')
    print(X_train.shape)
    print(y_train.shape)
    print()

    print('---- Shape of Testing Data(20%)----')
    print(X_test.shape)
    print(y_test.shape)
    print()

    print('Training Random Forest Model...')
    print()
    model = RandomForestClassifier(n_estimators=args.n_estimators,random_state=args.random_state,verbose=2,n_jobs=-1)
    model.fit(X_train,y_train)

    print()
    model_path = os.path.join(args.model_dir,'model.joblib')
    joblib.dump(model,model_path)

    print('Model Saved at : ',model_path)

    y_pred_test = model.predict(X_test)
    test_acc = accuracy_score(y_test,y_pred_test)
    test_rep = classification_report(y_test,y_pred_test)

    print()
    print('-----METRICS RESULTS FOR TESTING DATA------')

    print()

    print('Total Rows are : ', X_test.shape[0])
    print('[TESTING] Model Accuracy is : ',test_acc)
    print('[TESTING] REPORT: ')
    print(test_rep)




