from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse
from django import forms
from django.db.models import Q
from colt.models import *
from colt.config import *
from colt.fasta import Fasta
import re

# 404
def my_custom_404_view(request):
    context = {'owner': 'Phosphatome.Net'}
    return render(request, 'colt/404.html', context)

# 500
def my_custom_error_view(request):
    context = {'owner': 'Phosphatome.Net'}
    return render(request, 'colt/500.html', context)

# Create your views here.
def index(request):
    context = {}
    return render(request, 'colt/index.html', context)


# about
def about(request):
    context = {}
    return render(request, 'colt/about.html', context)

# news & history
def news(request):
    context = {'owner': 'Kinase.com'}
    return render(request, 'colt/news.html', context)

# disclaimer
def disclaimer(request):
    context = {'owner': 'Kinase.com'}
    return render(request, 'colt/disclaimer.html', context)

# related sites
def related_sites(request):
    context = {'owner': 'Kinase.com'}
    return render(request, 'colt/related_sites.html', context)

# help with viewers
def help_with_viewers(request):
    context = {'owner': 'Kinase.com'}
    return render(request, 'colt/help_with_viewers.html', context)

# Form
class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)

# contact
def contact(request):
    context = {'owner': OWNER,
               'active_navbar_about_contact': True}
    if request.method == 'POST': # If the form has been submitted...
        # ContactForm was defined in the previous section
        form = ContactForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['manning@manninglab.org', 'chen.jinan@gene.com']
            subject2 = 'Kinase.com Feedback: ' + subject
            message2 = 'Sender: ' + sender + '\n\n' + 'Subject: ' +  subject + '\n\n' + message            
            if cc_myself:
                recipients.append(sender)
            from django.core.mail import send_mail
            send_mail(subject2, message2, sender, recipients)
            return redirect('colt:thanks') # Redirect after POST
        else:
            context['warning_msg'] = u"<strong>Form is invalid.</strong> "
    else:
        form = ContactForm() # An unbound form
    return render(request, 'colt/contact.html', context)

# contact thanks
def thanks(request):
    context = {'owner': OWNER,
               'active_navbar_about_contact': True}
    return render(request, 'colt/thanks.html', context)

# hypertree
def hypertree(request):
    context = {}
    return render(request, 'colt/hypertree.html', context)

# logo
def logos(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'logos', 
               'title': 'Kinase Logos', }
    return render(request, 'colt/iframe.html', context)

# logo aligner
def logo_aligner(request):
    context = {}
    return render(request, 'colt/test.html', context)

# classification
def classification(request):
    context = {}
    return render(request, 'colt/test.html', context)

# wiki
def wiki(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'wiki/index.php/Main_Page',
                'title': 'Kinase.com Wiki', }
    return render(request, 'colt/iframe.html', context)

# doc
def doc(request, doc_name):
    context = {'owner': OWNER,
               'active_navbar_doc': True}
    return render(request, 'colt/doc/' + doc_name + '.html', context)

# blast
def blast(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'blast/blast.html',
               'title': 'BLAST Kinases', }
    return render(request, 'colt/iframe.html', context)    

# kinomes
def human_kinome(request):
    context = {}
    return render(request, 'colt/kinome/human.html', context)

def human_kinome_phylogeny(request):
    context = {}
    return render(request, 'colt/kinome/human_phylogeny.html', context)

def human_kinome_psu(request):
    context = {}
    return render(request, 'colt/kinome/human_psu.html', context)

def mouse_kinome(request):
    context = {}
    return render(request, 'colt/kinome/mouse.html', context)

def mouse_kinome_comparison(request):
    context = {}
    return render(request, 'colt/kinome/mouse_kinome_comparison.html', context)

def urchin_kinome(request):
    context = {}
    return render(request, 'colt/kinome/urchin.html', context)

def drosophila_kinome(request):
    context = {}
    return render(request, 'colt/kinome/drosophila.html', context)

def celegans_kinome(request):
    #context = {}
    #return render(request, 'colt/kinome/celegans.html', context)
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'celegans', 
               'title': 'C. elegans Protein Kinases', }
    return render(request, 'colt/iframe.html', context)

def sponge_kinome(request):
    context = {}
    return render(request, 'colt/kinome/sponge.html', context)

def monosiga_kinome(request):
    #context = {}
    #return render(request, 'colt/kinome/monosiga.html', context)
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'monosiga', 
               'title': 'Tyrosine kinase signaling in the protist Monosiga' }
    return render(request, 'colt/iframe.html', context)

def scerevisiae_kinome(request):
    context = {}
    return render(request, 'colt/kinome/scerevisiae.html', context)

def fungi_coprinopsis_kinome(request):
    context = {}
    return render(request, 'colt/kinome/fungi_coprinopsis.html', context)

def dictyostelium_kinome(request):
    context = {}
    return render(request, 'colt/kinome/dictyostelium.html', context)

def tetrahymena_kinome(request):
    context = {}
    return render(request, 'colt/kinome/tetrahymena.html', context)

