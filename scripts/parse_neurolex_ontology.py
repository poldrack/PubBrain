"""
parse neurolex ontology
"""

ontology='NIF-GrossAnatomy.owl'

import ontosPy

onto=ontosPy.Ontology('NIF-GrossAnatomy.owl')

onto.printClassTree()

target_class='birnlex_1103'  # gyrus rectus
parent_class='birnlex_928' # prefrontal cortex - has gyrus rectus as proper part

c_targ=onto.classFind(target_class)[0]
c_parent=onto.classFind(parent_class)[0]

subs=onto.classAllSubs(c[1])

for i in range(len(subs)):
    s=subs[i]
    rep=onto.classRepresentation(s)
    name=rep['label'][0].toPython()
    if name.find('rectus')>-1:
        print i,name,rep
    tripledict={}
    for t in rep['alltriples']:
        tripledict[t[0]]=t[1]
    #print onto.propertyDirectSupers(rep['class'])