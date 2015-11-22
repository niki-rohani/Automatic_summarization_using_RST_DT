///////// BIENVENUE DANS L'APPLICATION DE RESUME DE TEXTES //////
///// Auteurs : Rohani Niki
/////			Remi Cadene
////////////////////////////////////////////////////////////

L'application se d�compose en deux parties :
SummarizeApp : Application de r�sum�
EvaluationApp : Application pour �valuer des r�sumer

////////////////////////////////////////////////////////




INSTALLER :
Les pr�requis :
- nltk-2.0b9
- YAML-3.09
- gensim + english stopwords
- pulp

Compilation des fichiers pour HILDA :

1) Go to SummarizeApp/discourse/tools/svm_tools and do a "gcc -o svm-scale svm-scale.c" to compile the scaling utility.
2) Go to SummarizeApp/discourse/tools/svm_tools/liblinear and do a "make clean" then "make" to compile liblinear. 
3) Go to SummarizeApp/discourse/tools/svm_tools/libsvm and do a "make clean" then "make" to compile libsvm. 

1) Go to SummarizeApp/discourse/tools/svm_tools/svm_perf_stdin/ and do a "make clean" then "make" to compile all files.
2) Copy the svm_perf_classify file to the parent folder: "cp svm_perf_classify ../"
1) Go to SummarizeApp/discourse/tools/svm_tools/svm_multiclass_stdin/ and do a "make clean" then "make" to compile all files.
2) Copy the svm_multiclass_classify file to the parent folder: "cp svm_multiclass_classify ../"

----------------------------

Puis sur python:

import nltk
nltk.download()
wordnet
wordnet ic
verbnet


////////////////////// Commandes //////////////////////
/// Les fichiers de tests sont contenues dans SummarizeApp/discourse/TAL/

Afin de lancer un r�sum� automatique :

SummarizeApp/discourse/src/summarize.py -l MAX_NUMBER_W -i INPUT_FILE [-o OUTPUT_FILE]

Si ouput_file n'est pas pr�cis� alors le fichier de sortie sera INPUT_FILE.summary

MAX_NUMBER est le nombre maximum de mots dans un r�sum�.

/////////////////////////////////////

Fichiers Pour le r�sum� de textes :

SummarizeApp/discourse/src/summarize.py : fichier principale
SummarizeApp/discourse/src/tkp.py : fichier effectuant la r�solution du probl�me tkp
SummarizeApp/discourse/src/rst2dep.py : fichier effectuant la transformation d'un rst en dep
SummarizeApp/discourse/src/parse.py : fichier HILDA


Le repertoire :
SummarizeApp/discourse/TAL contien des examples
A chaque r�sum�, un fichier INPUT_FILE.tree est cr�� et repr�sentente l'arbre RST.


Pour l'�valuation voir EvaluationApp

