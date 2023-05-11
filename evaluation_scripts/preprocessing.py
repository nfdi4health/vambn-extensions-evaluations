unwanted_cols = ['Unnamed: 0', 'SUBJID']
all_vargroup_strings = {
    'SA': ['sex', 'fam_ID'], #SA
    'TI': ['alter', 'time'], #TIMES
    'AN': ['bmr','bmi', 'ovw', 'underrep'], #ANTHRO (this also selects m_ovw!)
    'SO': ['m_o', 'm_s', 'm_e'], #SOCIO
    'NU': ['wo_tage', 'e_cal', '_p']} #NUTRI


def clean_df(df_in):
    df_in.drop(columns=unwanted_cols, inplace=True, errors='ignore')
    cols_ordered = []
    for vg, vgstrings in all_vargroup_strings.items():
        vg_cols = [v for v in df_in.columns if any([vgs in v for vgs in vgstrings])]
        if vg is 'AN':
            vg_cols = [v for v in vg_cols if 'm_ovw' not in v]  # remove faulty selection again
        vg_cols.sort()
        cols_ordered = cols_ordered + vg_cols
    return df_in.reindex(columns=cols_ordered)
