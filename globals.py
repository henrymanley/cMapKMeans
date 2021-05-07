import pandas as pd
import random

# Read in Excel File with Statments by stakeholder group
xl = pd.ExcelFile('statements.xlsx')
stakeholders = xl.sheet_names

# Add additional factor variables
additionalDemoType = "Sex"
additionalDemoOptions = ["Male", "Female"]

iter = 0
for i in stakeholders:
    if iter ==0:
        allStatements = pd.read_excel('statements.xlsx', sheet_name=i, header=None)
    else:
        stakeholder_i = pd.read_excel('statements.xlsx', sheet_name=i, header=None)
        allStatements = allStatements.append(stakeholder_i, ignore_index = True)
    iter +=1

# Number of sorters
participants = 0
for i in stakeholders:
    participants += 12

# Make demographics tab
demographics = pd.DataFrame(index=range(participants))
demographics['SorterID'] = demographics.index + 1
demographics['Type'] = ""

iter = 0
for i in stakeholders:
    demographics['Type'][iter: iter + 12] = i
    iter += 12

demographics[additionalDemoType] = ""
for j in range(len(demographics)):
    i = random.randint(0,len(additionalDemoOptions) -1 )
    demographics[additionalDemoType][j] = additionalDemoOptions[i]

# Number of piles, at most, a participant can make
maxClusters = 15
minClusters = 4

# First rating variable
rating1 = "Feasibility"

# Second rating variable
rating2 = "Importance"

# Rating scale 1..rateMax
rateMax = 5
