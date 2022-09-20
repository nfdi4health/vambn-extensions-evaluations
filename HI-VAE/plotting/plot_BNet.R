############# README
# This is to plot the network for the paper
############# 
setwd("/path/to/output/files/")

rm(list=ls())
library(tidyverse)
library(bnlearn) # hc might be overwritten by arules or some such package "bnlearn::hc" if so; not currently used though
library(parallel)
library(stringr)
library(graph)
library(igraph)
library(RCy3)

### load final BN
finalBN <- readRDS("main_finalBN.rds")
graphNEL <- as.graphNEL(finalBN)
final_graph<-igraph.from.graphNEL(graphNEL)
edg.final<-as.data.frame(as_edgelist(final_graph, names = TRUE),stringsAsFactors=F)
colnames(edg.final)<-c('from','to')
edg.final$inBN = 1

### load bootstrapping results
boot.stren <- readRDS("main_bootBN.rds")
bootBN = boot.stren
boot_subgraph = bootBN[bootBN$strength >0.5 & bootBN$direction >0.5 , ]
boot_subgraph$inFilteredBoot = 1
boot_subgraph$strength = NULL
boot_subgraph$direction = NULL

### load knowledge graph
# load("data/knowledgeGraph/kg_bn.Rdata")
# edg.kg = as.data.frame(kg_bn$arcs, stringsAsFactors = F)
# edg.kg$inKG = 1

### get final dataframe with all attributes needed for visualization
name<-'Final Network Publication'

# final_df = merge(x=edg.final,y=edg.kg,by=c('from','to'), all = TRUE)
# final_df = merge(x=final_df,y=boot_subgraph,by=c('from','to'), all = TRUE)
final_df = merge(x=edg.final,y=boot_subgraph,by=c('from','to'), all = TRUE)

final_df = merge(x=final_df,y=bootBN,by=c('from','to'))
final_df[is.na(final_df)] = 0
final_df$strength = as.character(round(final_df$strength, 2 ))
final_df_boot50 = subset(final_df, strength>=0.5)

## rename Clusters with DONALD Terms
final_df_boot50[final_df_boot50=="SA_sex_VIS00"] = "sex"
final_df_boot50[final_df_boot50=="SA_fam_ID_VIS00"] = "fam_ID"

final_df_boot50[final_df_boot50=="zcode_times_VIS00"] = "TIMES 00"
final_df_boot50[final_df_boot50=="zcode_times_VIS01"] = "TIMES 01"
final_df_boot50[final_df_boot50=="zcode_times_VIS02"] = "TIMES 02"
final_df_boot50[final_df_boot50=="zcode_times_VIS03"] = "TIMES 03"
final_df_boot50[final_df_boot50=="zcode_times_VIS04"] = "TIMES 04"
final_df_boot50[final_df_boot50=="zcode_times_VIS05"] = "TIMES 05"
final_df_boot50[final_df_boot50=="zcode_times_VIS06"] = "TIMES 06"
final_df_boot50[final_df_boot50=="zcode_times_VIS07"] = "TIMES 07"
final_df_boot50[final_df_boot50=="zcode_times_VIS08"] = "TIMES 08"
final_df_boot50[final_df_boot50=="zcode_times_VIS09"] = "TIMES 09"
final_df_boot50[final_df_boot50=="zcode_times_VIS10"] = "TIMES 10"
final_df_boot50[final_df_boot50=="zcode_times_VIS11"] = "TIMES 11"
final_df_boot50[final_df_boot50=="zcode_times_VIS12"] = "TIMES 12"
final_df_boot50[final_df_boot50=="zcode_times_VIS13"] = "TIMES 13"
final_df_boot50[final_df_boot50=="zcode_times_VIS14"] = "TIMES 14"
final_df_boot50[final_df_boot50=="zcode_times_VIS15"] = "TIMES 15"

