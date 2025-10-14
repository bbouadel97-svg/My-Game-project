
from menu import *
from menu import afficher_menu
from menu import Utilisateur
from menu import Reponse
from Catgory import Category
from Algo import lancer_quizalgo


def main():
    afficher_menu()
    Utilisateur()
    Reponse()
    continuer_jeu = True
    while continuer_jeu : 
        Category()
        lancer_quizalgo()
        print("Voulez vous continuer de jouer? Oui ou Non")
        choix = input()
        continuer_jeu = choix.lower() == "oui"


 
    
    #TODO gerer la progression et sauvegarde de partie dans un game session // apres 
    #TODO gerer la sauvegarde du nom d'utilisateur et le demander aprés chaque partie // apres 
    #TODO charger les questions depuis le base de données script 
    #TODO boucler sur 20 questions la categorie choisie par utilisateur 
   
    # Exemple de question

       

    
if __name__ == "__main__":
    main()
    

    