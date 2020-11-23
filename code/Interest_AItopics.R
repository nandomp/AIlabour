## ---------------------------------------------------------------------------------------------------------------------------
## Packages
## ---------------------------------------------------------------------------------------------------------------------------

.lib<- c("xlsx", "readxl", "rvest", "plyr", "dplyr", "lubridate", "stringr", "reshape2", "igraph", "visNetwork", "gridExtra", "BBmisc", "plotly")
.inst <- .lib %in% installed.packages()
if (length(.lib[!.inst])>0) install.packages(.lib[!.inst], repos=c("http://rstudio.org/_packages", "http://cran.rstudio.com")) 
lapply(.lib, require, character.only=TRUE)

## ---------------------------------------------------------------------------------------------------------------------------
## Global options and variables
## ---------------------------------------------------------------------------------------------------------------------------

options(scipen = 999999999)
options("scipen"=1000000)
options( java.parameters = "-Xmx6g" )

years = 2008:2019
numbers = FALSE # Get the number of documents per year from AItopics
process = FALSE # Generation of "AIBenchmarks_CogAbs_process.xlsx" from original mapping ("AIBenchmarks_CogAbs.xlsx") DO NOT RUN (manual work done)
analysisInterest = FALSE 

## ---------------------------------------------------------------------------------------------------------------------------
## Functions
## ---------------------------------------------------------------------------------------------------------------------------

## Get number of docs from AI topics 
## ---------------------------------------------------------------------------------------------------------------------------

if (numbers){
  numDocs <- read.xlsx2("docsAItopics.xlsx", sheetIndex = 1)
  splitTemp <- str_split(numDocs$value, " TO ")

  for(i in 1:length(splitTemp)){
    numDocs$dateFrom[i] <- str_remove(str_split(splitTemp[[i]][1], "T")[[1]][1], "\\[")
    numDocs$dateTo[i] <- str_remove(str_split(splitTemp[[i]][2], "T")[[1]][1], "\\}")

  }
  numDocs$year <- year(ymd(numDocs$dateFrom))
  yearDocs <- data.frame(year = numDocs$year, count = numDocs$count)
  saveRDS(yearDocs, file = "yearDocsAItopics.rds")
}


## Get "interest" of an specific keyword in AItopics
## ---------------------------------------------------------------------------------------------------------------------------

