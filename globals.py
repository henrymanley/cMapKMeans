import pandas as pd

xl = pd.ExcelFile('statements.xlsx')
stakeholders = xl.sheet_names


iter = 0
for i in stakeholders:
    if iter ==0:
        allStatements = pd.read_excel('statements.xlsx', sheet_name=i, header=None)
    else:
        stakeholder_i = pd.read_excel('statements.xlsx', sheet_name=i, header=None)
        allStatements = allStatements.append(stakeholder_i, ignore_index = True)
    iter +=1

# Combination of all statements

# Number of sorters
participants = 5

# Number of piles, at most, a participant can make
maxClusters = 9

# First rating variable
rating1 = "Feasibility"

# Second rating variable
rating2 = "Importance"

# Rating scale 1..rateMax
rateMax = 5
