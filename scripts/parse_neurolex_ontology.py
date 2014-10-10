"""
parse neurolex ontology
1. convert csv file to tab-delimited text using excel
2. fix excel file using:  
cat allen_brain_atlas_human_ontology.txt | tr '\r' '\n' > allen_brain_atlas_human_ontology_fixed.txt

"""

import simplejson

ontologyfile='allen_brain_atlas_human_ontology_fixed.txt'
treefile='allen_human_brain_ontology_structure_graph.json'

f=open(ontologyfile)
header=f.readline().strip().split('\t')
lines=[i.strip().split('\t') for i in f.readlines()]
f.close()

tree=simplejson.load(open(treefile))

treeitems=tree['msg'][0]

ontologyRegions={}
for l in lines:
    key=l[0] # 2].replace(' ','_').replace('"','')
    ontologyRegions[key]={}
    for f in range(len(header)):
        ontologyRegions[key][header[f]]=l[f].replace('"','')
        
