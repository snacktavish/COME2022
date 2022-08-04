#!/usr/bin/env python3
"""example usage:
python diff_counter.py seq1.fas seq2.fas
Both sequences much be in fasta
"""


import sys
true = sys.argv[1]
sample = sys.argv[2]
ref = sys.argv[3]



def fasta_as_string(filename):
    fi = open(filename)
    seq = ''
    for lin in fi.readlines():
        if lin.startswith('>'):
            name = lin.strip()
        else:
            seq = seq+lin.strip()
    return name, seq



def compare_basecalls(seqfi1, seqfi2, unambiguous_only=True):
    name1, seq1 = fasta_as_string(seqfi1)
    name2, seq2 = fasta_as_string(seqfi2)


    print("Sequence {f1} is {l1} bp".format(f1=seqfi1,l1=len(seq1)))
    print("Sequence {f2} is {l2} bp".format(f2=seqfi2,l2=len(seq2)))

    assert(len(seq1) == len(seq2))
    bases=set(['a','t','g','c'])

    diff_dict = {}
    if unambiguous_only:
        for i, char in enumerate(seq1):
            if set([char.lower(), seq2[i].lower()]).issubset(bases):
                if char.lower() != seq2[i].lower():
                    diff_dict[i] = (char.lower(), seq2[i].lower())

    else:
        for i, char in enumerate(seq1):
            if char.lower() != seq2[i].lower():
                diff_dict[i] = (char.lower(), seq2[i].lower())

    print("The sequences differ at {d} sites".format(d=len(diff_dict)))

    not_gap_diff = 0

    differences = open("differences.csv", "w")
    differences.write("location,{},{}".format(name1, name2))

    keylist = list(diff_dict.keys())
    keylist.sort()

    for i in keylist:
        diff = diff_dict[i]
        if set(diff).issubset(bases):
            not_gap_diff += 1
        differences.write("{i}, {b1}, {b2}\n".format(i=i, b1=diff[0], b2=diff[1]))

    differences.close()

    return(diff_dict)

    print("Of those {d} sites, {ng} are not a gap or an ambiguity code in one taxon".format(d=len(diff_dict), ng=not_gap_diff))



def compare_diff_dicts(diff_dict1, diff_dict2):
    diffs_matching = 0
    diffs_not_matching = 0   
    for key in diff_dict1:
        if key not in diff_dict2:
            diffs_matching += 1
        if key in diff_dict2:
            diffs_not_matching += 1
    assert diffs_matching+diffs_not_matching == len(diff_dict1)
    return({'diff_matching':diffs_matching,'diffs_not_matching':diffs_not_matching})



true_vs_sample_dict = compare_basecalls(true, sample)
sample_vs_ref_dict = compare_basecalls(ref, sample)

comparison = compare_diff_dicts(true_vs_sample_dict, sample_vs_ref_dict)
print(comparison)