import random
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import MiniBatchKMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


empStatements = [
    "I am concerned about working fewer hours",
    "I want to have fun when I go to work",
    "I want less of a corporate feel to the workplace",
    "I would like to be able to play my own music over the PA",
    "I think having an open floor plan would be more welcoming",
    "I don’t think we ought to serve tables",
    "I want to make sure that our new boss values COVID safety",
    "I want to avoid the possibility of being understaffed",
    "It would be ideal to have a manger present at all times, especially in the first few weeks",
    "I was hoping to work for tips to feel like my effort is rewarded",
    "I want to build a culture that values honesty and humility",
    "We should meet with management more often to talk about how things are going",
    "I want a boss that respects me",
    "Employees will leave if it seems all that management cares about is making money",
    "I am concerned about my new coworkers being lazy",
    "It has been a while since this company has had a change like this",
    "I think there needs to be a promotional ladder of some sort",
    "I want to make sure the quality of our food stays high"
]

boardStatements = [
    "We should create a new brand that encompasses both of our old ones",
    "We need to focus on building customer loyalty first, making profit second",
    "I want to make sure our employees feel on board with all of the changes",
    "I want to listen to our respective patrons’ desires",
    "I want to stay open as a bar in the evenings to gain new market share",
    "I think we might have to hire new managers to embrace the new changes",
    "We will have to use social media marketing to make our patrons aware of the change",
    "We should revamp our menu to include top dishes from both places, and new ones",
    "We ought to work with the city government to reduce monopolistic concerns",
    "I want our workers to be tipped to supplement their wages",
    "We should try to hire high schoolers or BOCES students to diversity our labor",
    "We need to make the merger feel like both companies are represented equally",
    "Our investors will need to see steady growth, fast",
    "We should think about a way to reward our full-time employees making the transition with us",
    "We need to acquire new customers with the new brand",
    "We need to be careful in order to retain old customers",
    "I am concerned that the culture will be dominated by Waffle Frolic’s management",
    "I am worried that Waffle Frolic’s employees will not respect Ithaca Coffee. Co's management",
    "I think that we should focus our menu and market on the quality of our coffee",
    "We should schedule a community celebration event for the grand opening",
    "We need to put our employees to work"
]

allStatements = empStatements + boardStatements
participants = 5

# Define Global vectorized data
df = pd.DataFrame(allStatements, columns=['text'])
df['label'] = df.index
vec = TfidfVectorizer(stop_words="english")
vec.fit(df.text.values)
features = vec.transform(df.text.values)

# Merge on text for each iteration of the clustering algorithm
sorted = pd.DataFrame(allStatements, columns=['text'])


def clusterData(df, features, n, returnData):
    """
    @param df is the list of statements of type df
    @param n is the max number of clusters (categories) the data is to be sorted into.
    @param features is the vectorized text to cluster of type df.
    @param returnData is the df to write resulting data to.
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

        rating1 = np.random.uniform(1,5, size = len(returnData))
        rating1 = [round(num) for num in rating1]
        rating1 = pd.DataFrame(rating1, columns=['rating1/'+ str(p)])
        returnData = returnData.merge(rating1, left_index = True, right_index = True)

        rating2 = np.random.uniform(1,5, size = len(returnData))
        rating2 = [round(num) for num in rating2]
        rating2 = pd.DataFrame(rating2, columns=['rating2/'+ str(p)])
        returnData = returnData.merge(rating2, left_index = True, right_index = True)


    return returnData

# Write to xlsx
x = clusterData(df, features, 6, sorted)
x.columns  = [i.strip('_x').strip('_y') for i in x.columns]
x = x.loc[:,~x.sort_index(1).columns.duplicated()]
x['ID'] = x.index


statements = x['text']
statements.to_excel('sortData.xlsx', sheet_name='Statements', index=True)

del x['text']
x = pd.wide_to_long(x, ["participant", "rating2/", "rating1/"], i="ID", j="num")
x = x.sort_values(by=['num', 'ID'])
print(x.head(40))
clusters = [col for col in x.columns if 'cluster' in col]
clusters.to_excel('sortData.xlsx', sheet_name='Statements', index=True)

ratings = [col for col in x.columns if 'rating' in col]
ratings.to_excel('sortData.xlsx', sheet_name='Ratings', index=True)

# Graph the results
# pca = PCA(n_components=2, random_state=random_state)
# reduced_features = pca.fit_transform(features.toarray())
# reduced_cluster_centers = pca.transform(cls.cluster_centers_)
# plt.scatter(reduced_features[:,0], reduced_features[:,1], c=cls.predict(features))
# plt.scatter(reduced_cluster_centers[:, 0], reduced_cluster_centers[:,1], marker='x', s=150, c='b')
# plt.show()
