add_visitmiss_fruit<-function(discdata){
  #if, for some visit, the aux-vars for all vargroups are 1, the visitmiss-var will be set to 1.
  #and, if there are no AUX vars, visitmiss-var will also be 1 for some reason.
  discdata$visitmiss_VIS00<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS00',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS01<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS01',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  discdata$visitmiss_VIS02<-factor(ifelse(apply(discdata[,grepl('AUX_',colnames(discdata))&grepl('_VIS02',colnames(discdata))],1,function(x) (all(x==1))),1,0))
  #next, create one dX-var per visit summarizes its AUX-vars for every participant.
  #and for some reason this only works for visits that have a visitmiss=1 somewhere. if no participant missed this, code lands in a colname and everything is on fire
  #for some reason all dX vars contained visitmiss00, changed that
  d0<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS00', colnames(discdata)))|grepl('visitmiss_VIS00', colnames(discdata))]))
  d1<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS01', colnames(discdata)))|grepl('visitmiss_VIS01', colnames(discdata))]))
  d2<-as.data.frame(t(discdata[, (grepl('AUX_', colnames(discdata))&grepl('_VIS02', colnames(discdata)))|grepl('visitmiss_VIS02', colnames(discdata))]))
  rm0<-rownames(d0)[duplicated(d0, fromLast=TRUE)]
  rm1<-rownames(d1)[duplicated(d1, fromLast=TRUE)]
  rm2<-rownames(d2)[duplicated(d2, fromLast=TRUE)]
  rm<-c(rm0,rm1,rm2) # orphaned nodes are those whose immediate parent AUX is identical to the visitmiss at that visit
  return(list(data=discdata,rm=rm))
  
}