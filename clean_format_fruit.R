 #install.packages('readxl')

rm(list=ls())
#library(openxlsx)
#library(readxl)
#library(ADNIMERGE) # for risk scores, medhist, reccmeds
#load("./data/adnimerge.rdata")
#data(adnimerge)

visitData_complete<-read.csv('data/fruit-data.csv')
pt<-factor(visitData_complete$SUBJID)

colnames(visitData_complete)<-gsub('_BASELINE','_VIS00',colnames(visitData_complete))
colnames(visitData_complete)<-gsub('_FUP1','_VIS01',colnames(visitData_complete))
colnames(visitData_complete)<-gsub('_FUP2','_VIS02',colnames(visitData_complete))

######## Variable groups
vg_form <- visitData_complete[,grep("Weight|Redness", colnames(visitData_complete), value = TRUE)]
colnames(vg_form)<-paste0('FORM_',colnames(vg_form))
vg_form$SUBJID<-pt
vg_form_vis00<-vg_form[,grepl('SUBJID|_VIS00$',colnames(vg_form))]
vg_form_vis01<-vg_form[,grepl('SUBJID|_VIS01$',colnames(vg_form))]
vg_form_vis02<-vg_form[,grepl('SUBJID|_VIS02$',colnames(vg_form))]

vg_taste <- visitData_complete[,grep("Sweetness|Sourness", colnames(visitData_complete), value = TRUE)]
colnames(vg_taste)<-paste0('TASTE_',colnames(vg_taste))
vg_taste$SUBJID<-pt
vg_taste_vis00<-vg_taste[,grepl('SUBJID|_VIS00$',colnames(vg_taste))]
vg_taste_vis01<-vg_taste[,grepl('SUBJID|_VIS01$',colnames(vg_taste))]
vg_taste_vis02<-vg_taste[,grepl('SUBJID|_VIS02$',colnames(vg_taste))]


## Standalone
#fdg <- visitData_complete[,grep("PTID|FDG", colnames(visitData_complete), value = TRUE)]
#dx <- visitData_complete[,grep("PTID|DX", colnames(visitData_complete), value = TRUE)]
vg_stalone<-visitData_complete[,grepl("SUBJID|Type", colnames(visitData_complete))]
vg_stalone$SUBJID <- NULL #was only added to make sure that vg_stalone is a table, not a vector
colnames(vg_stalone)<-paste0('SA_',colnames(vg_stalone))
vg_stalone$SUBJID<-pt
vg_stalone_vis00<-vg_stalone[,grepl('SUBJID|_VIS00$',colnames(vg_stalone))]

data_all<-list('form_VIS00'=vg_form_vis00,
               'form_VIS01'=vg_form_vis01,
               'form_VIS02'=vg_form_vis02,
               'taste_VIS00'=vg_taste_vis00,
               'taste_VIS01'=vg_taste_vis01,
               'taste_VIS02'=vg_taste_vis02,
               'stalone_VIS00'=vg_stalone_vis00)
saveRDS(data_all,"data/fruit-data_condensed.rds")

