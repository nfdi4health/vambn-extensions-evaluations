import pandas as pd

df = #pd.read_sas('path/to/donald/data.sas7bdat')

rows_by_pers = dict()
for i, row in df.iterrows():
    if row.pers_ID not in rows_by_pers:
        rows_by_pers[row.pers_ID] = []
    rows_by_pers[row.pers_ID].append(row)

all_pers = []
for p_id, p_rows in rows_by_pers.items():
    ### FOR NOW:
    ages_rounded = [round(r.alter) for r in p_rows] #dataset min:3, max:18
    if len(set(ages_rounded)) != len(ages_rounded):
        print('skipping', p_id, 'because 2 ages round to the same visit') #happens to 38 of 1312 rows
        continue
    
    #save baseline variables
    all_visits = [p_rows[0][['pers_ID', 'fam_ID', 'sex']]]
    for p_visit in p_rows:
        p_visit.drop(['pers_ID', 'fam_ID', 'sex'], inplace=True)
        #save visit-specific variables
        all_visits.append(p_visit.add_suffix('_VIS'+str(round(p_visit.alter)-3).zfill(2))) #rename columns so that VIS00 is age 3, VIS15 is age 18.

    all_pers.append(pd.concat(all_visits))
df_vambn = pd.DataFrame(all_pers)

#reorder columns by visit
cols = ['pers_ID', 'fam_ID', 'sex']
for vis in range(16):
    cols += [col+'_VIS'+str(vis).zfill(2) for col in ['alter', 'time', 'e_cal', 'EW_p', 'Fett_p',
       'KH_p', 'Gluc_p', 'Fruc_p', 'Galac_p', 'MSacch_p', 'Sacch_p', 'MALT_p',
       'LACT_p', 'DISACCH_p', 'ZUCK_p', 'zuzu_p', 'free_s_p', 'FS_saft_p',
       'FS_obge_p', 'FS_sp_p', 'FS_bc_p', 'FS_cer_p', 'FS_oth_p', 'FS_dai_p',
       'FS_SSB_p', 'bmr', 'underrep', 'ovw', 'bmi', 'm_ovw', 'm_employ',
       'm_schulab', 'wo_tage']]
df_vambn = df_vambn.reindex(columns=cols)
df_vambn.rename(columns={'pers_ID': 'SUBJID'}, inplace=True) #rename pers_ID to SUBJID
df_vambn.to_csv('data/donald-data.csv')

print('fin')
