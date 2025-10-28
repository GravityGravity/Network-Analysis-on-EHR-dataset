# FILE: CSV_fieldname.py

# Description:
"""
    This script scans all CSV files within a specified folder and prints out their table field names (column headers).  
    It is used to quickly inspect data structure and confirm consistent schema alignment across multiple EHRShot files.
"""

# Import the CSV module
import csv
import os

dirname = os.path.dirname(__file__)
dirPath = os.path.join(dirname, 'EHRShot_Dataset')

newTxtfile = open('Fieldnames.txt', 'w+', newline='')

# For loop iterates through all files within EHRShot_dataset and prints out their fieldnames
for i, filesname in enumerate(os.listdir(dirPath)):
    file_path = os.path.join(dirPath, filesname)
    curFile = open(file_path, mode='r', encoding="utf-8", newline='')
    print(f'{i}: {file_path}')
    first_line = curFile.readline()
    first_line = first_line.replace(',', '\t')
    newTxtfile.write(filesname + '\n')
    newTxtfile.write(first_line + '\n')
    curFile.close()

newTxtfile.close()
