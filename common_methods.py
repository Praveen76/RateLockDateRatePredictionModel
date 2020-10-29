import pandas as pd
from build_variables import *

# Creating groups for Loan Purpose

def group_purpose(series):
	s = list()
	for v in series:
		v = str(v)
		if 'pur' in v.lower():
			s.append('Purchase')
		elif 'refi' in v.lower():
			s.append('Refinance')
		elif 'home' or 'equity' in v.lower():
			s.append('Home Equity')
		else:
			s.append('Other')
	return s

# Preparing training data

def compile_train_df(df):
	df['Total_Income'] = df['BorrowerTotalMonthlyIncome'] + df['CoBorrowerTotalMonthlyIncome']
	df.drop(['FundingDate', 'LoanNumber', 'BorrowerTotalMonthlyIncome', 'CoBorrowerTotalMonthlyIncome'], axis = 1, inplace=True)
	df['RateLockDate'] = pd.to_datetime(df['RateLockDate'])
	df['DateAdded'] = pd.to_datetime(df['DateAdded'])
	df = df.set_index('LeadID')

	zips = ['75', '76', '77', '78', '79']
	campaign = ['TV', 'Radio', 'Internet', 'Direct Mail', 'Social Media']
	ownrent = ['Own', 'Rent']
	gender = ['Male', 'Female']

	df['ZipCode'] = [str(zc)[:2] for zc in df['ZipCode']]
	df['ZipCode'] = [v if v in zips else 'Other' for v in df['ZipCode']]
	df['LeadSourceGroup'] = [v if v in campaign else 'Other' for v in df['LeadSourceGroup']]
	df['LoanPurpose'] = group_purpose(df['LoanPurpose'])
	df['BorrowerOwnRent'] = [v if v in ownrent else 'Other' for v in df['BorrowerOwnRent']]
	df['BorrowerGender'] = [v if v in gender else 'Other' for v in df['BorrowerGender']]
	df['days_tolock'] = (df['RateLockDate'] - df['DateAdded']).dt.days.values.reshape(-1, 1)
	df['days_tolock'] = df['days_tolock'].clip(lower = 0)
	df.dropna(inplace=True)
	return df

# Creating Dummy variables

def dummies(df_path):
	df = df_path[cat_cols]
	dummy = pd.get_dummies(df, drop_first=False)
	return dummy

# Preparing Testing Dataset

def compile_test_df(df):
	
	df['Total_Income'] = df['BorrowerTotalMonthlyIncome'] + df['CoBorrowerTotalMonthlyIncome']
	df.drop(['FundingDate',
			 'LoanNumber',
			 'BorrowerTotalMonthlyIncome',
			 'CoBorrowerTotalMonthlyIncome',
			 'RateLockDate'], axis = 1, inplace=True)

	zips = ['75', '76', '77', '78', '79']
	campaign = ['TV', 'Radio', 'Internet', 'Direct Mail', 'Social Media']
	ownrent = ['Own', 'Rent']
	gender = ['Male', 'Female']

	df['ZipCode'] = [str(zc)[:2] for zc in df['ZipCode']]
	df['ZipCode'] = [v if v in zips else 'Other' for v in df['ZipCode']]
	df['LeadSourceGroup'] = [v if v in campaign else 'Other' for v in df['LeadSourceGroup']]
	df['LoanPurpose'] = group_purpose(df['LoanPurpose'])
	df['BorrowerOwnRent'] = [v if v in ownrent else 'Other' for v in df['BorrowerOwnRent']]
	df['BorrowerGender'] = [v if v in gender else 'Other' for v in df['BorrowerGender']]
	df.dropna(inplace=True)
	return df

# Handing missing dummy variables	
	
def Diff(li1, li2):
	li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
	return li_dif
	






