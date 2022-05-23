import pandas as pd

### reads reconstructed real participants, transforms them into original donald csv format (one visit per row, multiple rows per participant)

df_vambn = pd.read_csv('HI-VAE/reconRP.csv')

separate_visits = dict()
for _, row in df_vambn.iterrows():
    this_person = {v: {'pers_ID': row['SUBJID']} for v in range(16)}
    for name, val in dict(row).items():
        if name != 'SUBJID':
            # this_person['pers_ID'] = val
            # continue
            name, vis = name.rsplit('_', 1)
            _, var = name.split('_', 1)
            vis = int(vis.replace('VIS', ''))
            this_person[vis][var] = val
    separate_visits[row['SUBJID']] = this_person

df_donald = pd.DataFrame(columns=separate_visits[27.0][0].keys())
for pers_ID, pers_dict in separate_visits.items():
    for vis, vis_data in pers_dict.items():
        df_donald = df_donald.append(pd.Series(vis_data), ignore_index=True)
df_donald = df_donald.reindex(columns=['pers_ID', 'alter', 'time', 'e_cal', 'EW_p', 'Fett_p',
       'KH_p', 'Gluc_p', 'Fruc_p', 'Galac_p', 'MSacch_p', 'Sacch_p', 'MALT_p',
       'LACT_p', 'DISACCH_p', 'ZUCK_p', 'zuzu_p', 'free_s_p', 'FS_saft_p',
       'FS_obge_p', 'FS_sp_p', 'FS_bc_p', 'FS_cer_p', 'FS_oth_p', 'FS_dai_p',
       'FS_SSB_p', 'bmr', 'underrep', 'ovw', 'bmi', 'm_ovw', 'm_employ',
       'm_schulab', 'wo_tage'])

df_donald.to_csv('data/donald-reconstructed.csv', index=False)

print('fin')
