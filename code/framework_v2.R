## ---------------------------------------------------------------------------------------------------------------------------
## Packages
## ---------------------------------------------------------------------------------------------------------------------------
source("Interest_AItopics.R")
.lib<- c("ggplot2", "readxl", "plyr", "dplyr", "lubridate", "stringr", "reshape2",  "gridExtra",  "plotly", "xtable", "rowr", "latex2exp")
.inst <- .lib %in% installed.packages()
if (length(.lib[!.inst])>0) install.packages(.lib[!.inst], repos=c("http://rstudio.org/_packages", "http://cran.rstudio.com")) 
lapply(.lib, require, character.only=TRUE)

openPDFEPS <- function(file, height= PDFheight, width= PDFwidth, PDFEPS = 1) {
  if (PDFEPS == 1) {
    pdf(paste(file, ".pdf", sep=""), width, height)
  } else if (PDFEPS == 2) {
    postscript(paste(file, ".eps", sep=""), width, height, horizontal=FALSE)
  }
}

## ---------------------------------------------------------------------------------------------------------------------------
## Data
## ---------------------------------------------------------------------------------------------------------------------------

cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")

# file = "Task2CogAbs_DelphyData.xlsx"
# delphy.1 <- read.xlsx(file, sheetIndex = 1)
# delphy.1 <- read_excel(file,sheet = 1)

# delphy.2 <- read.xlsx(file, sheetIndex = 2)
# delphy.2 <- read_excel(file,sheet = 2)

# idTasks <- read.xlsx(file, sheetIndex = 3)
# idTasks <- read_excel(file,sheet = 3)

# benchs = readRDS("interest_benchmarks_clean.rds")

# set.seed(123)
# cl <- kmeans(benchs.s, 6, nstart = 25)
# benchs$cluster  <- factor(cl$cluster)
# saveRDS(benchs, file = "benchmarks.Rds")

ClusterNames <- c("Computer Vision", "NLP & Inf. Extraction", "Human-Robot interation", "Prediction, KBs & Reasoning", "Multi-agent & Games", "Q. Answering & Sent. Analysis.")


benchs = readRDS("benchmarks.Rds")
levels(benchs$cluster) <- ClusterNames
benchs = interestPerYears(benchs, interestYears = 2008:2018)
benchs.s <- select(benchs, one_of(cogAbs))
rownames(benchs.s) <- benchs$keyword


# saveRDS(delphy.2, file = "delphy.Rds")
delphy.2 <- readRDS("delphy.Rds")
# saveRDS(idTasks, file = "tasks.Rds")
idTasks <- readRDS("tasks.Rds")



## ---------------------------------------------------------------------------------------------------------------------------
## Testing
## ---------------------------------------------------------------------------------------------------------------------------

