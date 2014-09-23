"""
perform query and get all matching anatomical terms
"""


from Bio import Entrez
import pickle
import nibabel

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key = seq.__getitem__)

def get_pubmed_query_results(query,entrez_email='poldrack@stanford.edu',retmax=20000):
    print 'searching for',query
    Entrez.email=entrez_email
    handle=Entrez.esearch(db='pubmed',term=query,retmax=retmax)
    record = Entrez.read(handle)
    return record
  
    
def get_pmids_with_anatomy(recordlist):
    print 'loading pmid library'
    pmids=pickle.load(open('/Users/poldrack/data_unsynced/pubbrain/pubmed_ids_with_matches.pkl','rb'))
 
    match_pmids=list(set(pmids.keys()).intersection(recordlist))
    return match_pmids

def get_query_matches(query,mk_image=False):
    assert len(query)>0
        
    # TBD: in the end we want to cache these results, and only search if the cached result
    # doesn't exist
    
    record = get_pubmed_query_results(query)
     
    # for id in record['IdList']:
    #     pm=Entrez.esummary(db='pubmed',id=id)
    #     rec=Entrez.read(pm)
    #     for r in rec:
    #         query_pmids.append(r['Id'])
    #         print r['Id'],r['Title']
    
    match_pmids=get_pmids_with_anatomy(record['IdList'])
    
    anat_terms=[]
    for m in match_pmids:
        for i in pmids[m]:
            anat_terms.append(i)
    
    anat_term_set=list(set(anat_terms))
    matchnums={}
    for j in anat_terms:
        matchnums[j]=0
    for i in range(len(anat_term_set)):
        for j in anat_terms:
            if j==anat_term_set[i]:
                matchnums[j]+=1
                
    term_voxkeys=pickle.load(open('term_voxkeys.cpkl','rb'))
        
    fullhierarchy=pickle.load(open('pubbrain_hierarchy.pkl'))
    results={}
    results['query']=query
    results['listing']=[]
    for w in sorted(matchnums,key=matchnums.get,reverse=True):
             results['listing'].append([w,matchnums[w]])
                                      
    if mk_image:
        img=numpy.zeros((60,72,60))
        for w in sorted(matchnums,key=matchnums.get,reverse=True):
            for at in fullhierarchy[w]['atlasterm']:
                img[term_voxkeys[at]]+=matchnums[w]
            print w,matchnums[w]
            
        affine=numpy.array([[  -3.,    0.,    0.,   90.],
               [   0.,    3.,    0., -126.],
               [   0.,    0.,    3.,  -72.],
               [   0.,    0.,    0.,    1.]])
        img_nii=nibabel.Nifti1Image(img,affine=affine)
        img_nii.to_filename('test_output_%s.nii.gz'%query.replace(' ','_'))
        
    return results
