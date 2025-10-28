# FILE: CSV_filter.py
#
# Description:
"""
This script filters large CSV files by specified criteria.  
It is primarily used to reduce EHRShot datasets to smaller, analysis-ready subsets by excluding rows for efficient data processing.
"""

# Import the CSV module
import csv
import os
from tqdm import tqdm  # Adds progress timer for long for loops

dirname = os.path.dirname(__file__)
datasetPath = os.path.join(dirname, 'EHRShot_dataset')
file_objects = {}

print("\n")
print(f"File Path: {dirname}")
print(f"EHRShot Data Set Path: {datasetPath}")
print("\n")


def get_file_read(filename: str, dict: bool):
    """_summary_
    Opens a file in readmode with optional dict reading
    """

    try:
        newReadFile = open(datasetPath + '\\' + (filename),
                           mode='r', errors='ignore', encoding='utf-8', newline='')

        if dict == True:
            file_objects[filename] = newReadFile
            return csv.DictReader(newReadFile, delimiter=",")
        else:
            file_objects[filename] = newReadFile
            return newReadFile

    except FileNotFoundError:
        print(
            f"ERROR: The file {datasetPath + '\\' + (filename)} not found!\n")
        return None

    except Exception:
        print("UNEXPECTED ERROR CODE: get_file_read() \n")
        return None


def get_file_read(filename: str, dict: bool):
    """_summary_
    Opens a file in readmode with optional dict reading
    """

    try:
        newReadFile = open(datasetPath + '\\' + (filename),
                           mode='r', errors='ignore', encoding='utf-8', newline='')

        if dict == True:
            file_objects[filename] = newReadFile
            return csv.DictReader(newReadFile, delimiter=",")
        else:
            file_objects[filename] = newReadFile
            return newReadFile

    except FileNotFoundError:
        print(
            f"ERROR: The file {datasetPath + '\\' + (filename)} not found!\n")
        return None

    except Exception:
        print("UNEXPECTED ERROR CODE: get_file_read() \n")
        return None


def get_file_write(filename: str):
    """_summary_
    Opens a file writer
    """

    try:
        newWriteFile = open(filename,
                            mode='w', errors='ignore', newline='')
        file_objects[filename] = newWriteFile
        return newWriteFile

    except IOError as e:
        print(
            f"ERROR: The file {filename} could not be opened or created: {e}!\n")
        return None

    except Exception:
        print("UNEXPECTED ERROR CODE: get_file_write() \n")
        return None


def close_allfiles():
    """_summary_
    Close all file readers and writer handles created
    """
    for f in file_objects:
        try:
            file_objects[f].close()
        except Exception as e:
            print(f'ERROR closing file: {e} for {f} in close_allfiles()\n')


def close_file(filename: str):
    """_summary_
    Call to close a single file reader or writer
    """
    try:
        file_objects[filename].close()
        file_objects.pop(filename)
    except Exception as e:
        print(f'ERROR closing file: {e} for {filename} in close_files()\n')


# Read in CSV files
sample_drugs_exposure = get_file_read('drug_exposure.csv', True)
procedures_half_2020file = get_file_read(
    'proceduers_with_drug_exposure.csv', True)

# Create a CSV file
csvWriter = csv.DictWriter(get_file_write(
    'drugs_+_procedures.csv'), sample_drugs_exposure.fieldnames)
csvWriter.writeheader()

# Store procedure NODE IDs
procedures_half_2020 = set()

# Filter drug exposures to procedures done in beginning 2020
for row in tqdm(procedures_half_2020file):
    if row['visit_occurrence_id'] not in procedures_half_2020:
        procedures_half_2020.add(row['visit_occurrence_id'])

# Write to CSV file
for row in tqdm(sample_drugs_exposure):
    if row['visit_occurrence_id'] in procedures_half_2020:
        csvWriter.writerow(row)

close_allfiles()
