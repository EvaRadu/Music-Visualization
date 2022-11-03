setwd("C:/Users/evara/Desktop/OneDrive_2022-11-03/Wasabi Data")

library(stringr)

rds2csv <- function(file) {
  data <- readRDS(str_replace_all(string=paste(file,".rds"), pattern=" ", repl=""))
  df <- as.data.frame(data)
  write.csv(df,str_replace_all(string=paste(file,".csv"), pattern=" ", repl=""), row.names = FALSE)
  
}

rds2csv("data/albums_all_artists_3000")
rds2csv("data/songs_all_artists_3000")
rds2csv("data/songs_all_artists_72000")
rds2csv("data/songs_all_artists_72200")
rds2csv("data/songs_all_artists_72400")
rds2csv("data/songs_all_artists_72600")
rds2csv("data/songs_all_artists_72800")
rds2csv("data/songs_all_artists_73000")
rds2csv("data/songs_all_artists_73200")
rds2csv("data/songs_all_artists_73400")
rds2csv("data/songs_all_artists_73600")
rds2csv("data/songs_all_artists_73800")
rds2csv("data/songs_all_artists_74000")
rds2csv("data/songs_all_artists_74200")
rds2csv("data/songs_all_artists_74400")
rds2csv("data/songs_all_artists_74600")
rds2csv("data/songs_all_artists_74800")
rds2csv("data/wasabi_all_artists_3000")






