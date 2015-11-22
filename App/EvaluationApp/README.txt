EvaluationApp

#######################################################################

@author: Rémi Cadène

#######################################################################
EvaluationApp

> evaluation.py
> src
  > summaries2rouge
  > ROUGE-1.5.5
  > rouge2csv
> corpus
  > RST-DT
    > EXT-EDUS-30
  > txt
  > summaries
> rslt

#######################################################################
evaluation.py 

evaulation.py appelle summaries2rouge pour formater les summaries contenus
dans EXT-EDUS-30 et summaries. Ce dernier appelle ROUGE-1.5.5 pour 
rendre un fichier score et appeler rouge2csv pour formater le fichier
score.

#######################################################################
src

src contient les différentes sources python et perl.

#######################################################################
EXT-EDUS-30

EXT-EDUS-30 contient 30 * 5 résumés des 30 textes gold générés
manuellement avec différents nombres d'EDUs sélectionnés.

#######################################################################
txt

txt contient les 30 textes gold qui sont à résumer.

#######################################################################
summaries

summaries contient les 30 * 5 résumés de textes gold, générés
automatiquement avec différentes nombre d'EDUs sélectionnés, en
utilisant l'application summarize que nous avons développés.

#######################################################################
rslt

rslt contient les résultats des évaluations par ROUGE.




