# Defi4-innovation
Génération de phrases au moyen d’énergie textuelle

Ce projet a pour objectif la création de modèles de génération de phrases littéraires en utilisant l'énergie textuelle. Ces modèles incluent une génération de phrases basée sur les modèles de langage unigramme et bigramme (ML-1 et ML-2) ainsi qu'une génération de phrases basée sur l'apprentissage neuronal (RNA) et un contexte (query). Nous avons utilisé des ressources telles que le corpus littéraire MegaLite-Fr, une table associative, des embeddings littéraires et une baseline pour réaliser ce projet. Nous avons évalué manuellement la grammaticalité et la littéracité des phrases générées.



# Modèle basé sur les chaînes de Markov

Le fichier "fusion_bigrams.py" permet d'extraire les bigrammes avec leurs occurences dans le corpus. Ces fichiers seront enregistrés dans le même répertoire où le script a été lancé sous le nom bigramfile.txt. La syntaxe suivante est utilisée : mot \t mot \t occurence.

Pour utiliser le générateur de phrases basé sur les bigrams et unigrams, il suffit de lancer d'abord le fichier "fusion_bigrams.py" dans le même répertoire que le fichier "sentence_generator_model_basiline.py". Ensuite, vous pouvez exécuter ce dernier fichier en utilisant la commande python3 sentence_generator_model_basiline.py pour obtenir des phrases générées.

Note : il est recommandé de tester le programme avec un corpus de petite taille afin de le lancer plus rapidement.

# Modèle neuronal RNA

Le fichier RNA.py contient le code source d'un modèle de génération de phrases utilisant. Pour utiliser ce modèle, il suffit d'exécuter le fichier en utilisant la commande python3 RNA.py.