final_df_boot50[final_df_boot50=="zcode_nutrition_VIS00"] = "NUTRI 00"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS01"] = "NUTRI 01"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS02"] = "NUTRI 02"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS03"] = "NUTRI 03"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS04"] = "NUTRI 04"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS05"] = "NUTRI 05"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS06"] = "NUTRI 06"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS07"] = "NUTRI 07"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS08"] = "NUTRI 08"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS09"] = "NUTRI 09"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS10"] = "NUTRI 10"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS11"] = "NUTRI 11"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS12"] = "NUTRI 12"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS13"] = "NUTRI 13"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS14"] = "NUTRI 14"
final_df_boot50[final_df_boot50=="zcode_nutrition_VIS15"] = "NUTRI 15"

final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS00"] = "ANTHRO 00"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS01"] = "ANTHRO 01"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS02"] = "ANTHRO 02"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS03"] = "ANTHRO 03"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS04"] = "ANTHRO 04"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS05"] = "ANTHRO 05"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS06"] = "ANTHRO 06"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS07"] = "ANTHRO 07"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS08"] = "ANTHRO 08"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS09"] = "ANTHRO 09"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS10"] = "ANTHRO 10"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS11"] = "ANTHRO 11"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS12"] = "ANTHRO 12"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS13"] = "ANTHRO 13"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS14"] = "ANTHRO 14"
final_df_boot50[final_df_boot50=="zcode_anthropometric_VIS15"] = "ANTHRO 15"

final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS00"] = "SOCIO 00"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS01"] = "SOCIO 01"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS02"] = "SOCIO 02"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS03"] = "SOCIO 03"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS04"] = "SOCIO 04"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS05"] = "SOCIO 05"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS06"] = "SOCIO 06"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS07"] = "SOCIO 07"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS08"] = "SOCIO 08"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS09"] = "SOCIO 09"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS10"] = "SOCIO 10"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS11"] = "SOCIO 11"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS12"] = "SOCIO 12"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS13"] = "SOCIO 13"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS14"] = "SOCIO 14"
final_df_boot50[final_df_boot50=="zcode_socioeconomic_VIS15"] = "SOCIO 15"


final_graph<-graph_from_data_frame(final_df_boot50, directed = TRUE, vertices = )

# set attribute
E(final_graph)$strength<-as.character(E(final_graph)$strength)
E(final_graph)$direction<-as.character(E(final_graph)$direction)

#boot_graph<-delete_vertices(boot_graph, V(boot_graph)$name[grepl('AUX_|visitmiss_',V(boot_graph)$name)])

netcont<-createNetworkFromIgraph(final_graph,name,collection="Paper Plot")
layoutNetwork('hierarchical')
setVisualStyle('default')


### general setting
setEdgeColorDefault("#E4E4E4")
lockNodeDimensions(FALSE)
setNodeFontSizeDefault(50)
setNodeWidthDefault(300)
setNodeHeightDefault(150)
setNodeShapeDefault('ellipse')
setEdgeLineWidthDefault(5)
setEdgeFontSizeDefault(50)

edgedata = getTableColumns("edge")


### color standalone genes / variables
standalones = c("sex", "fam_ID")
standalone = V(final_graph)$name[V(final_graph)$name%in%standalones]
setNodeColorBypass (standalone, '#dde55c')

# setNodeColorBypass ("zcode_times_VIS00", '#A01080')
# setNodeColorBypass ("zcode_times_VIS01", '#A01080')
# setNodeColorBypass ("zcode_times_VIS02", '#A01080')
# setNodeColorBypass ("zcode_times_VIS03", '#A01080')
# setNodeColorBypass ("zcode_times_VIS04", '#A01080')
# setNodeColorBypass ("zcode_times_VIS05", '#A01080')
# setNodeColorBypass ("zcode_times_VIS06", '#A01080')
# setNodeColorBypass ("zcode_times_VIS07", '#A01080')
# setNodeColorBypass ("zcode_times_VIS08", '#A01080')
# setNodeColorBypass ("zcode_times_VIS09", '#A01080')
# setNodeColorBypass ("zcode_times_VIS10", '#A01080')
# setNodeColorBypass ("zcode_times_VIS11", '#A01080')
# setNodeColorBypass ("zcode_times_VIS12", '#A01080')
# setNodeColorBypass ("zcode_times_VIS13", '#A01080')
# setNodeColorBypass ("zcode_times_VIS14", '#A01080')
# setNodeColorBypass ("zcode_times_VIS15", '#A01080')

