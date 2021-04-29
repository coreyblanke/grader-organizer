# Grader-Organizer
A python program which helps optimize your computer science grading workflow. Built to be run in barebones python 3.8 across multiple platforms. 

## Usage tl;dr
Drop the python file anywhere on your machine, open a terminal and run it with the command ``` python3 gradecsv.py {args} ```, and follow the instructions in the --help menu (written below). 
## Usage
```usage: gradecsv.py [-h] [-d DIRECTORY] [-o OUTPUT] [-n NUMCOLLABORATORS] [-i INPUTFILE] [-tl] {csv,zip,folder}

positional arguments:
  {csv,zip,folder}      csv - create grade book; zip - mass unzip; folder - generate name folders from file

optional arguments:
  -h, --help            show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        csv mode - directory that student information is stored in;zip mode - target directory to copy unzipped folders into; folder
                        mode - directory to write student folders into
  -o OUTPUT, --output OUTPUT
                        name of csv file to be created, do not include directory info here, will be placed in target directory
  -n NUMCOLLABORATORS, --numcollaborators NUMCOLLABORATORS
                        maximum number of collaborators for the assignment
  -i INPUTFILE, --inputfile INPUTFILE
                        csv mode - filename of student input file, include directory info if relevant; zip mode - directory containing zip files in
                        student folders
  -tl, --toplevel       allow copying of top level files in zip mode```
