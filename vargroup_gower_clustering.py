import pandas as pd
import gower
from sklearn.cluster import AgglomerativeClustering


n = 4 #number of vargroups

# Required data format: 1 col per variable, 1 row per attended visit of a participant
df = pd.read_sas('path/to/donald/data.sas7bdat')
df = df.drop(columns=['pers_ID', 'fam_ID', 'sex']) #exclude stalones
df = df.fillna(df.mean()) #impute NaN with column averages
df = df.transpose() #find clusters of columns, not rows

distance_matrix = gower.gower_matrix(df)

model = AgglomerativeClustering(n_clusters=n, linkage='complete', affinity='precomputed')
clusters = model.fit_predict(distance_matrix)

groups = {}
for column, cluster in zip(df.index, clusters):
    if cluster not in groups.keys():
        groups[cluster] = [column]
    else:
        groups[cluster].append(column)

print('Finished clustering '+str(n)+' variable groups:\n'+str(groups))
