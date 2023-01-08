# Génération de phrases au moyen d’énergie textuelle
# Générateur de phrases contextuel par apprentissage neuronal (RNA)

# Abderrahim BOUHRIZ
# Rania BOUAITA


import re
import numpy as np
import math

dictionnaireDesPos = {}
dictionnaireDesMotEmbiding = {}

# Calcul de la similarité cosinus entre deux vecteurs
def calculate_cosine_similarity(vect1, vect2):
    # Initialisation de la variable de somme à 0
    c = 0
    # Initialisation des variables de norme à 0
    normA = 0
    normB = 0
    # Boucle sur les éléments des vecteurs
    for i in range(100):
        # Calcul de la somme des produits des éléments correspondants des vecteurs
        c += vect1[i] * vect2[i]
        # Calcul de la norme du vecteur 1 (somme des carrés des éléments)
        normA += math.pow(vect1[i], 2)
        # Calcul de la norme du vecteur 2 (somme des carrés des éléments)
        normB += math.pow(vect2[i], 2) 
    # Calcul de la similarité cosinus en divisant la somme par le produit des normes
    distance_cosine = c / float(math.sqrt(normA) * math.sqrt(normB))
    # Retourne la valeur de la similarité cosinus
    return distance_cosine

# Trouve les mots similaires au mot de requête dans le POS donné
def find_similar_words_to_query(pos, query):
    # Initialisation du dictionnaire de mots similaires
    similar_words_dict = dict()
    # Essaie de récupérer le vecteur du mot de requête
    # Si le mot n'est pas dans la base de données, le vecteur est initialisé à des 0
    try:
        vector_word = dictionnaireDesMotEmbiding[query]
    except KeyError:
        vector_word = np.zeros(100)

    for el in dictionnaireDesPos[pos]:
        # Essaie de récupérer le vecteur du mot en cours de traitement
        # Si le mot n'est pas dans la base de données, le vecteur est initialisé à des 0
        try:
            vector_el = dictionnaireDesMotEmbiding[el]
        except KeyError:
            vector_el = np.zeros(100)
        # Calcul de la similarité cosinus entre le vecteur du mot en cours de traitement et celui de la requête
        dot_product = calculate_cosine_similarity(vector_el, vector_word)
        # Si la similarité est négative, prendre sa valeur absolue
        if dot_product < 0:
            dot_product = abs(dot_product)
        # Ajouter le mot et sa similarité au dictionnaire
        similar_words_dict[el] = dot_product
    # Trier le dictionnaire par valeur de similarité (du plus grand au plus petit)
    similar_words_dict = sorted(similar_words_dict.items(), key=lambda x:x[1],reverse=True)
    # Convertir le dictionnaire en un dictionnaire Python (objet de type dict)
    similar_words_dict = dict(similar_words_dict)
    # Si le mot de requête est dans le dictionnaire, le supprimer
    if query in similar_words_dict:
        del similar_words_dict[query]
    # Retourner le dictionnaire de mots similaires
    return similar_words_dict

# Trouve les mots dissimilaires au mot donné dans le POS donné
def find_dissimilar_words(pos, word,query):
    # Initialisation du dictionnaire de mots dissimilaires
    dissimilar_words_dict = {}
    # Essaie de récupérer le vecteur du mot donné
    # Si le mot n'est pas dans la base de données, le vecteur est initialisé à des 0
    try:
        vector_word = dictionnaireDesMotEmbiding[word]
    except KeyError:
        vector_word = np.zeros(100)

    for other_word in dictionnaireDesPos[pos]:
        # Essaie de récupérer le vecteur du mot en cours de traitement
        # Si le mot n'est pas dans la base de données, le vecteur est initialisé à des 0
        try:
            vector_other_word = dictionnaireDesMotEmbiding[other_word]
        except KeyError:
            vector_other_word = np.zeros(100)
        # Calcul de la similarité cosinus entre le vecteur du mot en cours de traitement et celui du mot donné
        dissimilarity = calculate_cosine_similarity(vector_other_word, vector_word)
        #  Prendre la valeur absolue de la similarité
        dissimilarity = abs(dissimilarity)
        # Ajouter le mot et sa dissimilarité au dictionnaire
        dissimilar_words_dict[other_word] = dissimilarity
    # Trier le dictionnaire par valeur de dissimilarité (du plus grand au plus petit)
    dissimilar_words_dict = sorted(dissimilar_words_dict.items(), key=lambda x:x[1], reverse=True)
    # Convertir le dictionnaire en un dictionnaire Python (objet de type dict)
    dissimilar_words_dict = dict(dissimilar_words_dict)
    # Si le mot de requête est dans le dictionnaire, le supprimer
    if query in dissimilar_words_dict:
        del dissimilar_words_dict[query]
    # Retourner le dictionnaire de mots dissimilaires
    return dissimilar_words_dict

