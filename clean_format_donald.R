
rm(list=ls())

print(getwd())
visitData_complete<-read.csv('data/donald-data.csv')
#print(colnames(visitData_complete))
pt<-factor(visitData_complete$SUBJID)

colnames(visitData_complete)<-gsub('fam_ID','fam_ID_VIS00',colnames(visitData_complete))
colnames(visitData_complete)<-gsub('sex','sex_VIS00',colnames(visitData_complete))

######## Variable groups
vg_times <- visitData_complete[,grep("alter|time", colnames(visitData_complete), value = TRUE)]
colnames(vg_times)<-paste0('TIMES_',colnames(vg_times))
vg_times$SUBJID<-pt
vg_times_vis00<-vg_times[,grepl('SUBJID|_VIS00$',colnames(vg_times))]
vg_times_vis01<-vg_times[,grepl('SUBJID|_VIS01$',colnames(vg_times))]
vg_times_vis02<-vg_times[,grepl('SUBJID|_VIS02$',colnames(vg_times))]
vg_times_vis03<-vg_times[,grepl('SUBJID|_VIS03$',colnames(vg_times))]
vg_times_vis04<-vg_times[,grepl('SUBJID|_VIS04$',colnames(vg_times))]
vg_times_vis05<-vg_times[,grepl('SUBJID|_VIS05$',colnames(vg_times))]
vg_times_vis06<-vg_times[,grepl('SUBJID|_VIS06$',colnames(vg_times))]
vg_times_vis07<-vg_times[,grepl('SUBJID|_VIS07$',colnames(vg_times))]
vg_times_vis08<-vg_times[,grepl('SUBJID|_VIS08$',colnames(vg_times))]
vg_times_vis09<-vg_times[,grepl('SUBJID|_VIS09$',colnames(vg_times))]
vg_times_vis10<-vg_times[,grepl('SUBJID|_VIS10$',colnames(vg_times))]
vg_times_vis11<-vg_times[,grepl('SUBJID|_VIS11$',colnames(vg_times))]
vg_times_vis12<-vg_times[,grepl('SUBJID|_VIS12$',colnames(vg_times))]
vg_times_vis13<-vg_times[,grepl('SUBJID|_VIS13$',colnames(vg_times))]
vg_times_vis14<-vg_times[,grepl('SUBJID|_VIS14$',colnames(vg_times))]
vg_times_vis15<-vg_times[,grepl('SUBJID|_VIS15$',colnames(vg_times))]

vg_nutrition <- visitData_complete[,grep("e_cal|EW_p|Fett_p|KH_p|Gluc_p|Fruc_p|Galac_p|MSacch_p|Sacch_p|MALT_p|LACT_p|DISACCH_p|ZUCK_p|zuzu_p|free_s_p|FS_saft_p|FS_obge_p|FS_sp_p|FS_bc_p|FS_cer_p|FS_oth_p|FS_dai_p|FS_SSB_p|wo_tage", colnames(visitData_complete), value = TRUE)]
colnames(vg_nutrition)<-paste0('NUTRI_',colnames(vg_nutrition))
vg_nutrition$SUBJID<-pt
vg_nutrition_vis00<-vg_nutrition[,grepl('SUBJID|_VIS00$',colnames(vg_nutrition))]
vg_nutrition_vis01<-vg_nutrition[,grepl('SUBJID|_VIS01$',colnames(vg_nutrition))]
vg_nutrition_vis02<-vg_nutrition[,grepl('SUBJID|_VIS02$',colnames(vg_nutrition))]
vg_nutrition_vis03<-vg_nutrition[,grepl('SUBJID|_VIS03$',colnames(vg_nutrition))]
vg_nutrition_vis04<-vg_nutrition[,grepl('SUBJID|_VIS04$',colnames(vg_nutrition))]
vg_nutrition_vis05<-vg_nutrition[,grepl('SUBJID|_VIS05$',colnames(vg_nutrition))]
vg_nutrition_vis06<-vg_nutrition[,grepl('SUBJID|_VIS06$',colnames(vg_nutrition))]
vg_nutrition_vis07<-vg_nutrition[,grepl('SUBJID|_VIS07$',colnames(vg_nutrition))]
vg_nutrition_vis08<-vg_nutrition[,grepl('SUBJID|_VIS08$',colnames(vg_nutrition))]
vg_nutrition_vis09<-vg_nutrition[,grepl('SUBJID|_VIS09$',colnames(vg_nutrition))]
vg_nutrition_vis10<-vg_nutrition[,grepl('SUBJID|_VIS10$',colnames(vg_nutrition))]
vg_nutrition_vis11<-vg_nutrition[,grepl('SUBJID|_VIS11$',colnames(vg_nutrition))]
vg_nutrition_vis12<-vg_nutrition[,grepl('SUBJID|_VIS12$',colnames(vg_nutrition))]
vg_nutrition_vis13<-vg_nutrition[,grepl('SUBJID|_VIS13$',colnames(vg_nutrition))]
vg_nutrition_vis14<-vg_nutrition[,grepl('SUBJID|_VIS14$',colnames(vg_nutrition))]
vg_nutrition_vis15<-vg_nutrition[,grepl('SUBJID|_VIS15$',colnames(vg_nutrition))]

