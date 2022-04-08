add_visitmiss_donald<-function(discdata){
  #if, for some visit, the aux-vars for all vargroups are 1, the visitmiss-var will be set to 1.
  #and, if there are no AUX vars, visitmiss-var will also be 1 for some reason.
  discdata$visitmiss_VIS00<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS00',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS01<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS01',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS02<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS02',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS03<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS03',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS04<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS04',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS05<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS05',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS06<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS06',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS07<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS07',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS08<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS08',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS09<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS09',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS10<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS10',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS11<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS11',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS12<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS12',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS13<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS13',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS14<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS14',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS15<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS15',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  #next, create one dX-var per visit summarizes its AUX-vars for every participant.
  #and for some reason this only works for visits that have a visitmiss=1 somewhere. if no participant missed this, code lands in a colname and everything is on fire
  #for some reason all dX vars contained visitmiss00, changed that
  d00<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS00', colnames(discdata)))|grepl('visitmiss_VIS00', colnames(discdata))]))
  d01<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS01', colnames(discdata)))|grepl('visitmiss_VIS01', colnames(discdata))]))
  d02<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS02', colnames(discdata)))|grepl('visitmiss_VIS02', colnames(discdata))]))
  d03<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS03', colnames(discdata)))|grepl('visitmiss_VIS03', colnames(discdata))]))
  d04<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS04', colnames(discdata)))|grepl('visitmiss_VIS04', colnames(discdata))]))
  d05<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS05', colnames(discdata)))|grepl('visitmiss_VIS05', colnames(discdata))]))
  d06<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS06', colnames(discdata)))|grepl('visitmiss_VIS06', colnames(discdata))]))
  d07<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS07', colnames(discdata)))|grepl('visitmiss_VIS07', colnames(discdata))]))
  d08<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS08', colnames(discdata)))|grepl('visitmiss_VIS08', colnames(discdata))]))
  d09<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS09', colnames(discdata)))|grepl('visitmiss_VIS09', colnames(discdata))]))
  d10<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS10', colnames(discdata)))|grepl('visitmiss_VIS10', colnames(discdata))]))
  d11<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS11', colnames(discdata)))|grepl('visitmiss_VIS11', colnames(discdata))]))
  d12<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS12', colnames(discdata)))|grepl('visitmiss_VIS12', colnames(discdata))]))
  d13<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS13', colnames(discdata)))|grepl('visitmiss_VIS13', colnames(discdata))]))
  d14<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS14', colnames(discdata)))|grepl('visitmiss_VIS14', colnames(discdata))]))
  d15<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS15', colnames(discdata)))|grepl('visitmiss_VIS15', colnames(discdata))]))
  rm00<-rownames(d00)[duplicated(d00, fromLast=TRUE)]
  rm01<-rownames(d01)[duplicated(d01, fromLast=TRUE)]
  rm02<-rownames(d02)[duplicated(d02, fromLast=TRUE)]
  rm03<-rownames(d03)[duplicated(d03, fromLast=TRUE)]
  rm04<-rownames(d04)[duplicated(d04, fromLast=TRUE)]
  rm05<-rownames(d05)[duplicated(d05, fromLast=TRUE)]
  rm06<-rownames(d06)[duplicated(d06, fromLast=TRUE)]
  rm07<-rownames(d07)[duplicated(d07, fromLast=TRUE)]
  rm08<-rownames(d08)[duplicated(d08, fromLast=TRUE)]
  rm09<-rownames(d09)[duplicated(d09, fromLast=TRUE)]
  rm10<-rownames(d10)[duplicated(d10, fromLast=TRUE)]
  rm11<-rownames(d11)[duplicated(d11, fromLast=TRUE)]
  rm12<-rownames(d12)[duplicated(d12, fromLast=TRUE)]
  rm13<-rownames(d13)[duplicated(d13, fromLast=TRUE)]
  rm14<-rownames(d14)[duplicated(d14, fromLast=TRUE)]
  rm15<-rownames(d15)[duplicated(d15, fromLast=TRUE)]
  rm<-c(rm00,rm01,rm02,rm04,rm05,rm06,rm07,rm08,rm09,rm10,rm11,rm12,rm13,rm14,rm15) # orphaned nodes are those whose immediate parent AUX is identical to the visitmiss at that visit
  return(list(data=discdata,rm=rm))
  
}