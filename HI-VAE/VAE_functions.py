#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 10:59:14 2018

@author: anazabal
"""

import csv
import tensorflow as tf
from keras.layers import *
import loglik_models_missing_normalize
import numpy as np

def place_holder_types(types_file, batch_size, n_vis):
    
    #Read the types of the data from the files
    with open(types_file) as f:
        types_list = [{k: v for k, v in row.items()}
        # types_list = [{k: v if k == 'type' else int(v) for k, v in row.items()} in case of
        for row in csv.DictReader(f, skipinitialspace=True)]
        
    #Create placeholders for every data type, with appropriate dimensions
    batch_data_list = []
    for i in range(len(types_list)):
        batch_data_list.append(tf.placeholder(tf.float32, shape=(batch_size, n_vis, types_list[i]['dim'])))
    tf.concat(batch_data_list, axis=2) #result not used
    
    #Create placeholders for every missing data type, with appropriate dimensions
    batch_data_list_observed = []
    for i in range(len(types_list)):
        batch_data_list_observed.append(tf.placeholder(tf.float32, shape=(batch_size, n_vis, types_list[i]['dim'])))
    tf.concat(batch_data_list_observed, axis=2)
        
    #Create placeholders for the missing data indicator variable
    miss_list = tf.placeholder(tf.int32, shape=(batch_size, n_vis, len(types_list)))
    miss_list_VP = tf.placeholder(tf.int32, shape=(batch_size, n_vis, len(types_list)))
    
    #Placeholder for Gumbel-softmax parameter
    tau = tf.placeholder(tf.float32,shape=())
    
    zcodes=tf.placeholder(tf.float32, shape=(batch_size,1))
    scodes=tf.placeholder(tf.int32, shape=(batch_size,1))
    
    return batch_data_list, batch_data_list_observed, miss_list,miss_list_VP, tau, types_list,zcodes,scodes

def batch_normalization(batch_data_list, types_list, miss_list):
    
    normalized_data = []
    normalization_parameters = []
    
    for i,d in enumerate(batch_data_list):
        #Partition the data in missing data (0) and observed data n(1)
        missing_data, observed_data = tf.dynamic_partition(d, miss_list[:,i], num_partitions=2)
        condition_indices = tf.dynamic_partition(tf.range(tf.shape(d)[0]), miss_list[:,i], num_partitions=2)
        
        if types_list[i]['type'] == 'real':
            #We transform the data to a gaussian with mean 0 and std 1
            data_mean, data_var = tf.nn.moments(observed_data,0)
            data_var = tf.clip_by_value(data_var,1e-6,1e20) #Avoid zero values
            aux_X = tf.nn.batch_normalization(observed_data,data_mean,data_var,offset=0.0,scale=1.0,variance_epsilon=1e-6)
            
            normalized_data.append(tf.dynamic_stitch(condition_indices, [missing_data, aux_X]))
            normalization_parameters.append([data_mean, data_var])
            
        #When using log-normal
        elif types_list[i]['type'] == 'pos':
#           #We transform the log of the data to a gaussian with mean 0 and std 1
            observed_data_log = tf.log(1 + observed_data)
            data_mean_log, data_var_log = tf.nn.moments(observed_data_log,0)
            data_var_log = tf.clip_by_value(data_var_log,1e-6,1e20) #Avoid zero values
            aux_X = tf.nn.batch_normalization(observed_data_log,data_mean_log,data_var_log,offset=0.0,scale=1.0,variance_epsilon=1e-6)
            
            normalized_data.append(tf.dynamic_stitch(condition_indices, [missing_data, aux_X]))
            normalization_parameters.append([data_mean_log, data_var_log])
            
        elif types_list[i]['type'] == 'count':
            
            #Input log of the data
            aux_X = tf.log(observed_data)
            
            normalized_data.append(tf.dynamic_stitch(condition_indices, [missing_data, aux_X]))
            normalization_parameters.append([0.0, 1.0])
            
            
        else:
            #Don't normalize the categorical and ordinal variables
            normalized_data.append(d)
            normalization_parameters.append([0.0, 1.0]) #No normalization here
    
    return normalized_data, normalization_parameters

def s_proposal_multinomial(X, batch_size, s_dim, tau, reuse, kr_layers):
    
    #We propose a categorical distribution to create a GMM for the latent space z
    layername = 'layer_1_' + 'enc_s'
    if reuse:
        dense = kr_layers[layername]
    else:
        dense = Dense(units=s_dim, activation=None, kernel_initializer=tf.random_normal_initializer(stddev=0.05), name=layername)
        kr_layers[layername] = dense
    log_pi = dense(X)

    #Gumbel-softmax trick
    U = -tf.log(-tf.log(tf.random_uniform([batch_size,s_dim])))
    samples_s = tf.nn.softmax((log_pi + U)/tau)
    
    return samples_s, log_pi

def z_proposal_GMM(X, samples_s, batch_size, z_dim, reuse, kr_layers):
    
    #We propose a GMM for z
    layer1name = 'layer_1_' + 'mean_enc_z'
    layer2name = 'layer_1_' + 'logvar_enc_z'
    if reuse:
        dense1 = kr_layers[layer1name]
        dense2 = kr_layers[layer2name]
    else:
        dense1 = Dense(units=z_dim, activation=None, kernel_initializer=tf.random_normal_initializer(stddev=0.05), name=layer1name)
        kr_layers[layer1name] = dense1
        dense2 = Dense(units=z_dim, activation=None, kernel_initializer=tf.random_normal_initializer(stddev=0.05), name=layer2name)
        kr_layers[layer2name] = dense2
    mean_qz = dense1(tf.concat([X,samples_s],1))
    log_var_qz = dense2(tf.concat([X,samples_s],1))
    
    # Avoid numerical problems
    log_var_qz = tf.clip_by_value(log_var_qz,-15.0,15.0)
    # Rep-trick
    eps = tf.random_normal((batch_size, z_dim), 0, 1, dtype=tf.float32)
    samples_z = mean_qz+tf.multiply(tf.exp(log_var_qz/2), eps)
    
    return samples_z, [mean_qz, log_var_qz]

def z_distribution_GMM(samples_s, z_dim, reuse, kr_layers):
    
    #We propose a GMM for z
    layername = 'layer_1_' + 'mean_dec_z'
    if reuse:
        dense = kr_layers[layername]
    else:
        dense = Dense(units=z_dim, activation=None, kernel_initializer=tf.random_normal_initializer(stddev=0.05), name=layername)
        kr_layers[layername] = dense
    mean_pz = dense(samples_s)
    log_var_pz = tf.zeros([tf.shape(samples_s)[0],z_dim])
    
    # Avoid numerical problems
    log_var_pz = tf.clip_by_value(log_var_pz,-15.0,15.0)
    
    return mean_pz, log_var_pz

def y_partition(samples_y, types_list, y_dim_partition, n_vis):

    grouped_samples_y = []
    #First element must be 0 and the length of the partition vector must be len(types_dict)+1
    if len(y_dim_partition) != len(types_list):
        raise Exception("The length of the partition vector must match the number of variables in the data + 1")
        
    #Insert a 0 at the beginning of the cumsum vector
    partition_vector_cumsum = np.insert(np.cumsum(y_dim_partition),0,0)
    y_split = tf.split(samples_y, n_vis, axis=1)
    for vis_samples_y in y_split:
        vis_grouped_samples_y = []
        for i in range(len(types_list)):
            vis_grouped_samples_y.append(vis_samples_y[:,partition_vector_cumsum[i]:partition_vector_cumsum[i+1]])
        grouped_samples_y.append(vis_grouped_samples_y)
    
    return grouped_samples_y

def theta_estimation_from_y(samples_y, types_list, miss_list, batch_size, reuse, kr_layers):
    
    theta = []
    for v, vis_samples in enumerate(samples_y):
        vis_theta = []
        #Independet yd -> Compute p(xd|yd)
        for i,d in enumerate(vis_samples):

            #Partition the data in missing data (0) and observed data (1)
            missing_y, observed_y = tf.dynamic_partition(d, miss_list[:,v,i], num_partitions=2)
            condition_indices = tf.dynamic_partition(tf.range(tf.shape(d)[0]), miss_list[:,v,i], num_partitions=2)
            nObs = tf.shape(observed_y)[0]

            #Different layer models for each type of variable
            if types_list[i]['type'] == 'real':
                params = theta_real(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers)

            elif types_list[i]['type'] == 'pos':
                params = theta_pos(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers)

            elif types_list[i]['type'] == 'count':
                params = theta_count(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers)

            elif types_list[i]['type'] == 'cat':
                params = theta_cat(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers)

            elif types_list[i]['type'] == 'ordinal':
                params = theta_ordinal(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers)

            vis_theta.append(params)
        theta.append(vis_theta)
            
    return theta

def theta_real(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers):
    
    #Mean layer
    h2_mean = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=types_list[i]['dim'], name='layer_h2' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    #Sigma Layer
    h2_sigma = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=types_list[i]['dim'], name='layer_h2_sigma' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    
    return [h2_mean, h2_sigma]

def theta_pos(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers):
    
    #Mean layer
    h2_mean = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=types_list[i]['dim'], name='layer_h2' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    #Sigma Layer
    h2_sigma = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=types_list[i]['dim'], name='layer_h2_sigma' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    
    return [h2_mean, h2_sigma]

def theta_count(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers):
    
    #Lambda Layer
    h2_lambda = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=types_list[i]['dim'], name='layer_h2' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    
    return h2_lambda

def theta_cat(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers):
    
    #Log pi layer, with zeros in the first value to avoid the identificability problem
    h2_log_pi_partial = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=int(types_list[i]['dim'])-1, name='layer_h2' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    h2_log_pi = tf.concat([tf.zeros([batch_size,1]), h2_log_pi_partial],1)
    
    return h2_log_pi

def theta_ordinal(observed_y, missing_y, condition_indices, types_list, nObs, batch_size, i, v, reuse, kr_layers):
    
    #Theta layer, Dimension of ordinal - 1
    h2_theta = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=int(types_list[i]['dim'])-1, name='layer_h2' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    #Mean layer, a single value
    h2_mean = observed_data_layer(observed_y, missing_y, condition_indices, output_dim=1, name='layer_h2_sigma' + str(i) + str(v), reuse=reuse, kr_layers=kr_layers)
    
    return [h2_theta, h2_mean]

def observed_data_layer(observed_data, missing_data, condition_indices, output_dim, name, reuse, kr_layers):
    
    #Train a layer with the observed data and reuse it for the missing data
    if reuse: #if True, also reuse for obs, otherwise only reuse for miss
        dense = kr_layers[name]
    else:
        dense = Dense(units=int(output_dim), activation=None, kernel_initializer=tf.random_normal_initializer(stddev=0.05),name=name,trainable=True)
        kr_layers[name] = dense
    obs_output = dense(observed_data)
    miss_output = dense(missing_data) #trainable=False?
    #Join back the data
    output = tf.dynamic_stitch(condition_indices, [miss_output,obs_output])
    
    return output


def loglik_evaluation(batch_data_list, types_list, miss_list, theta, normalization_params, reuse):
    #reuse arg never used -> manual reuse via kr_layers not implemented

    log_p_x = []
    log_p_x_missing = []
    samples_x = []
    params_x = []

    for v, vis_data in enumerate(batch_data_list):
        vis_log_p_x = []
        vis_log_p_x_missing = []
        vis_samples_x = []
        vis_params_x = []

        #Independet yd -> Compute log(p(xd|yd))
        for i,d in enumerate(vis_data):

            # Select the likelihood for the types of variables
            loglik_function = getattr(loglik_models_missing_normalize, 'loglik_' + types_list[i]['type'])

            out = loglik_function([d,miss_list[:,v,i]], types_list[i], theta[v][i], normalization_params[v][i],
                                      kernel_initializer=tf.random_normal_initializer(stddev=0.05), name='layer_1_mean_dec_x' + str(i), reuse=reuse)

            vis_log_p_x.append(out['log_p_x'])
            vis_log_p_x_missing.append(out['log_p_x_missing']) #Test-loglik element
            vis_samples_x.append(out['samples'])
            vis_params_x.append(out['params'])

        log_p_x.append(vis_log_p_x)
        log_p_x_missing.append(vis_log_p_x_missing)
        samples_x.append(vis_samples_x)
        params_x.append(vis_params_x)
        
    return log_p_x, log_p_x_missing, samples_x, params_x