import sys

infi = open(sys.argv[1]).readlines()
 
outfi = open(sys.argv[2], 'w')
seqs = {}
taxa = []
for lin in infi:
    if lin.startswith('>'):
        name = lin
        taxa.append(name)
        seqs[name]=''
    else:
        seqs[name] = seqs[name] + lin.strip()

alnlen = len(seqs[name])
print(alnlen)

snps = {}
for name in taxa:
    snps[name] = ''

for i in range(alnlen):
    bases = set()
    for name in taxa:
        bases.add(seqs[name][i])
    if len(bases)>1:
        for name in taxa:
            snps[name] = snps[name] + seqs[name][i]

for name in snps:
    outfi.write(name)
    outfi.write(snps[name])
    outfi.write('\n')
            
outfi.close()