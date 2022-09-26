import pandas as pd
import numpy as np

all_val_orig = pd.read_csv('../data/data_out/data_names.csv')['x'].values
all_val = np.array([v if '_VIS' in v else v+'_VISALL'
                    for v in all_val_orig])


white_list = pd.DataFrame(columns=['from', 'to'])
for i in all_val:
    # separate column name and visit
    # split column name
    split_col, split_vis = i.split('_VIS')

    # (ascending timeline)
    # if there exist visit + 1, append connection to df
    if split_vis != 'ALL':
        colname_tosearch_asc = f"{split_col}_VIS{int(split_vis)+1:02d}"
        if colname_tosearch_asc in all_val:
            print(f"From: {i}, To: {colname_tosearch_asc}")
            white_list = white_list.append({'from': i, 'to': colname_tosearch_asc}, ignore_index=True)

    # Rule 7: scode_ (colname + vis) to zcode_ (colname + vis)
    if 'scode_' in split_col and split_vis != 'ALL':
        colname = split_col.split('_')[1]
        colname_tosearch_scode = f"zcode_{colname}_VIS{split_vis}"
        if colname_tosearch_scode in all_val:
            print(f"From: {i}, To: {colname_tosearch_scode}")
            white_list = white_list.append({'from': i, 'to': colname_tosearch_scode}, ignore_index=True)

    # Rule 8: AUX_ (colname + vis) to zcode_ (colname + vis)
    # Rule 9: AUX_SA_ (colname + vis) to SA_ (colname + vis)
    if 'AUX_' in split_col and split_vis != 'ALL':
        if 'AUX_SA_' in split_col:
            colname = split_col.split('SA_')[1]
            colname_tosearch_aux_sa = f"SA_{colname}_VIS{split_vis}"
            if colname_tosearch_aux_sa in all_val:
                print(f"From: {i}, To: {colname_tosearch_aux_sa}")
                white_list = white_list.append({'from': i, 'to': colname_tosearch_aux_sa}, ignore_index=True)
        else:
            colname = split_col.split('AUX_')[1]
            colname_tosearch_aux = f"zcode_{colname}_VIS{split_vis}"
            if colname_tosearch_aux in all_val:
                print(f"From: {i}, To: {colname_tosearch_aux}")
                white_list = white_list.append({'from': i, 'to': colname_tosearch_aux}, ignore_index=True)

    # Rule 10: visitmiss_ (vis) to zcode_ (vis)
    # Rule 11: visitmiss_ (vis) to AUX_ (vis)
    # Rule 12: visitmiss_ (vis) to AUX_SA_ (vis)
    # Rule 13: visitmiss_ (vis) to SA_ (vis)
    # if current column name is not visitmiss or scode, append this entry
    if not 'visitmiss' in split_col and not 'scode' in split_col and not 'SA_' in split_col and split_vis != 'ALL':
        colname_tosearch_visitmiss = f"visitmiss_VIS{split_vis}"
        if colname_tosearch_visitmiss in all_val:
            print(f"From: {colname_tosearch_visitmiss}, To: {i}")
            white_list = white_list.append({'from': colname_tosearch_visitmiss, 'to': i}, ignore_index=True)

# drop duplicates, sort values and reset index
white_list = white_list.drop_duplicates()
white_list = white_list.sort_values(by=['from'])
white_list = white_list.reset_index(drop=True)
white_list.to_csv('../data/data_out/main_wl.csv', index=False)


black_list = pd.DataFrame(columns=['from', 'to'])
val_df = pd.DataFrame([x.split('_VIS') for x in all_val])
val_df = val_df.rename(columns={0: 'column_name', 1: 'visit'})
val_df = val_df[val_df['visit'] != 'ALL'] #never blacklist VISALL-modules!
val_df['visit'] = val_df['visit'].astype(int)
val_df['original'] = [x for x in all_val if not 'ALL' in x]
all_vis = [int(i) for i in val_df['visit'].unique()]

