#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 15:49:15 2018

Graph definition for all models

@author: anazabal, olmosUC3M, ivaleraM
"""

import tensorflow as tf
import numpy as np
import VAE_functions

def HVAE_graph(model_name, types_file, batch_size, n_vis, learning_rate=1e-3, z_dim=2, y_dim=1, s_dim=2, y_dim_partition=[]):
    
    #We select the model for the VAE
    print('[*] Importing model: ' + model_name)
    model = __import__(model_name)
    
    #Load placeholders
    print('[*] Defining placeholders')
    batch_data_list, batch_data_list_observed, miss_list, miss_list_VP, tau, types_list,zcodes,scodes = VAE_functions.place_holder_types(types_file, batch_size, n_vis)

    #reformat (rf) batch data lists TODO just read data as ncols*nvis*[batch,coldim] in the first place, kick this reformatting
    unstacked = [tf.unstack(t, axis=1) for t in batch_data_list] #ncols*nvis*[batch,coldim]
    batch_data_list_rf = [list(z) for z in list(zip(*unstacked))] #nvis*ncols*[batch,coldim]
    unstacked = [tf.unstack(t, axis=1) for t in batch_data_list_observed] #ncols*nvis*[batch,coldim]
    batch_data_list_observed_rf = [list(z) for z in list(zip(*unstacked))] #nvis*ncols*[batch,coldim]

    #Batch normalization of the data, called for each visit separately
    tup_X, tup_np = zip(*[VAE_functions.batch_normalization(batch_data_list_observed_rf[v], types_list, miss_list[:,v,:]) for v in range(n_vis)])
    X_list = list(tup_X)
    normalization_params = list(tup_np)

    #Set dimensionality of Y
    if y_dim_partition:
        y_dim_output = np.sum(y_dim_partition)
    else:
        y_dim_partition = y_dim*np.ones(len(types_list),dtype=int)
        y_dim_output = np.sum(y_dim_partition)

    #TF1 uses 'reuse' arg to reuse layers by the same name. Incorporating LSTMs meant switching everything to keras layers, which do not use this arg
    #   -> keras layers are supposed to be reused by referring to the initialized object again
    #Mimic the old reuse behaviour by remembering all initialized layers in this dict, with their names as keys
    kr_layers = {}

    print('[*] Defining LSTM_In...')
    h_end = model.lstm_in(X_list, n_units=20)

    print('[*] Defining Encoder...')
    samples, q_params = model.encoder(h_end, miss_list, batch_size, z_dim, s_dim, tau, kr_layers)
    
    print('[*] Defining Decoder...')
    theta, samples, p_params, log_p_x, log_p_x_missing = model.decoder(batch_data_list_rf, miss_list, types_list, samples, q_params, normalization_params, batch_size, z_dim, y_dim_output, y_dim_partition, n_vis, kr_layers)
    
    print('[*] Defining Cost function...')
    ELBO, loss_reconstruction, KL_z, KL_s = model.cost_function(log_p_x, p_params, q_params, types_list, z_dim, y_dim_output, s_dim)
    
    loss_reg=tf.losses.get_regularization_loss() # not using this at the moment (set weight_decay to 0 to be safe)
    optim = tf.train.AdamOptimizer(learning_rate).minimize(-ELBO)# + loss_reg)

    # fixed decoder for passing s/z codes and miss_list of VPs generated in the BNet
    samples_zgen, test_params_zgen, log_p_x_zgen, log_p_x_missing_zgen = model.fixed_decoder(batch_data_list_rf, miss_list_VP,miss_list, types_list, batch_size, z_dim, y_dim_output, y_dim_partition, n_vis, s_dim, tau, normalization_params,zcodes,scodes,kr_layers)

    #Packing results
    tf_nodes = {'ground_batch' : batch_data_list,
                'ground_batch_observed' : batch_data_list_observed,
                'miss_list': miss_list,
                'miss_list_VP': miss_list_VP,
                'tau_GS': tau,
                'zcodes': zcodes,
                'scodes': scodes,
                'samples': samples,
                'log_p_x': log_p_x,
                'log_p_x_missing': log_p_x_missing,
                'loss_re' : loss_reconstruction,
                'loss': -ELBO,
                'loss_reg':loss_reg,
                'optim': optim,
                'KL_s': KL_s,
                'KL_z': KL_z,
                'p_params': p_params,
                'q_params': q_params,
                'samples_zgen': samples_zgen,
                'test_params_zgen': test_params_zgen,
                'log_p_x_zgen': log_p_x_zgen,
                'log_p_x_missing_zgen': log_p_x_missing_zgen}

    return tf_nodes