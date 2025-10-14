
def Quiz_algo():
   question = {
    1:["Qu’est-ce qu’un algorithme ?", "Une suite d’instructions permettant de résoudre un problème ou d’accomplir une tâche."],
    2:["Quelle structure de contrôle permet de répéter des instructions ?", "Une boucle (for, while)."],
    3:["Quelle est la différence entre un algorithme itératif et récursif ?", "L’itératif utilise des boucles, le récursif s’appelle lui-même."],
    4:["Qu’est-ce qu’une variable dans un algorithme ?", "Un espace de stockage pour une valeur qui peut changer."],
    5:["Qu’est-ce qu’une condition dans un algorithme ?", "Une expression qui permet de décider quel chemin suivre."],
    6:["À quoi sert un diagramme de flux (flowchart) ?", "À représenter visuellement un algorithme."],
    7:["Qu’est-ce qu’une fonction ou procédure ?", "Un bloc d’instructions réutilisable pour effectuer une tâche précise."],
    8:["Que signifie \"complexité algorithmique\" ?", "L’évaluation du temps ou de l’espace nécessaires pour exécuter un algorithme."],
    9:["Quel est le rôle d’un tableau (array) dans un algorithme ?", "Stocker plusieurs valeurs du même type sous un même nom."],
    10:["Qu’est-ce qu’une pile (stack) ?", "Une structure de données où le dernier élément ajouté est le premier à sortir (LIFO)."],
    11:["Qu’est-ce qu’une file (queue) ?", "Une structure de données où le premier élément ajouté est le premier à sortir (FIFO)."],
    12:["Quelle est la différence entre tri par insertion et tri à bulles ?", "Tri par insertion insère chaque élément à sa place, tri à bulles échange les éléments adjacents."],
    13:["Qu’est-ce qu’une condition \"if-else\" ?", "Une structure qui exécute un bloc si la condition est vraie et un autre bloc sinon."],
    14:["Qu’est-ce que la récursivité ?", "Quand une fonction s’appelle elle-même pour résoudre un problème."],
    15:["Qu’est-ce qu’un algorithme de recherche linéaire ?", "Chercher un élément dans une liste en vérifiant un par un tous les éléments."],
    16:["Qu’est-ce qu’un algorithme de recherche binaire ?", "Chercher dans une liste triée en divisant la liste par deux à chaque étape."],
    17:["Qu’est-ce qu’une complexité en O(n) ?", "Le temps d’exécution augmente proportionnellement à la taille des données."],
    18:["Qu’est-ce qu’une structure de données ?", "Une organisation particulière des données pour faciliter leur manipulation."],
    19:["Qu’est-ce qu’une liste chaînée ?", "Une suite d’éléments où chaque élément pointe vers le suivant."],
    20:["Qu’est-ce qu’un algorithme glouton (greedy) ?", "Un algorithme qui fait le choix le plus optimal à chaque étape."]
    } 
   return question

def lancer_quizalgo(score: int) -> int:
    questions = Quiz_algo()  # Doit retourner un dictionnaire {num: [question, réponse]}
    print(f"Votre score actuel : {str(score)}")
    for num, question in questions.items():
        print (f"{num} : {question[0]}")
        reponse = input("Votre reponse: ")
        if reponse.lower() == question[1].lower():
            print(" Bonne réponse")
            score += 1
        else:
            print(f" Perdu ! La bonne réponse était : {question[1]}")
    print(f"\n🎯 Score final : {score}/{len(questions)}")
    return score
    



