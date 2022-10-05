############# README
# This file runs the Bayesian network and saves out VPs
#############

############################
############################ Dependencies and helper functions
############################
rm(list=ls())
library(tidyverse)
library(arules)
library(mclust)
library(rpart)
library(bnlearn)
library(parallel)
# general helpers
# source('helper/plot_bn.R')
source('helper/clean_help.R')
source('helper/simulate_VP.R')
source('helper/save_VPmisslist.R')
# study specific helpers
source('helper/merge_data_fruit.R') #fruit can be reused
source('helper/addnoise.R') #unlike for fruit, default can be reused
source('helper/add_visitmiss_donald.R')
source('helper/make_bl_wl_donald.R')

############################
############################ Settings and preprocessing
############################

# Name output files
name<-'main'
data_out<-paste0('data/data_out/',name)
scr<-"bic-cg" # BN score
mth<-"mle" # BN method

# Load data & remaining formatting of standalone
data<-merge_data_fruit() # merge imputed standalone and zcodes from HIVAE
#this merges all info, incl AUX, into one table (data) and also writes that into data_final.rds

# remove subject variable
pt<-data$SUBJID
data$SUBJID<-NULL

# add noise to the imputed/constant levels of continuous variables, prevents error in the BN due to singular data
discdata<-addnoise(data,0.01)

# Add parents for AUX variables
# This node represents whether a whole visit is missing for a participant
# AUX variables will be connected through these and it will account for their high correlation
# AUX variables that are identical to the visitmiss variables will be removed and its child node connected directly to the visitmiss variable at that visit
out<-add_visitmiss_donald(discdata)
discdata<-out[['data']]
rm<-out[['rm']]
discdata<-discdata[ , !(names(discdata) %in% rm)]
# remove AUX that are almost identical to visitmiss nodes
lowaux<-discdata[,grepl('AUX_',colnames(discdata))&!(colnames(discdata) %in% rm)]
#this tmp is <2-dimensional if there weren't at least 2 working dX-vars in add_visitmiss, and breaks everything
if (dim(lowaux)[2] > 0){
  # tmp<-sapply(colnames(lowaux),function(x) sum(as.numeric(as.character(lowaux[,x])))<=5) #only if 5 vars, ignore this because tiny data
  tmp<-sapply(colnames(lowaux),function(x) sum(as.numeric(as.character(lowaux[,x])))<=1)
  lowaux<-colnames(lowaux)[tmp]
  discdata<-discdata[ , !(names(discdata) %in% lowaux)]
}
orphans<-gsub('AUX_','',rm)
orphans<-unname(sapply(orphans,function(x) ifelse(!grepl('SA_',x),paste0('zcode_',x),x)))

############################
############################ Bnet
############################

# Make bl/wl
datan<-names(discdata)
write.csv(datan,'data/data_out/data_names.csv',row.names = F)
#stop()
blname<-paste0(data_out,'_bl.csv')
wlname<-paste0(data_out,'_wl.csv')
#make_bl_wl_donald(discdata,blname,wlname,F,orphans) # rm has info about "orphaned" nodes (need to be connected to visitmiss, not to AUX)
bl<-read.csv(blname)
wl<-read.csv(wlname)

# Final bayesian network
finalBN = tabu(discdata, maxp=5, blacklist=bl, whitelist=wl, score=scr)

saveRDS(finalBN,paste0(data_out,'_finalBN.rds'))
print('TABU DONE')

# Bootstrapped network
cores = detectCores()
cl =  makeCluster(cores)
boot.stren = boot.strength(discdata, algorithm="tabu", R=1000, algorithm.args = list(maxp=5, blacklist=bl, whitelist=wl, score=scr), cluster=cl)
stopCluster(cl)
saveRDS(boot.stren,paste0(data_out,'_bootBN.rds'))
print('BOOT DONE')

# save fitted network
real = discdata
finalBN<-readRDS(paste0(data_out,'_finalBN.rds'))
fitted = bn.fit(finalBN, real, method=mth)
saveRDS(fitted,paste0(data_out,'_finalBN_fitted.rds'))
print('FIT DONE')

############################
############################ VP vs RP
############################

# Virtual Patient Generation
virtual<-simulate_VPs(real,finalBN,fitted,iterative=F,scr,mth,wl,bl,n=1312)

############################
############################ save out all data
############################

# save out real and virtual patients
real$SUBJID<-pt
saveRDS(virtual,paste0(data_out,'_VirtualPPts.rds'))
write.csv(virtual,paste0(data_out,'_VirtualPPts.csv'),row.names=FALSE)
saveRDS(real,paste0(data_out,'_RealPPts.rds'))
real$SUBJID<-NULL
write.csv(real,paste0(data_out,'_RealPPts.csv'),row.names=FALSE)

# save out VP misslist (for HIVAE decoding, tells HIVAE which zcodes the BN considers missing)
save_VPmisslist(virtual,'HI-VAE/') #originally data/HI-VAE/

############################
############################ plot graphs in cytoscape (careful about dashed line maps!)
############################
# source('network_plot_paper.R')

print('BNet finished')
