from django.db import models



# represents a brain region from the ontology   
class BrainRegion(models.Model):
    
    # name of the region - from the ontology
    name=models.CharField(max_length=100)
    
    # the pubmed query for the region
    query=models.CharField(max_length=255)
    
    # is this a native region in the atlas?
    is_atlasregion=models.BooleanField(default=False)
    
    # if so, save the voxels associated with the region (as a cPickle)
    atlas_voxels=models.TextField()
    
    # parent-child relations in the partonomy
    # a region can only have one parent but can have multiple children
    parent=models.ForeignKey('self', null=True, blank=True)
    children=models.ManyToManyField('self', null=True, blank=True)
    
    # a list of the atlas areas associated with this term
    # if is_atlasregion==True then this will be same as the name
    # in other cases, it may refer to a single parent
    # or to multiple children (e.g., "frontal lobe" is represented
    # by a number of specific parts of the frontal lobe in the atlas)
    atlasregions=models.ManyToManyField('self', null=True, blank=True)
    
    @classmethod
    def create(cls, name):
        region = cls(name=name)
        return region


# represents a PubMed ID

class Pmid(models.Model):
    pubmed_id=models.CharField(max_length=20)
    date_added=models.DateField(auto_now_add=True,auto_now=True)
    # link to the brain regions mentioned in the abstract
    brain_regions_named=models.ManyToManyField(BrainRegion)
    title=models.CharField(max_length=255,default='')
    
    @classmethod
    def create(cls, pmid):
        entry = cls(pubmed_id=pmid)
        return entry

