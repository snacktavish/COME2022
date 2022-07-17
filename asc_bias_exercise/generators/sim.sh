
seq-gen -l1000000 -mGTR -of true_tree.tre > all_sites.fas 
python snp_extractor.py all_sites.fas variable_sites.fas

