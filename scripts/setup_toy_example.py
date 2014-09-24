"""
script to set up toy example
"""


import django
django.setup()

from pubbrain_app import models

# set up toy DB

try:
    foo=models.BrainRegion.objects.get(name='Hippocampus')
except:
    print 'setting up toy brainregion database'
    foo=models.BrainRegion.create('Hippocampus')
    foo.query='"Hippocampus"[tiab]'
    foo.is_atlasregion=True
    foo.save()

foo.atlasregions.add(foo)

print 'doing toy pubmed search'

execfile('scripts/index_pubmed.py')

# use the outputs from mk_combined_atlas.py
# generate a toy atlas dictionary
f=open('scripts/atlas_to_ontology_dict.txt','w')
f.write('hippocampus\thippocampus\n')
f.close()



