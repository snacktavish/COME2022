# Ascertainment Bias Exercise
Simulated data can be a great way to investigate model misspecification and biases. This exercise uses a data set simulated on a tree with some short branches, and high rate variation among lineages (a hard tree to estimate correctly). Data was simulated using seq-gen (http://tree.bio.ed.ac.uk/software/seqgen/).


Many analysis pipelines enriched datasets for variable sites, or include exclusively alignment columns with variable sites, e.g. Single nucleotide polymorphism (SNP) data. This is an example of 'ascertainment bias'. 
The data that you have 'ascertained' and included in your alignment are not a random subset of the genome. They does not include invariant sites. 
If the data if pruned to sites with only two states, you have also removed sites at which repeated mutations have resulted in the same base at the tips (homoplasy).

## Part 1: tree inference


Clone the exercise repo and cd into the directory for this example if you havn't aleady done so:

    git clone git@github.com:snacktavish/sequence_data_exercise.git
    cd sequence_data_exercise/asc_bias_exercise


Take a look at the true tree -   the tree that the data was simulated on true_tree.tre
This is a tree shape that makes correct topologies particularly hard to estimate.


Lets take a simulated data set based on that tree, that has not been subject to any ascertainment bias.
The alignment is in the file asc_bias_exercise/sim_noasc.phy, and estimate a tree:

Depending on your version of raxml, run either:

   raxmlHPC -m GTRGAMMA -p 2 -s  sim_noasc.phy -n  no_asc_bias 

or 

    raxml-ng -model GTR+G -msa  sim_noasc.phy




Open the ML tree in a tree viewer 
Compare the topology of the best tree estimate to the true tree.

**Q. Did you estimate the correct topology?**

**Q. How do the branch lengths compare to the true tree (sim.tre)?**

Now lets run that same analysis on only the variable sites from that alignment, sim_variablesites.phy. This is the exact same alignment, but with the invariant columns removed.


    raxml-ng -model GTR+G -msa  sim_variablesites.phy
OR
    raxmlHPC -m GTRGAMMA -p 2 -s sim_variablesites.phy -n asc_uncorrected


**Q. Did you get the correct topology?**
**Q. How do the branch lengths compare to the true tree (sim.tre)**


Lets bootstrap it!


    raxml-ng -model GTR+G -msa  sim_variablesites.phy -bootstrap 100
    raxml-ng --support --tree variable_sites.raxml.bestTree --bs-trees variable_sites.raxml.bootstraps

OR 
    raxmlHPC -m GTRGAMMA -p 123 -# 100 -b 123 -s sim_variablesites.phy -n asc_uncorr_boot
    raxmlHPC -m GTRGAMMA -f b -t RAxML_bestTree.asc_uncorrected -z RAxML_bootstrap.asc_uncorr_boot -n asc_uncorr_bipart




**Q: What is the bootstrap support for the one bipartition in the tree? (You can open it in figtree, but with such a simple tree you can also just look at the text file directly)**

**Q: Is that bipartition in the true tree?**

However, even if you only have the variable sites, by using an appropriate model of evolution, it is possible to rescue your analysis. In RAxML you can you a model corrected for ascertainment bias by using a model corrected for these known biases. We will use th ASC_GTRGAMMA model, with the lewis (as in Paul Lewis) correction for discarding sites that don't vary in the alignment.


    raxmlHPC -m ASC_GTRGAMMA --asc-corr lewis -p 2 -s datafiles/sim_variablesites.phy -n asc_corrected


**Q: Did you get the correct tree?**

Bootstrap it!

    raxml-ng -model GTR+G -msa  sim_variablesites.phy -bootstrap 100


   raxmlHPC -m ASC_GTRGAMMA --asc-corr lewis -p 2 -# 100 -b 123 -s datafiles/sim_variablesites.phy -n asc_corr_boot
   raxmlHPC -m ASC_GTRGAMMA -f b -t RAxML_bestTree.asc_corrected -z RAxML_bootstrap.asc_corr_boot -n asc_corr_bipart


**Q: What is the bootstrap support for the one bipartition in the tree?**
**Q: Is that bipartition in the true tree?**

This is the exact same dataset! If our model of evolution is not appropriate for our data, our results can be systematically biased. Incorrect inferences can have 100% bootstrap support, because sampling across our data does not capture the problem.
NOTE: The ascertainment bias corrections in RAxML will not run if there are ANY invariant columns in your alignment.

## Part 2: Exploring statements of homology

Open each of the two data files (sim_noasc, and sim_variable sites) in seaview.

Take a look at where the sites in the variable file from from in the full alignment.

**Q: What is the location of the first eight variable sites in the full alignment?**

This data is already correctly aligned, based on the simulation, but we can see what 'aligning' it does.

Use muscle to align the data in the full alignment. 
```
muscle -in sim_noasc.fas -out sim_noasc_align.fas
```

**Q: Did the alignment change?**

Estimate the tree using this new alignemnt.

**Q: Did the ML tree change?**

Use muscle to align the data in the variable sites alignment. 
```
muscle -in sim_variablesites.fas -out sim_variablesites_realign.fas
```

**Q: Did the alignment change?**


Open the full alignment (sim_noasc.phy) in seaview.

Use the space bar to add gaps, and the delete key to remove them.
Align the sequences to capture the same homology statement that is made by the first two variable site in the "sim_variablesites_realign.fas".
NOTE: the taxa may be re-ordered in the estmated alignment. You can try the hand alignment with them re-ordered, but it is easier if you put them back in A,B,C,D order first using a text editor. (Presumably you can re-order them in seaview, but I don't know how)


**Q: How do these homology statements look?**


Estimate the ML tree using this new alignemnt.

**Q: Do you get the correct tree? Do you expect to?**


