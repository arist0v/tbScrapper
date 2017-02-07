# tbScrapper

script to find valid termbin. could be use with keyword 

usage: tbScrapper.py [-h] [-m MAXGRABS] [-f FOLDER] [-k KEYWORD] [-t THREAD]

try to find valid termbin page and download data

optional arguments:
  -h, --help            show this help message and exit
  -m MAXGRABS, --maxgrabs MAXGRABS
                       number of valid url to get, Default: 10
  -f FOLDER, --folder FOLDER
                       folder to save the data in, default: current folder
  -k KEYWORD, --keyword KEYWORD
                       only get data that contain this keyword
  -t THREAD, --thread THREAD
                       number of thread to use. Default: 1
