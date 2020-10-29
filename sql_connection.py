import pyodbc


server = 'aspire-devops-sqlinstance.public.0fb73495fad6.database.windows.net,3342'
database = 'Marketing_Analytical_Data_mart_QA'
username = 'devopsadmin'
password = 'UH3$9r8nr3DuugDcq4g'   
driver= '{ODBC Driver 17 for SQL Server}'

def sql_connect():
	cnxn  = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
	return cnxn

# -------------------------------------------------------------------
# 			Loading Training Data
#
q = """ 
WITH CTE_DateAdded
AS (
    SELECT *
    FROM (
        SELECT ROW_NUMBER() OVER (
                PARTITION BY d.LEADID ORDER BY d.[StatusChangeDate] DESC
                ) RNOW
            ,f.[LeadID]
            ,f.[LeadSourceGroup]
			,f.[ZipCode]
			,f.[LoanPurpose]
            ,d.[Status]
            ,d.[StatusChangeDate] AS DateAdded
            ,f.LQB_LoanNumber AS LoanNumber
        FROM VLF.DimLead AS f
        INNER JOIN VLF.DimLeadStatuses AS d ON f.LeadID = d.LeadID
        WHERE d.[Status] = 'New'
        ) T
    WHERE t.RNOW = 1
    )
    ,CTE_DateContacted
AS (
        SELECT *
        FROM (
            SELECT ROW_NUMBER() OVER (
                    PARTITION BY d.LEADID ORDER BY d.[StatusChangeDate]
                    ) RNOW
                ,f.[LeadID]
                ,A.[DateAdded]
                ,d.[Status]
                ,d.[StatusChangeDate]
                ,f.[LeadSourceGroup]
				,f.[ZipCode]
				,f.[LoanPurpose]
                ,A.LoanNumber
            FROM VLF.DimLead AS f
            INNER JOIN VLF.DimLeadStatuses AS d ON f.LeadID = d.LeadID
            INNER JOIN CTE_DateAdded As A ON A.LeadID=d.LeadID
            WHERE d.[Status] IN (
                    'Contacted'
                    ,'DNQ - Final'
                    ,'Loan Sold'
                    ,'Nurture'
                    ,'Nurture - Cash out'
                    ,'Nurture - Credit'
                    ,'Nurture - FHA/VA'
                    ,'Nurture - Rates'
                    ,'PreQual Docs Requested'
                    ,'Refused - Final'
                    ,'Processing'
                    ,'Refused - HELOC'
                    )
                AND d.[StatusChangeDate]>A.DateAdded
            ) T
        WHERE t.RNOW = 1
        )
,
CTE_FL as
(
select
Tfact.LoanNumber,
TotalLoanAmount,
BorrowerAge,
BorrowerYearsInSchool,
BorrowerTotalMonthlyIncome,
CoBorrowerTotalMonthlyIncome,
BorrowerOwnRent,
CreditScore,
CLTV,
DTI,
BorrowerGender
from
LQB.DimBorrower as Tdimbor,
LQB.DimSubjectProperty as TdimSub,
LQB.FactLoan as Tfact,
LQB.lkpBranch as Tbran,
LQB.lkpLoanPurpose as Tloanp,
LQB.lkpLoanType as Tloant,
LQB.lkpMileStone as Tmile
where
    Tbran.BranchID = Tfact.BranchID
    and Tloanp.LoanPurposeID = Tfact.LoanPurposeID
    and Tloant.LoanTypeID = Tfact.LoanTypeID
    and Tmile.MileStoneID = Tfact.MileStoneID
    and Tfact.BorrowerID = Tdimbor.BorrowerID
    and Tfact.PropertyID = TdimSub.PropertyID
)
,
final_table as 
(
select          C.[LeadID]
                ,C.[DateAdded]
				,C.[ZipCode]
				,C.[LoanPurpose]
                ,C.[LeadSourceGroup]
				,A.*
from CTE_DateContacted  AS C
INNER JOIN CTE_FL AS A ON  C.LoanNumber=A.LoanNumber
)

select * from final_table 
"""



