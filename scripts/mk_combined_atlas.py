"""
combine across atlases and across regions within atlases
to create composite atlas for pubbrain
"""

import nibabel
import xml.etree.ElementTree as ET
import numpy
import os

def mk_3mm_atlas(infile,outfile):
    import run_shell_cmd
    cmd='/Applications/fmri_progs/fsl/bin/fslcreatehd 60 72 60 1 3 3 3 1 0 0 0 2  tmp_hdr.nii.gz'
    run_shell_cmd.run_shell_cmd(cmd)
    cmd='/Applications/fmri_progs/fsl/bin/flirt -in %s -applyxfm -init /Applications/fmri_progs/fsl/etc/flirtsch/ident.mat -out %s -paddingsize 0.0 -interp nearestneighbour -ref tmp_hdr.nii.gz'%(infile,outfile)
    run_shell_cmd.run_shell_cmd(cmd)


# start with cortical atlas

tree = ET.parse('/Applications/fmri_progs/fsl/data/atlases/HarvardOxford-Cortical.xml')
root = tree.getroot()


combined={}
combined['Inferior Frontal Gyrus']=[4,5]
combined['Superior Temporal Gyrus']=[8,9]
combined['Middle Temporal Gyrus']=[10,11,12]
combined['Inferior Temporal Gyrus']=[13,14,15]
combined['Supramarginal Gyrus']=[18,19]
combined['Lateral Occipital Cortex']=[21,22]
combined['Cingulate Gyrus']=[28,29]
combined['Parahippocampal Gyrus']=[33,34]
combined['Temporal Fusiform Cortex']=[36,37]

all_combined_keys=[]
for c in combined.iterkeys():
    for i in combined[c]:
        all_combined_keys.append(i)

image_values={}
for i in range(len(root[1])):
    idx=int(root[1][i].attrib['index'])
    name=root[1][i].text.split('(')[0].replace("'",'').rstrip(' ').lower()
    if name.find('juxtapositional')==0:
        name='supplementary motor area'
    if idx in all_combined_keys:
        combined_key=name.split(',')[0]
        if not image_values.has_key(combined_key):
            image_values[combined_key]=[]
        image_values[combined_key].append(idx+1)
    else:
        image_values[name]=[idx+1]
    print idx,name


def combine_voxels(set1,set2):
    """
    combine two tuples of coordinates from numpy.where
    """
    tmp=numpy.zeros((60,72,60))
    tmp[set1]=1
    tmp[set2]=1
    return numpy.where(tmp>0)


# use 3mm version of maxprob atlas
# created using: /Applications/fmri_progs/fsl/bin/fslcreatehd 60 72 60 1 3 3 3 1 0 0 0 2  HarvardOxford-cort-maxprob-thr25-3mm.nii.gz_tmp.nii.gz ; /Applications/fmri_progs/fsl/bin/flirt -in /Applications/fmri_progs/fsl/data/atlases/HarvardOxford/HarvardOxford-cort-maxprob-thr25-2mm.nii.gz -applyxfm -init /Applications/fmri_progs/fsl/etc/flirtsch/ident.mat -out HarvardOxford-cort-maxprob-thr25-3mm.nii.gz -paddingsize 0.0 -interp nearestneighbour -ref HarvardOxford-cort-maxprob-thr25-3mm.nii.gz_tmp

atlas=nibabel.load('/Applications/fmri_progs/fsl/data/atlases/HarvardOxford-cort-maxprob-thr25-3mm.nii.gz')
atlas_data=atlas.get_data()
term_voxkeys={}
for k in image_values.keys():
    if len(image_values[k])==1:
        term_voxkeys[k]=numpy.where(atlas_data==image_values[k])
    else:
        print image_values[k]
        tmp=[]
        for i in image_values[k]:
            if not tmp==[]:
                tmp=combine_voxels(tmp, numpy.where(atlas_data==i))
            else:
                tmp=numpy.where(atlas_data==i)
        term_voxkeys[k]=tmp


# do subcortical
# set up combinations by hand

sc_atlasfile='/Applications/fmri_progs/fsl/data/atlases/HarvardOxford-sub-maxprob-thr25-3mm.nii.gz'
if not os.path.exists(sc_atlasfile):
    mk_3mm_atlas('/Applications/fmri_progs/fsl/data/atlases/HarvardOxford/HarvardOxford-sub-maxprob-thr25-2mm.nii.gz',sc_atlasfile)
