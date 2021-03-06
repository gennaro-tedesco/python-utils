import pandas as pd 
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from src.utils import *

def train_rfr_model(estimator, train_features, train_actuals):
	assert isinstance(train_features, pd.DataFrame)
	assert isinstance(estimator, RandomForestRegressor)	
	param_grid = { 
			"n_estimators": [100, 200, 500, 1000],
			"max_features": ["auto", "sqrt", "log2"]
			}

	rfr_gscv = GridSearchCV(estimator, param_grid, n_jobs=-1, cv=10, scoring='r2')
	rfr_gscv.fit(train_features, train_actuals)
	print("best parameters are: {}".format(rfr_gscv.best_estimator_))
	print("best validation r2 training score is: {}".format(rfr_gscv.best_score_))
	return rfr_gscv.best_estimator_

def rfr_main(data_df):
	assert isinstance(data_df, pd.DataFrame)
	actuals = get_regressor_actuals(data_df)
	encoded_df = get_regressor_encoding(data_df)  
	feat_vectors, features_names = get_regressor_features(encoded_df) 

	train_features, test_features, train_actuals, test_actuals = get_split(feat_vectors, actuals)
	train_features, test_features = get_scaling(train_features, test_features)

	print("training random forest regressor...")
	estimator = RandomForestRegressor()
	rfr_model = train_rfr_model(estimator, train_features, train_actuals)
	test_pred = pd.Series(rfr_model.predict(test_features))

	print_regression_summary(test_actuals, test_pred)
	feature_importances = pd.Series(rfr_model.feature_importances_, index=features_names).sort_values(ascending=False)
	print("\nfeatures importance")
	print(feature_importances)
	plot_regressor_predictions(test_actuals, test_pred)