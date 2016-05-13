library(ggmap)
library(RgoogleMaps)
library(rgdal)
library(ggplot2)
library(plotrix)
library(classInt) 
library(dismo)
library(raster)
library(plyr)         # To manipulate data
library(lattice)      # To have Lattice graphic interface
library(sp)   
gpclibPermit()
  


setwd('~/Desktop/1004/project/')

CenterOfMap <- geocode("New York City")
#whole NYC
NYC <- get_map(c(-73.8549,40.755),zoom = 11, maptype = 'satellite', source = "google")
NYC <- ggmap(NYC)

#manhatton center
NYC <- get_map(c(-73.989,40.765),zoom = 12,maptype = 'terrain-lines', source = "google")
NYC <- ggmap(NYC)
NYC
#broklyn
NYC <- get_map(c(-73.965,40.715),zoom = 12, maptype = 'terrain-lines', source = "stamen")
NYC <- ggmap(NYC)
NYC


  
dist_man_normal = read.csv('dist_man_normal.csv',col.names = c('id','man'))
dist_brok_normal = read.csv(' dist_brok_snow.csv',col.names = c('id','brok'))
dist_que_normal = read.csv(' dist_que_snow.csv',col.names = c('id','que'))

#dist_brok_normal$brok = sqrt(dist_brok_normal$brok) 
#dist_que_normal$que = sqrt(dist_que_normal$que)

Neighborhoods <- readOGR(dsn = "." ,"geo_export_b9ed049f-9a51-476c-bbfa-739885e2831f")
Neighborhoods <- spTransform(Neighborhoods, CRS("+proj=longlat +datum=WGS84"))
Neighborhoods$id <- row.names(Neighborhoods)


temp1 = join(Neighborhoods@data,dist_man_normal,by = 'id')
temp1[is.na(temp1$man),'man'] =0
Neighborhoods@data$man = temp1$man

temp2 = join(Neighborhoods@data,dist_que_normal,by = 'id')
temp2[is.na(temp2$que),'que'] =0
Neighborhoods@data$que = temp2$que

temp3 = join(Neighborhoods@data,dist_brok_normal,by = 'id')
temp3[is.na(temp3$brok),'brok'] =0
Neighborhoods@data$brok = temp3$brok

Neighborhoods.df = fortify(Neighborhoods)
Neighborhoods.df <- join(Neighborhoods.df, Neighborhoods@data)


#NYCMap <- NYC + 
                geom_polygon(aes(x=long, y=lat, group=group), fill ='grey' , size=.2,color='black', data=Neighborhoods, alpha=0.2)

pal3 <- colorRampPalette(c("white", "blue"))
              
NYC <- NYC + 
  #ggplot( data =sample, aes(x = long, y = lat))+
  geom_polygon(aes(x=long, y=lat, group=group ,alpha = sqrt(man)),show.legend = FALSE,fill= 'red',data=Neighborhoods.df)+
  geom_polygon(aes(x=long, y=lat, group=group ,alpha = sqrt(brok)),show.legend = FALSE,fill = 'green',data=Neighborhoods.df)+
  geom_polygon(aes(x=long, y=lat, group=group ,alpha = sqrt(que)),show.legend = FALSE,fill = 'blue',data=Neighborhoods.df)+
  geom_polygon(aes(x=long, y=lat, group=group), fill ='grey' , size=.2,color='black', data=Neighborhoods, alpha=0.2)+
  ggtitle("Pick Up Distribution")+
  theme(plot.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=32, hjust=0)) +
  theme(axis.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=22)) + theme_bw()



###################plot 
setwd('~/Desktop/1004/project/')
dist_man_normal = read.csv('pointer_man_snow.csv',col.names = c('id','to','man'))

connection = c()
place = c()
for (i in 1:nrow(dist_man_normal)){
  from = as.numeric(dist_man_normal[i,][1]+1)
  to = as.numeric(dist_man_normal[i,][2]+1)
  if (from != to){
  connection = rbind(connection,
                     c(Neighborhoods@polygons[[from]]@labpt,Neighborhoods@polygons[[to]]@labpt,
                       as.numeric(dist_man_normal[i,][3]),Neighborhoods@polygons[[from]]@area,Neighborhoods@polygons[[to]]@area))
  place = rbind(place,c(Neighborhoods@polygons[[from]]@labpt,as.character(Neighborhoods@data[from,'ntaname'])))
  place = rbind(place,c(Neighborhoods@polygons[[to]]@labpt,as.character(Neighborhoods@data[to,'ntaname'])))
  }
  }
place = place[!duplicated(place), ]
#colnames(place) = c('x1','x2','text')
place = data.frame(x1 = as.numeric(place[,1]),x2 = as.numeric(place[,2]),text = place[,3])

connection = data.frame(x1 = connection[,1],x2 = connection[,2], y1 =  connection[,3], y2 =connection[,4],val =  connection[,5],afrom = connection[,6],ato = connection[,7])

points = c()
for (i in 1:(nrow(connection))){
  temp = as.numeric(connection[i,])
  points = rbind(points,c(temp[1:2],temp[5]))
  points = rbind(points,c(temp[3:4],temp[5]))
}

sample = c()
for (i in 1:nrow(points)){
  temp = points[i,]
  sample = rbind(sample,cbind(rnorm(3,temp[1],sqrt(temp[3])/100), rnorm(3,temp[2],sqrt(temp[3])/100)))
} 

sample = data.frame(long = sample[,1],lat = sample[,2])