getInterest <- function(keyword, exact = TRUE, years =2008:2019, extra = ""){

  print("Getting INTEREST from AItopics...")
  
  yearDocs = readRDS("yearDocsAItopics.rds") #constant (18/06/2019)
  
  if(exact){
    
    print("- Exact match")
    key = paste0("\"",keyword,"\" ",extra)
    url <- paste0("https://aitopics.org/explore/classifications?sort=score%20desc&q=", str_replace_all(key, "[ ]" , "%20"), "&filters=modified:%5B2000-01-01T00%3A00%3A00.000Z%20TO%20NOW%5D&from-modified=true")  
    url_res <- paste0("https://aitopics.org/search?filters=&sort=score+desc&q=\"", str_replace_all(key, "[ ]" , "+"), "\"")
      
  }else{
    
    print("- Regular match")
    key = paste0(keyword," ",extra)
    url <- paste0("https://aitopics.org/explore/classifications?sort=score%20desc&q=", str_replace_all(key, "[ ]" , "%20"),"&filters=modified:%5B2000-01-01T00%3A00%3A00.000Z%20TO%20NOW%5D&from-modified=true")
    url_res <- paste0("https://aitopics.org/search?filters=&sort=score+desc&q=", str_replace_all(keyword, "[ ]" , "+"))
  }
  
  #Total results (if 0 -> no docs returned by AItipics)
  webpage <- read_html(url_res)
  title_html <- html_nodes(webpage, "[class='text-muted']")
  title <- html_text(title_html)
  numbers <- regmatches(title, gregexpr("[[:digit:]]+", title))
  if(length(numbers[[1]]) > 1){
    value <- paste0(numbers[[1]][2:length(numbers[[1]])],collapse="")  
  }else{
    value <- numbers[[1]][1]
  }
  
  print(paste0("- There are ", value, " results in AItopics for the term: ", key))
  
  if(as.numeric(value)>0){
    
    print("- Let's get the links to download the data (results per year)...")
          
    #Links
    webpage <- read_html(url)
    links_html <- html_nodes(webpage, "[class='pull-right']")
    # View(links_html)
    links_html_2 <- html_nodes(links_html, "[class='btn btn-link']")
    link_excel <- html_attr(links_html_2[1], "href")
    
    
    target <- paste0("https://aitopics.org", link_excel)
    path <- paste0(getwd(),"/","_temp.xlsx")
    download.file(target, destfile = path, mode="wb")
    if (file.exists("_temp.xlsx")){
      con = file("_temp.xlsx")
      
      data <- tryCatch({
        read.xlsx2("_temp.xlsx", sheetIndex = 1)},
        error=function(cond) {
          message(paste("--> No results for", keyword))
          # message("Here's the original error message:")
          # message(cond)
          # Choose a return value in case of error
          return(NA)
        })
      
      close(con)
    }
    
    if(!is.na(data)){
      print("- Data downloaded correctly...")
      
      splitTemp <- str_split(data$value, " TO ")
      
      for(i in 1:length(splitTemp)){
        data$dateFrom[i] <- str_remove(str_split(splitTemp[[i]][1], "T")[[1]][1], "\\[")
        data$dateTo[i] <- str_remove(str_split(splitTemp[[i]][2], "T")[[1]][1], "\\}")
        
      }
      
      data$year <- year(ymd(data$dateFrom))
      # head(data)
      data$count <- as.numeric(as.character(data$count))
      data.g <- group_by(data, year)
      data.s <- summarise(data.g, hits = sum(count))
      data.s <- merge(data.s, yearDocs, by.x = "year", by.y = "year", all.x = TRUE, all.y = TRUE)
      
      data.s[is.na(data.s$hits),"hits"] <- 0
      data.s
      data.s$count <- as.numeric(as.character(data.s$count))
      data.s$hits.norm <- (data.s$hits/data.s$count)*100
      
      data.s$keyword = keyword
      data.sf <- filter(data.s, year %in% years)
      
      print("- Data aggregated by year:")
      print(data.sf)
      print("- Everything went well! Bye dude!")
      
      return(select(data.sf, keyword, year, hits, hits.norm))
      
      
    }else{
      print("- Dataframe is NA... checkt it!")
      print(data)
      return(data.frame())
    }
  }else{
    print("-> No interest at all dude, sorry.")
    return(data.frame())
  }

}

plotInterest <- function(data, years = 2008:2019, norm = FALSE){
  require(ggplot2)
  if (norm){
    g <- ggplot(data, aes(year, hits.norm))
  }else{
    g <- ggplot(data, aes(year, hits))
  }
  g + geom_bar(stat = "identity") + 
    scale_x_continuous(labels = years, breaks = years) + 
    xlab("") + ylab("AItopics hits (normalised)") + 
    theme_light() + theme(axis.text.x = element_text(angle = 90))
  
}


# TESTING --------------------------------------------------------------------------------------------------------------------
# keyword = "imagenet"
# keyword = "Arcade Learning Environment"
# keyword = "alpha go"
# keyword = "ITOP front-view"
# keyword = "AFLW-LFPA
# keyword = "COCO"
# d <- getInterest(keyword, exact = T, extra = "dataset")
# plotInterest(d)


## ---------------------------------------------------------------------------------------------------------------------------
## Generation of "AIBenchmarks_CogAbs_process.xlsx" from original mapping ("AIBenchmarks_CogAbs.xlsx") DO NOT RUN 
## ---------------------------------------------------------------------------------------------------------------------------