def giardia_kinome(request):
    context = {}
    return render(request, 'colt/kinome/giardia.html', context)

def microbial_kinome(request):
    context = {}
    return render(request, 'colt/kinome/giardia.html', context)

# bsk
def microbial_bsk(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'microbial/bsk/', 
               'title': 'The Bacterial Spore Kinases' }
    return render(request, 'colt/iframe.html', context)

# kinase evolution
def evolution(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'evolution', 
               'title': 'Protein Kinase Evolution' }
    return render(request, 'colt/iframe.html', context)

# pseudokinase
def pseudokinase(request):
    url = request.build_absolute_uri('/')
    context = { 'url': url + 'pseudokinase', 
               'title': 'The Life of a Dead Enzyme: Structure of the Pseudokinase VRK3' }
    return render(request, 'colt/iframe.html', context)

# kinbase form
# Form
class DbSearchForm(forms.Form):
    gene_name = forms.CharField()
    domain_name = forms.CharField()
    group_name = forms.CharField()
    family_name = forms.CharField()
    subfamily_name = forms.CharField()
    #species_name = forms.MultipleChoiceField(choices=[ (s.id, s.name) for s in KSpecies.objects.all()])

# kinbase database index + search
def kinbase(request, sep=','):
    context = {}
    all_species = KSpecies2.objects.all().order_by('order_index')
    context['species'] = all_species
    if request.method == 'POST': # If the form has been submitted...
        form = DbSearchForm(request.POST) # A form bound to the POST data
        flag = 0
        page_header = 'Search result'
        query_name = ''
        if request.POST.get("gene_name", ""):
            flag = 1
            query_name = request.POST.get("gene_name", "")
            #genes = get_list_or_404(KSearch.objects.filter(field='Name'), value=request.POST.get("gene_name", ""))
            genes = KSearch.objects.filter(field='Name', value=request.POST.get("gene_name", ""))
            gene_ids = list(set([ks.gene_id for ks in genes]))
        if request.POST.get("domain_name", ""):
            flag = 1
            query_name = request.POST.get("domain_name", "")
            #genes = get_list_or_404(KSearch.objects.filter(field='Domain'), value=request.POST.get("domain_name", ""))           
            genes = KSearch.objects.filter(field='Domain', value=request.POST.get("domain_name", "")) 
            gene_ids = list(set([ks.gene_id for ks in genes]))
        if request.POST.get("group_name", ""):
            flag = 1
            query_name = request.POST.get("group_name", "")
            #genes = get_list_or_404(KSearch.objects.filter(field='Group'), value=request.POST.get("group_name", ""))
            genes = KSearch.objects.filter(field='Group', value=request.POST.get("group_name", ""))
            gene_ids = list(set([ks.gene_id for ks in genes]))
        if request.POST.get("family_name", ""):
            flag = 1
            query_name = request.POST.get("family_name", "")
            #genes = get_list_or_404(KSearch.objects.filter(field='Family'), value=request.POST.get("family_name", ""))
            genes = KSearch.objects.filter(field='Family', value=request.POST.get("family_name", ""))
            gene_ids = list(set([ks.gene_id for ks in genes]))
        if request.POST.get("subfamily_name", ""):
            flag = 1
            query_name = request.POST.get("subfamily_name", "")
            #genes = get_list_or_404(KSearch.objects.filter(field='Subfamily'), value=request.POST.get("subfamily_name", ""))
            genes = KSearch.objects.filter(field='Subfamily', value=request.POST.get("subfamily_name", ""))
            gene_ids = list(set([ks.gene_id for ks in genes]))
        if not request.POST.getlist("species_name", ""):
            flag = 0            
        if flag == 1:
            if len(gene_ids) > 0:
                genes = Genes(gene_ids)
                species_id = request.POST.getlist("species_name", "")
                if not request.POST.has_key("pseudogene"): genes.remove_pseudogene()
                if len(species_id) != len(all_species): genes.filter_species(set(species_id))
                context['genes'] = genes.list()
                context['page_header'] = page_header
                #context['debug'] = str(set(species_id))
                return render(request, 'colt/kinbase/gene_list_search_result.html', context)
            else:
                if query_name:
                    genes = KSearch.objects.filter(Q(value=query_name) | Q(lcvalue=query_name))
                    suggestions = list(set([(ks.field, ks.value) for ks in genes]))
                    if suggestions:
                        context['suggestions'] = suggestions
                    else:
                        context['warning_msg'] = u"<strong>Sorry, There were no genes corresponding to this query, please try again.</strong> "
        else:
            context['warning_msg'] = u"<strong>Form is invalid.</strong> "
    else:
         form = DbSearchForm() # An unbound form
    context['form'] = form
    return render(request, 'colt/kinbase/index.html', context)

