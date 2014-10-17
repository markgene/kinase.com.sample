from django.conf.urls import patterns, url
from colt import views
from colt import jsons

#handler404 = 'colt.views.my404'

urlpatterns = patterns('',
    url(r'^$', views.index, name="index"),
    
    url(r'^about/$', views.about, name="about"),
    url(r'^about/disclaimer/$', views.disclaimer, name="disclaimer"),
    url(r'^about/news/$', views.news, name="news"),
    url(r'^about/related-sites/$', views.related_sites, name="related_sites"),
    url(r'^about/help-with-viewers/$', views.help_with_viewers, name="help_with_viewers"),
    url(r'^about/contact/$', views.contact, name="contact"),
    url(r'^about/thanks/$', views.thanks, name="thanks"),
    
    url(r'^logos/$', views.logos, name="logos"),
    url(r'^logo-aligner/$', views.logo_aligner, name="logo_aligner"),  
    url(r'^classification/$', views.classification, name="classification"),
    url(r'^hypertree/$', views.hypertree, name="hypertree"),
    url(r'^wiki/$', views.wiki, name="wiki"), 
    url(r'^blast/$', views.blast, name="blast"),
    url(r'^doc/(?P<doc_name>.+)/$', views.doc, name="doc"),
    
    url(r'^human/$', views.human_kinome, name="human_kinome"),
    url(r'^human/phylogeny/$', views.human_kinome_phylogeny, name="human_kinome_phylogeny"),
    url(r'^human/psu/$', views.human_kinome_psu, name="human_kinome_psu"),
    url(r'^mouse/$', views.mouse_kinome, name="mouse_kinome"),
    url(r'^mouse/comparison/$', views.mouse_kinome_comparison, name="mouse_kinome_comparison"),
    url(r'^urchin/$', views.urchin_kinome, name="urchin_kinome"),
    url(r'^drosophila/$', views.drosophila_kinome, name="drosophila_kinome"),
    url(r'^celegans/$', views.celegans_kinome, name="celegans_kinome"),    
    url(r'^sponge/$', views.sponge_kinome, name="sponge_kinome"),
    url(r'^monosiga/$', views.monosiga_kinome, name="monosiga_kinome"),
    url(r'^scerevisiae/$', views.scerevisiae_kinome, name="scerevisiae_kinome"),
    url(r'^fungi/coprinopsis/$', views.fungi_coprinopsis_kinome, name="fungi_coprinopsis_kinome"),
    url(r'^dictyostelium/$', views.dictyostelium_kinome, name="dictyostelium_kinome"),
    url(r'^tetrahymena/$', views.tetrahymena_kinome, name="tetrahymena_kinome"),
    url(r'^giardia/$', views.giardia_kinome, name="giardia_kinome"),
    url(r'^microbial/$', views.microbial_kinome, name="microbial_kinome"),
    url(r'^microbial/bsk/$', views.microbial_bsk, name="microbial_bsk"),
    
    url(r'^evolution/$', views.evolution, name="evolution"),    
    url(r'^pseudokinase/$', views.pseudokinase, name="pseudokinase"),  
    
    url(r'^kinbase/$', views.kinbase, name="kinbase"),
    url(r'^kinbase/browser/SpeciesID/(?P<species_id>\d+)$', views.kinbase_browser_species, name="kinbase_browser_species"),
    url(r'^kinbase/gene/(?P<id>.*)$', views.kinbase_gene_detail, name="kinbase_gene_detail"),
    url(r'^kinbase/gene-sequences/$', views.kinbase_process_sequence, name="kinbase_process_sequence"),
    url(r'^kinbase/gene-sequences/(?P<seqtype>protein|RNA|kinase_domain)/$', views.kinbase_retrieve_sequence, name="kinbase_retrieve_sequence"),
    #url(r'^kinbase/gene-sequences-alignment/(?P<seqtype>protein|RNA|kinase_domain)/$', views.kinbase_alignment, name="kinbase_alignment"),
    url(r'^kinbase/genes/(?P<field>Group|Family|Subfamily)/(?P<value>.*)/alignment/(?P<alntype>protein|domain)/view$', views.kinbase_klass_alignment, name="kinbase_klass_alignment"),
    url(r'^kinbase/genes/(?P<field>[A-Za-z0-9 ]*)/(?P<value>.*)/$', views.kinbase_search_field, name="kinbase_search_field"),
    url(r'^kinbase/genes-ips/(?P<field>[A-Za-z0-9 ]*)/(?P<value>.*)/$', views.kinbase_search_field_including_pseudogene, name="kinbase_search_field_including_pseudogene"),
    url(r'^kinbase/sequence/fasta/(?P<id>.*)/$', views.kinbase_sequence_fasta, name="kinbase_sequence_fasta"),
    
    url(r'^other/aur_kinases$', views.other__aur_kinases, name="other__aur_kinases"),
    url(r'^dev/log$', views.dev_log, name="dev_log"),
    url(r'^data/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': '/Users/bioinfo/Dropbox/workspace/web/kinase/kinase/colt/static/colt/data/', 'show_indexes': True}, name="static_directory",),
    
    url(r'^api/gene-tree/(?P<species_id>\d+)/$', jsons.gene_tree, name='api_gene_tree'),                   
    url(r'^api/search-autocomplete', jsons.search_autocomplete, name='api_search_autocomplete'),
    url(r'^api/sequence/(?P<id>[0-9]*)/domains/$', jsons.sequence_domains, name='api_sequence_domains'),
)

