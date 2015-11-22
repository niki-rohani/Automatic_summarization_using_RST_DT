INSTALLER :

installer nltk-2.0b9 : pip install nltk. remplacer le contenue de repertoire de /usr/lib/python2.7/site-packages/nltk-3. ... par nltk-2.0b, transferer le dossier nltk dans /usr/lib/p.../site-packages

---------------------------

installer YAML-3.09

* Compile the SVM scaling utility and classification tools for liblinear and libsvm. In order to do that:
1) Go to ./svm_tools and do a "gcc -o svm-scale svm-scale.c" to compile the scaling utility.
2) Go to ./svm_tools/liblinear and do a "make clean" then "make" to compile liblinear. 
3) Go to ./svm_tools/libsvm and do a "make clean" then "make" to compile libsvm. 

* Compile the svm_perf and svm_multiclass classifiers. In order to do that:
1) Go to ./svm_tools/svm_perf_stdin/ and do a "make clean" then "make" to compile all files.
2) Copy the svm_perf_classify file to the parent folder: "cp svm_perf_classify ../"
1) Go to ./svm_tools/svm_multiclass_stdin/ and do a "make clean" then "make" to compile all files.
2) Copy the svm_multiclass_classify file to the parent folder: "cp svm_multiclass_classify ../"

----------------------------

Puis sur python:

import nltk
nltk.download()
wordnet
wordnet ic
verbnet


