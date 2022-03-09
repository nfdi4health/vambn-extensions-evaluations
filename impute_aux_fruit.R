############# README
# This is the data imputation file. For HI-VAE there is no actual imputation, just saveout.
# Before this, run the R files clean_data->format_data->impute_aux (scripts with fixed settings).
# After this, run the autoencoder jupyter notebook (HI-VAE).
############## 

# install.packages('missForest')
# install.packages('beepr')

rm(list=ls())
library(missForest)
source('helper/make_dummy.R') # create dummies for categorical variables
source('helper/clean_help.R') # check for constant variables
source('helper/fill_na.R') # fill na with mean or most frequent cat
source('helper/save_py.R') # fill na with mean or most frequent cat
data_out<-'data/data_out/'
data_out_py<-'HI-VAE/data_python/' #originally data/HI-VAE/data_python/

###################### Imputation & AUX
#setwd("./paper/ADNI")
data_all<-readRDS(file = paste0("data/fruit-data_condensed.rds"))
data_aux=list()
for (datan in names(data_all)){ # for every variable group
  
  # load data & remove SUBJID
  data<-data_all[[datan]]
  pt<-data$SUBJID
  data$SUBJID<-NULL
  
  #if (!grepl('stalone_VIS6|stalone_VIS12|stalone_VIS24|snp_VIS1', datan)){ #JS: does this skip all vargroups with only 1 column, as they can't be accessed by [x,y]?
  if (!grepl('stalone_VIS00', datan)){
    # remove bad data
    data=data[,includeVar(data)]
    data=data[,rmMiss(data)]
  }
  
  ###################### AUX variables
  
  # make AUX columns and save in separate list (with SUBJID)
  # AUX if A) stalone missing, or B) all/any entries of a vargroup are missing: which one?
  nms<-colnames(data)
  if (grepl('stalone', datan)){
    dataux<-as.data.frame(sapply(as.data.frame(is.na(data)), as.numeric)) #A
    dataux<-as.data.frame(sapply(dataux,factor))
    colnames(dataux)<-paste('AUX',nms,sep='_')
  }else{
    dataux<-data.frame(factor(apply(data,1,function(x) as.numeric(any(is.na(x)))))) #B: all( or any(is.na(x)) ?
    colnames(dataux)<-paste('AUX',datan,sep='_')
  }
  
  # update AUX list
  dataux$SUBJID<-pt
  data_aux[[datan]]<-dataux
  
  ###################### Imputation
  print(datan)
  if (grepl('stalone', datan))
    data<-fillna(data) # if standalone data, mean and most frequent class imputation

  # if (!grepl('stalone_VIS6|stalone_VIS12|stalone_VIS24|snp_VIS1', datan)){
  if (!grepl('stalone_VIS00', datan)){
    # remove bad data
    data=data[,includeVar(data)]
    data=data[,rmMiss(data)]
  }
  
  # add ppt variable and update data list
  data$SUBJID <- pt
  data_all[[datan]]<-data
  
  # save out csv's of scaled continous and dummy coded categorical data for autoencoders
  pt<-data$SUBJID
  data$SUBJID<-NULL

  #missing write
  if (!grepl('stalone', datan))
    write.table(which(is.na(data), arr.ind=TRUE),paste0(data_out_py,datan,'_missing.csv'),sep=',',row.names = F,col.names = F,quote=F)
  
  #data write
  if (!grepl('stalone', datan))
    write.table(data,paste0(data_out_py,datan,'.csv'),sep=',',row.names = F,col.names = F,quote=F, na = "NaN")
  
  write.table(as.character(pt),paste0('HI-VAE/python_names/',datan,'_subj.csv'),sep=',',row.names = F,col.names = T,quote=T, na = "NaN") #originally data/HI-VAE/python_names/
  write.table(colnames(data),paste0('HI-VAE/python_names/',datan,'_cols.csv'),sep=',',row.names = F,col.names = T,quote=T, na = "NaN") #originally data/HI-VAE/python_names/
}

# save all
saveRDS(data_all, file = paste0(data_out,'data_all_imp.rds'))
saveRDS(data_aux, file = paste0(data_out,'data_aux.rds'))

library(beepr)
beep()


