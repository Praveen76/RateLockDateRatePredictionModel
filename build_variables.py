import os

cat_cols = ['LoanPurpose', 'LeadSourceGroup', 'ZipCode', 'BorrowerOwnRent', 'BorrowerGender']
num_cols = ['TotalLoanAmount','BorrowerAge','BorrowerYearsInSchool','Total_Income','CreditScore','CLTV','DTI']

dummy_features = [
	 'LoanPurpose_Home Equity',
	 'LoanPurpose_Purchase',
	 'LoanPurpose_Refinance',
	 'LeadSourceGroup_Direct Mail',
	 'LeadSourceGroup_Internet',
	 'LeadSourceGroup_Other',
	 'LeadSourceGroup_Radio',
	 'LeadSourceGroup_Social Media',
	 'LeadSourceGroup_TV',
	 'ZipCode_75',
	 'ZipCode_76',
	 'ZipCode_77',
	 'ZipCode_78',
	 'ZipCode_79',
	 'ZipCode_Other',
	 'BorrowerOwnRent_Other',
	 'BorrowerOwnRent_Own',
	 'BorrowerOwnRent_Rent',
	 'BorrowerGender_Female',
	 'BorrowerGender_Male',
	 'BorrowerGender_Other'
]