vg_anthropometric <- visitData_complete[,grep("bmr|bmi|^ovw|underrep", colnames(visitData_complete), value = TRUE)]
colnames(vg_anthropometric)<-paste0('ANTHRO_',colnames(vg_anthropometric))
vg_anthropometric$SUBJID<-pt
vg_anthropometric_vis00<-vg_anthropometric[,grepl('SUBJID|_VIS00$',colnames(vg_anthropometric))]
vg_anthropometric_vis01<-vg_anthropometric[,grepl('SUBJID|_VIS01$',colnames(vg_anthropometric))]
vg_anthropometric_vis02<-vg_anthropometric[,grepl('SUBJID|_VIS02$',colnames(vg_anthropometric))]
vg_anthropometric_vis03<-vg_anthropometric[,grepl('SUBJID|_VIS03$',colnames(vg_anthropometric))]
vg_anthropometric_vis04<-vg_anthropometric[,grepl('SUBJID|_VIS04$',colnames(vg_anthropometric))]
vg_anthropometric_vis05<-vg_anthropometric[,grepl('SUBJID|_VIS05$',colnames(vg_anthropometric))]
vg_anthropometric_vis06<-vg_anthropometric[,grepl('SUBJID|_VIS06$',colnames(vg_anthropometric))]
vg_anthropometric_vis07<-vg_anthropometric[,grepl('SUBJID|_VIS07$',colnames(vg_anthropometric))]
vg_anthropometric_vis08<-vg_anthropometric[,grepl('SUBJID|_VIS08$',colnames(vg_anthropometric))]
vg_anthropometric_vis09<-vg_anthropometric[,grepl('SUBJID|_VIS09$',colnames(vg_anthropometric))]
vg_anthropometric_vis10<-vg_anthropometric[,grepl('SUBJID|_VIS10$',colnames(vg_anthropometric))]
vg_anthropometric_vis11<-vg_anthropometric[,grepl('SUBJID|_VIS11$',colnames(vg_anthropometric))]
vg_anthropometric_vis12<-vg_anthropometric[,grepl('SUBJID|_VIS12$',colnames(vg_anthropometric))]
vg_anthropometric_vis13<-vg_anthropometric[,grepl('SUBJID|_VIS13$',colnames(vg_anthropometric))]
vg_anthropometric_vis14<-vg_anthropometric[,grepl('SUBJID|_VIS14$',colnames(vg_anthropometric))]
vg_anthropometric_vis15<-vg_anthropometric[,grepl('SUBJID|_VIS15$',colnames(vg_anthropometric))]