framework <- function(benchs, delphy.2, ploting = FALSE){
  
  cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")
  
  # -------- R.norm x b -> a ----------------------------------------------------------------------------------------------------------
  R <- t(select(benchs, one_of(cogAbs)))
  # dim(R) #[1]  14 328
  b <- as.matrix(benchs$mean.Interest)
  rownames(b) <- benchs$name
  # dim(b) #[1] 328   1
  R.norm <- t(t(as.matrix(R))/colSums(R))
  # colSums(R.norm)
  # dim(R.norm) #[1]  14 328
  a <- R.norm %*% b
  # dim(a) #[1] 14  1
  
  # --------- W.norm x a -> t  --------------------------------------------------------------------------------------------------------------
  delphy.2.clean <- delphy.2[rowSums(select(delphy.2,-Id)) != 0,]
  id.task <- delphy.2.clean$Id
  W <- as.matrix(select(delphy.2.clean,-Id))/6  
  # dim(W) # 62 14 [1] 59 14 clean
  W.norm <- as.matrix(W)/rowSums(W)
  # rowSums(W.norm)
  t <- W.norm %*% a #row-wise
  
  rownames(t) <- filter(idTasks, Id %in% id.task)$Task
  
  if(ploting){
    # --------- Relevance abilities  ----------------------------------------------------------------------------------------------
    relevance <- data.frame(id = cogAbs, value = rowSums(R.norm))
    R.plot <- ggplot(relevance, aes(id, value)) + 
      geom_bar(stat = "identity", alpha = 0.7) + 
      geom_text(aes(y = value + 3, label = round(value, 3))) + 
      scale_x_discrete(limits = cogAbs, labels = cogAbs) +
      labs(y = TeX("$\\sum_{b}\\mathbf{R}_{ab}$"), x ="") +
      theme_minimal()
    
    
    
    periods <- list(2008:2010, 2011:2013, 2014:2016, 2017:2018)
    # periods <- list(2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018)
    data = readRDS("interest_benchmarks_clean.rds")
    data[,cogAbs] <- t(R.norm)
    all <- plotProgressPeriods(data, periods)
    all.s <- summarise(group_by(all, period, variable), mean = mean(value))
    all.s$period <- factor(all.s$period)
    levels(all.s$period) <- c("2008-2010","2011-2013","2014-2016","2017-2018")
    # levels(all.s$period)
    all.ag <- summarise(group_by(all, variable), mean = mean(value))
    # write.csv(all.s, file = "a_intensity.csv")
    a.plot <- ggplot(all.s, aes(variable,mean )) +
      geom_bar(data = all.ag, aes(variable, mean), stat = "identity", alpha = 0.5, linetype = "dashed", colour = "gray", fill = "white") +
      geom_bar(aes(fill = period), stat = "identity",position = "dodge", alpha  = 0.8) +
      xlab("") + ylab("Mean Interest") + 
      scale_fill_brewer(palette = "Paired") + 
      theme_minimal() +  theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods)))
    
  

    taskAIimpact <- data.frame(Id = id.task, AIimpact = t)
    taskAIimpact$Id <- as.factor(taskAIimpact$Id)
    taskAIimpact <- merge(taskAIimpact, idTasks, by = "Id")
    names(taskAIimpact)[3] <- "Task"
    taskAIimpact$names <- paste0(taskAIimpact$Task, " (",taskAIimpact$Id,")")
    periods = 2008:2018
    
    t.plot <- ggplot(taskAIimpact, aes(reorder(names, AIimpact), AIimpact)) + 
      geom_bar(stat = "identity", alpha = 0.7, width = .15) + 
      geom_point(colour = "steelblue") + 
      coord_flip() + 
      labs(y = "t", x ="") +
      theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods))) +theme_minimal()
    
    return(list(R.plot,a.plot,t.plot))
  }

  return(list(a,t,b))
  
}

# out <- framework(benchs, delphy.2, ploting = T)
# 
# openPDFEPS("R_bars", heigh =4 , width = 8)
# out[[1]]
# dev.off()
# 
# openPDFEPS("a_bars", heigh = 6, width = 10)
# out[[2]]
# dev.off()
# 
# openPDFEPS("t_bars", heigh = 7.5, width = 8)
# out[[3]]
# dev.off()


# -------------------------------------------------------------------------------------------------------
# Simulaciones en las que se hace énfasis en otro vector de capacidades

sim.a <- function(a, delphy.2, col = "steelblue"){
  
  cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")
  # --------- W.norm x a -> t  --------------------------------------------------------------------------------------------------------------
  delphy.2.clean <- delphy.2[rowSums(select(delphy.2,-Id)) != 0,]
  id.task <- delphy.2.clean$Id
  W <- as.matrix(select(delphy.2.clean,-Id))/6  
  # dim(W) # 62 14 [1] 59 14 clean
  W.norm <- as.matrix(W)/rowSums(W)
  # rowSums(W.norm)
  t <- W.norm %*% a #row-wise
  
  
  taskAIimpact <- data.frame(Id = id.task, AIimpact = t)
  colnames(taskAIimpact) <- c("Id", "AIimpact")
  taskAIimpact$Id <- as.factor(taskAIimpact$Id)
  taskAIimpact <- merge(taskAIimpact, idTasks, by = "Id")
  names(taskAIimpact)[3] <- "Task"
  taskAIimpact$names <- paste0(taskAIimpact$Task, " (",taskAIimpact$Id,")")
  periods = 2008:2018
  
  t <- ggplot(taskAIimpact, aes(reorder(names, AIimpact), AIimpact)) + 
    geom_bar(stat = "identity", alpha = 0.7, width = .15) + 
    geom_point(colour = col) + 
    coord_flip() + 
    labs(y = "t", x ="") +
    theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods))) +theme_minimal()
  
  return(t)
  
}

