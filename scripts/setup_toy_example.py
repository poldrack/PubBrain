"""
script to set up toy example
"""


import django
django.setup()

from pubbrain_app import models
from PubBrain.utils import *

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

    
try:
    foo=models.BrainRegion.objects.get(name='Inferior frontal gyrus')
except:
    print 'setting up toy brainregion database'
    foo=models.BrainRegion.create('Inferior frontal gyrus')
    foo.query='"inferior frontal gyrus"[tiab]'
    foo.is_atlasregion=True
    foo.save()
    foo.atlasregions.add(foo)

try:
    foo=models.BrainRegion.objects.get(name='Middle frontal gyrus')
except:
    print 'setting up toy brainregion database'
    foo=models.BrainRegion.create('Middle frontal gyrus')
    foo.query='"Middle frontal gyrus"[tiab]'
    foo.is_atlasregion=True
    foo.save()
    foo.atlasregions.add(foo)

try:
    foo=models.BrainRegion.objects.get(name='Prefrontal cortex')
except:
    print 'setting up toy brainregion database'
    foo=models.BrainRegion.create('Prefrontal cortex')
    foo.query='"Prefrontal cortex"[tiab]'
    foo.is_atlasregion=False
    foo.save()
    foo.children.add(models.BrainRegion.objects.get(name='Middle frontal gyrus'))
    foo.children.add(models.BrainRegion.objects.get(name='Inferior frontal gyrus'))

print 'doing toy pubmed search'

#execfile('scripts/index_pubmed.py')

# use the outputs from mk_combined_atlas.py
# generate a toy atlas dictionary
f=open('scripts/atlas_to_ontology_dict.txt','w')
f.write('hippocampus\thippocampus\n')
f.write('inferior frontal gyrus\tinferior frontal gyrus\n')
f.write('middle frontal gyrus\tmiddle frontal gyrus\n')
f.close()


# use the toy dictionary to add voxel mappings for atlas regions to db
#execfile('scripts/link_atlasRegions_to_brainRegions.py')

srch=models.PubmedSearch.create('hippocampus')
srch.save()
srch.pubmed_ids.add(models.Pmid.objects.get(pubmed_id='25244639'))
srch.pubmed_ids.add(models.Pmid.objects.get(pubmed_id='25244085'))
srch.pubmed_ids.add(models.Pmid.objects.get(pubmed_id='14497900'))
srch.pubmed_ids.add(models.Pmid.objects.get(pubmed_id='22511924'))