if (process){
  BenchCog <- read.xlsx2("AIBenchmarks_CogAbs.xlsx", sheetIndex = 1)
  BenchCog$TaskHierarchies <- ""

  TaskCog <- read.xlsx2("AITasks_CogAbs.xlsx", sheetIndex = 1)
  TaskCog[TaskCog$task2 == "ERROR",]$task2 <- ""
  TaskCog[TaskCog$task3 == "ERROR",]$task3 <- ""

  for(i in 1:nrow(BenchCog)){
    print(paste0("Bench: ", BenchCog[i,]$benchmarks))

    for(j in 1:nrow(TaskCog)){
      if(grepl(BenchCog[i,]$benchmarks, TaskCog[j,]$benchmarks)){

        temp <- paste(TaskCog[j,]$category,TaskCog[j,]$task1,TaskCog[j,]$task2,TaskCog[j,]$task3, sep = " > ")
        temp <- str_trim(temp)
        if(substr(temp,nchar(temp), nchar(temp)) == ">"){temp <- substr(temp,1,nchar(temp)-2)}

        BenchCog[i,]$TaskHierarchies <- paste(temp, BenchCog[i,]$TaskHierarchies, sep =" \n")

      }
    }

  }

  write.xlsx(BenchCog, sheetName = "Mapping", file = "AIBenchmarks_CogAbs_process.xlsx")

}


## ---------------------------------------------------------------------------------------------------------------------------
## Analysis of interest (generate csv/rds files)
## ---------------------------------------------------------------------------------------------------------------------------

getCoeff <- function(fit){
  l <- list(R2 = signif(summary(fit)$adj.r.squared, 5),
            Intercept = signif(fit$coef[[1]],5 ),
            Slope = signif(fit$coef[[2]], 5),
            P = signif(summary(fit)$coef[2,4], 5))
  
  return(l)
} 

analysisInterestProcess <- function(mapping = "AIBenchmarks_CogAbs_process.xlsx", years = 2008:2019, RAW = TRUE){
  
  
  ## STEP 1. Process data (benchmarks) to get interest
  ## ---------------------------------------------------------------------------------------------------------------------------
  
  keyword = ""
  BenchCog <- read.xlsx(mapping, sheetIndex = 1)
  interest.df <- data.frame()
  
  for(i in 1:nrow(BenchCog)){
    
    print(paste0(i, " - Bench: ", BenchCog[i,]$benchmarks))
    #d <- getInterest(BenchCog[i,]$name, exact = T, extra = BenchCog[i,]$type)
    d <- getInterest(BenchCog[i,]$name, exact = T, extra = "dataset")
    
    if(nrow(d)>0){
      if(RAW){
        d <- select(d, keyword, year, hits)
      }else{
        d <- select(d, keyword, year, hits.norm)
      }
      interest.df <- rbind(interest.df, cbind(BenchCog[i,], dcast(d, formula = keyword ~ year)))
      
    }else{
      interest.df <- rbind(interest.df, cbind(BenchCog[i,], dcast(data.frame(keyword = BenchCog[i,]$name, year = years, hits.norm = rep(0, length(years))), formula = keyword ~ year)))
    }
  }
  write.csv(interest.df, "interestAIbench_0819.csv")
  if(RAW){
    # Let's normalise by sumcols
    # colnames(interest.df)
    # y <- select(interest.df, c("name", as.character(years)))
    y <- select(interest.df, as.character(years))
    interest.df[, as.character(years)] <- y / colSums(y)[col(y)]
  }

  
  
  
  ## STEP 2. Model/tendencies from data (benchmarks) interest over the years specified
  ## ---------------------------------------------------------------------------------------------------------------------------
  
  toModel <- select(interest.df, one_of(as.character(years)))
  interest.df$Slope <- NA
  interest.df$Intercept <- NA
  interest.df$R2 <- NA
  interest.df$P <- NA
  
  for (i in 1:nrow(interest.df)){
    temp <- melt(toModel[i,])
    temp$variable <- as.numeric(temp$variable)
    temp$value <- as.numeric(temp$value)
    fit <- lm (temp$value ~ variable, data = temp)
    coeff <- getCoeff(fit)
    interest.df[i,]$Slope <-     coeff$Slope
    interest.df[i,]$Intercept <-     coeff$Intercept
    interest.df[i,]$R2 <-     coeff$R2
    interest.df[i,]$P <-     coeff$P
    
  }
  
  
  interest.df = colwise(type.convert)(interest.df)
  interest.df$mean.Interest <- rowSums(select(interest.df, as.character(years)))/length(years)
  # interest.df$mean.Interest.range <- rowSums(select(interest.df, as.character(years.range)))/(rangeMean+1)
  
  write.xlsx(interest.df, file = "interest_kw_processed_raw_slope.xlsx")
  saveRDS(interest.df, file = "interest_kw_processed_raw_slope.rds")
  
  
  
  
  ## STEP 3. Clean Data
  ## ---------------------------------------------------------------------------------------------------------------------------
  
  data = colwise(type.convert)(interest.df)
  data <- select(data, -contains("X.")) #row name
  
  # Change colnames of the years ("X2000" -> "2000")
  ini <- which(colnames(data) == paste0("X",years[1]))
  fin <- which(colnames(data) == paste0("X",years[length(years)]))
  colnames(data)[ini:fin] <- as.character(years)
  
  data$mean.Interest <- (rowSums(select(data, as.character(years)))/length(years))
  data[data$mean.Interest == 0, "mean.Interest"]<- 0.0000000000001
  
  # ERROR data in R2 and P because of NO interest
  data$R2 <- as.numeric(as.character(data$R2))
  data$P <- as.numeric(as.character(data$P))
  data[is.na(data$R2),]$R2 <- 0.0
  data[is.na(data$P),]$P <- 0.0
  
  # Get categories from PwC
  sapply(interest, function(x) sum(is.na(x)))
  data$category  <- NA
  for(i in 1:nrow(data)){
    data$category[i] <- str_trim(str_split(data$TaskHierarchies[i], pattern = ">")[[1]][1])
  } # unique(interest.df$category)
  
  saveRDS(data, file = "interest_benchmarks_clean.rds")
  write.xlsx2(data, file = "interest_benchmarks_clean.xlsx", row.names = FALSE, )
  
}

