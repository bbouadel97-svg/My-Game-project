def Category(): 

    categorie = {
        "1": "Algorithme",
        "2": "Metiers de l'informatique",
        "3": "Logique",
        "4": "Culture Générale",
        "5": "Anglais",
    }
    print("Choix de catégories :")
    for numero, nom in categorie.items():
        print(f"{numero} : {nom}")
    while True:
        choix = input("Choisis une catégorie : ").strip().upper()
        if choix in categorie:
            print(f"Tu as choisi la catégorie : {choix}")
            return choix
        else:
            print("Catégorie invalide. Réessaie.")
