import re

class Alignment:
    def __init__(self, filepath):
        self.filepath = filepath
    def aln_to_html(self):
        body = []
        with open(self.filepath, 'r') as f:
            for line in f:
                line = line.rstrip()
                flag = 0
                if re.search(r'CLUSTAL W', line):
                    continue
                newline = ''
                for s in line:
                    if s == ' ': 
                        flag = 1
                    if flag == 1 and s != ' ': 
                        s = '<span class="' + s + '">' + s + '</span>'
                    newline = newline + s
                body.append(newline)
        self.html = { 'body': '\n'.join(body) }