interestPerYears <- function(data, years=2008:2019, interestYears = "All"){
  
  set.seed(288)
  
  # Mean Interest
  if (interestYears == "All"){
    data$mean.Interest <- (rowSums(select(data, as.character(years)))/length(years))
  }else{
    sel <- select(data, as.character(interestYears))
    data$mean.Interest <- (rowSums(sel)/length(interestYears))
  }
  data[data$mean.Interest == 0, "mean.Interest"]<- 0.0000000000001
  
  return(data)
  
}

plotProgressPeriods <- function(data, periods){
  
  all <- data.frame()
  
  for (p in periods){
    print(p)
    dataPeriod = interestPerYears(data, interestYears = p)
    dataPeriod = prepareVis(dataPeriod)[[1]]
    dataPeriod$period = paste0(as.character(p), collapse = "-")
    dataPeriod$benchmark <- rownames(dataPeriod)
    melted <- melt(dataPeriod, id.vars = c("benchmark", "period"))
    all <- rbind(all, melted)
    
  }
  return(all)
  
}

plotIterest.Cat <- function(data, cat, years = 2008:2019){
  data <- filter(data, category == cat,,year %in% years)
  ann = unique(select(data, keyword, title))
  mean = unique(select(data, keyword, mean.Interest))
  
  plot <- ggplot(data, aes(year, hits.norm)) + 
    geom_bar(stat = "identity", alpha = 0.6) + 
    stat_smooth(method = "lm", col = "darkred", linetype = "dashed", size = 1.2, se = FALSE) + 
    # geom_hline(yintercept = data$mean.Interest) +
    geom_hline(data = mean, aes(yintercept = mean.Interest), colour = "darkgreen", size = 1.2, linetype = "dashed") +
    geom_text(data = ann, aes(x=-Inf, y = +Inf, label = title), vjust = 1, hjust = 0)  + 
    facet_wrap(keyword ~., ncol = 6, scales = "free_y") +
    scale_x_continuous(labels = years, breaks = years) + 
    xlab("") + ylab("AItopics hits (normalised)") + 
    theme_light() 
  return(plot)
}


