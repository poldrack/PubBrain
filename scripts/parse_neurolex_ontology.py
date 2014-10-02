"""
parse neurolex ontology
"""

ontology='pubbrain_app/static/data/result_fixed.txt'
f=open(ontology)
lines=[i.strip().split('\t') for i in f.readlines()]
f.close()

terms={}
for line in lines:
    name=line[0].replace(':Category:','').lower().replace(' ','_')
    try:
        id=line[1]
    except:
        print 'no id:',line
        continue
    try:
        parent=line[3].replace(':Category:','').lower().replace(' ','_')
    except:
        print 'no parent:',line
    try:
        assert not terms.has_key(id)
    except:
        print 'dupe key:',line
    terms[id]={}
    terms[id]['name']=name
    
    
    