NYC +
  ggplot( data =sample, aes(x = long, y = lat))+
  geom_polygon(aes(x=long, y=lat, group=group),color = 'grey', alpha = 0.1,fill ='white', data=Neighborhoods.df,show.legend = FALSE)+ 
  stat_density2d(aes(x = long, y = lat, fill = ..level.., alpha = ..level..),
                     bins = 10, geom = "polygon",data = sample,size = 10,show.legend = FALSE)+
  scale_fill_gradient(low = "black", high = "red")+
  #geom_polygon(aes(x=long, y=lat, group=group), fill ='grey' , size=.2,color='black', data=Neighborhoods, alpha=0.2)
  #geom_polygon(aes(x=long, y=lat, group=group ,alpha = 1),show.legend = FALSE,fill= 'black',data=Neighborhoods.df)+
  geom_point(data = connection,aes(x =x1 , y =x2),color = 'blue',alpha = 1)+scale_size_continuous(range=c(1,10))+
  geom_point(data = connection,aes(x =y1 , y =y2),color = 'blue',alpha =1)+
  geom_curve(aes(xend = connection$x1, yend = connection$x2, x = connection$y1, y = connection$y2),color= 'blue',size = connection$val*10,  curvature = 0.26,data = connection,arrow=arrow(angle=15,ends="first",length=unit(0.4,"cm"),type="closed")) +                    
  coord_cartesian(xlim = c(-73.989-0.05, -73.989+0.05),ylim = c(40.765-0.05,40.765+0.05))+theme_bw()+
  geom_text(data = place, aes(x = x1, y = x2+0.003, label = as.character(text)), size=4)+
  ggtitle("Trips in Manhattan")+
  theme(plot.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=32, hjust=0)) +
  theme(axis.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=25))
  #theme(panel.background = element_rect(fill = "white", colour = "grey"),
  #        panel.grid.major = element_line(colour = "grey"))
  #geom_polygon(aes(x=long, y=lat, group=group), fill ='grey' , size=.2,color='black', data=Neighborhoods, alpha=0.2)


############
#plot connections
sample = read.csv('sample_day.csv')

NYC <- get_map(c(-73.8549,40.755),zoom = 10, maptype = 'satellite', source = "google")
NYC <- ggmap(NYC)

theme_temp = theme(axis.line=element_blank(),
                   axis.text.x=element_blank(),
                   axis.text.y=element_blank(),
                   axis.ticks=element_blank(),
                   axis.title.x=element_blank(),
                   axis.title.y=element_blank(),
                   legend.position="none",
                   panel.background=element_blank(),
                   panel.border=element_blank(),
                   panel.grid.major=element_blank(),
                   panel.grid.minor=element_blank(),
                   plot.background=element_blank())

hist_top <- ggplot()+geom_histogram(aes(sample$x1),breaks=seq(-73.905-0.13, -73.905+0.13, by = 0.01),fill = 'red')+theme(axis.title.x = element_blank())+theme_temp
hist_right <- ggplot()+geom_histogram(aes(sample$x2),breaks=seq(40.735-0.13,40.735+0.13, by = 0.01),fill = 'red')+coord_flip()+theme_temp
hist_bot <- ggplot()+geom_histogram(aes(sample$y1),breaks=seq(-73.905-0.13, -73.905+0.13, by = 0.01),fill = 'white',col = 'black')+scale_y_reverse()+theme_temp
hist_left <- ggplot()+geom_histogram(aes(sample$y2),breaks=seq(40.735-0.13,40.735+0.13, by = 0.01),fill = 'white',col = 'black')+scale_y_reverse() +coord_flip()+theme_temp


NYC =
  ggplot( data =sample, aes(x = x1, y = x2))+
  geom_polygon(aes(x=long, y=lat, group=group),color = 'white', alpha = 1,fill ='black', data=Neighborhoods.df,show.legend = FALSE)+ 
  #geom_polygon(aes(x=long, y=lat, group=group), fill ='grey' , size=.2,color='black', data=Neighborhoods, alpha=0.2)
  #geom_polygon(aes(x=long, y=lat, group=group ,alpha = 1),show.legend = FALSE,fill= 'black',data=Neighborhoods.df)+
  geom_curve(aes(xend = x1, yend = x2, x = y1, y = y2),color= 'skyblue1',size =0.18,  curvature = 0.26,data = sample,arrow=arrow(angle=25,ends="first",length=unit(0.01,"cm"),type="closed")) +                    
  coord_cartesian(xlim = c(-73.905-0.13, -73.905+0.13),ylim = c(40.735-0.13,40.735+0.13))+
  geom_point(data = sample,aes(x =x1 , y =x2),color = 'red',alpha = 1,size = 0.03)+scale_size_continuous(range=c(1,10))+
  geom_point(data = sample,aes(x =y1 , y =y2),color = 'white',alpha =1,size = 0.03)+
  theme(panel.background = element_rect(fill = "black"))

empty <- ggplot()+geom_point(aes(1,1), colour="white")+
  theme(axis.ticks=element_blank(), 
        panel.background=element_blank(), 
        axis.text.x=element_blank(), axis.text.y=element_blank(),           
        axis.title.x=element_blank(), axis.title.y=element_blank())

grid.arrange(empty,hist_top, empty,hist_left,NYC, hist_right,empty,hist_bot, empty, ncol=3, nrow=3, widths=c(1,6, 1), heights=c(1, 6,1))

  geom_text(data = place, aes(x = x1, y = x2+0.003, label = as.character(text)), size=4)+
  ggtitle("Trips in Manhattan")+
  theme(plot.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=32, hjust=0)) +
  theme(axis.title = element_text(family = "Trebuchet MS", color="#666666", face="bold", size=25))+theme_map()
#theme(panel.background = element_rect(fill = "white", colour = "grey"),