setNodeColorBypass ("NUTRI 00", '#50D050')
setNodeColorBypass ("NUTRI 01", '#50D050')
setNodeColorBypass ("NUTRI 02", '#50D050')
setNodeColorBypass ("NUTRI 03", '#50D050')
setNodeColorBypass ("NUTRI 04", '#50D050')
setNodeColorBypass ("NUTRI 05", '#50D050')
setNodeColorBypass ("NUTRI 06", '#50D050')
setNodeColorBypass ("NUTRI 07", '#50D050')
setNodeColorBypass ("NUTRI 08", '#50D050')
setNodeColorBypass ("NUTRI 09", '#50D050')
setNodeColorBypass ("NUTRI 10", '#50D050')
setNodeColorBypass ("NUTRI 11", '#50D050')
setNodeColorBypass ("NUTRI 12", '#50D050')
setNodeColorBypass ("NUTRI 13", '#50D050')
setNodeColorBypass ("NUTRI 14", '#50D050')
setNodeColorBypass ("NUTRI 15", '#50D050')

setNodeColorBypass ("ANTHRO 00", '#F0B050')
setNodeColorBypass ("ANTHRO 01", '#F0B050')
setNodeColorBypass ("ANTHRO 02", '#F0B050')
setNodeColorBypass ("ANTHRO 03", '#F0B050')
setNodeColorBypass ("ANTHRO 04", '#F0B050')
setNodeColorBypass ("ANTHRO 05", '#F0B050')
setNodeColorBypass ("ANTHRO 06", '#F0B050')
setNodeColorBypass ("ANTHRO 07", '#F0B050')
setNodeColorBypass ("ANTHRO 08", '#F0B050')
setNodeColorBypass ("ANTHRO 09", '#F0B050')
setNodeColorBypass ("ANTHRO 10", '#F0B050')
setNodeColorBypass ("ANTHRO 11", '#F0B050')
setNodeColorBypass ("ANTHRO 12", '#F0B050')
setNodeColorBypass ("ANTHRO 13", '#F0B050')
setNodeColorBypass ("ANTHRO 14", '#F0B050')
setNodeColorBypass ("ANTHRO 15", '#F0B050')

setNodeColorBypass ("SOCIO 00", '#C070FF')
setNodeColorBypass ("SOCIO 01", '#C070FF')
setNodeColorBypass ("SOCIO 02", '#C070FF')
setNodeColorBypass ("SOCIO 03", '#C070FF')
setNodeColorBypass ("SOCIO 04", '#C070FF')
setNodeColorBypass ("SOCIO 05", '#C070FF')
setNodeColorBypass ("SOCIO 06", '#C070FF')
setNodeColorBypass ("SOCIO 07", '#C070FF')
setNodeColorBypass ("SOCIO 08", '#C070FF')
setNodeColorBypass ("SOCIO 09", '#C070FF')
setNodeColorBypass ("SOCIO 10", '#C070FF')
setNodeColorBypass ("SOCIO 11", '#C070FF')
setNodeColorBypass ("SOCIO 12", '#C070FF')
setNodeColorBypass ("SOCIO 13", '#C070FF')
setNodeColorBypass ("SOCIO 14", '#C070FF')
setNodeColorBypass ("SOCIO 15", '#C070FF')

hideNodes(c('visitmiss_VIS00','visitmiss_VIS01','visitmiss_VIS02','visitmiss_VIS03',
            'visitmiss_VIS04','visitmiss_VIS05','visitmiss_VIS06','visitmiss_VIS07',
            'visitmiss_VIS08','visitmiss_VIS09','visitmiss_VIS10','visitmiss_VIS11',
            'visitmiss_VIS12','visitmiss_VIS13','visitmiss_VIS14','visitmiss_VIS15'))

