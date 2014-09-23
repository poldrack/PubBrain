"""
convert orginal ontology to YAML
make two files:
- one that just contains the hierarchy
- another that just contains the mappings from ontology terms to search queries


"""

import pickle
from run_shell_cmd import run_shell_cmd
from matplotlib.cbook import flatten

# fix the ontology for mac
run_shell_cmd("cat PubBrainOntology.txt | tr '\r' '\n' > PubbrainOntology_fixed.txt")


# first need to run mk_combined_atlas.py to generate atlas terms

term_voxkeys=pickle.load(open('term_voxkeys.cpkl','rb'))
lower_term_voxkeys=[i.lower() for i in term_voxkeys.keys()]


f = open('PubbrainOntology_fixed.txt')
lines=f.readlines()
f.close()

# find indention level of each line
level=[]
tree={}
ctr=0
fullhierarchy={}
current=[]
searchdict={}
atlasterms={}
parents=[None]

prevctr=0

for linenum in range(len(lines)):
    l=lines[linenum]
    prevctr=ctr
    ctr=0
    for i in l.split('"')[0]:
        if i=='\t':
            ctr+=1
    level.append(ctr)
    
        
    # get the term and query
    
    lstrip=l.strip().split('\t')[0]
    l_s=lstrip.split(':')
    term=l_s[0].lstrip(' ').rstrip(' ').lower().replace('"','')
    query=l_s[1].lower()
    searchdict[term]=query
    if sum([1 for i in l.strip().split('\t') if len(i)>0]) > 1:
        srchterm=l.strip().split('\t')[-1].lower()
        if srchterm in lower_term_voxkeys:
            atlasterms[term]=srchterm
        else:
            print 'unmatched atlas term:',srchterm
        
    if ctr<prevctr:
        for x in range(prevctr-ctr):
            parents.pop()
    elif ctr>prevctr:
        parents.append(prevterm)
    #print ctr,prevctr,term,parents
    
    prevterm=term
    # put into full hierarchy
    if ctr==0:
        # highest level
        
        fullhierarchy[term]={'query':query,'parent':None,'children':[]}
        
    else: # child of previous
        
        fullhierarchy[term]={'query':query,'parent':parents[-1],'children':[]}
        
    #print ctr,term,'parent:',fullhierarchy[term]['parent']
    #print current
    #print term,query,fullhierarchy[term]

for i in fullhierarchy.keys():
    parent=fullhierarchy[i]['parent']
    if not parent==None:
        fullhierarchy[parent]['children'].append(i)
    if atlasterms.has_key(i):
        fullhierarchy[i]['atlasterm']=[atlasterms[i]]

# find sets of atlas terms for parents without terms
# by combining across children

def findChildrenWithAtlasTerms(name,fullhierarchy):
    atlasterms=[]
    print 'checking',name
    if fullhierarchy[name].has_key('children'):
        for child in fullhierarchy[name]['children']:
            if fullhierarchy[child].has_key('atlasterm'):
                atlasterms.append(fullhierarchy[child]['atlasterm'])
                print 'found',atlasterms
            else:
                print 'drilling down:',child
                at=findChildrenWithAtlasTerms(child,fullhierarchy)
                atlasterms.append(at)
                
    return list(flatten(atlasterms))

for i in fullhierarchy.keys():
    if not fullhierarchy[i].has_key('atlasterm'):
        # look for children with atlas terms
        #print i,fullhierarchy[i]['children']
        fullhierarchy[i]['atlasterm']=findChildrenWithAtlasTerms(i,fullhierarchy)
            

# find atlas terms for items from parents
for i in fullhierarchy.keys():
    if not fullhierarchy[i].has_key('atlasterm'):
        # find nearest parent with atlas term
        term_not_found=True
        parent=fullhierarchy[i]['parent']
        while term_not_found:
            if parent==None:
                term_not_found=False
                break
            if fullhierarchy[parent].has_key('atlasterm'):
                fullhierarchy[i]['atlasterm']=fullhierarchy[parent]['atlasterm']
                term_not_found=False
            else:
                parent=fullhierarchy[parent]['parent']


    
pickle.dump(fullhierarchy,open('pubbrain_hierarchy.pkl','w'))

