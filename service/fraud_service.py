from urllib import request, response

import pandas as pd

import joblib
from sklearn.ensemble import RandomForestClassifier

from domain.domain import FraudRequest, FraudResponse

import tarfile
import joblib

class FraudService():
    def __init__(self):
        # Point this to the actual tarball file on disk
        self.path_to_model = 'artifacts/fraud_rf_model.pkl.tar.gz'
        self.model = self.load_artifact(self.path_to_model)

    def load_artifact(self, path_to_artifact):
        '''Load the model from inside the compressed tar.gz file.'''
        # 1. Open the tarball archive ('r:gz' means read with gzip compression)
        with tarfile.open(path_to_artifact, 'r:gz') as tar:
            
            # 2. Extract the specific .pkl file object from inside the archive
            model_file = tar.extractfile('fraud_rf_model.pkl')
            
            # 3. Pass the file stream straight to joblib
            artifact = joblib.load(model_file)
            
        return artifact
      
    def preprocess(self, request: FraudRequest) -> pd.DataFrame:
        data_dict = {
            'amount_usd': request.amount_usd,
            'transaction_dy': request.transaction_dy,
            'transaction_hr': request.transaction_hr,
            'transaction_min': request.transaction_min,
            'transaction_sec': request.transaction_sec,
            'device_type': request.device_type
        }
        
        data_dict['device_type']=data_dict['device_type'].lower()
        
        #encoding the device type using one-hot encoding
        data_dict['device_type_desktop'] = 1 if request.device_type == 'desktop' else 0
        data_dict['device_type_mobile'] = 1 if request.device_type == 'mobile' else 0
        data_dict['device_type_tablet'] = 1 if request.device_type == 'tablet' else 0
        
        data = pd.DataFrame([data_dict])

        data=data.drop(columns=['device_type'])

        return data
    
    def predict_fraud(self, request: FraudRequest) -> FraudResponse:
        # Convert the request to a DataFrame
        data = self.preprocess(request)
        
        # Predict fraud
        fraud_prediction = self.model.predict(data)[0]
        
        response = FraudResponse(is_fraud=int(fraud_prediction))
        return response

#test the service    
#if __name__ == "__main__":
 #   service = FraudService()
  #  request = FraudRequest(amount_usd=100, transaction_dy=1, transaction_hr=12, transaction_min=30, transaction_sec=45, device_type='mobile')
   # response = service.predict_fraud(request)
    #print(response)
    
    
    
#run: "python -m service.fraud_service" before running the above code, make sure to have the model and scaler artifacts in the specified paths.