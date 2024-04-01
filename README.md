# Quelques précisions sur la structure de ce dossier

- `auto_run_lambda` et `auto_run_nu` ont été utilisés pour tester automatiquement (sur une nuit) de nombreuses valeurs de $\lambda$ et de $\nu$ avec un petit script bash (respectivement, lambdas.sh et nus.sh)
    - le sous-dossier `resultats` contient les résultats intéressants de ces exécutions ; pour ne pas trop alourdir ce dossier nous avons supprimé la majorité des fichiers issus de ces tests.
    - attention : ne pas lancer le script bash (il effectue près d'une centaine d'exécutions de Perona-Malik!)

- `photos` contient les images que nous avons utilisé comme tests
- `resultats` contient beaucoup de résultats de tests, avec le fichier log qui enregistre leurs paramètres

# Les scripts

- `chaleur_lin.py` résout l'équation de la chaleur à partir de paramètres donnés.
- `chaleur_lin_essairgb.py` contient une tentative non-aboutie de passer à des images couleur.
- `peronamalick.py` résout l'équation de Perona-Malik à partir de paramètres donnés.
