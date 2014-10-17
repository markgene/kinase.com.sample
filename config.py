OWNER = 'Nuabio'

PROJ_ROOT_URL = 'http://kinase.com/web/current/'

PROJ_ROOT_DIR = '/Users/kp/workspace/web/kinase/'

KLASS_FASTA_DIR = PROJ_ROOT_DIR + 'colt/static/colt/data/alntree/'
KLASS_ALIGNMENT_DIR = PROJ_ROOT_DIR + 'colt/static/colt/data/alntree/'
KLASS_ALIGNMENT_DIR_REL = 'colt/data/alntree/'
KLASS_PHY_DIR = PROJ_ROOT_DIR + 'colt/static/colt/data/alntree/'
KLASS_PHY_DIR_REL = 'colt/data/alntree/'
KLASS_HMM_DIR = PROJ_ROOT_DIR + 'colt/static/colt/data/alntree/'
KLASS_HMM_DIR_REL = 'colt/data/alntree/'
KLASS_HMM_JSON_DIR_REL = 'colt/data/alntree/'
KLASS_LEVELS = ['Group', 'Family', 'Subfamily']

FASTA_DIR = PROJ_ROOT_DIR + 'colt/static/colt/private/tmp/'

CLASSIFIER_FASTA_DIR = PROJ_ROOT_DIR + 'colt/static/colt/private/tmp/'
CLASSIFIER_HMM_PD = {'id': 'PD_v1', 
                     'file': PROJ_ROOT_DIR + 'colt/static/colt/data/HMM/specific/PD.hmm3',}
CLASSIFIER_HMM_PROTEIN = {'id': 'protein_v1',
                          'file': PROJ_ROOT_DIR + 'colt/static/colt/data/HMM/specific/protein.hmm3',}
CLASSIFIER_HMMSCAN = '/opt/local/bin/hmmscan'
CLASSIFIER_MAX_SEQ = 20

BLASTALL = '/opt/local/bin/blastall'
BLASTDB_PD = {'id': 'pd',
              'name': 'Phosphatase Domain',
              'file': PROJ_ROOT_DIR + 'colt/static/colt/data/blastdb/PD.fasta',}
BLASTDB_PROTEIN = {'id': 'protein',
                   'name': 'Protein',
                   'file': PROJ_ROOT_DIR + 'colt/static/colt/data/blastdb/protein.fasta',}
BLASTDB_PD_4GENOMES = {'id': 'pd4genomes',
                       'name': 'Phosphatase Domain (Human, Fly, C. elegans, Yeast)',
                       'file': PROJ_ROOT_DIR + 'colt/static/colt/data/blastdb/PD_4genomes.fasta',}
BLASTDB_PROTEIN_4GENOMES = {'id': 'protein4genomes',
                            'name': 'Protein (Human, Fly, C. elegans, Yeast)',
                            'file': PROJ_ROOT_DIR + 'colt/static/colt/data/blastdb/protein_4genomes.fasta',}
BLASTDB_HUMAN_CDNA = {'id': 'human_cdna',
                      'name': 'Human cDNA',
                      'file': PROJ_ROOT_DIR + 'colt/static/colt/data/blastdb/human_cdna.fasta',}
BLASTDB = [BLASTDB_PROTEIN_4GENOMES, BLASTDB_PROTEIN, BLASTDB_PD_4GENOMES, BLASTDB_PD, BLASTDB_HUMAN_CDNA]
BLAST_JOB_DIR = PROJ_ROOT_DIR + 'colt/static/colt/data/tmp/blast/'
BLAST_DISPLAY_N = 20

ALIGNMENT_PROGRAM = 'muscle'
TREE_PROGRAM = 'ninja'

HMM_CUTOFF = 0.00001
HMM_CUTOFF_EXPECTLOG = 5

JSON_DIR = PROJ_ROOT_DIR + 'colt/static/colt/json/'