vg_socioeconomic <- visitData_complete[,grep("m_ovw|m_employ|m_schulab", colnames(visitData_complete), value = TRUE)]
colnames(vg_socioeconomic)<-paste0('SOCIO_',colnames(vg_socioeconomic))
vg_socioeconomic$SUBJID<-pt
vg_socioeconomic_vis00<-vg_socioeconomic[,grepl('SUBJID|_VIS00$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis01<-vg_socioeconomic[,grepl('SUBJID|_VIS01$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis02<-vg_socioeconomic[,grepl('SUBJID|_VIS02$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis03<-vg_socioeconomic[,grepl('SUBJID|_VIS03$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis04<-vg_socioeconomic[,grepl('SUBJID|_VIS04$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis05<-vg_socioeconomic[,grepl('SUBJID|_VIS05$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis06<-vg_socioeconomic[,grepl('SUBJID|_VIS06$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis07<-vg_socioeconomic[,grepl('SUBJID|_VIS07$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis08<-vg_socioeconomic[,grepl('SUBJID|_VIS08$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis09<-vg_socioeconomic[,grepl('SUBJID|_VIS09$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis10<-vg_socioeconomic[,grepl('SUBJID|_VIS10$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis11<-vg_socioeconomic[,grepl('SUBJID|_VIS11$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis12<-vg_socioeconomic[,grepl('SUBJID|_VIS12$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis13<-vg_socioeconomic[,grepl('SUBJID|_VIS13$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis14<-vg_socioeconomic[,grepl('SUBJID|_VIS14$',colnames(vg_socioeconomic))]
vg_socioeconomic_vis15<-vg_socioeconomic[,grepl('SUBJID|_VIS15$',colnames(vg_socioeconomic))]


## Standalone
vg_stalone<-visitData_complete[,grepl("SUBJID|fam_ID|sex", colnames(visitData_complete))]
vg_stalone$SUBJID <- NULL #was only added to make sure that vg_stalone is a table, not a vector
colnames(vg_stalone)<-paste0('SA_',colnames(vg_stalone))
vg_stalone$SUBJID<-pt
vg_stalone_vis00<-vg_stalone[,grepl('SUBJID|_VIS00$',colnames(vg_stalone))]

data_all<-list('times_VIS00'=vg_times_vis00,
               'times_VIS01'=vg_times_vis01,
               'times_VIS02'=vg_times_vis02,
               'times_VIS03'=vg_times_vis03,
               'times_VIS04'=vg_times_vis04,
               'times_VIS05'=vg_times_vis05,
               'times_VIS06'=vg_times_vis06,
               'times_VIS07'=vg_times_vis07,
               'times_VIS08'=vg_times_vis08,
               'times_VIS09'=vg_times_vis09,
               'times_VIS10'=vg_times_vis10,
               'times_VIS11'=vg_times_vis11,
               'times_VIS12'=vg_times_vis12,
               'times_VIS13'=vg_times_vis13,
               'times_VIS14'=vg_times_vis14,
               'times_VIS15'=vg_times_vis15,
               'nutrition_VIS00'=vg_nutrition_vis00,
               'nutrition_VIS01'=vg_nutrition_vis01,
               'nutrition_VIS02'=vg_nutrition_vis02,
               'nutrition_VIS03'=vg_nutrition_vis03,
               'nutrition_VIS04'=vg_nutrition_vis04,
               'nutrition_VIS05'=vg_nutrition_vis05,
               'nutrition_VIS06'=vg_nutrition_vis06,
               'nutrition_VIS07'=vg_nutrition_vis07,
               'nutrition_VIS08'=vg_nutrition_vis08,
               'nutrition_VIS09'=vg_nutrition_vis09,
               'nutrition_VIS10'=vg_nutrition_vis10,
               'nutrition_VIS11'=vg_nutrition_vis11,
               'nutrition_VIS12'=vg_nutrition_vis12,
               'nutrition_VIS13'=vg_nutrition_vis13,
               'nutrition_VIS14'=vg_nutrition_vis14,
               'nutrition_VIS15'=vg_nutrition_vis15,
               'anthropometric_VIS00'=vg_anthropometric_vis00,
               'anthropometric_VIS01'=vg_anthropometric_vis01,
               'anthropometric_VIS02'=vg_anthropometric_vis02,
               'anthropometric_VIS03'=vg_anthropometric_vis03,
               'anthropometric_VIS04'=vg_anthropometric_vis04,
               'anthropometric_VIS05'=vg_anthropometric_vis05,
               'anthropometric_VIS06'=vg_anthropometric_vis06,
               'anthropometric_VIS07'=vg_anthropometric_vis07,
               'anthropometric_VIS08'=vg_anthropometric_vis08,
               'anthropometric_VIS09'=vg_anthropometric_vis09,
               'anthropometric_VIS10'=vg_anthropometric_vis10,
               'anthropometric_VIS11'=vg_anthropometric_vis11,
               'anthropometric_VIS12'=vg_anthropometric_vis12,
               'anthropometric_VIS13'=vg_anthropometric_vis13,
               'anthropometric_VIS14'=vg_anthropometric_vis14,
               'anthropometric_VIS15'=vg_anthropometric_vis15,
               'socioeconomic_VIS00'=vg_socioeconomic_vis00,
               'socioeconomic_VIS01'=vg_socioeconomic_vis01,
               'socioeconomic_VIS02'=vg_socioeconomic_vis02,
               'socioeconomic_VIS03'=vg_socioeconomic_vis03,
               'socioeconomic_VIS04'=vg_socioeconomic_vis04,
               'socioeconomic_VIS05'=vg_socioeconomic_vis05,
               'socioeconomic_VIS06'=vg_socioeconomic_vis06,
               'socioeconomic_VIS07'=vg_socioeconomic_vis07,
               'socioeconomic_VIS08'=vg_socioeconomic_vis08,
               'socioeconomic_VIS09'=vg_socioeconomic_vis09,
               'socioeconomic_VIS10'=vg_socioeconomic_vis10,
               'socioeconomic_VIS11'=vg_socioeconomic_vis11,
               'socioeconomic_VIS12'=vg_socioeconomic_vis12,
               'socioeconomic_VIS13'=vg_socioeconomic_vis13,
               'socioeconomic_VIS14'=vg_socioeconomic_vis14,
               'socioeconomic_VIS15'=vg_socioeconomic_vis15,
               'stalone_VIS00'=vg_stalone_vis00)
saveRDS(data_all, "data/donald-data_condensed.rds")
write.csv(data_all, "data/donald-data_condensed.csv")

