import os, sys, tempfile, string, random
from subprocess import call
from colt.alignment import Alignment


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class Fasta:
    def __init__(self, fasta):
        self.tempdir = '/Users/kp/workspace/web/kinase/colt/static/colt/private/tmp'
        self.prefix = id_generator() + '_'
        self.fasta = fasta
    def save_fasta(self):
        fd, self.fasta_file = tempfile.mkstemp(prefix=self.prefix, suffix=".fasta", dir=self.tempdir)
        with os.fdopen(fd, 'w') as tf:
            tf.write(self.fasta)
    def run_muscle(self):
        if not hasattr(self, 'fasta_file'): self.save_fasta()
        self.muscle_file = self.fasta_file + '.muscle.aln'
        if os.path.exists(self.muscle_file):
            sys.stderr.write('#LOG: alignment exists. skip muscle\n')
            return 0
        sys.stderr.write("#LOG: run muscle\n")
        muscle_bin = '/Applications/Bio/muscle3.8.31_i86darwin64'
        cline = ' '.join((muscle_bin, '-in', self.fasta_file, '-out', self.muscle_file, '-clwstrict -quiet'))
        call(cline, shell=True)
        self.muscle_alignment = Alignment(self.muscle_file)
        
        
