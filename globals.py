import pandas as pd

stakeholder1 = "Employees"
stakeholder2 = "Board"

stakeholder1Statements = pd.read_excel('statements.xlsx', sheet_name=stakeholder1, header=None)
stakeholder2Statements = pd.read_excel('statements.xlsx', sheet_name=stakeholder2, header=None)
# Combination of all statements
allStatements = stakeholder2Statements.append(stakeholder1Statements, ignore_index = True)
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
