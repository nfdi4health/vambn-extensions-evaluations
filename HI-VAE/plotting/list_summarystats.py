import numpy as np
import pandas
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from scipy import stats
import os,re


#Calculates summary statistics for every variable across original+RP+VP data, and writes them into big csv
#to use, create folder 'result-RP-VP-store/' that includes the original training data and your resulting RP+VP files
which_run = 'origin-Jul30'

original=pd.read_csv('result-RP-VP-store/donald-data_TRAIN.csv')
original.drop(columns=['Unnamed: 0', 'SUBJID'],inplace=True)

recRP=pd.read_csv('result-RP-VP-store/reconRP-'+which_run+'.csv', sep =',')
recRP = recRP[recRP.columns.drop(list(recRP.filter(regex='SUBJID|scode_')))]
recRP.columns = recRP.columns.str.replace('TIMES_', '')
recRP.columns = recRP.columns.str.replace('NUTRI_', '')
recRP.columns = recRP.columns.str.replace('SOCIO_', '')
recRP.columns = recRP.columns.str.replace('ANTHRO_', '')

decVP = pd.read_csv('result-RP-VP-store/decodedVP-'+which_run+'.csv', sep =',')
decVP = decVP[decVP.columns.drop(list(decVP.filter(regex='SUBJID|scode_')))]
decVP.columns = decVP.columns.str.replace('TIMES_', '')
decVP.columns = decVP.columns.str.replace('NUTRI_', '')
decVP.columns = decVP.columns.str.replace('SOCIO_', '')
decVP.columns = decVP.columns.str.replace('ANTHRO_', '')
decVP.rename(columns={'SA_fam_ID_VIS00': 'fam_ID', 'SA_sex_VIS00': 'sex'}, inplace=True)


# Quartile functions
def q25(x):
    return x.quantile(0.25)
def q75(x):
    return x.quantile(0.75)

agg_orig = original.agg(['min', q25, 'median', q75, 'max', 'mean', 'var', 'std']).T
agg_RP = recRP.agg(['min', q25, 'median', q75, 'max', 'mean', 'var', 'std']).T
agg_VP = decVP.agg(['min', q25, 'median', q75, 'max', 'mean', 'var', 'std']).T

agg_orig.to_csv('plots/summarystats_original.csv')
agg_RP.to_csv('plots/summarystats_RP-'+which_run+'.csv')
agg_VP.to_csv('plots/summarystats_VP-'+which_run+'.csv')
print('fin')

