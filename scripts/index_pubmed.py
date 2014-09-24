"""
index pubmed for anatomical ontology terms
"""

from Bio import Entrez
from Bio.Entrez import efetch, read
import pickle
Entrez.email='poldrack@stanford.edu'

import django
django.setup()
from pubbrain_app import models

#ontology=pickle.load(open('pubbrain_hierarchy.pkl'))


print 'getting pubmed records from scratch'
records={}

for brainRegion in models.BrainRegion.objects.all():
    print brainRegion.name,brainRegion.query
    handle=Entrez.esearch(db='pubmed',term=brainRegion.query,retmax=10)
    record = Entrez.read(handle)
    for id in record['IdList']:
        try:
            entry=models.Pmid.objects.get(pubmed_id=id)
        except:
            entry=models.Pmid.create(id)
            entry.save()
        entry.brain_regions_named.add(brainRegion)


