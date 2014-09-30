from django.shortcuts import render
from django.http import HttpResponse
from PubBrain.utils import *
from django.template import RequestContext, loader

class anatomyCount():
    name=''
    count=-1
    def __init__(self,name,count,regionalPmids):
        self.name=name
        self.count=count
        self.name_query=name.replace(" ","+")
        self.regionalPmids='+OR+'.join(regionalPmids)

def sortDict(dict):
    " return set of dict keys sorted based on values"
    keys=dict.keys()
    values=[dict[key] for key in keys]
    sorted_values=sorted(range(len(values)), key = values.__getitem__)[::-1]
    return [keys[k] for k in sorted_values]

# Create your views here.
def index(request):
    query='hippocampus'
    q=get_pubmed_query_results(query)
    m=get_matching_pmids(q)
        
    c,regionalPmids=get_anatomy_count(m)
    imgfile=mk_image_from_anatomy_count(c,query)
    regions=[]
    anatkeys=sortDict(c)
    for region in anatkeys:
        regions.append(anatomyCount(region,c[region],regionalPmids[region]))
    template=loader.get_template('pubbrain_app/index.html')
    context=RequestContext(request,{'query_results':regions,'query':query,
                                    'img_max':max(c.values()),'file_name':'%s'%imgfile})
    return HttpResponse(template.render(context))
    #return HttpResponse('Welcome to PubBrain')