for idx, row_val in val_df.iterrows():
    # (descending timeline)
    # if there exist bigger visit, append connection to df
    higher_vis = [i for i in all_vis if i > int(row_val['visit'])]
    # if list not empty, search for greater vis column names, and append
    if len(higher_vis) > 0:
        for vis in higher_vis:
            colnames_higher = val_df[val_df['visit'] == vis]['original']
            for col in colnames_higher:
                # print(f"From: {col}, To: {row_val['original']}")
                black_list = black_list.append({'from': col, 'to': row_val['original']}, ignore_index=True)

    # Rule 2: SA_dcfdx to all, except current SA_dcfdx's higher visits (vis 0 can affect vis 1 and onwards)
    if row_val['column_name'] == 'SA_dcfdx':
        higher_vis_colname = [f"{row_val['column_name']}_VIS{i}" for i in all_vis if i > int(row_val['visit'])]
        for idx, col_val in val_df.iterrows():
            if not col_val['original'] in higher_vis_colname:
                # print(f"From: {row_val['original']}, To: {col_val['original']}")
                black_list = black_list.append({'from': row_val['original'], 'to': col_val['original']}, ignore_index=True)

    # Rule 3: all to SA_age_at_visit, except current SA_age_at_visit's lower visits and related AUX_SA
    if row_val['column_name'] == 'SA_age_at_visit':
        lower_vis_colname = [f"{row_val['column_name']}_VIS{i}" for i in all_vis if i < int(row_val['visit'])]
        for idx, col_val in val_df.iterrows():
            aux_sa = f"AUX_SA_{row_val['column_name']}_VIS{row_val['visit']}"
            if col_val['original'] != aux_sa:
                if len(lower_vis_colname) > 0:
                    if not col_val['original'] in lower_vis_colname:
                        # print(f"From: {col_val['original']}, To: {row_val['original']}")
                        black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)
                else:
                    # print(f"From: {col_val['original']}, To: {row_val['original']}")
                    black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)

    # Rule 4: all AUX_ and AUX_SA_ to zcode_, except current zcode_'s lower visits and related AUX_
    if 'zcode_' in row_val['column_name']:
        lower_vis_colname = [f"{row_val['column_name']}_VIS{i}" for i in all_vis if i < int(row_val['visit'])]
        for idx, col_val in val_df.iterrows():
            if 'AUX_' in col_val['column_name'] or 'AUX_SA_' in col_val['column_name']:
                root_zcode = row_val['column_name'].split('zcode_')[1]
                aux = f"AUX_{root_zcode}_VIS{row_val['visit']}"
                if col_val['original'] != aux:
                    if len(lower_vis_colname) > 0:
                        if not col_val['original'] in lower_vis_colname:
                            # print(f"From: {col_val['original']}, To: {row_val['original']}")
                            black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)
                    else:
                        # print(f"From: {col_val['original']}, To: {row_val['original']}")
                        black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)

    # Rule 5: all AUX_ and AUX_SA_ to SA_, except current SA_'s lower visits and related AUX_SA_
    if 'SA_' in row_val['column_name'] and not 'AUX_SA_' in row_val['column_name']:
        lower_vis_colname = [f"{row_val['column_name']}_VIS{i}" for i in all_vis if i < int(row_val['visit'])]
        for idx, col_val in val_df.iterrows():
            if 'AUX_' in col_val['column_name'] or 'AUX_SA_' in col_val['column_name']:
                root_sa = row_val['column_name'].split('SA_')[1]
                aux_sa = f"AUX_SA_{root_sa}_VIS{row_val['visit']}"
                if col_val['original'] != aux_sa:
                    if len(lower_vis_colname) > 0:
                        if not col_val['original'] in lower_vis_colname:
                            # print(f"From: {col_val['original']}, To: {row_val['original']}")
                            black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)
                    else:
                        # print(f"From: {col_val['original']}, To: {row_val['original']}")
                        black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)

    # Rule 6: all to AUX_ and AUX_SA_, except current AUX_ or AUX_SA's lower visits
    # Rule 7: all to visitmiss_, except current visitmiss_'s lower visits
    if 'AUX_' in row_val['column_name'] or 'AUX_SA_' in row_val['column_name'] or 'visitmiss_' in row_val['column_name'] or 'SA_' in row_val['column_name']:
        lower_vis_colname = [f"{row_val['column_name']}_VIS{i}" for i in all_vis if i < int(row_val['visit'])]
        for idx, col_val in val_df.iterrows():
            if len(lower_vis_colname) > 0:
                if not col_val['original'] in lower_vis_colname:
                    print(f"From: {col_val['original']}, To: {row_val['original']}")
                    black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)
            else:
                print(f"From: {col_val['original']}, To: {row_val['original']}")
                black_list = black_list.append({'from': col_val['original'], 'to': row_val['original']}, ignore_index=True)

black_list = black_list.drop_duplicates()
black_list = black_list.sort_values(by=['from'])
black_list = black_list.reset_index(drop=True)
black_list.to_csv('../data/data_out/main_bl.csv', index=False)

print('fin')
