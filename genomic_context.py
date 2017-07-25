#!/usr/local/bin/python3

from Bio import SeqIO,Entrez
from sys import argv

try:
    orig_id=argv[1]
except IndexError:
    orig_id='SIS32979.1'

Entrez.email = 'xchen18@uoguelph.ca'

orig_ipg=Entrez.efetch(db='protein',id=orig_id,rettype='ipg',retmode="xml")
orig_rec=Entrez.read(orig_ipg)

for i in orig_rec[0]['ProteinList']:
    if i.attributes['source']=='INSDC': 
       genome= i
       break
    else:
        genome=orig_rec[0]['ProteinList'][0]

genomeid=genome['CDSList'][0].attributes['accver']
start=genome['CDSList'][0].attributes['start']
end=genome['CDSList'][0].attributes['stop']
strand=genome['CDSList'][0].attributes['strand']

if strand=="+":
    gen_strand=1
else:
     gen_strand=2

gen_gb=Entrez.efetch(db='nucleotide',id=genomeid,
        strand=gen_strand,seq_start=int(start)-55000,seq_stop=int(end)+55000,
            rettype='gb',retmode='text')

record=SeqIO.read(gen_gb,'genbank')

for i in record.features:
    if 'protein_id' in i.qualifiers:
        print(i.qualifiers['protein_id'][0],':',i.qualifiers['product'][0])