def kinbase_browser_species(request, species_id):
    species = get_object_or_404(KSpecies2, id=species_id)
    context = {'active_navbar_db_browser': True,
               'species_id': species_id,
               'species': species,
               'species_list': KSpecies2.objects.all().order_by('order_index')}   
    return render(request, 'colt/kinbase/browser-species.html', context)

def kinbase_gene_detail(request, id):
    gene0 = get_object_or_404(KGene, id=id)
    gene = Gene(id)
    gene.full()
    gene.pviz_for_domain()
    context = {'gene': gene,
               'show_group_gene_list': 1,
               'show_family_gene_list': 1,
               'use_pviz': 1,
               'color': Colors(),}
    return render(request, 'colt/kinbase/gene_detail.html', context)

def kinbase_sequence_fasta(request, id):
    sequence = KSeq.objects.get(id=id)
    seq = re.sub("(.{60})", "\\1\n", sequence.seq, 0, re.DOTALL)
    fasta = '>' + sequence.acc + '\n' + seq 
    return HttpResponse(fasta, content_type="text/plain")

def kinbase_search_field(request, field, value):
    genes = get_list_or_404(KSearch.objects.filter(field=field), value=value)
    gene_ids = list(set([ks.gene_id for ks in genes]))
    genes2 = Genes(gene_ids)
    genes2.remove_pseudogene()
    context = {'search_field': field,
               'search_value': value,
               'genes': genes2.list(),
               'is_class': False}
    if field == 'Group' or field == 'Family' or field == 'Subfamily':
        context['is_class'] = True
        klass = get_object_or_404(KClassHeirarchy.objects.filter(heirarchy=field), name=value)
        klass.full()
        context['klass'] = klass
        context['verbose'] = True
        #context['debug'] = str(klass.protein_hmm_png_sys)
    else:
        context['page_header'] = 'Search genes: ' + field + ' = "' + value + '"'
    return render(request, 'colt/kinbase/gene_list_search_result.html', context)

def kinbase_search_field_including_pseudogene(request, field, value):
    genes = get_list_or_404(KSearch.objects.filter(field=field), value=value)
    gene_ids = list(set([ks.gene_id for ks in genes]))
    context = {'search_field': field,
               'search_value': value,
               'genes': Genes(gene_ids).list(),
               'is_class': False}
    if field == 'Group' or field == 'Family' or field == 'Subfamily':
        context['is_class'] = True
        klass = get_object_or_404(KClassHeirarchy.objects.filter(heirarchy=field), name=value)
        klass.full()
        context['klass'] = klass
        context['verbose'] = True
        #context['debug'] = str(klass.protein_hmm_png_sys)
    else:
        context['page_header'] = 'Search genes: ' + field + ' = "' + value + '"'
    return render(request, 'colt/kinbase/gene_list_search_result.html', context)

def kinbase_klass_alignment(request, field, value, alntype):
    klass = get_object_or_404(KClassHeirarchy.objects.filter(heirarchy=field), name=value)
    klass.full()
    alignment = klass.get_alignment(alntype)
    alignment.aln_to_html()
    context = {'is_class': True,
               'klass': klass,
               'alignment': alignment,}
    return render(request, 'colt/kinbase/alignment.html', context)

def kinbase_process_sequence(request):
    service = request.POST.get('service')
    gene_ids = set(request.POST.getlist('gene_id', []))
    genes = Genes(gene_ids)
    if re.search(r'^Retrieve', service):
        if service == 'Retrieve Protein':
            seqtype = 'protein'
        elif service == 'Retrieve RNA':
            seqtype = 'RNA'
        elif service == 'Retrieve Kinase Domain':
            seqtype = 'kinase_domain'
        else:
            seqtype = 'protein'
        fasta = genes.fasta(seqtype)
        return HttpResponse(fasta, content_type="text/plain")
    elif service == 'View Domains':
        genes.prepare_pviz()
        pviz_json = genes.prepare_pviz_overall()
        context = {'genes': genes.genes,
                   'use_pviz': 1,
                   'color': Colors(),
                   'pviz_json': pviz_json,}
        return render(request, 'colt/kinbase/gene_domain_pviz.html', context)
    elif re.search(r'^Align', service):
        if service == 'Align Protein':
            seqtype = 'protein'
        elif service == 'Align RNA':
            seqtype = 'RNA'
        elif service == 'Align Kinase Domain':
            seqtype = 'kinase_domain'
        else:
            seqtype = 'protein'
        fasta = genes.muscle(seqtype)
        alignment = getattr(fasta, 'muscle_alignment')
        alignment.aln_to_html()
        context = {'alignment': alignment,}
        return render(request, 'colt/kinbase/alignment.html', context)
    return HttpResponse(result, content_type="text/plain")

def kinbase_retrieve_sequence(request, seqtype):
    fasta = str(request.POST)
    return HttpResponse(fasta, content_type="text/plain")

def other__aur_kinases(request):
    context = {}
    return render(request, 'colt/test.html', context)

# dev log
def dev_log(request):
    context = {}
    return render(request, 'colt/dev_log.html', context)