hideNodes(c('scode_anthropometric_VIS00','scode_anthropometric_VIS01','scode_anthropometric_VIS02','scode_anthropometric_VIS03',
            'scode_anthropometric_VIS04','scode_anthropometric_VIS05','scode_anthropometric_VIS06','scode_anthropometric_VIS07',
            'scode_anthropometric_VIS08','scode_anthropometric_VIS09','scode_anthropometric_VIS10','scode_anthropometric_VIS11',
            'scode_anthropometric_VIS12','scode_anthropometric_VIS13','scode_anthropometric_VIS14','scode_anthropometric_VIS15'))

hideNodes(c('scode_socioeconomic_VIS00','scode_socioeconomic_VIS01','scode_socioeconomic_VIS02','scode_socioeconomic_VIS03',
            'scode_socioeconomic_VIS04','scode_socioeconomic_VIS05','scode_socioeconomic_VIS06','scode_socioeconomic_VIS07',
            'scode_socioeconomic_VIS08','scode_socioeconomic_VIS09','scode_socioeconomic_VIS10','scode_socioeconomic_VIS11',
            'scode_socioeconomic_VIS12','scode_socioeconomic_VIS13','scode_socioeconomic_VIS14','scode_socioeconomic_VIS15'))

### show strength as edge label
setEdgeLabelMapping('strength')

### dashed lines for only bootstrapped edges
edgesOnlyBOOT = edgedata$name[edgedata$inBN==0 & edgedata$inFilteredBoot==1] #edgedata$inKG==0 &
setEdgeLineStyleBypass(edgesOnlyBOOT, "DOT")

### color edges
## only KG
#edgesOnlyKG = edgedata$name[edgedata$inBN==0 & edgedata$inKG==1] #no more edges only KG

## both BN and KG
# edgesBoth = edgedata$name[edgedata$inBN==1 & edgedata$inKG==1] #all from KG
# setEdgeColorBypass(edgesBoth, "#01A3A4")


### line width larger for interesting edges
# moreInteresting = c(edgedata$name[edgedata$target=="cognition"],
#                     edgedata$name[edgedata$source=="PatDemo_age"],
#                     edgedata$name[edgedata$source=="CD33" | edgedata$target=="CD33"],
#                     edgedata$name[edgedata$source=="GPR3 | ARRB2" & edgedata$target=="Ubiquitin degradation subgraph"])
# moreInteresting = setdiff(moreInteresting, "CD33 (interacts with) PatDemo_age")
# setEdgeLineWidthBypass(moreInteresting, 10)
# setEdgeColorBypass(moreInteresting, "#000000")

#setEdgeColorBypass(edgesOnlyKG, "#FF00E3")





# shortest_paths(final_graph, "CD33", to = "cognition")
##########################################
setNodeColorMapping('degree', c(min(degAll), mean(degAll), max(degAll)), c('#F5EDDD', '#F59777', '#F55333'))
setNodeSizeMapping('betweenness', c(min(betAll.norm), mean(betAll.norm), max(betAll.norm)), c(30, 60, 100))
setEdgeLineWidthMapping('weight', c(min(as.numeric(dataSet.ext$V3)), mean(as.numeric(dataSet.ext$V3)), max(as.numeric(dataSet.ext$V3))), c(1,3,5))
setEdgeColorMapping('weight', c(min(as.numeric(dataSet.ext$V3)), mean(as.numeric(dataSet.ext$V3)), max(as.numeric(dataSet.ext$V3))), c('#BBEE00', '#77AA00', '#558800'))
setBackgroundColorDefault('#D3D3D3')
setNodeBorderColorDefault('#000000')
setNodeBorderWidthDefault(3)
setNodeShapeDefault('ellipse')
setNodeFontSizeDefault(20)
setNodeLabelColorDefault('#000000')

saveSession('tutorial_session')
exportImage(filename='tutorial_image2', type = 'PDF')