simulate.abilities <- function(a,  col = "steelblue"){
  a.norm <- a/sum(a)
  rownames(a.norm) <- cogAbs
  return(sim.a(a.norm, delphy.2, col))
}

# all.social = matrix(c(0.0, # MP
#              0.0, # SI
#              0.0, # VP
#              0.0, # AP
#              0.0, # AS
#              0.0, # PA
#              0.0, # CE
#              1.0, # CO
#              1.0, # EC
#              0.0, # NV
#              0.0, # CL
#              0.0, # QL
#              1.0, # MS
#              0.0))  # MC
# 
# openPDFEPS("t_bars_social", heigh = 7.5, width = 8)
# simulate.abilities(all.social)
# dev.off()



# -------------------------------------------------------------------------------------------------------
# From t to b 


sim.t.a <- function(t, delphy.2){ # return a^T
  
  cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")

  delphy.2.clean <- delphy.2[rowSums(select(delphy.2,-Id)) != 0,]
  id.task <- delphy.2.clean$Id
  W <- as.matrix(select(delphy.2.clean,-Id))/6  
  # dim(W) # 62 14 [1] 59 14 clean
  W.norm <- as.matrix(W)/rowSums(W)
  # rowSums(W.norm)
  a <- t(t) %*% W.norm
  
  
  relevance <- data.frame(id = cogAbs, value = t(a))
  a.plot <- ggplot(relevance, aes(id, value)) + 
    geom_bar(stat = "identity", alpha = 0.7) + 
    geom_text(aes(y = value + 0.03, label = round(value, 3))) + 
    scale_x_discrete(limits = cogAbs, labels = cogAbs) +
    labs(y = "", x ="") +
    theme_minimal()
  
  return(list(a, a.plot))
  
}

sim.a.b <- function(a, benchs, limit = 60, col = "steelblue"){
  
  cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")
  
  # -------- R.norm x b -> a ----------------------------------------------------------------------------------------------------------
  R <- t(select(benchs, one_of(cogAbs)))
  R.norm <- t(t(as.matrix(R))/colSums(R))
  b <- a %*% R.norm

  relevance <- data.frame(id = benchs$name, value = t(b), cluster = benchs$cluster)
  relevance$id <- as.character(relevance$id)
  
  relevance <- relevance[with(relevance, order(-value)),]
  relevance <- relevance[1:limit, ]
  
  relevance <- relevance[complete.cases(relevance),]
  relevance <- filter(relevance, value > 0)
  b.plot <- ggplot(relevance, aes(reorder(id, value), value)) + 
    geom_bar(stat = "identity", alpha = 0.7, width = .15) + 
    geom_point(aes(colour = cluster)) + 
    coord_flip() + 
    labs(y = "b", x ="") + theme_minimal() + 
    theme(legend.position = "bottom", legend.title = element_blank()) 
  
  return(list(b, b.plot))
}

generate.t <- function(id){
  temp <- rep(0,59)
  temp[id] <- 1
  return(t(temp))
}



# t <- generate.t(49) #advising people)
# t <- generate.t(9) #arm-hand steadines
# t <- generate.t(29) #number facility
# t <- generate.t(58) #instructing
# 
# 
# 
# aT <- sim.t.a(t(t), delphy.2)[[1]]
# sim.t.a(t(t), delphy.2)[[2]]
# sim.a.b(aT, benchs)
# 
# 







# -------------------------------------------------------------------------------------------------------
# From b to t 

