from rdflib import Graph

g = Graph()
g.parse("APIbusterHierarch.owl")
# g.parse("peopleOntology.owl")
print (g.serialize(format='json-ld'))