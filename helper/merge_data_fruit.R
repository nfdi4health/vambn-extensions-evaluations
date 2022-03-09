
######### merge all data into right directories
merge_data_fruit<-function(){
  # Dir
  data_out<-'data/data_out/'
  
  #(standalone)
  data_all<-readRDS(file = paste0(data_out,'data_all_imp.rds'))
  data_stalone<-list(data_all[['stalone_VIS00']])
  data_stalone<-data_stalone %>% reduce(merge, by = 'SUBJID')
  #(aux)
  data_aux<-readRDS('data/data_out/data_aux.rds')
  data_aux<-data_aux %>% reduce(merge, by = 'SUBJID')
  data_aux<-as.data.frame(lapply(data_aux,factor))
  
  #(meta)
  data_meta<-read.csv('HI-VAE/metaenc.csv') #originally data/HI-VAE/metaenc.csv

  # merge all
  data<-list(data_meta,data_aux,data_stalone) %>% reduce(merge, by = 'SUBJID')
  
  #flag 0 var cols
  print(colnames(data)[-includeVar(data)])
  data<-data[includeVar(data)] #this removes all cols full of zeros => scodes and all the AUX cols where no entry is marked as 1
  
  data$SUBJID<-factor(data$SUBJID)
  # refactor all factor columns (so there are no empty levels)
  for(col in colnames(data)){
    if (is.factor(data[,col])|grepl('scode_',col)){
      data[,col]<-factor(data[,col])
    }else if (is.factor(data[,col])){
      data[,col]<-as.numeric(data[,col])
    }
  }
  
  name<-'data_final'
  saveRDS(data,paste0(data_out,name,'.rds'))
  return(data)
}
