source("Interest_AItopics.R")
#plots

openPDFEPS <- function(file, height= PDFheight, width= PDFwidth, PDFEPS = 1) {
  if (PDFEPS == 1) {
    pdf(paste(file, ".pdf", sep=""), width, height)
  } else if (PDFEPS == 2) {
    postscript(paste(file, ".eps", sep=""), width, height, horizontal=FALSE)
  }
}

data = readRDS("interest_benchmarks_clean.rds")
a<- plotIterest.Bench(data, "CIFAR",years = 2009:2018)
b<- plotIterest.Bench(data, "MNIST",years = 2009:2018)
c<-plotIterest.Bench(data, "CoNLL",years = 2009:2018)
d<-plotIterest.Bench(data, "Go",years = 2009:2018)

e<-plotIterest.Bench(data, "MovieLens",years = 2009:2018)
f<-plotIterest.Bench(data, "UCI",years = 2009:2018)
g <- plotIterest.Bench(data, "Arcade Learning Environment",years = 2009:2018)
h <- plotIterest.Bench(data, "SQuAD",years = 2009:2018)

i <- plotIterest.Bench(data, "ImageNet",years = 2009:2018)
j <- plotIterest.Bench(data, "CUHK",years = 2009:2018)
k <- plotIterest.Bench(data, "PASCAL VOC",years = 2009:2018)
l <- plotIterest.Bench(data, "TREC",years = 2009:2018)

openPDFEPS("interest_benchmarks12", heigh = 9, width = 16)
grid.arrange(a,b,c,d,e,f,g,h,i,j,k,l, ncol = 4)
dev.off()




periods <- list(2008:2010, 2011:2013, 2014:2016, 2017:2018)

all <- plotProgressPeriods(data, periods)
all.s <- summarise(group_by(all, period, variable), mean = mean(value))
all.s$period <- factor(all.s$period)
levels(all.s$period) <- c("2008-2010","2011-2013","2014-2016","2017-2018")

p1 <- ggplot(all.s, aes(variable,mean, fill = period)) +
  geom_bar(stat = "identity",position = "dodge") + 
  xlab("") + ylab("Mean Interest") + 
  scale_fill_manual(values = c("#E63946", "#A8DADC", "#457B9D", "#1D3557")) + 
  theme_minimal() +  theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods)))

openPDFEPS("4Periods", heigh = 6, width = 10)
p1
dev.off()


all.ag <- summarise(group_by(all, variable), mean = mean(value))

p1b <- ggplot(all.s, aes(variable,mean )) +
  geom_bar(data = all.ag, aes(variable, mean), stat = "identity", alpha = 0.5, linetype = "dashed", colour = "gray", fill = "white") +
  geom_bar(aes(fill = period), stat = "identity",position = "dodge", alpha  = 0.8) +
  xlab("") + ylab("Mean Interest") + 
  scale_fill_manual(values = c("#E63946", "#A8DADC", "#457B9D", "#1D3557")) + 
  theme_minimal() +  theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods)))

openPDFEPS("4Periods", heigh = 6, width = 10)
p1b
dev.off()



periods <- 2008:2018

all2 <- plotProgressPeriods(data, periods)
all2.s <- summarise(group_by(all2, period, variable), mean = mean(value))

p2 <- ggplot(all2.s, aes(variable,mean, fill = period)) + geom_bar(stat = "identity",position = "dodge") + xlab("") + ylab("Mean Interest") + 
           scale_fill_brewer(palette = "Paired") + theme_minimal() + theme(legend.position = "bottom", legend.title = element_blank()) + guides(fill=guide_legend(ncol=length(periods)))


openPDFEPS("yearPeriods", heigh = 6, width = 10)
p2
dev.off()







COCO <- readRDS("ProgresDataRank.RDS")

levels(COCO$metric)

levels(COCO$metric) <- c("Average Precision", "Average Precision", "Average Recall", "Bounding Box", "Error rate", "F-Measure", "FID", "FPS", "Inception score", 
                        "mAP", "Mean Precision", "Mean IoU", "mAP", "runtime (ms)", "Top 1 Accuracy", "Top 5 Accuracy"   )
library(lubridate)
d = dmy("31-12-2018")
COCO$years <- year(COCO$date)
COCO <- filter(COCO, !(metric %in% c("FID", "FPS", "Inception score")))
COCO <- filter(COCO, years <= 2018)
unique(COCO$metric)
COCO$date

class(COCO$years)



met <- ggplot(COCO, aes(date, value, colour = metric, shape = metric)) + 
  geom_point(size = 4) + 
  geom_smooth(method = lm, formula = y ~ splines::ns(x, 2), se = FALSE, linetype = "dashed") +
  scale_colour_manual(values=c("#E63946", "#A8DADC", "#1D3557")) + 
  scale_shape_manual(values=c(15, 16, 17, 18, 13, 14,19,20))  +
  labs(colour = "Evaluation Metric", shape = "Evaluation Metric") +
  theme_minimal() + ggtitle("COCO")


met
openPDFEPS("COCOmetrics", heigh = 4, width = 10)
met
dev.off()
