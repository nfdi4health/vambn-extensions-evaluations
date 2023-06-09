make_bl_wl_donald<-function(data,blname,wlname,out=F,orphans){
  library(tidyverse)
  # get all possible combinations
  datan<-names(data)
  combs<-expand.grid(datan,datan)
  colnames(combs)<-c('from','to')
  
  # numeric visit columns
  combs$visfrom<-gsub('[a-zA-Z0-9_\\.]{1,}_VIS','',combs$from)
  combs$visto<-gsub('[a-zA-Z0-9_\\.]{1,}_VIS','',combs$to)
  
  #mark AUX data
  combs$aux<-ifelse((grepl('AUX_',combs$from) | grepl('AUX_',combs$to)),1,0)
  combs$auxto<-ifelse((grepl('AUX_',combs$to)),1,0)
  combs$auxfrom<-ifelse((grepl('AUX_',combs$from)),1,0)
  combs$vismis<-ifelse((grepl('visitmiss_',combs$from)|(grepl('visitmiss_',combs$to))),1,0)
  combs$vismisto<-ifelse((grepl('visitmiss_',combs$to)),1,0)
  combs$vismisfrom<-ifelse((grepl('visitmiss_',combs$from)),1,0)
  if (!any(is.na(orphans)))
    combs$orphan<-ifelse((combs$visto==combs$visfrom)&(combs$to %in% orphans)&(grepl('visitmiss_',combs$from)),1,0)
  
  # get numerical values for visit tps
  visits<-c(0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
  names(visits)<-c('00','01','02','03','04','05','06','07','08','09','10','11','12','13','14','15')
  combs$fromn<-unlist(lapply(combs$visfrom,function(x) visits[as.character(x)]))
  combs$ton<-unlist(lapply(combs$visto,function(x) visits[as.character(x)]))
  
  # blacklist (some of these deliberately overridden by whitelist settings)
  #  - duplicate connections #  - those back in time
  #  - those to family or gender #  - all to and from AUX
  #  - all from visitmiss, all to visitmiss if same visit
  bl<-subset(combs, fromn>ton | to=='SA_fam_ID_VIS00' | to=='SA_sex_VIS00' | aux==1 | vismisfrom==1 |(vismisto==1 & fromn==ton))
  bl<-rbind(bl,combs[grepl('scode_',combs$from),])
  
  # whitelist
  #  - aux to matching normal column #  - aux to future aux
  #  - parent missing visit to aux
  auxtonode<-subset(combs,auxfrom==1 | (auxfrom==1 & auxto==1 & ton-1==fromn))
  auxtonode<-auxtonode[gsub('zcode_|scode_','',auxtonode$to)==gsub('AUX_','',auxtonode$from),]
  auxtoaux<-subset(combs,(auxfrom==1 & auxto==1 & ton-1==fromn))
  auxtoaux<-auxtoaux[gsub('AUX_|_VIS[0-9]{1,}','',auxtoaux$to)==gsub('AUX_|_VIS[0-9]{1,}','',auxtoaux$from),]
  misstoaux<-subset(combs,vismisfrom==1 & auxto==1 & ton==fromn)
  misstomiss<-subset(combs,(vismisfrom==1 & vismisto==1 & ton-1==fromn))
  if (!any(is.na(orphans))){
    misstonode<-subset(combs,orphan==1) # this is when AUX identical to visitmiss! connect visitmiss to orphaned node
  }else{
    misstonode<-subset(combs,1==0)
  }
  s_to_z_node<-combs[grepl('scode_',combs$from)&grepl('zcode_',combs$to),]
  s_to_z_node<-s_to_z_node[gsub('zcode_','',s_to_z_node$to)==gsub('scode_','',s_to_z_node$from),]
  wl=rbind(auxtonode,auxtoaux,misstoaux,misstomiss,misstonode,s_to_z_node)
  
  # remove loop (shouldnt matter as bnlearn should do it automatically)
  bl<-bl[bl$from!=bl$to,]
  bl<-bl[!duplicated(bl), ]
  bl<-bl[order(bl$from),]
  wl<-wl[wl$from!=wl$to,]
  wl<-wl[!duplicated(wl),]
  wl<-wl[order(wl$from),]
  
  if (out){
    list(bll=bl[,c('from','to')],whl=wl[,c('from','to')])
  }else{
    # write lists to file
    write.csv(bl[,c('from','to')],blname,row.names = F)
    write.csv(wl[,c('from','to')],wlname,row.names = F)
  }
}