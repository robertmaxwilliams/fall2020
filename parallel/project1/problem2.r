require(scales)
library(ggplot2)
library(patchwork)

t <- function(p, n) {
    n/p - 1 + 7*log2(p)
}
tprime <- function(p) {
    1023 + 7*log2(p)
}
speedup <- function(p) {
    (1024*p-1)/(1023+7*log2(p))
}
efficiency <- function(p) {
    100*(1024*p-1)/(p*(1023+7*log2(p)))
}

xdata=c(1,2,4,8,16,32,64,128,256,512)
df <- data.frame("x" = xdata, "speedup"=speedup(xdata), "efficiency"=efficiency(xdata))
left <- ggplot(df, aes(x = x, y = speedup)) +
    geom_line() +
    scale_x_continuous(trans = log2_trans(), breaks = xdata)
right <- ggplot(data=df, aes(x=x, y=efficiency)) +
    geom_bar(stat="identity") +
    scale_x_continuous(trans = log2_trans(), breaks = xdata)
ggsave( "/Users/max/Repos/fall2020/parallel/project1/plot2.png",
       plot = left+right,
       device=png(),
       width=8, height=4, dpi=100)
