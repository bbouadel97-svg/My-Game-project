
CHOIX = {
    "PLAY": 1, 
    "SAVE": 2,
    "RESTART": 3,
    "Partie sauvegardée": 4
}


def afficher_choix(choix):
    for nom, valeur in choix.items():
        # Affiche le numéro en premier pour que l'utilisateur puisse entrer le chiffre
        print(f"{valeur} : {nom}") 
def afficher_menu():
    print(""" 
       
                                                ╻ ╻┏━╸╻  ╻  ┏━┓   ╺┳╸┏━┓   ╻ ╻┏━┓╻ ╻┏━┓   ┏━╸┏━┓┏┳┓┏━╸
                                                ┣━┫┣╸ ┃  ┃  ┃ ┃    ┃ ┃ ┃   ┗┳┛┃ ┃┃ ┃┣┳┛   ┃╺┓┣━┫┃┃┃┣╸ 
                                                ╹ ╹┗━╸┗━╸┗━╸┗━┛    ╹ ┗━┛    ╹ ┗━┛┗━┛╹┗╸   ┗━┛╹ ╹╹ ╹┗━╸
                                                      
                                                        ┏━┓╻  ┏━╸┏━┓┏━┓┏━╸   ┏━╸┏┓╻ ┏┓┏━┓╻ ╻   ╻
                                                        ┣━┛┃  ┣╸ ┣━┫┗━┓┣╸    ┣╸ ┃┗┫  ┃┃ ┃┗┳┛   ╹
                                                        ╹  ┗━╸┗━╸╹ ╹┗━┛┗━╸   ┗━╸╹ ╹┗━┛┗━┛ ╹    ╹
                                                                                                                                                                                                                                                                     
            """)
    print("""
          
        ╻┏┓╻┏━┓╺┳╸┏━┓╻ ╻┏━╸╺┳╸╻┏━┓┏┓╻┏━┓        ┏━╸╻ ╻┏━┓╻┏━┓╻┏━┓┏━┓┏━╸╺━┓   ╻ ╻┏┓╻┏━╸     ┏━┓┏━┓╺┳╸╻┏━┓┏┓╻   ╺┳┓╻ ╻   ┏┳┓┏━╸┏┓╻╻ ╻ 
        ┃┃┗┫┗━┓ ┃ ┣┳┛┃ ┃┃   ┃ ┃┃ ┃┃┗┫┗━┓   ╹    ┃  ┣━┫┃ ┃┃┗━┓┃┗━┓┗━┓┣╸ ┏━┛   ┃ ┃┃┗┫┣╸      ┃ ┃┣━┛ ┃ ┃┃ ┃┃┗┫    ┃┃┃ ┃   ┃┃┃┣╸ ┃┗┫┃ ┃ 
        ╹╹ ╹┗━┛ ╹ ╹┗╸┗━┛┗━╸ ╹ ╹┗━┛╹ ╹┗━┛   ╹    ┗━╸╹ ╹┗━┛╹┗━┛╹┗━┛┗━┛┗━╸┗━╸   ┗━┛╹ ╹┗━╸     ┗━┛╹   ╹ ╹┗━┛╹ ╹   ╺┻┛┗━┛   ╹ ╹┗━╸╹ ╹┗━┛
          
           """)
    print("""
                                                                        ┏┳┓┏━╸┏┓╻╻ ╻
                                                                        ┃┃┃┣╸ ┃┗┫┃ ┃
                                                                        ╹ ╹┗━╸╹ ╹┗━┛ 
                                                         """)
    afficher_choix(CHOIX) #OKKKK

def Sauvegarder_partie_en_cours():
    nom_fichier = input("Entrez le nom du fichier pour sauvegarder la partie en cours : ").strip()
    # Logique de sauvegarde de la partie en cours dans le fichier spécifié
    print(f"Partie sauvegardée dans le fichier : {nom_fichier}")

def Utilisateur():
    # Demander le choix sous forme de numéro (ex: 1, 2, ...)
    while True:
        choix_str = input("Entrez le numéro de votre choix : ").strip()
        if not choix_str.isdigit():
            print("Veuillez entrer un numéro valide correspondant à une option.")
            continue
        choix_num = int(choix_str)
        # Trouver la clé correspondant au numéro
        selection = None
        for nom, valeur in CHOIX.items():
            if valeur == choix_num:
                selection = nom
                break
        if selection is None:
            print("Option inconnue. Réessayez.")
            continue
        nom_utilisateur = input("Quel est ton prénom ? ").strip()
        print(f"Tu as choisi l'option {selection} ({choix_num}).")
        return choix_num, nom_utilisateur
    
def Reponse():
    reponse = input("""
                    
                                                                        ┏━┓┏━╸┏━┓╺┳┓╻ ╻   ┏━┓
                                                                        ┣┳┛┣╸ ┣━┫ ┃┃┗┳┛    ╺┛
                                                                        ╹┗╸┗━╸╹ ╹╺┻┛ ╹     ╹ 
                     """).strip().lower()
    if reponse == "oui":
        print("OKAAAAY , Let's Go")
    elif reponse == "non":
        print("D'accord, à la prochaine!")
        exit()
    else:
        print("Réponse invalide. Veuillez répondre par 'Oui' ou 'Non'.")
        return Reponse()        
    return reponse