plotIterest.Bench <- function(data, bench, years = 2008:2019){
  
  cols <- c("keyword", c(years), "Slope", "Intercept", "R2", "P", "mean.Interest", "category" )
  interest.s <- select(data, cols)
  
  interest.m <- melt(interest.s, id.vars = c("keyword", "Slope", "Intercept", "R2", "P", "mean.Interest", "category"))
  colnames(interest.m)[8:9] <- c("year", "hits.norm")
  
  interest.m <- colwise(type.convert)(interest.m)
  interest.m$title <- paste0("Adj R2 = ",round(interest.m$R2,2),
                             "\nIntercept = ",round(interest.m$Intercept,2), 
                             "\nSlope =",round(interest.m$Slope,2),
                             "\nP =",round(interest.m$P,2),
                             "\nMean =",round(interest.m$mean.Interest,2))

  interest.m <- filter(interest.m, keyword == bench, year %in% years)
  ann = unique(select(interest.m, keyword, title))
  mean = unique(select(interest.m, keyword, mean.Interest))
  
  plot <- ggplot(interest.m, aes(year, hits.norm)) + 
    geom_bar(stat = "identity", alpha = 0.7, fill = "#A8DADC") + 
    stat_smooth(method = "lm", col = "#E63946", linetype = "dashed", size = 1.2, se = FALSE) + 
    # geom_hline(yintercept = data$mean.Interest) +
    geom_hline(data = mean, aes(yintercept = mean.Interest), colour = "#1D3557", size = 1.2, linetype = "dashed") +
    geom_text(data = ann, aes(x=-Inf, y = +Inf, label = title), vjust = 1, hjust = 0.0)  + 
    facet_wrap(keyword ~., ncol = 6, scales = "free_y") +
    scale_x_continuous(labels = years, breaks = years) + 
    xlab("") + ylab("AItopics hits (normalised)") + 
    theme_minimal() 
  return(plot)
}


## ---------------------------------------------------------------------------------------------------------------------------
## Graphs (Visnetwork)
## ---------------------------------------------------------------------------------------------------------------------------

prepareVis <- function(data, norm = T, years = 2008:2019, cogAbs = c("MP", "SI", "VP", "AP", "AS", "PA", "CE", "CO", "EC", "NV", "CL", "QL", "MS", "MC")) {
  
  
  set.seed(288)
  
  interest <- select(data, one_of(c("keyword", "category",cogAbs,"mean.Interest")))
  keywords <- interest$keyword
  categories <- interest$category
  rownames(interest) <- keywords
  interest <- interest[,-(1:2)]
  # interest = colwise(type.convert)(interest)
  
  interest.mean <- interest$mean.Interest
  interest <- select(interest, -mean.Interest)
  
  # indx <- sapply(interest, is.factor)
  # interest[indx] <- lapply(interest[indx], function(x) as.numeric(as.character(x)))
  # indxNA <- which(sapply(interest, function(x) sum(is.na(x)))>0)
  # 
  
  
  interest.pond <- interest * interest.mean ## change factor to numeric
  return(list(interest.pond, interest, interest.mean))

}

plotVis <- function(data, categories, norm = T){
  
  set.seed(288)
  
  # shapes =  c("square", "triangle", "box", "circle", "dot", "star",
  #             "ellipse", "database", "text", "diamond", "square", "triangle","box")
  # vis$nodes$shape <- c(shapes[as.numeric(as.factor(categories))], rep("#dot",14))
  
  colours = c("1" = "blalck", "2" = "#543005","3" = "#8c510a","4" = "#bf812d",
              "5" = "#dfc27d","6" = "#f6e8c3","7" = "#f5f5f5","8" = "#c7eae5",
              "9" = "#80cdc1", "10" = "#35978f", "11" = "#01665e", "12" = "#003c30", "13" = "#FAFAFA")
  
  vis <- toVisNetworkData(graph_from_incidence_matrix(data, directed = F, weighted = T))
  
  vis$nodes$value = c(rep(10, nrow(vis$nodes)-14), colSums(data)*10000)
  vis$nodes$title <- vis$nodes$label
  vis$nodes$category <- c(categories, rep("CogAb", 14))
  vis$nodes$group <- vis$nodes$category 
  vis$nodes$color <- colours[as.numeric(as.factor(vis$nodes$category))]
  
  # vis$edges$value <- log(vis$edges$weight+1)
  vis$edges$value <- log(normalize(vis$edges$weight+0.00001, method = "range", range = c(0,1))+0.00001)
  
  # vis$edges$width <- vis$edges$weight
  
  v <- visNetwork(vis$nodes, vis$edges,  height = "1000px", width = "100%") %>% 
    visEdges(arrows = "to", color = list(color = 'rgba(70,130,180,0.3)', highlight ="#4682B4")) %>%
    visIgraphLayout(
      physics = F,
      randomSeed = 2017,
      layout = "layout_with_fr"
    ) %>%  
    visInteraction(navigationButtons = TRUE) %>% 
    visOptions(selectedBy = "group",highlightNearest = TRUE )
  
  return(v)
  
}