# Trouve le mot candidat parmi les mots du POS donné
def find_candidate_word(similar_words, dissimilar_words):
    candidate_word = ""
    best_score = 0
    for word in similar_words:
        # Calcul du score du mot en cours de traitement (similarité - dissimilarité)
        current_score = similar_words[word] - dissimilar_words[word]
        # Si le score est supérieur au meilleur score enregistré jusqu'à présent, mettre à jour le meilleur score et le mot candidat
        if current_score > best_score:
            best_score = current_score
            candidate_word = word
    # Retourner le mot candidat
    return candidate_word


# Regroupe les phrases générées par leur requête
def group_generated_phrases(phrase, query, phrase_dict):
    # Ajoute la phrase et la requête au dictionnaire de phrases
    phrase_dict[phrase] = query

# Génère un fichier texte UTF-8 contenant les 30 phrases générées
def generate_phrase_file(phrase_dict):
    with open("generated_phrases.txt", "w", encoding="utf8") as f:
        # Écrit chaque phrase et sa requête dans le fichier, séparées par une tabulation
        for phrase in phrase_dict:
            f.write(phrase + " : " + phrase_dict[phrase] + "\n")
 
# Cette fonction retourne le premier élément d'un dictionnaire
def get_first_element(dictionary):
    # Crée un itérateur sur les valeurs du dictionnaire
    value_iterator = iter(dictionary)
    # Récupère la première valeur de l'itérateur
    first_value = next(value_iterator)
    # Retourne la première valeur
    return first_value

# Cette fonction lit les données du fichier "TableAssociative.csv" et les stocke dans le dictionnaire dictionnaireDesPos
def read_associative_data_pos():
    # Ouvre le fichier "TableAssociative.csv" en mode lecture
    with open("TableAssociative.csv", 'r') as read_obj:
        data_table_associative = read_obj.readlines()
    for row in data_table_associative:
        tab = row.split("\t")
        # Récupère le premier élément de la liste tab (le POS)
        pos = tab[0] 
         # Supprime le retour à la ligne du dernier élément de la liste tab
        tab[len(tab)-1]= tab[len(tab)-1].replace("\n","")
         # Ajoute les mots du POS au dictionnaire dictionnaireDesPos
        dictionnaireDesPos[pos] = tab[1:] 
    # Retourne le dictionnaire dictionnaireDesPos
    return dictionnaireDesPos

# Cette fonction lit les données du fichier "embeddings-Fr.txt" et les stocke dans le dictionnaire dictionnaireDesMotEmbedding  
def read_embedding_data_word():
    with open("embeddings-Fr.txt", 'r') as read_obj:
        data_table_embedding = read_obj.readlines()
    for row in data_table_embedding:

        tab_vecteur_embbiding = row.replace('[',"").replace("]","").replace("\t"," ").replace(",","").replace("\n","").split(" ")    
        tab_vecteur_embbiding = [i for i in tab_vecteur_embbiding if i!=''] #On supprime les champs  vides  exemple :  , ,
        dictionnaireDesMotEmbiding[tab_vecteur_embbiding[0]] = np.asarray(tab_vecteur_embbiding[1:], dtype = float) # Transferer le tableau embedding en des floats
    
    return dictionnaireDesMotEmbiding
# Cette fonction affiche les 15 premiers mots similaires contenus dans le dictionnaire dictionnaire_mot_proche
def display_similar_words(similar_word_dictionary):
    print("\n---------------Similar words------------------ \n")
    # Affiche le mot et sa similarité
    i=0
    for word, similarity in similar_word_dictionary.items():
        print(word + "  " + str(similarity))
        # si le nombre de mots affichés est supérieur ou égal à 10, arrêter la boucle
        if i >= 10:
            break

# Cette fonction affiche les 15 premiers mots dissimilaires contenus dans le dictionnaire dictionnaire_mot_eloigner
def display_dissimilar_words(dissimilar_word_dictionary):
    print("\n---------------Dissimilar words------------------ \n")
    # On affiche les mot proches et les mot éloignées
    i=0
    for word, dissimilarity in dissimilar_word_dictionary.items():
        print(word + "  " + str(dissimilarity))
        # si le nombre de mots affichés est supérieur ou égal à 10, arrêter la boucle
        if i >= 10:
            break

# Cette fonction affiche le mot choisi, ou bien le premier mot du dictionnaire si le mot choisi est vide
def display_chosen_words(chosen_word, word_dictionary):
    # Si le mot choisi est vide
    if not chosen_word:
        # Récupère le premier mot du dictionnaire
        chosen_word = list(word_dictionary.keys())[0]
    print("Size of word is {}".format(len(chosen_word)))
    print(chosen_word)


