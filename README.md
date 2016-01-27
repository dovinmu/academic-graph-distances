# academic-graph-distances
Computes Erdos, Knuth, Hofstadter, etc numbers; i.e. the degrees of separation between two authors, from dblp.uni-trier.de.

Usage:
  distances.py [options] <author 1>
    -v: Verbose option
  Note: Authors need to be entered as actual (partial) URLs to avoid ambiguity. Example:
  >>> python distances.py k/Knuth:Donald_E= 

  This command will search the connection graph outwards from Donald Knuth for connections to other famous computer scientists and those with low Erdos numbers, and print out the paths between them.
