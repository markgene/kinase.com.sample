# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
import re, copy, random, json, os.path
from django.db import models
from colt.alignment import Alignment
from colt.fasta import Fasta

ROOT_DIR = '/Users/kp/workspace/web/kinase/'

class KAlias(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    gene_id = models.IntegerField(db_column='GENE_ID') # Field name made lowercase.
    symbol = models.CharField(db_column='SYMBOL', max_length=255, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True) # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=45, blank=True) # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_ALIAS'

class KAtt(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    seqid = models.IntegerField(db_column='SEQID', blank=True, null=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=255, blank=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=64, blank=True) # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=255, blank=True) # Field name made lowercase.
    class_field = models.CharField(db_column='CLASS', max_length=255, blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    astart = models.IntegerField(db_column='ASTART', blank=True, null=True) # Field name made lowercase.
    aend = models.IntegerField(db_column='AEND', blank=True, null=True) # Field name made lowercase.
    range = models.CharField(db_column='RANGE', max_length=255, blank=True) # Field name made lowercase.
    attsrcid = models.IntegerField(db_column='ATTSRCID', blank=True, null=True) # Field name made lowercase.
    score = models.FloatField(db_column='SCORE', blank=True, null=True) # Field name made lowercase.
    expectlog = models.FloatField(db_column='EXPECTLOG', blank=True, null=True) # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    araw = models.TextField(db_column='ARAW', blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_ATT'

class KAttSrc(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=64, blank=True) # Field name made lowercase.
    version = models.CharField(db_column='VERSION', max_length=16, blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    params = models.CharField(db_column='PARAMS', max_length=255, blank=True) # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, blank=True) # Field name made lowercase.
    seqdbfile = models.CharField(db_column='SEQDBFILE', max_length=255, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_ATT_SRC'

class KClassHeirarchy(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=64) # Field name made lowercase.
    heirarchy = models.CharField(db_column='HEIRARCHY', max_length=9, blank=True) # Field name made lowercase.
    parent = models.CharField(db_column='PARENT', max_length=64, blank=True) # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True) # Field name made lowercase.
    def full(self):
        self.get_parent_model()
        self.get_child_models()
        self.get_gain_loss_graph()
        self.get_protein_alignment()
        self.get_domain_alignment()
        self.get_phylogeny('protein')
        self.get_phylogeny('domain')
        self.get_hmm('KD', 'png')
        self.get_hmm('KD', 'hmm')
        self.get_hmm('protein', 'png')
        self.get_hmm('protein', 'hmm')
    def get_parent_model(self):
        if hasattr(self, 'parent_model'):
            return self.parent_model
        else:
            if not self.parent:
                self.parent_model = {}
            else:
                if self.heirarchy == 'Subfamily': 
                    parent_heirarchy = 'Family'
                elif self.heirarchy == 'Family':
                    parent_heirarchy = 'Group'
                self.parent_model = KClassHeirarchy.objects.get(name=self.parent, heirarchy=parent_heirarchy)
            return self.parent_model
    def get_child_models(self):
        if hasattr(self, 'child_models'):
            return self.child_models
        else:
            if self.heirarchy == 'Subfamily':
                self.child_models = []
            else:
                if self.heirarchy == 'Family': 
                    child_heirarchy = 'Subfamily'
                elif self.heirarchy == 'Group':
                    child_heirarchy = 'Family'
                self.child_models = KClassHeirarchy.objects.filter(parent=self.name, heirarchy=child_heirarchy)   
            return self.child_models 
    def get_gain_loss_graph(self):
        if hasattr(self, 'gain_loss_graph_filepath'):
            return self.gain_loss_graph_filepath
        file = '.'.join((self.heirarchy, self.name, 'png'))
        dir = 'colt/data/gainlossgraph/'
        path_in_template_html = dir + file
        path = ROOT_DIR + 'colt/static/' + path_in_template_html
        self.gain_loss_graph_filepath = path_in_template_html if os.path.isfile(path) else '' 
        return self.gain_loss_graph_filepath
    def get_alignment(self, alntype):
        if alntype == 'protein':
            return self.get_protein_alignment()
        elif alntype == 'domain':
            return self.get_domain_alignment()
        else:
            raise
    def get_protein_alignment(self):
        if hasattr(self, 'protein_alignment'):
            return self.protein_alignment
        file = '.'.join((self.heirarchy, 'protein', self.name, 'aln'))
        dir = 'colt/data/alntree/'
        path_in_template_html = dir + file
        path = ROOT_DIR + 'colt/static/' + path_in_template_html
        if os.path.isfile(path):
            self.protein_alignment_filepath = path_in_template_html
            self.protein_alignment = Alignment(path)
        else:
            self.protein_alignment_filepath = ''
            self.protein_alignment = Alignment('')
        return self.protein_alignment
    def get_domain_alignment(self):
        if hasattr(self, 'domain_alignment'):
            return self.domain_alignment
        file = '.'.join((self.heirarchy, 'domain', self.name, 'aln'))
        dir = 'colt/data/alntree/'
        path_in_template_html = dir + file
        path = ROOT_DIR + 'colt/static/' + path_in_template_html
        if os.path.isfile(path):
            self.domain_alignment_filepath = path_in_template_html
            self.domain_alignment = Alignment(path)
        else:
            self.domain_alignment_filepath = '' 
            self.domain_alignment = Alignment('')
        return self.domain_alignment
    def get_phylogeny(self, moltype):
        attr = moltype + '_phylogeny_filepath'
        if hasattr(self, attr):
            return getattr(self, attr)
        file = '.'.join((self.heirarchy, moltype, self.name, 'phy'))
        dir = 'colt/data/alntree/'
        path_in_template_html = dir + file
        path = ROOT_DIR + 'colt/static/' + path_in_template_html
        if os.path.isfile(path):
            setattr(self, attr, path_in_template_html)
        else:
            setattr(self, attr, '') 
        return getattr(self, attr)
    def get_hmm(self, moltype, filetype):
        attr = moltype + '_hmm_' +  filetype
        if hasattr(self, attr):
            return getattr(self, attr)
        file = '.'.join((self.heirarchy, self.name, moltype, filetype))
        dir = 'colt/data/kinbase/hmmlogos/'
        path_in_template_html = dir + file
        path = ROOT_DIR + 'colt/static/' + path_in_template_html
        if os.path.exists(path):
            setattr(self, attr, path_in_template_html)
        else:
            setattr(self, attr, '') 
        attr_sys = moltype + '_hmm_' +  filetype + '_sys'
        setattr(self, attr_sys, path)
        return getattr(self, attr)
    class Meta:
        managed = False
        db_table = 'K_CLASS_HEIRARCHY'

class KDomain(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    kattid = models.IntegerField(db_column='KATTID', blank=True, null=True) # Field name made lowercase.
    seqid = models.IntegerField(db_column='SEQID', blank=True, null=True) # Field name made lowercase.
    type = models.CharField(db_column='TYPE', max_length=255, blank=True) # Field name made lowercase.
    domainname = models.CharField(db_column='DOMAINNAME', max_length=255, blank=True) # Field name made lowercase.
    domainid = models.CharField(db_column='DOMAINID', max_length=255, blank=True) # Field name made lowercase.
    start = models.IntegerField(db_column='START', blank=True, null=True) # Field name made lowercase.
    end = models.IntegerField(db_column='END', blank=True, null=True) # Field name made lowercase.
    tstart = models.IntegerField(db_column='TSTART', blank=True, null=True) # Field name made lowercase.
    tend = models.IntegerField(db_column='TEND', blank=True, null=True) # Field name made lowercase.
    targetlength = models.IntegerField(db_column='TARGETLENGTH', blank=True, null=True) # Field name made lowercase.
    score = models.FloatField(db_column='SCORE', blank=True, null=True) # Field name made lowercase.
    expectlog = models.FloatField(db_column='EXPECTLOG', blank=True, null=True) # Field name made lowercase.
    queryaa = models.TextField(db_column='QUERYAA', blank=True) # Field name made lowercase.
    targetaa = models.TextField(db_column='TARGETAA', blank=True) # Field name made lowercase.
    comparison = models.TextField(db_column='COMPARISON', blank=True) # Field name made lowercase.
    def full(self):
        self.display_name()
        self.is_kinase()
        self.significance()
        self.profile_source()
        self.domain_group()
        self.get_alignment()
    def domain_group(self):
        if re.search(r'\.KD$', self.domainname):
            self.domain_group = 'kinase'
        else:
            self.domain_group = self.domainname
    def display_name(self):
        self.display_name = self.domainname
        if re.search(r'\.KD$', self.display_name):
            self.display_name = re.sub(r'^\w+\.(.*)\.KD$', r'\1', self.display_name)
    def is_kinase(self):
        if re.search(r'\.KD$', self.domainname):
            self.is_kinase = True     
        else:
            self.is_kinase = False
    def significance(self):
        self.significance = 10 ** (-self.expectlog)
    def profile_source(self):           
        if self.type == 'Pfam_fs':
            self.profile_source = 'Pfam'
        elif self.type == 'smart.hmm':
            self.profile_source = 'SMART'
        elif self.type == 'KD_all_classes':
            self.profile_source = 'In-house'
        else:
            self.profile_source = self.type
    def get_alignment(self):
        self.sequence_identity()
        aln = 'Range on Protein: ' + str(self.start) + '-' + str(self.end) + '\n'
        aln = aln + 'Range on HMM: ' + str(self.tstart) + '-' + str(self.tend) + '/' + str(self.targetlength) + '\n'
        aln = aln + 'Sequence Identity: ' + str(self.sequence_identity) + '% (' + str(self.identical_residues) + ' aa)\n\n'
        queryaa = re.sub("(.{100})", "\\1\n", self.queryaa, 0, re.DOTALL).split('\n')
        comparison = re.sub("(.{100})", "\\1\n", self.comparison, 0, re.DOTALL).split('\n')
        targetaa = re.sub("(.{100})", "\\1\n", self.targetaa, 0, re.DOTALL).split('\n')
        for i, qaa in enumerate(queryaa):
            aln = aln + qaa + '\n'
            aln = aln + comparison[i] + '\n'
            aln = aln + targetaa[i] + '\n\n'
        self.alignment = aln
    def sequence_identity(self):
        self.identical_residues = len(re.findall(r'\|', self.comparison))
        self.sequence_identity = int(float(self.identical_residues) / len(self.comparison) * 100)
    class Meta:
        managed = False
        db_table = 'K_DOMAIN'

class KDomainAlias(models.Model):
    name = models.CharField(db_column='NAME', max_length=64, blank=True) # Field name made lowercase.
    alias = models.CharField(db_column='ALIAS', max_length=64, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_DOMAIN_ALIAS'

class KGene(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255, blank=True) # Field name made lowercase.
    species_id = models.IntegerField(db_column='SPECIES_ID') # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    replaced_by = models.IntegerField(db_column='REPLACED_BY') # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_GENE'

class KGenotation(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    gene_id = models.IntegerField(db_column='GENE_ID') # Field name made lowercase.
    class_field = models.CharField(db_column='CLASS', max_length=45, blank=True) # Field name made lowercase. Field renamed because it was a Python reserved word.
    title = models.CharField(db_column='TITLE', max_length=34, blank=True) # Field name made lowercase.
    annotation = models.TextField(db_column='ANNOTATION') # Field name made lowercase.
    annotation2 = models.TextField(db_column='ANNOTATION2', blank=True) # Field name made lowercase.
    hyperlink = models.TextField(db_column='HYPERLINK', blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_GENOTATION'

class KMap(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    gene_id = models.IntegerField(db_column='GENE_ID') # Field name made lowercase.
    band = models.CharField(db_column='BAND', max_length=32, blank=True) # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=32, blank=True) # Field name made lowercase.
    source = models.CharField(db_column='SOURCE', max_length=64, blank=True) # Field name made lowercase.
    notes = models.TextField(db_column='NOTES', blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_MAP'

class KSearch(models.Model):
    gene_id = models.IntegerField(db_column='Gene_ID') # Field name made lowercase.
    field = models.CharField(db_column='FIELD', max_length=64, blank=True) # Field name made lowercase.
    value = models.CharField(db_column='VALUE', max_length=64, blank=True) # Field name made lowercase.
    lcvalue = models.CharField(db_column='LCVALUE', max_length=64, blank=True) # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_SEARCH'

class KSeq(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    gene_id = models.IntegerField(db_column='GENE_ID') # Field name made lowercase.
    acc = models.TextField(db_column='ACC') # Field name made lowercase.
    acc2 = models.TextField(db_column='ACC2', blank=True) # Field name made lowercase.
    description = models.TextField(db_column='DESCRIPTION', blank=True) # Field name made lowercase.
    seqtype = models.CharField(db_column='SEQTYPE', max_length=21, blank=True) # Field name made lowercase.
    length = models.IntegerField(db_column='LENGTH') # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    status = models.CharField(db_column='STATUS', max_length=64, blank=True) # Field name made lowercase.
    origin = models.CharField(db_column='ORIGIN', max_length=34, blank=True) # Field name made lowercase.
    dbname = models.CharField(db_column='DBNAME', max_length=32, blank=True) # Field name made lowercase.
    dbversion = models.CharField(db_column='DBVERSION', max_length=16, blank=True) # Field name made lowercase.
    seq = models.TextField(db_column='SEQ') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_SEQ'

class KSpecies(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255) # Field name made lowercase.
    latin = models.CharField(db_column='LATIN', max_length=255, blank=True) # Field name made lowercase.
    abbreviation = models.CharField(db_column='ABBREVIATION', max_length=2, blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    class Meta:
        managed = False
        db_table = 'K_SPECIES'

class KSpecies2(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True) # Field name made lowercase.
    name = models.CharField(db_column='NAME', max_length=255) # Field name made lowercase.
    latin = models.CharField(db_column='LATIN', max_length=255, blank=True) # Field name made lowercase.
    abbreviation = models.CharField(db_column='ABBREVIATION', max_length=2, blank=True) # Field name made lowercase.
    clock = models.DateTimeField(db_column='CLOCK') # Field name made lowercase.
    order_index = models.FloatField(unique=True, blank=True, null=True)
    is_used = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'K_SPECIES2'

class Sequence:
    def __init__(self, id):
        self.basic = KSeq.objects.get(id=id)
        self.get_domains()
    def full(self):
        self.group_domains()
        self.domains = sorted(self.domains, key=lambda d: (d.group_index, d.significance))
    def get_domains(self):
        self.domains = KDomain.objects.filter(seqid=self.basic.id).order_by('start', '-score')
        for d in self.domains:
            d.full()
        return self.domains
    def collapse_domains(self):
        cd = []
        for d in self.domains:
            if cd and cd[-1].end >= d.start - 1:
                if d.end > cd[-1].end: cd[-1].end = d.end
                if d.score > cd[-1].score: cd[-1].score = d.score
                if d.domain_group == 'kinase': 
                    cd[-1].domain_group = 'kinase'
                    cd[-1].display_name = 'Kinase'
            else:
                cd.append(copy.deepcopy(d)) 
        self.collapse_domains = cd 
    def group_domains(self):
        cd = []
        for d in self.domains:
            if cd and cd[-1].end >= d.start - 1:
                if d.end > cd[-1].end: cd[-1].end = d.end
                if d.score > cd[-1].score: cd[-1].score = d.score
                if d.domain_group == 'kinase': 
                    cd[-1].domain_group = 'kinase'
                    cd[-1].display_name = 'Kinase'
                if cd[-1].domain_group == 'kinase':
                    d.domain_group = 'kinase'
                d.group_index = len(cd) - 1      
            else:                                
                cd.append(copy.deepcopy(d))
                d.group_index = len(cd) - 1
        self.collapse_domains = cd


class Gene:
    def __init__(self, id):
        self.id = id
        self.simple()
    def simple(self):
        gene = KGene.objects.get(id=self.id)
        self.gene = gene     
        self.species = KSpecies2.objects.get(id=gene.species_id)
        self.group = KGenotation.objects.get(gene_id=self.id, title='Group').annotation
        try:
            self.family = KGenotation.objects.get(gene_id=self.id, title='Family').annotation
        except KGenotation.DoesNotExist:
            self.family = ''
        try:
            self.subfamily = KGenotation.objects.get(gene_id=self.id, title='Subfamily').annotation
        except KGenotation.DoesNotExist:
            self.subfamily = ''
        self.classification = ':'.join((self.group, self.family, self.subfamily))
        self.alias = list(set([ ks.value for ks in KSearch.objects.filter(gene_id=self.id, field='Name') ]))
        if KGenotation.objects.filter(gene_id=self.id, title='Pseudogene').exists():
            self.pseudogene = True
        else:
            self.pseudogene = False
    def full(self):
        self.annotation = KGenotation.objects.filter(gene_id=self.id)
        self.sequence()
        self.domain()
    def sequence(self):
        self.sequence = {}
        self.sequence['protein'] = KSeq.objects.filter(gene_id=self.id, seqtype='Protein')
        self.sequence['kinase_domain'] = KSeq.objects.filter(gene_id=self.id, seqtype='Protein Kinase Domain')
        self.sequence['RNA'] = KSeq.objects.filter(gene_id=self.id, seqtype='RNA')
        self.sequence['all'] = KSeq.objects.filter(gene_id=self.id)
    def domain(self):
        if not self.sequence:
            self.sequence()
        for p in self.sequence['protein']:
            sequence = Sequence(p.id)
            sequence.full()
            p.collapse_domain = sequence.collapse_domains
            p.domain = sequence.domains
    def pviz_for_domain(self):
        pdname = set()
        pd = set()
        for p in self.sequence['protein']:
            s = Sequence(p.id)
            s.collapse_domains()
            for d in s.collapse_domains:                
                if d.domainname not in pdname:
                    pd.add(d)
                pdname.add(d.domainname)
        color = Colors()
        color_pd = color.get(len(pd))
        self.pviz_css_for_domain = []
        for i, d in enumerate(pd):
            if d.domain_group == 'kinase' or d.domain_group == 'Kinase':
                dd = {'name': 'kinase',
                      'rect_color': color.kinase['rect'],
                      'font_color': color.kinase['font'],
                      'fill_opacity': 0.8}
            else:
                dd = {'name': d.display_name,
                      'rect_color': color_pd[i]['rect'],
                      'font_color': color_pd[i]['font'],
                      'fill_opacity': 0.8}
            self.pviz_css_for_domain.append(dd)
                   

class Genes:
    def __init__(self, ids):
        self.genes = []
        for id in list(set(ids)):
            self.genes.append(Gene(id))
        self.ordered()
    def remove_pseudogene(self):
        genes = []
        for i, g in enumerate(self.genes):
            if not g.pseudogene:
                genes.append(self.genes[i])  
        self.genes = genes
    def filter_species(self, species_id):
        genes = []
        for i, g in enumerate(self.genes):
            if str(g.gene.species_id) in species_id:
                genes.append(self.genes[i])
        self.genes = genes
    def ordered(self):
        self.genes = sorted(self.genes, key=lambda g: (g.species.order_index, g.classification, g.gene.name))
    def list(self):
        return self.genes
    def fasta(self, seqtype):
        fasta = ''
        for g in self.genes:
            g.full()
            for p in g.sequence[seqtype]:
                seq = re.sub("(.{60})", "\\1\n", p.seq, 0, re.DOTALL)
                title = g.species.abbreviation + '_' + p.acc  + ' class=' + g.classification + ' gene=' + g.gene.name + ' species="' + g.species.name + '"' 
                fasta = fasta + '>' + title + '\n' + seq + '\n\n'
        return fasta
    def muscle(self, seqtype):
        fa = self.fasta(seqtype)
        fasta = Fasta(fa)
        fasta.save_fasta()
        fasta.run_muscle()
        return fasta
    def prepare_pviz(self):
        for g in self.genes:
            g.full()
            g.pviz_for_domain()
    def prepare_pviz_overall(self):
        features = []
        sequence = ''
        id = ''
        seqlen = 0
        for g in self.genes:
            if not g.sequence: g.full()
            for p in sorted(g.sequence['protein'], key=lambda p: (-p.length)):
                if seqlen < p.length: 
                    sequence = p.seq
                    id = p.id
                    seqlen = p.length
                category = g.species.name + ': ' + g.gene.name
#                 ff = {'category': category,
#                       'type': 'fullseq',
#                       'start': 1,
#                       'end': p.length,
#                       'text': p.acc + ' full sequence',}
#                 features.append(ff)
                for i, cd in enumerate(p.collapse_domain):
                    cdtype = cd.domain_group if cd.domain_group else 'bar'
                    if i == 0 and cd.start > 1:
                        f0 = {'category': category, 
                              'type': 'no_domain', 
                              'start': 1, 
                              'end': cd.start - 1, 
                              'text' : ''}
                        features.append(f0)
                    else:
                        f0 = {'category': category, 
                              'type': 'no_domain', 
                              'start': features[-1]['end'] + 1, 
                              'end': cd.start - 1, 
                              'text' : ''}
                        features.append(f0)
                    f = {'category': category, 
                         'type': cdtype, 
                         'start': cd.start, 
                         'end': cd.end, 
                         #'text' : cd.display_name + ': ' + str(cd.score)},
                         'text' : cd.display_name}
                    features.append(f)
                # tail
                f0 = {'category': category, 
                          'type': 'no_domain', 
                          'start': features[-1]['end'] + 1, 
                          'end': p.length, 
                          'text' : ''}
                features.append(f0)
        context = {'sequence': sequence,
                   'features': features,
                   'isoform_id': id,}
        return json.dumps(context)             
    def add_species(self):
        for g in self.genes:
            g['taxon_id'] = KGene.objects.get(id=g['id'])


class Colors:
    def __init__(self):
        fill_color = ('aqua', 'blue', 'fuchsia', 'gray', 'green', 'lime', 'maroon', 'navy', 'olive', 'orange', 'purple', 'silver', 'teal', 'yellow')
        font_color = ('black', 'white', 'white', 'white', 'white', 'black', 'white', 'white', 'white', 'black', 'white', 'black', 'white', 'black')
        self.colors = []
        for i, fc in enumerate(fill_color):
            self.colors.append({'rect': fc, 'font': font_color[i]})
        self.kinase = {'rect': 'red', 'font': 'white'}
        self.best_hit_kinase = {'rect': '#4169E1', 'font': 'white'}
    def get(self, N):
        return random.sample(self.colors, N)
