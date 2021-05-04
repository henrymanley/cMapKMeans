library("reticulate")
reticulate::use_condaenv("py37")
py_run_file("autoSort.py")

