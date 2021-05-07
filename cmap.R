# Calls the sorting function, feeds rCMAP

library("reticulate")
library("shiny")
library("DT")
library("readxl")
library("rtf")
library("smacof")
library("xtable")

path = getwd()
if (!grepl("cMapKMeans", path)){
  setwd(paste(path, "/cMapKMeans", sep = ""))
}

# Make data -- need to fix this
py_run_file("autoSort.py")


# Run App
runApp("/Users/henrymanley/Downloads/RCMAP",display.mode="no", launch.browser=TRUE, port=2197)