# -------------------------------------------------------------------
# 			Loading Testing Data
#

query = """
WITH CTE_DateAdded
AS (
    SELECT *
    FROM (
        SELECT ROW_NUMBER() OVER (
                PARTITION BY d.LEADID ORDER BY d.[StatusChangeDate] DESC
                ) RNOW
            ,f.[LeadID]
            ,f.[LeadSourceGroup]
			,f.[ZipCode]
			,f.[LoanPurpose]
            ,d.[Status]
            ,d.[StatusChangeDate] AS DateAdded
            ,f.LQB_LoanNumber AS LoanNumber
        FROM VLF.DimLead AS f
        INNER JOIN VLF.DimLeadStatuses AS d ON f.LeadID = d.LeadID
        WHERE d.[Status] = 'New'
        ) T
    WHERE t.RNOW = 1
    )
    ,CTE_DateContacted
AS (
        SELECT *
        FROM (
            SELECT ROW_NUMBER() OVER (
                    PARTITION BY d.LEADID ORDER BY d.[StatusChangeDate]
                    ) RNOW
                ,f.[LeadID]
                ,A.[DateAdded]
                ,d.[Status]
                ,d.[StatusChangeDate]
                ,f.[LeadSourceGroup]
				,f.[ZipCode]
				,f.[LoanPurpose]
                ,A.LoanNumber
            FROM VLF.DimLead AS f
            INNER JOIN VLF.DimLeadStatuses AS d ON f.LeadID = d.LeadID
            INNER JOIN CTE_DateAdded As A ON A.LeadID=d.LeadID
            WHERE d.[Status] IN (
                    'Contacted'
                    ,'DNQ - Final'
                    ,'Loan Sold'
                    ,'Nurture'
                    ,'Nurture - Cash out'
                    ,'Nurture - Credit'
                    ,'Nurture - FHA/VA'
                    ,'Nurture - Rates'
                    ,'PreQual Docs Requested'
                    ,'Refused - Final'
                    ,'Processing'
                    ,'Refused - HELOC'
                    )
                AND d.[StatusChangeDate]>A.DateAdded
            ) T
        WHERE t.RNOW = 1
        )
,
CTE_FL as
(
select
Tfact.LoanNumber,
TotalLoanAmount,
BorrowerAge,
BorrowerYearsInSchool,
BorrowerTotalMonthlyIncome,
CoBorrowerTotalMonthlyIncome
BorrowerOwnRent,
CreditScore,
CLTV,
DTI,
BorrowerGender
from
LQB.DimBorrower as Tdimbor,
LQB.DimSubjectProperty as TdimSub,
LQB.FactLoan as Tfact,
LQB.lkpBranch as Tbran,
LQB.lkpLoanPurpose as Tloanp,
LQB.lkpLoanType as Tloant,
LQB.lkpMileStone as Tmile
where
    Tbran.BranchID = Tfact.BranchID
    and Tloanp.LoanPurposeID = Tfact.LoanPurposeID
    and Tloant.LoanTypeID = Tfact.LoanTypeID
    and Tmile.MileStoneID = Tfact.MileStoneID
    and Tfact.BorrowerID = Tdimbor.BorrowerID
    and Tfact.PropertyID = TdimSub.PropertyID
)
,
final_table as 
(
select          C.[LeadID]
                ,C.[DateAdded]
				,C.[ZipCode]
				,C.[LoanPurpose]
                ,C.[LeadSourceGroup]
				,A.*
from CTE_DateContacted  AS C
INNER JOIN CTE_FL AS A ON  C.LoanNumber=A.LoanNumber
)

select * from final_table where DateAdded between '{}' and '{}' """.format(start_date, end_date)