## ---------------------------------------------------------------------------------------------------------------------------
## Visualisations
## ---------------------------------------------------------------------------------------------------------------------------

# data = readRDS("interest_benchmarks_clean.rds")
# data2 = interestPerYears(data, interestYears = 2009:2018)
# plotVis(prepareVis(data2)[[1]], categories = data2$category)

# 
# data = readRDS("interest_benchmarks_clean.rds")
# data2 = interestPerYears(data, interestYears = 2009:2013)
# plotVis(prepareVis(data2)[[1]], categories = data2$category)
# 
# 
# data2b = interestPerYears(data, interestYears = 2014:2018)
# plotVis(prepareVis(data2b)[[1]], categories = data2b$category)
# 
# 
# data2c = interestPerYears(data, interestYears = 2019)
# plotVis(prepareVis(data2c)[[1]], categories = data2c$category)
# 
# 
# ## Mean Interest per AI benchmak ---------------------------------------------
# 
# data = readRDS("interest_benchmarks_clean.rds")
# 
# df.interest <- data.frame(Benchmark = data$keyword,
#                           "2009-2013" = data2$mean.Interest, 
#                           "2014-2018" = data2b$mean.Interest,
#                           "2019" = data2c$mean.Interest)
# 
# 
# df.interest.m <- melt(df.interest, id.vars = "Benchmark")
# 
# a <- ggplot(df.interest.m, aes(reorder(Benchmark,value), value, colour = variable)) + 
#   geom_point(alpha = 1/3, size = 1) +
#   coord_flip() + theme_minimal() + theme(legend.position="bottom")
# 
# b <- ggplot(df.interest.m, aes(reorder(Benchmark,value), log(value), colour = variable)) + 
#   geom_point(alpha = 1/3, size = 1) + xlab("") + ylab("") + 
#   coord_flip() + theme_minimal() + theme(legend.position="bottom")
# 
# grid.arrange(a,b, ncol = 2)
# 
# 
# 
# 
# dataA = interestPerYears(data, interestYears = 2008:2010)
# dataB = interestPerYears(data, interestYears = 2011:2013)
# dataC = interestPerYears(data, interestYears = 2014:2016)
# dataD = interestPerYears(data, interestYears = 2017:2019)
# 
# df.interest <- data.frame(Benchmark = data$keyword,
#                           "2008:2010" = dataA$mean.Interest, 
#                           "2011:2013" = dataB$mean.Interest,
#                           "2014:2016" = dataC$mean.Interest,
#                           "2017:2019" = dataD$mean.Interest)
# 
# 
# df.interest.m <- melt(df.interest, id.vars = "Benchmark")
# 
# a <- ggplot(df.interest.m, aes(reorder(Benchmark,value), value, colour = variable)) + 
#   geom_point(alpha = 1/3, size = 1) +
#   coord_flip() + theme_minimal() + theme(legend.position="bottom")
# 
# b <- ggplot(df.interest.m, aes(reorder(Benchmark,value), log(value), colour = variable)) + 
#   geom_point(alpha = 1/3, size = 1) + xlab("") + ylab("") + 
#   coord_flip() + theme_minimal() + theme(legend.position="bottom")
# 
# grid.arrange(a,b, ncol = 2)
# 
# 


### Relevance of the cognitive abilities in diferent periods ----------------------------------------------

# periods <- list(2008:2010, 2011:2013, 2014:2016, 2017:2019)
# periods <- 2008:2019
# 

# 
# periods <- list(2008:2010, 2011:2013, 2014:2016, 2017:2019)
# periods <- 2008:2019
# 
# 
# all <- plotProgressPeriods(data, periods)
# 
# all.s <- summarise(group_by(all, period, variable), mean = mean(value))
# 
# ggplotly(ggplot(all.s, aes(variable,mean, fill = period)) + geom_bar(stat = "identity",position = "dodge") + xlab("") + ylab("Mean Interest") + 
#            scale_fill_brewer(palette = "Paired") + theme_minimal())
