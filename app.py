import numpy as np
import datetime as dt
from flask import Flask, request, jsonify, render_template, url_for
import pickle
from common_methods import *
from build_variables import *
#from sql_connection import *

#cnxn = sql_connect()

app = Flask(__name__)

model = pickle.load(open('./model/RF_Model.sav','rb'))

@app.route('/')
def home():
	return render_template('home.html')


@app.route('/predict',methods = ['POST'])
def predict():
	int_features = [x for x in request.form.values()]
	print('int_features',int_features)

	start_date = dt.datetime.strptime(int_features[0], '%Y-%d-%m')
	end_date = dt.datetime.strptime(int_features[1], '%Y-%d-%m')

	test = pd.read_csv('./ratelock_master.csv', parse_dates = ["DateAdded"])
	#test = pd.read_sql(query, cnxn, parse_dates=["DateAdded"])

	test = test.set_index('LeadID')
	test_df = test[(test['DateAdded'] >= start_date) & (test['DateAdded'] <= end_date)]
	test_org = test_df.copy()

	testing = compile_test_df(test_df)
	dummy_test = dummies(testing)
	test_cols = dummy_test.columns.to_list()
	cols = Diff(dummy_features, test_cols)
	print('Missing Dummy columns: ', cols)

	for col in cols:
		dummy_test[col] = 0

	test_final = pd.concat([test_df[num_cols], dummy_test], axis = 1)
	print('Shape of final test data set: ', test_final.shape)

	prediction = pd.DataFrame(pd.Series(np.ceil(model.predict(test_final)), index = test_final.index), columns=['No_days'])
	temp = prediction['No_days'].apply(lambda x: pd.Timedelta(x, unit='D'))
	test_org.drop(['LoanNumber', 'FundingDate', 'RateLockDate'], axis=1, inplace=True)
	test_org['pred_ratelock'] = test_org['DateAdded'] + temp
	test_org['pred_ratelock'] = pd.to_datetime(test_org['pred_ratelock']).dt.date
	test_org['DateAdded'] = pd.to_datetime(test_org['DateAdded']).dt.date
	test_org.to_csv('prediction.csv')
	return render_template('home.html', prediction_text="Rate Lock Date predictions for the leads in specified period is exported" )

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000,debug=True)
