# File: graph_create.py
#
# Description:
#   This script constructs a bipartite network graph of medical procedures and drug exposures
#   using the filtered EHRShot dataset created by CSV_filter.py
#
#   The resulting graph object provides the structural basis for subsequent network analysis,
#   visualization, and computation of metrics such as degree, centrality, and density.
#
# Import the CSV module
import csv
import os
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict

# Get file directory of csv we want
dirname = os.path.dirname(__file__)
dataSetPath = os.path.join(dirname, 'Filtered_Datasets')
file_objects = {}
write_graph_data_csv = True


def get_file_read(filename: str, dict: bool):
    """_summary_
    Opens a file in readmode with optional dict reading
    """

    try:
        newReadFile = open(dataSetPath + '\\' + (filename),
                           mode='r', errors='ignore', encoding='utf-8', newline='')

        if dict == True:
            file_objects[filename] = newReadFile
            return csv.DictReader(newReadFile, delimiter=",")
        else:
            file_objects[filename] = newReadFile
            return newReadFile

    except FileNotFoundError:
        print(
            f"ERROR: The file {dataSetPath + '\\' + (filename)} not found!\n")
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


# Create a graph
G = nx.Graph()

# Read CSVs
proceduresCSV = get_file_read(
    'procedures_with_drug_exposure_begin_2020.csv', True)

drugsCSV = get_file_read(
    'drugs_exposure_from_procedures_begin_2020.csv', True)

IDtranslationCSV = get_file_read(
    'medical_concept_dictionary', True)

# Storing medical_concept_ids of procedures and drugs and visits
IDdictionary = {}
procedureIDset = set()
drugIDset = set()

# Order concept IDs by visit ID
procedureByVisit = defaultdict(list)
drugByVisit = defaultdict(list)

# Procedures Node Creation w/ Weights
for row in tqdm(proceduresCSV):

    procedureByVisit[row['visit_occurrence_id']].append(
        row['procedure_concept_id'])

    if row['procedure_concept_id'] not in procedureIDset:
        procedureIDset.add(row['procedure_concept_id'])
        G.add_node('P-' + row['procedure_concept_id'],
                   weight=1, color='blue', **row)
        continue
    else:
        G.nodes['P-' + row['procedure_concept_id']]['weight'] += 1

print(procedureIDset)

# Drug nodes creation without weights
for row in tqdm(drugsCSV):

    drugByVisit[row['visit_occurrence_id']].append(
        row['drug_concept_id'])

    if row['drug_concept_id'] not in drugIDset:
        drugIDset.add(row['drug_concept_id'])
        G.add_node('D-' + row['drug_concept_id'],
                   weight=1, color='red', **row)


# Creation of edges between a procedure and drug that was prescribed during the same visit
for visitid, procid in tqdm(procedureByVisit.items()):
    drugid = drugByVisit.get(visitid, [])

    for proc in procid:
        for drug in drugid:
            if G.has_edge('P-' + proc, 'D-' + drug):
                print('EDGE EXISTS', end='')
                G['P-' + proc]['D-' + drug]["weight"] += 1
            else:
                print('EDGE ADDED', end="")
                G.add_edge('P-' + proc, 'D-' + drug, weight=1)


# Output graph edges as a CSV
if write_graph_data_csv == True:
    graph_data_fieldsnames = ['Procedure ID',
                              'Drug Prescription occurence During Procedural Visits', 'Drug ID']

    CSV_graph_data = csv.DictWriter(
        get_file_write('Graph_data_all_edges.csv'), graph_data_fieldsnames)

    CSV_graph_data.writeheader()

# Filter out edges that have a weight less than 500
for u, v, data in list(G.edges(data=True)):
    if data.get("weight", 1) > 500:
        print(u, v, data)
        if write_graph_data_csv == True:
            CSV_graph_data.writerow(
                {"Procedure ID": u, "Drug Prescription occurence During Procedural Visits": data.get('weight', 1), "Drug ID": v})
    else:
        G.remove_edge(u, v)

# Graph Creation

for node, data in G.nodes(data=True):
    print(node, data.get('weight'))

weights = [data.get("weight", 0) for _, data in G.nodes(data=True)]
node_colors = list(nx.get_node_attributes(G, 'color').values())

# Output graph as .gefx file
nx.write_gexf(G, "EHR_Analysis.gexf")

# Draw graph with random node placement
nx.draw_random(
    G,
    with_labels=False,
    node_color=node_colors,
    node_size=[w*0.5 for w in weights],  # optional: scale size by weight
    edge_color="gray",
    font_size=2,
    font_color="black"
)

# Plot graph
plt.show()
print('\n')
