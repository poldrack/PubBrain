"""
given a set of anatomical labels, create an MNI image with those regions
"""

import cPickle
termvox_keys=cPickle.load(open('term_voxkeys.cpkl','rb'))
import nibabel,numpy

regions=['Forceps minor','Brain Stem','Lingual Gyrus','Lingual Gyrus','Lingual Gyrus']
outfile='tmp.nii.gz'
example_img=nibabel.load('/Applications/fmri_progs/fsl/data/atlases/Cerebellum-MNIflirt-maxprob-thr25-3mm.nii.gz')

data=numpy.zeros((60,72,60))
for region in regions:
    if termvox_keys.has_key(region):
        print 'adding',region
        data[termvox_keys[region]]+=1

img=nibabel.Nifti1Image(data,affine=example_img.get_affine())
img.to_filename(outfile)