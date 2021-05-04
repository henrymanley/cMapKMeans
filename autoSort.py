import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from globals import *


# Define Global vectorized data
df = pd.DataFrame(allStatements, columns=['text'])
df['label'] = df.index
vec = TfidfVectorizer(stop_words="english")
vec.fit(df.text.values)
features = vec.transform(df.text.values)

# Merge on text for each iteration of the clustering algorithm
sorted = pd.DataFrame(allStatements, columns=['text'])

def clusterData(df, features, n, returnData, rateMax):
    """
    @param df is the list of statements of type df
    @param n is the max number of clusters (categories) the data is to be sorted into.
    @param features is the vectorized text to cluster of type df.
    @param returnData is the df to write resulting data to.
    @param rateMax is the maximum rating a statement can get. This function assumes
        there are only two variables to rank on.
    """
    for p in range(1, participants +1):
        start = df
        n_clusters = random.randint(2,n)
        random_state = random.randint(0,10)
        cls = MiniBatchKMeans(n_clusters=n_clusters, random_state=random_state)
        cls.fit(features)
        cls.predict(features)
        start['participant' + str(p)] = pd.Series(cls.labels_, index=start.index)
        start = start[start.columns.drop(list(start.filter(regex='label')))]
        returnData = start.merge(returnData, left_index = True, on = 'text')

        rating1 = np.random.uniform(1,rateMax, size = len(returnData))
        rating1 = [round(num) for num in rating1]
        rating1 = pd.DataFrame(rating1, columns=['rating1/'+ str(p)])
        returnData = returnData.merge(rating1, left_index = True, right_index = True)

        rating2 = np.random.uniform(1,rateMax, size = len(returnData))
        rating2 = [round(num) for num in rating2]
        rating2 = pd.DataFrame(rating2, columns=['rating2/'+ str(p)])
        returnData = returnData.merge(rating2, left_index = True, right_index = True)
    return returnData


def buildAll():
    """
    From KMeans clusters, build the sorted and rated data set.
    """
    x = clusterData(df, features, 6, sorted, rateMax)
    x.columns  = [i.strip('_x').strip('_y') for i in x.columns]
    x = x.loc[:,~x.sort_index(1).columns.duplicated()]
    x['ID'] = x.index
    data = x
    x = x.rename(columns={'text': 'Statement',})
    x['Statement ID'] = x.index
    statementsWrite = x[['Statement ID', 'Statement']]

    x["UserID"] = x['ID']
    x = pd.wide_to_long(x, ["participant", "rating2/", "rating1/"], i="ID", j="num")
    x = x.sort_values(by=['num', 'ID'])
    x = x.rename(columns={"rating1/": rating1, "rating2/": rating2})
    x["StatementID"] = x.groupby('num').ngroup(ascending=True)
    x["StatementID"] += 1
    col_names = ["UserID", "StatementID", rating1, rating2]
    ratingsWrite = x.reindex(columns=col_names)

    y = data
    y["UserID"] = y['ID']
    del y['ID']
    keep = [col for col in y.columns if 'participant' in col]
    keep = keep + ['UserID']
    y = y[keep]
    y = pd.wide_to_long(y, ["participant"], i="UserID", j="num")
    y = y.rename(columns={"participant": "cluster"})
    y["UserID1"] = y.groupby('num').ngroup(ascending=True)
    y["StatementID1"] = y.groupby('UserID').ngroup(ascending=True)
    y = y.sort_values(by=[ "UserID1", "cluster"])
    y["StatementID1"] += 1
    y = y.reset_index(drop=True)
    y = y.rename(columns={"StatementID1": "StatementID", "UserID1" : "UserID"})

    nStatements = y.groupby(['UserID', 'cluster']).count().max() + 1
    nStatements = nStatements['StatementID']
    accum = ['UserID', 'Cluster']
    for st in range(nStatements):
        accum.append('Statement' + str(st))

    z = pd.DataFrame(columns = accum)
    for i in range(len(y)-1):
        clusterCurrent = y.loc[y.index[i], "cluster"]
        clusterNext = y.loc[y.index[i+1], "cluster"]
        userCurrent = y.loc[y.index[i], "UserID"]
        userNext = y.loc[y.index[i+1], "UserID"]

        if i == 0:
            statements = [userCurrent, clusterCurrent]
        if (clusterNext == clusterCurrent):
            statement = y.loc[y.index[i], "StatementID"]
            statements.append(statement)
        else:
            statement = y.loc[y.index[i], "StatementID"]
            statements.append(statement)
            diff = nStatements + 2 - len(statements)
            for k in range(diff):
                statements.append(0)
            series = pd.Series(statements, index = z.columns)
            z = z.append(series, ignore_index=True)
            statements = [userNext, clusterNext]

    z = z.sort_values(by=[ "UserID", "Cluster"])
    z["UserID"] += 1
    z["Cluster"] += 1
    sortedCardsWrite = z.reset_index(drop=True)

    accum = ["Variable", rating1, rating2]
    r = pd.DataFrame(columns = accum)
    series1 = pd.Series(['Min', 1, 1], index = r.columns)
    series2 = pd.Series(['Max', rateMax, rateMax], index = r.columns)
    r = r.append(series1, ignore_index=True)
    r = r.append(series2, ignore_index=True)
    ratingsScaleWrite = r

    with pd.ExcelWriter('sortData.xlsx') as writer:
        sortedCardsWrite.to_excel(writer, sheet_name='SortedCards', index = False, header = False)
        statementsWrite.to_excel(writer, sheet_name='Statements', index = False)
        ratingsWrite.to_excel(writer, sheet_name='Ratings', index = False)
        ratingsScaleWrite.to_excel(writer, sheet_name='RatingsScale', index = False)

buildAll()


# Graph the results
# pca = PCA(n_components=2, random_state=random_state)
# reduced_features = pca.fit_transform(features.toarray())
# reduced_cluster_centers = pca.transform(cls.cluster_centers_)
# plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
# plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
# plt.show()

#need to add demographics, favor based on certain variables here.
#clean up code, abstract variables to global file and import
