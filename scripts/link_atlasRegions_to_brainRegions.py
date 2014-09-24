"""
load the atlas voxels and the mapping from atlas to ontology regions
and save to database
"""

import django
django.setup()

from pubbrain_app import models
import cPickle


# mapping from atlas terms to voxels
term_voxkeys=cPickle.load(open('scripts/term_voxkeys.cpkl','rb'))

# mapping from ontology terms to atlas terms
f=open('scripts/atlas_to_ontology_dict.txt')
atlas_to_ontology_dict={}
ontology_to_atlas_dict={}
for l in f.readlines():
    l_s=l.strip().split('\t')
    atlas_to_ontology_dict[l_s[0]]=l_s[1]
    ontology_to_atlas_dict[l_s[1]]=l_s[0]
f.close()


for brainRegion in models.BrainRegion.objects.all():
    print brainRegion.name
    if not ontology_to_atlas_dict.has_key(brainRegion.name.lower()):
        print 'skipping missing ontology key:',brainRegion.name.lower()
        continue
    brainRegion.atlas_voxels=cPickle.dumps(term_voxkeys[brainRegion.name.lower()])
    brainRegion.save()
    