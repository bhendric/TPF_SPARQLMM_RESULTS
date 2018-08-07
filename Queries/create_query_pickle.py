# File that will contain all the sparql queries used in performance testing. It will dump these as a pickle file and then allow the performance test scripts to read all the sparql queries and randomly select Done
import pickle

queries = [
"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}LIMIT 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}LIMIT 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:rightBeside(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:rightBeside(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:rightBeside(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:leftBeside(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:rightBeside(?f1, ?f2)
}limit 200""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Animal".

  FILTER mm:rightAbove(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Animal".

  FILTER mm:rightAbove(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Animal".

  FILTER mm:rightAbove(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:leftAbove(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:leftAbove(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:leftAbove(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:leftAbove(?f1, ?f2)
}limit 150""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:below(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:below(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:below(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:below(?f1, ?f2)
}limit 500""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".
  ?f3 dc:description "Person".

  FILTER mm:rightBeside(?f1, ?f2)
  FILTER mm:rightBeside(?f2, ?f3)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".
  ?f3 dc:description "Person".

  FILTER mm:rightBeside(?f1, ?f2)
  FILTER mm:rightBeside(?f2, ?f3)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".
  ?f3 dc:description "Person".

  FILTER mm:rightBeside(?f1, ?f2)
  FILTER mm:rightBeside(?f2, ?f3)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".
  ?f3 dc:description "Person".

  FILTER mm:leftBeside(?f1, ?f2)
  FILTER mm:leftBeside(?f2, ?f3)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".
  ?f3 dc:description "Person".

  FILTER mm:leftBeside(?f1, ?f2)
  FILTER mm:leftBeside(?f2, ?f3)
} limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".
  ?f3 dc:description "Person".

  FILTER mm:leftBeside(?f1, ?f2)
  FILTER mm:leftBeside(?f2, ?f3)
} limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".
  ?f3 dc:description "Person".

  FILTER mm:leftBeside(?f1, ?f2)
  FILTER mm:leftBeside(?f2, ?f3)
} limit 425""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:spatialEquals(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:spatialEquals(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:spatialEquals(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Person".

  FILTER mm:spatialEquals(?f1, ?f2)
}limit 500""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Tree".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Person".
  ?f2 dc:description "Car".

  FILTER mm:spatialDisjoint(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".

  FILTER mm:spatialContains(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".

  FILTER mm:spatialContains(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".

  FILTER mm:spatialContains(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:covers(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:covers(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Car".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:covers(?f1, ?f2)
}limit 100""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Tree".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:spatialOverlaps(?f1, ?f2)
}""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Tree".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:spatialOverlaps(?f1, ?f2)
}limit 50""",

"""PREFIX ma: <http://www.w3.org/ns/ma-ont#>
PREFIX mm:  <http://linkedmultimedia.org/sparql-mm/ns/2.0.0/function#>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?subject ?f1 ?f2 WHERE {
  ?subject ma:hasFragment ?f1;
            ma:hasFragment ?f2;
            ma:hasFragment ?f3;
            dc:title ?topic.
  ?f1 dc:description "Tree".
  ?f2 dc:description "Tree".
  ?f3 dc:description "Person".

  FILTER mm:spatialOverlaps(?f1, ?f2)
}limit 100"""   ]

with open('queries.pkl', 'wb') as fp:
    pickle.dump(queries, fp)