# Cette fonction remplace les POS dans la SGP (sequence générée de phrases) par les mots choisis dans les listes tableau_mots_candidat et tableaux_POS
def replace_sgp_with_phrase(tableau_mots_candidat,tableaux_POS,res,phrase):
    print("--------------------------------- Recherche Pour le query Suivant -------------------------------")
    # Pour chaque POS de la liste tableaux_POS
    j=0
    for j in range(len(tableaux_POS)):
        # Remplace le POS par le mot choisi dans la SGP
        phrase = phrase.replace(res[j],tableau_mots_candidat[j])
        print("\n   {}".format(tableau_mots_candidat[j]))
    print(phrase)
    # Retourne la SGP mise à jour
    return phrase

    


# programme principal
def main():
    # Chaîne de caractères contenant une phrase annotée avec des parties du discours
    #SGP = "la *NCCS000/plume de la *AQ0FS00/belle *NCFS000/tante ."
    #SGP = "Je *VMIP1S0/vais au *NCMS000/marché pour *VMN0000/couper les *NCFP000/fleurs ."
    #SGP = "Le *NCMS000/chien est sur la *NCFS000/table ."
    SGP = "Je *VMIP1S0/suis *VMP00SM/désolé, je ne *VMIP1S0/parle pas *NP00000/bien le *NCMN000/francais ."
    #SGP = "J' *VMIP3S0/adore la *VMIP1S0/musique *AQ0CS00/classique ."

    # Extraire les mots annotés de la chaîne de caractères "SGP"
    res = re.findall(r'[*]\w+[/]\w+', SGP, flags=re.IGNORECASE)

    tableaux_POS = []
    tableaux_mots = []

    [tableaux_POS.append(res[i].split('/')[0].replace("*","")) for i  in range(len(res)) ]

    [tableaux_mots.append(res[i].split('/')[1].replace("*","")) for i  in range(len(res)) ]
    
    # Initialiser et construire dictionnaires des POS
    dictionnaireDesPos = read_associative_data_pos()
    # Initialiser et construire dictionnaires des mots
    dictionnaireDesMotEmbiding = read_embedding_data_word()

    dictionnaire_des_phrase = {}
    # La liste de requêtes
    query_context = ['amour', 'tristesse', 'haine', 'rouge']

   
    for query in query_context:

        tableau_mots_candidat=[]
        phrase  = SGP
        # pour chaque mot annoté de la chaîne de caractères "SGP"
        for i in range(len(res)):
            # Trouver les mots similaires à la requête dans la partie du discours correspondante
            dictionnaire_mot_proche = find_similar_words_to_query(tableaux_POS[i], query)
            # Trouver les mots dissimilaires au mot actuellement traité dans la partie du discours correspondante
            dictionnaire_mot_eloigner = find_dissimilar_words(tableaux_POS[i],tableaux_mots[i],query)
            #  Si le mot actuellement traité se trouve dans le dictionnaire de mots dissimilaires, le supprimer de ce dictionnaire
            if tableaux_mots[i] in dictionnaire_mot_eloigner:
                del dictionnaire_mot_proche[tableaux_mots[i]]
                del dictionnaire_mot_eloigner[tableaux_mots[i]]
            # Afficher les mots similaires à la requête
            display_similar_words(dictionnaire_mot_proche)
            # Afficher les mots dissimilaires au mot actuellement traité
            display_dissimilar_words(dictionnaire_mot_eloigner)
            # Trouver le mot candidat en comparant les mots similaires et dissimilaires
            mot_choisit = find_candidate_word(dictionnaire_mot_proche, dictionnaire_mot_eloigner)
            #  Afficher le mot candidat sélectionné
            display_chosen_words(mot_choisit,dictionnaire_mot_proche)
            # Ajouter le mot candidat à la liste de mots candidats
            tableau_mots_candidat.append(mot_choisit)
        # Remplacer les mots annotés de la chaîne de caractères "SGP" par les mots candidats
        phrase = replace_sgp_with_phrase(tableau_mots_candidat,tableaux_POS,res,phrase)  

        # Ajouter la phrase modifiée au dictionnaire de phrases
        group_generated_phrases(phrase,query,dictionnaire_des_phrase)
        # Réinitialiser la chaîne de caractères "phrase" avec la chaîne de caractères "SGP" originale
        phrase = SGP

    # Générer un fichier contenant toutes les phrases modifiées
    generate_phrase_file(dictionnaire_des_phrase)
# Exécuter le programme principal
main()
