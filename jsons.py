import json
import os.path
import urllib2
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from colt.models import *
from colt.config import HMM_CUTOFF, PROJ_ROOT_URL, JSON_DIR


# index
def index(request):
    context = {}
    #return render(request, 'api/index.html', context)
    
def klass_tree(request):
    group_name = list(set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Group')]))
    kc = []
    for gn in group_name:
        gc = []
        for fn in set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Family', parent=gn)]):
            fc = [] # family children
            for sn in set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Subfamily', parent=fn)]):
                s = {'name': sn, 'size': 1, 'level': 'Subfamily'}
                fc.append(s)
            f = {'name': fn, 'size': len(fc), 'children': fc, 'level': 'Family'}
            gc.append(f)
        g = {'name': gn, 'size': len(gc), 'children': gc, 'level': 'Group'}
        kc.append(g)
    ktree = {'name': 'Phosphatase', 'size': len(kc), 'children': kc}
    return HttpResponse(json.dumps(ktree), content_type="application/json")

def get_url(k):
    if k['level'] != 'Gene':
        url = PROJ_ROOT_URL + 'kinbase/genes/' + k['level'] + '/' + k['name']
    else:
        url = PROJ_ROOT_URL + 'kinbase/gene/' + str(k['id'])
    return url    
    
def gene_tree(request, species_id, clean=False):
    json_file = JSON_DIR + 'd3tree-' + str(species_id) + '.json'
    if not clean and os.path.isfile(json_file):
        print "#LOG: read file " + json_file
        with open(json_file, 'r') as content_file:
            content = content_file.read()
        return HttpResponse(content, content_type="application/json")
    remove_empty = True
    field = 'SpeciesID'
    gene_id0 = list(set([c.gene_id for c in KSearch.objects.filter(field=field, value=species_id)]))
    genes2 = Genes(gene_id0)
    genes2.remove_pseudogene()
    gene_id = [g.id for g in genes2.list()]
    group_name = list(set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Group')]))
    kc = []
    for gn in group_name:
        gc = []
        gg = []
        for fn in set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Family', parent=gn)]):
            fc = [] # family children - subfamilies
            fg = [] # genes in the family
            for sn in set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Subfamily', parent=fn)]):
                sc = [] # subfamily children - genes
                for g1 in KGenotation.objects.filter(title="Subfamily", annotation=sn, gene_id__in=gene_id):
                    g10 = KGene.objects.get(id=g1.gene_id)
                    go = {'name': g10.name, 'size': 1, 'level': 'Gene', 'id': g1.gene_id}
                    go['url'] = get_url(go)
                    sc.append(go)
                s = {'name': sn, 
                     'size': len(sc),
                     'size0': len(sc), 
                     'children': sc, 
                     'level': 'Subfamily'}
                s['url'] = get_url(s)
                if remove_empty:
                    if s['size'] > 0: fc.append(s)
                else:
                    fc.append(s)
            for g2 in KGenotation.objects.filter(title="Family", annotation=fn, gene_id__in=gene_id):
                g20 = KGene.objects.get(id=g2.gene_id)
                fg.append({'name': g20.name, 'size': 1, 'level': 'Gene'})
            f = {'name': fn, 
                 'size': len(fg),
                 'size0': len(fc), 
                 'children': fc, 
                 'level': 'Family'}
            f['url'] = get_url(f)
            #print fn, str(len(fg))
            if remove_empty:
                if f['size'] > 0: gc.append(f)
            else:
                gc.append(f)            
        for g3 in KGenotation.objects.filter(title="Group", annotation=gn, gene_id__in=gene_id):
            g30 = KGene.objects.get(id=g3.gene_id)
            gg.append({'name': g30.name, 'size': 1, 'level': 'Gene'})
        g = {'name': gn, 
             'size': len(gg),
             'size0': len(gc), 
             'children': gc, 
             'level': 'Group'}
        g['url'] = get_url(g)
        if remove_empty:
            if g['size'] > 0: kc.append(g)
        else:
            kc.append(g)
    ktree = {'name': 'Kinome', 
             'size': len(gene_id),
             'size0': len(kc), 
             'children': kc,
             'level': ''}
    content = json.dumps(ktree, indent=2, separators=(',', ': '))
    print "#LOG: write file " + json_file
    with open(json_file, 'w') as content_file:
        content_file.write(content)
    return HttpResponse(content, content_type="application/json")

def search_autocomplete(request):
    gene_name = list(set([g.value for g in KSearch.objects.filter(field='Name')]))
    domain_name = list(set([g.value for g in KSearch.objects.filter(field='Domain')]))
    group_name = list(set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Group')]))
    family_name = list(set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Family')]))
    subfamily_name = list(set([c.name for c in KClassHeirarchy.objects.filter(heirarchy='Subfamily')]))
    #group_name = list(set([g.value for g in KSearch.objects.filter(field='Group')]))
    #family_name = list(set([g.value for g in KSearch.objects.filter(field='Family')]))
    #subfamily_name = list(set([g.value for g in KSearch.objects.filter(field='Subfamily')]))
    context = {'gene_name': gene_name,
               'domain_name': domain_name, 
               'group_name': group_name,  
               'family_name': family_name,
               'subfamily_name': subfamily_name}
    return HttpResponse(json.dumps(context), content_type="application/json")

def sequence_domains(request, id):
    sequence = Sequence(id)
    sequence.full()
    features = []
    i = 0
    best_hit_kinase_index = 0
    best_hit_kinase_score = 0
    for cd in sequence.collapse_domains:
        cdtype = cd.domain_group if cd.domain_group else 'bar'
        f = {'category': 'Summary', 
             'type': cdtype, 
             'start': cd.start, 
             'end': cd.end, 
             'text' : cd.display_name + ': ' + str(cd.score)}
        features.append(f)
        i = i + 1
    context = {'sequence': sequence.basic.seq,
               'features': features,
               'isoform_id': sequence.basic.acc,}
    return HttpResponse(json.dumps(context), content_type="application/json")

def sequence_domains_full(request, id):
    sequence = Sequence(id)
    sequence.full()
    features = []
    i = 0
    best_hit_kinase_index = 0
    best_hit_kinase_score = 0
    for cd in sequence.collapse_domains:
        cdtype = cd.domain_group if cd.domain_group else 'bar'
        f = {'category': 'Summary', 
             'type': cdtype, 
             'start': cd.start, 
             'end': cd.end, 
             'text' : cd.display_name + ': ' + str(cd.score)}
        features.append(f)
        i = i + 1
    for d in sequence.domains:
        dtype = d.domain_group if d.domain_group else 'bar'
        f = {'category': 'Details', 
             'type': dtype, 
             'start': d.start, 
             'end': d.end, 
             'text' : d.display_name + ': ' + str(d.score)}
        features.append(f)
        if dtype == 'kinase' and best_hit_kinase_score < d.score:
            best_hit_kinase_score = d.score
            best_hit_kinase_index = i
        i = i + 1 
    features[best_hit_kinase_index]['type'] = 'best_hit_kinase'
    context = {'sequence': sequence.basic.seq,
               'features': features,
               'isoform_id': sequence.basic.acc,}
    return HttpResponse(json.dumps(context), content_type="application/json")
    

# def gene_domain(request, id):
#     gene = Gene(id)
#     gene.full()
#     protein_sequence = gene.sequence['protein'][0].seq
#         #isoform_id = urllib2.unquote(isoform_id).decode('utf8')
#     isoform = get_object_or_404(Isoform, isoform_id=isoform_id)
#     target_domain = get_list_or_404(PhosphataseDomain, primary_isoform_id=isoform_id)
#     features = []
#     for d in target_domain:
#         hmm = get_object_or_404(HMM, hmm_name=d.hmm_name) 
#         f = {'category': 'Phosphatase domain', 'type': 'bar', 'start': d.hit_from, 'end': d.hit_to, 'text' : hmm.name + ' (' + str(d.hmm_from) + '-' + str(d.hmm_to) + '): ' + str(d.evalue)}
#         #f = {'category': 'Phosphatase domain', 'type': 'bar', 'start': d.hit_from, 'end': d.hit_to, 'text' : hmm.superfamily + ': ' +  hmm.name + ' (' + str(d.hmm_from) + '-' + str(d.hmm_to) + ')'}
#         features.append(f)
#     context = {'sequence': isoform.peptide_sequence,
#                'features': features,
#                'isoform_id': isoform_id}
#     return HttpResponse(json.dumps(context), content_type="application/json")
#     context = {''}