framework.bt <- function(benchs, delphy.2, b, col = "steelblue"){
  
  cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")
  b.norm <- b/sum(b)
  rownames(b.norm) <- benchs$name

  # -------- R.norm x b -> a ----------------------------------------------------------------------------------------------------------
  R <- t(select(benchs, one_of(cogAbs)))
    # b <- as.matrix(benchs$mean.Interest)
  # rownames(b) <- benchs$name
  R.norm <- t(t(as.matrix(R))/colSums(R))
  a <- R.norm %*% b

  # --------- W.norm x a -> t  --------------------------------------------------------------------------------------------------------------
  delphy.2.clean <- delphy.2[rowSums(select(delphy.2,-Id)) != 0,]
  id.task <- delphy.2.clean$Id
  W <- as.matrix(select(delphy.2.clean,-Id))/6  
  W.norm <- as.matrix(W)/rowSums(W)
  t <- W.norm %*% a #row-wise
  
  rownames(t) <- filter(idTasks, Id %in% id.task)$Task

  
  # --------- Relevance abilities  ----------------------------------------------------------------------------------------------
  relevance <- data.frame(id = cogAbs, value = a)
  a.plot <- ggplot(relevance, aes(id, value)) + 
    geom_bar(stat = "identity", alpha = 0.7) + 
    geom_text(aes(y = value + 0.03, label = round(value, 3))) + 
    scale_x_discrete(limits = cogAbs, labels = cogAbs) +
    labs(y = "", x ="") +
    theme_minimal()


  
  taskAIimpact <- data.frame(Id = id.task, AIimpact = t)
  taskAIimpact$Id <- as.factor(taskAIimpact$Id)
  taskAIimpact <- merge(taskAIimpact, idTasks, by = "Id")
  names(taskAIimpact)[3] <- "Task"
  taskAIimpact$names <- paste0(taskAIimpact$Task, " (",taskAIimpact$Id,")")
  periods = 2008:2018
  
  t.plot <- ggplot(taskAIimpact, aes(reorder(names, AIimpact), AIimpact)) + 
    geom_bar(stat = "identity", alpha = 0.7, width = .15) + 
    geom_point(colour = col) + 
    coord_flip() + 
    labs(y = "t", x ="") +
    theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods))) +theme_minimal()
  
  return(list(a,a.plot,t,t.plot))
  
}



generate.b <- function(id){
  temp <- rep(0,328)
  temp[id] <- 1
  return(as.matrix(c(temp)))
}







generate.b(2)
framework.bt(benchs, delphy.2, b = generate.b(2))




















# # Usamos el mapping para determinar qué habilidades deberían tener valores más altos para  
# # mejorar en una tarea (labour) y luego ver qué benchmarks les corresponden. 
# 
# 
# getTaskName <- function(id){
#   require(dplyr)
#   return(filter(idTasks, Id == id)$Task)
# }
# 
# get_ab_from_tasks <- function(id, delphy.2){
#   require(dplyr)
#   delphy.2.clean <- delphy.2[rowSums(delphy.2) != 0,]
#   data <- filter(delphy.2.clean, Id == id)[-1]
#   ids <- filter(delphy.2.clean, Id == id)[1]
#   data <- data/6  
#   data <- data/rowSums(data)
#   rownames(data) <- ids
#   task = getTaskName(id)
#   barplot(as.matrix(data), main = task)
#   return(as.matrix(data))
# }
# 
# get_benchs_from_ab <- function(abs, benchs.s, major = T, limit.bench = F){
#   require(dplyr)
#   
#   numAbs = sum(abs!=0)
#   if(major){
#     abs.major <- colnames(abs)[which(abs >= 1/numAbs)]
#     total = length(abs.major)
#   }else{
#     abs.major <- colnames(abs)[which(abs > 0)]
#     total = numAbs
#   }
#   
#   if(limit.bench){
#     selection <- select(benchs.s, one_of(abs.major))
#     
#   }else{
#     selection <- select(benchs.s, one_of(abs.major))
#     
#   }
#   
#   sums <- rowSums(selection)
#   print(paste0("Principal abilities: ", paste(abs.major, collapse = " ")))
#   
#   for(i in 0:(total-1)){
#     
#     sel.i <- rownames(selection[which(sums == total - i),])
#     howMany = length(sel.i)
#     print(paste0("There are ", howMany," benchmarks covering ", length(abs.major)-i, " of the abilities"))
#     print("Benchmarks: ")
#     print(sel.i)
#   }
# 
# 
# }
# 
# 
# abs = get_ab_from_tasks(46, delphy.2)
# get_benchs_from_ab(abs, benchs.s, major = T)
# simulate.abilities(t(as.matrix(abs)))
# 





