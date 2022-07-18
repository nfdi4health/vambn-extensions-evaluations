#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  6 15:40:14 2017

Functions needed to read the data from different databases

@author: anazabal, olmosUC3M, ivaleraM
"""

import csv
import numpy as np
import os
from sklearn.metrics import mean_squared_error

def read_data(data_file0, types_file0, miss_file0, true_miss_file0, n_vis):

    #Prepare reading all visits at once, not just VIS00
    data_files = [data_file0.replace('_VIS00', '_VIS'+str(v).zfill(2)) for v in range(n_vis)]
    types_files = [types_file0.replace('_VIS00', '_VIS'+str(v).zfill(2)) for v in range(n_vis)]
    miss_files = [miss_file0.replace('_VIS00', '_VIS'+str(v).zfill(2)) for v in range(n_vis)]
    true_miss_files = [true_miss_file0.replace('_VIS00', '_VIS'+str(v).zfill(2)) for v in range(n_vis)]

    #Read types of data from data files
    data_visits = []
    for types_file in types_files:
        with open(types_file) as f:
            types_dict = [{k: v for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
    
    #Read data from input files
    data_visits = []
    for data_file in data_files:
        with open(data_file, 'r') as f:
            data_vis = [[float(x) for x in rec] for rec in csv.reader(f, delimiter=',')]
            data_visits.append(np.array(data_vis))
    data = np.stack(data_visits, 1)
    
    #Sustitute NaN values by something (we assume we have the real missing value mask)
    true_miss_mask_visits = []
    for true_miss_file in true_miss_files:
        true_miss_mask_vis = np.ones([np.shape(data)[0], len(types_dict)])
        if true_miss_file and os.path.getsize(true_miss_file) > 0:
            with open(true_miss_file, 'r') as f:
                missing_positions = [[int(x) for x in rec] for rec in csv.reader(f, delimiter=',')]
                missing_positions = np.array(missing_positions)
            true_miss_mask_vis[missing_positions[:,0]-1,missing_positions[:,1]-1] = 0 #Indexes in the csv start at 1
        true_miss_mask_visits.append(true_miss_mask_vis)
    true_miss_mask = np.stack(true_miss_mask_visits, 1)

    data_masked = np.ma.masked_where(np.isnan(data),data)
    #We need to fill the data depending on the given data...
    data_filler = []
    for i in range(len(types_dict)):
        if types_dict[i]['type'] == 'cat' or types_dict[i]['type'] == 'ordinal':
            aux = np.unique(data[:,:,i])
            if not np.isnan(aux[0]):
                data_filler.append(aux[0])  #Fill with the first element of the cat (0, 1, or whatever)
            else:
                data_filler.append(int(0))
        else:
            data_filler.append(0.0)

    data = data_masked.filled(data_filler)
    
    #Construct the data matrices
    data_complete = []
    for i in range(np.shape(data)[2]):
        
        if types_dict[i]['type'] == 'cat':
            data_allvis = []
            for v in range(n_vis):
                #Get categories
                cat_data = [int(x) for x in data[:,v,i]]
                categories, indexes = np.unique(cat_data,return_inverse=True)
                #Transform categories to a vector of 0:n_categories
                new_categories = np.arange(int(types_dict[i]['dim']))
                cat_data = new_categories[indexes]
                #Create one hot encoding for the categories
                aux = np.zeros([np.shape(data)[0],len(new_categories)])
                aux[np.arange(np.shape(data)[0]),cat_data] = 1
                data_allvis.append(aux)
            data_complete.append(np.stack(data_allvis,1))
            
        elif types_dict[i]['type'] == 'ordinal':
            data_allvis = []
            for v in range(n_vis):
                #Get categories
                cat_data = [int(x) for x in data[:,v,i]]
                categories, indexes = np.unique(cat_data,return_inverse=True)
                #Transform categories to a vector of 0:n_categories
                new_categories = np.arange(int(types_dict[i]['dim']))
                cat_data = new_categories[indexes]
                #Create thermometer encoding for the categories
                aux = np.zeros([np.shape(data)[0],1+len(new_categories)])
                aux[:,0] = 1
                aux[np.arange(np.shape(data)[0]),1+cat_data] = -1
                aux = np.cumsum(aux,1)
                data_allvis.append(aux)
            data_complete.append(np.stack(data_allvis,1))
            
        else:
            data_complete.append(np.expand_dims(data[:,:,i],2))

    data = np.concatenate(data_complete,2)
    
        
    #Read Missing mask from csv (contains positions of missing values)
    n_samples = np.shape(data)[0]
    n_variables = len(types_dict)
    miss_mask_visits = []
    for miss_file in miss_files:
        miss_mask_vis = np.ones([np.shape(data)[0],n_variables])
        #If there is no mask, assume all data is observed
        if os.path.isfile(miss_file):
            with open(miss_file, 'r') as f:
                missing_positions = [[int(x) for x in rec] for rec in csv.reader(f, delimiter=',')]
                missing_positions = np.array(missing_positions)
            miss_mask_vis[missing_positions[:,0]-1,missing_positions[:,1]-1] = 0 #Indexes in the csv start at 1
        miss_mask_visits.append(miss_mask_vis)
    miss_mask = np.stack(miss_mask_visits, 1)
        
    return data, types_dict, miss_mask, true_miss_mask, n_samples


def next_batch(data, types_dict, miss_mask, batch_size, index_batch):
    
    #Create minibath
    batch_xs = data[index_batch*batch_size:(index_batch+1)*batch_size, :, :]
    
    #Slipt variables of the batches
    data_list = []
    initial_index = 0
    for d in types_dict:
        dim = int(d['dim'])
        data_list.append(batch_xs[:,:,initial_index:initial_index+dim])
        initial_index += dim
    
    #Missing data
    miss_list = miss_mask[index_batch*batch_size:(index_batch+1)*batch_size, :]

    return data_list, miss_list

def samples_concatenation(samples):

    batches_samples_x = []
    for i,batch in enumerate(samples):
        vis_samples_x = []
        for v, vis_x in enumerate(batch['x']):
            vis_samples_x.append(np.concatenate(vis_x,1))
        batches_samples_x.append(vis_samples_x)
        if i == 0:
            samples_y = batch['y']
            samples_z = batch['z']
            samples_s = batch['s']
        else:
            samples_y = np.concatenate([samples_y,batch['y']],0)
            samples_z = np.concatenate([samples_z,batch['z']],0)
            samples_s = np.concatenate([samples_s,batch['s']],0)
    x_arr = list(np.swapaxes(np.array(batches_samples_x), 1, 2)) #nbatch*[batchsize,nvis,coldim]
    return samples_s, samples_z, samples_y, np.concatenate(x_arr, 0)

def discrete_variables_transformation(data, types_dict):

    output = []
    for v in range(data.shape[1]):
        vis_data = data[:,v,:]
        ind_ini = 0
        vis_output = []
        for d in range(len(types_dict)):
            ind_end = ind_ini + int(types_dict[d]['dim'])
            if types_dict[d]['type'] == 'cat':
                vis_output.append(np.reshape(np.argmax(vis_data[:,ind_ini:ind_end],1),[-1,1]))
            elif types_dict[d]['type'] == 'ordinal':
                vis_output.append(np.reshape(np.sum(vis_data[:,ind_ini:ind_end],1) - 1,[-1,1]))
            else:
                vis_output.append(vis_data[:,ind_ini:ind_end])
            ind_ini = ind_end
        output.append(np.concatenate(vis_output,1))
    
    return np.stack(output,1)

#Several baselines
def mean_imputation(train_data, miss_mask, types_dict):
    
    ind_ini = 0
    est_data = []
    for dd in range(len(types_dict)):
        #Imputation for cat and ordinal is done using the mode of the data
        if types_dict[dd]['type']=='cat' or types_dict[dd]['type']=='ordinal':
            ind_end = ind_ini + 1
            #The imputation is based on whatever is observed
            miss_pattern = (miss_mask[:,dd]==1)
            values, counts = np.unique(train_data[miss_pattern,ind_ini:ind_end],return_counts=True)
            data_mode = np.argmax(counts)
            data_imputed = train_data[:,ind_ini:ind_end]*miss_mask[:,ind_ini:ind_end] + data_mode*(1.0-miss_mask[:,ind_ini:ind_end])
            
        #Imputation for the rest of the variables is done with the mean of the data
        else:
            ind_end = ind_ini + int(types_dict[dd]['dim'])
            miss_pattern = (miss_mask[:,dd]==1)
            #The imputation is based on whatever is observed
            data_mean = np.mean(train_data[miss_pattern,ind_ini:ind_end],0)
            data_imputed = train_data[:,ind_ini:ind_end]*miss_mask[:,ind_ini:ind_end] + data_mean*(1.0-miss_mask[:,ind_ini:ind_end])
            
        est_data.append(data_imputed)
        ind_ini = ind_end
    
    return np.concatenate(est_data,1)

def p_distribution_params_concatenation(params,types_dict,z_dim,s_dim):
    
    keys = params[0].keys()
    out_dict = {key: [] for key in keys}
    
    for i,batch in enumerate(params):
        
        for d,k in enumerate(keys):
            
            if k == 'z' or k == 'y':
                if i == 0:
                    out_dict[k] = batch[k]
                else:
                    out_dict[k] = np.concatenate([out_dict[k],batch[k]],1)
                    
            elif k == 'x':
                if i == 0:
                    out_dict[k] = batch[k]
                else:
                    for v in range(len(types_dict)):
                        if types_dict[v]['type'] == 'pos' or types_dict[v]['type'] == 'real':
                            out_dict[k][v] = np.concatenate([out_dict[k][v],batch[k][v]],1)
                        else:
                            out_dict[k][v] = np.concatenate([out_dict[k][v],batch[k][v]],0)
        
    return out_dict

def q_distribution_params_concatenation(params,z_dim,s_dim):
    
    keys = params[0].keys()
    out_dict = {key: [] for key in keys}
    
    for i,batch in enumerate(params):
        for d,k in enumerate(keys):
            out_dict[k].append(batch[k])
            
    out_dict['z'] = np.concatenate(out_dict['z'],1)
    out_dict['s'] = np.concatenate(out_dict['s'],0)
        
    return out_dict

def statistics(loglik_params,types_dict):
    
    loglik_mean = []
    loglik_mode = []
    
    for d,attrib in enumerate(loglik_params):
        if types_dict[d]['type'] == 'real':
            #Normal distribution (mean, sigma)
            loglik_mean.append(attrib[0])
            loglik_mode.append(attrib[0])
        #Only for log-normal
        elif types_dict[d]['type'] == 'pos':
            #Log-normal distribution (mean, sigma)
            loglik_mean.append(np.exp(attrib[0] + 0.5*attrib[1]) - 1.0)
            loglik_mode.append(np.exp(attrib[0] - attrib[1]) - 1.0)
        elif types_dict[d]['type'] == 'count':
            #Poisson distribution (lambda)
            loglik_mean.append(attrib)
            loglik_mode.append(np.floor(attrib))
        
        else:
            #Categorical and ordinal (mode imputation for both)
            loglik_mean.append(np.reshape(np.argmax(attrib,1),[-1,1]))
            loglik_mode.append(np.reshape(np.argmax(attrib,1),[-1,1]))
        
            
    return np.transpose(np.squeeze(loglik_mean)), np.transpose(np.squeeze(loglik_mode))

def error_computation(x_train, x_hat, types_dict, miss_mask):
    
    error_observed = []
    error_missing = []
    ind_ini = 0
    for dd in range(len(types_dict)):
        #Mean classification error
        if types_dict[dd]['type']=='cat':
            ind_end = ind_ini + 1
            error_observed.append(np.mean(x_train[miss_mask[:,dd]==1,ind_ini:ind_end] != x_hat[miss_mask[:,dd]==1,ind_ini:ind_end]))
            if np.sum(miss_mask[:,dd]==0,0) == 0:
                error_missing.append(0)
            else:
                error_missing.append(np.mean(x_train[miss_mask[:,dd]==0,ind_ini:ind_end] != x_hat[miss_mask[:,dd]==0,ind_ini:ind_end]))
        #Mean "shift" error        
        elif types_dict[dd]['type']=='ordinal':
            ind_end = ind_ini + 1
            error_observed.append(np.mean(np.abs(x_train[miss_mask[:,dd]==1,ind_ini:ind_end] -x_hat[miss_mask[:,dd]==1,ind_ini:ind_end]))/int(types_dict[dd]['dim']))
            if np.sum(miss_mask[:,dd]==0,0) == 0:
                error_missing.append(0)
            else:
                error_missing.append(np.mean(np.abs(x_train[miss_mask[:,dd]==0,ind_ini:ind_end] -x_hat[miss_mask[:,dd]==0,ind_ini:ind_end]))/int(types_dict[dd]['dim']))
        #Normalized root mean square error
        else:
            ind_end = ind_ini + int(types_dict[dd]['dim'])
            norm_term = np.max(x_train[miss_mask[:,dd]==1,dd]) - np.min(x_train[miss_mask[:,dd]==1,dd])
            error_observed.append(np.sqrt(mean_squared_error(x_train[miss_mask[:,dd]==1,ind_ini:ind_end],x_hat[miss_mask[:,dd]==1,ind_ini:ind_end]))/norm_term)
            if np.sum(miss_mask[:,dd]==0,0) == 0:
                error_missing.append(0)
            else:
                error_missing.append(np.sqrt(mean_squared_error(x_train[miss_mask[:,dd]==0,ind_ini:ind_end],x_hat[miss_mask[:,dd]==0,ind_ini:ind_end]))/norm_term)
                
        ind_ini = ind_end
                
    return error_observed, error_missing


"""
Creates a random permutation of the indexes in range(len(miss_list)), meant to be used for splitting data into minibatches.
However, it makes sure that nonmissing values are evenly distributed across all the batches.
This prevents batches with 100% missing values, which would lead to NaN loss.
author: jschneider
"""
def stratified_permutation(miss_list, batch_size, n_batches):
    # get indexes of missing/observed values
    m_idx = np.random.permutation(np.argwhere(miss_list[:,0,0] == 0.0)) #0.0 indicates missingness
    o_idx = np.random.permutation(np.argwhere(miss_list[:,0,0] == 1.0))
    assert len(o_idx) > n_batches, 'There are less observed values than minibatches'

    stratified_idx = np.empty(shape=(0, 0), dtype='int64')
    for o_part in np.array_split(o_idx, n_batches): #split available observed values evenly into batches
        add_n = batch_size - len(o_part) #this many missing values need to be added to reach batch size
        batch = np.random.permutation(np.append(o_part, m_idx[:add_n]))
        m_idx = m_idx[add_n:]
        stratified_idx = np.append(stratified_idx, batch)

    # np.append(stratified_idx, m_idx) #use this in case len(stratified_idx) needs to be increased from batch_size*n_batch to sample_size
    return stratified_idx