sc_atlas=nibabel.load(sc_atlasfile)
sc_atlas_data=sc_atlas.get_data()

subcort_regions={}
subcort_regions['nucleus accumbens']=[21,11]
subcort_regions['caudate']=[5,16]
subcort_regions['putamen']=[6,17]
subcort_regions['globus pallidus']=[7,18]
subcort_regions['hippocampus']=[9,19]
subcort_regions['thalamus']=[4,15]
subcort_regions['brain stem']=[8]

subcort_regions['amygdala']=[10,20]

for k in subcort_regions.iterkeys():
    tmp=[]
    for i in subcort_regions[k]:
        if not tmp==[]:
                tmp=combine_voxels(tmp, numpy.where(sc_atlas_data==i))
        else:
                tmp=numpy.where(sc_atlas_data==i)
        term_voxkeys[k]=tmp
        
print tmp


# load STN atlas and combine L/R
stn_atlasfile='/Applications/fmri_progs/fsl/data/atlases/STN-maxprob-thr25-3mm.nii.gz'
if not os.path.exists(stn_atlasfile):
    mk_3mm_atlas('/Applications/fmri_progs/fsl/data/atlases/STN/STN-maxprob-thr25-0.5mm.nii.gz',stn_atlasfile)
stn_atlas=nibabel.load(stn_atlasfile)   
stn_atlas_data=stn_atlas.get_data()
term_voxkeys['subthalamic nucleus']=numpy.where(stn_atlas_data>0)


# load tract atlas, combine L/R
#NOTE: labeling here is different, not from zero like others
dti_atlasfile='/Applications/fmri_progs/fsl/data/atlases/JHU-ICBM-labels-3mm.nii.gz'
if not os.path.exists(dti_atlasfile):
    mk_3mm_atlas('/Applications/fmri_progs/fsl/data/atlases/JHU/JHU-ICBM-labels-2mm.nii.gz',dti_atlasfile)
dti_atlas=nibabel.load(dti_atlasfile)
dti_atlas_data=dti_atlas.get_data()

tree = ET.parse('/Applications/fmri_progs/fsl/data/atlases/JHU-labels.xml')
root = tree.getroot()


image_values={}
for i in range(len(root[1])):
    idx=int(root[1][i].attrib['index'])
    name=root[1][i].text.rstrip(' R').rstrip(' L').split(' (')[0].lower()
    print idx,name
    if not image_values.has_key(name):
        image_values[name]=[idx]    
    else:
        image_values[name].append([idx])

for k in image_values.keys():
        print k
        print image_values[k]
        tmp=[]
        for i in image_values[k]:
            try:
                tmp=combine_voxels(tmp, numpy.where(dti_atlas_data==i))
            except:
                tmp=numpy.where(dti_atlas_data==i)
        term_voxkeys[k]=tmp


# load subset of regions from Juelich atlas
# this uses the numbers from the XML index, not from the image
Juelich_regions_to_combine={'amygdala_centromedial':[6,7],'amygdala_laterobasal':[8,9],'amygdala_superficial':[10,11],'brocas area':[12,13,14,15],
                            'entorhinal cortex':[18,19],'dentate gyrus':[20,21],'subiculum':[24,25],'LGN':[102,103],'MGN':[105,106],
                            'mammilary body':[104],'acoustic radiation':[92,93],'corticospinal tract':[97,98],
                            'inferior fronto-occipital fasciculus':[100,101],'optic radiation':[107,108]}

# TBD


# load cbl atlas
cbl_atlasfile='/Applications/fmri_progs/fsl/data/atlases/Cerebellum-MNIflirt-maxprob-thr25-3mm.nii.gz'
if not os.path.exists(cbl_atlasfile):
    mk_3mm_atlas('/Applications/fmri_progs/fsl/data/atlases/Cerebellum/Cerebellum-MNIflirt-maxprob-thr25-2mm.nii.gz',cbl_atlasfile)
cbl_atlas=nibabel.load(cbl_atlasfile)
cbl_atlas_data=cbl_atlas.get_data()

term_voxkeys['cerebellum']=numpy.where(cbl_atlas_data>0)


import cPickle
cPickle.dump(term_voxkeys,open('term_voxkeys.cpkl','wb'))

