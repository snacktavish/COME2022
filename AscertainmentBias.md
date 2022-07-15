# Ascertainment Bias Exercise
Simulated data can be a great way to investigate model misspecification and biases. This exercise uses a data set simulated on a Felsenstein Zone tree. Data was simulated using seq-gen


Many datasets are enriched for variable sites, or include exclusively alignment columns with variable sites, i.e. Single nucleotide polymorphism (SNP) data. This is an example of 'ascertainment bias'. 
The data that you have 'ascertained' and included in your alignment are not a random subset of the genome. This does not include invariant sites. 
If the data if pruned to sites with only two states, you have removed sites at which repeated mutations have resulted in the same base at the tips (homoplasy).

## Part 1: tree inference

Take a look at the true tree -   the tree that the data was simulated on datafiles/sim.tre
This is a tree shape that makes correct topologies particularly hard to estimate - the "Felsenstein Zone" (read more about this at ????)


Lets take a simulated data set based on that tree, that has not been subject to any ascertainment bias.
The alignment is in the file asc_bias_exercise/sim_noasc.phy, and estimate a tree:

```
raxmlHPC -m GTRGAMMA -p 2 -s  asc_bias_exercise/datafiles/sim_noasc.phy -n  asc_bias_exercise/no_asc_bias
```


Open the ML tree in a tree viewer 
Compare the topology of the best tree estimate to the true tree.

**Q. Did you estimate the correct topology?**


Now lets run that same analysis on only the variable sites from that alignment, sim_variablesites.phy. This is the exact same alignment, but with the invariant columns removed.

```
raxmlHPC -m GTRGAMMA -p 2 -s datafiles/sim_variablesites.phy -n asc_uncorrected
```

**Q. Did you get the correct topology?**
**Q. How do the branch lengths differ from the true tree?**


Lets bootstrap it!

```
raxmlHPC -m GTRGAMMA -p 123 -# 100 -b 123 -s datafiles/sim_variablesites.phy -n asc_uncorr_boot

raxmlHPC -m GTRGAMMA -f b -t RAxML_bestTree.asc_uncorrected -z RAxML_bootstrap.asc_uncorr_boot -n asc_uncorr_bipart
```

**Q: What is the bootstrap support for the one bipartition in the tree? (You can open it in figtree, but with such a simple tree you can also just look at the text file directly)**

**Q: Is that bipartition in the true tree?**

However, even if you only have the variable sites, by using an appropriate model of evolution, it is possible to rescue your analysis. In RAxML you can you a model corrected for ascertainment bias by using a model corrected for these known biases. We will use th ASC_GTRGAMMA model, with the lewis (as in Paul Lewis) correction for discarding sites that don't vary in the alignment.

```
raxmlHPC -m ASC_GTRGAMMA --asc-corr lewis -p 2 -s datafiles/sim_variablesites.phy -n asc_corrected
```

**Q: Did you get the correct tree?**

Bootstrap it!
```
raxmlHPC -m ASC_GTRGAMMA --asc-corr lewis -p 2 -# 100 -b 123 -s datafiles/sim_variablesites.phy -n asc_corr_boot
raxmlHPC -m ASC_GTRGAMMA -f b -t RAxML_bestTree.asc_corrected -z RAxML_bootstrap.asc_corr_boot -n asc_corr_bipart
```

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


