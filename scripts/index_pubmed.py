"""
index pubmed for anatomical ontology terms
"""

from Bio.Entrez import efetch, read
import pickle

ontology=pickle.load(open('pubbrain_hierarchy.pkl'))

try:
    records = pickle.load(open('/Users/poldrack/data_unsynced/pubbrain/pubmed_search_records.pkl','rb'))
except:
    print 'getting pubmed records from scratch'
    records={}
    for term in ontology.iterkeys():
    
        handle=Entrez.esearch(db='pubmed',term=ontology[term]['query'],retmax=100000)
        records[term] = Entrez.read(handle)
    
    pickle.dump(records,open('/Users/poldrack/data_unsynced/pubbrain/pubmed_search_records.pkl','wb'))


# map terms to each PMID

try:
    pmids=pickle.load(open('/Users/poldrack/data_unsynced/pubbrain/pubmed_ids_with_matches.pkl','rb'))
except:
    pmids={}
    for r in records:
        for id in records[r]['IdList']:
            if not pmids.has_key(id):
                pmids[id]=[]
            pmids[id].append(r)
            
    pickle.dump(pmids,open('/Users/poldrack/data_unsynced/pubbrain/pubmed_ids_with_matches.pkl','wb'))


