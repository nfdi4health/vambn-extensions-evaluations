import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os,re
from numpy import linalg as LA


#### Calculates pearson correlation matrices and plots their heatmaps for:
#       the original dataset
#       decodings of the embedded original participants (RP)
#       decodings of virtual embeddings from the BNet (VP)


# def relativ_error(matrix_real, matrix_sim, method="pearson"):
#     """
#     Relative error of Frobenius norms of correlation matrices between two dataframes
#     """
#     assert matrix_real.shape == matrix_sim.shape, 'can not calculate relative error of inputs with different shapes'
#     RC = matrix_real.corr(method=method)
#     SC = matrix_sim.corr(method=method)
#     sub = RC.sub(SC)
#     top = LA.norm(sub)
#     bot = LA.norm(RC, "fro")
#     return (top / bot)

unwanted_cols = ['Unnamed: 0', 'SUBJID']
all_vargroup_strings = {
    'SA':['sex','fam_ID'], #SA
    'TI':['alter','time'], #TIMES
    'AN':['bmr','bmi','ovw','underrep'], #ANTHRO (this also selects m_ovw!)
    'SO':['m_o','m_s','m_e'], #SOCIO
    'NU':['wo_tage','e_cal','_p']} #NUTRI

def clean_df(df_in):
    df_in.drop(columns=unwanted_cols, inplace=True, errors='ignore')
    cols_ordered = []
    for vg, vgstrings in all_vargroup_strings.items():
        vg_cols = [v for v in df_in.columns if any([vgs in v for vgs in vgstrings])]
        if vg is 'AN':
            vg_cols = [v for v in vg_cols if 'm_ovw' not in v] #remove faulty selection again
        vg_cols.sort()
        cols_ordered = cols_ordered + vg_cols
    return df_in.reindex(columns=cols_ordered)


original = clean_df(pd.read_csv('../../data/donald-data.csv', sep = ','))
recRP = clean_df(pd.read_csv('../reconRP.csv', sep =','))
decVP = clean_df(pd.read_csv('../decodedVP.csv', sep =','))


corr_orig = original.corr(method = "pearson")
corr_RP = recRP.corr(method = "pearson")
corr_VP = decVP.corr(method = "pearson")


#ensure same heat coloration across all 3 heatmaps
vmin = min(corr_orig.values.min(), corr_RP.values.min(), corr_VP.values.min())
vmax = max(corr_orig.values.max(), corr_RP.values.max(), corr_VP.values.max())

for corr,title,dpi in zip([corr_orig, corr_RP, corr_VP], ['original','reconstructed real','reconstructed virtual'], [143.5,143,143.5]):
    plt.figure()
    hm = sns.heatmap(data=corr, xticklabels = False, yticklabels = False, vmin=vmin, vmax=vmax)
    hm.set_title('Pearson correlations '+title)
    hm.set_aspect('equal','box')
    plt.savefig('plots/corr_mat_'+title.replace(' ', '-')+'.png', dpi=dpi, bbox_inches='tight', pad_inches=0.2) #input magic dpi numbers that make each corr-mat entry be juuuust over 1px in size
    # plt.savefig('plots/corr_mat_'+title.replace(' ', '-')+'.pdf') #dpi irrelevant for PDF, but it becomes huge file :(
    plt.show()
    plt.close()

# rel_err = relativ_error(original, decVP)
# print('Relative Error orig<->VP:',rel_err)


print('fin')
