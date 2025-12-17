CREATE TABLE quiz_algo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO quiz_algo (question, answer) VALUES
("Qu'est-ce qu'un algorithme ?","Une suite d'instructions permettant de résoudre un problème ou d'accomplir une tâche."),
("Quelle structure de contrôle permet de répéter des instructions ?","Une boucle (for, while)."),
('Quelle est la différence entre un algorithme itératif et récursif ?', 'L'itératif utilise des boucles, le récursif s'appelle lui-même.'),
('Qu'est-ce qu'une variable dans un algorithme ?', 'Un espace de stockage pour une valeur qui peut changer.'),
('Qu'est-ce qu'une condition dans un algorithme ?', 'Une expression qui permet de décider quel chemin suivre.'),
('À quoi sert un diagramme de flux (flowchart) ?', 'À représenter visuellement un algorithme.'),
('Qu'est-ce qu'une fonction ou procédure ?', 'Un bloc d'instructions réutilisable pour effectuer une tâche précise.'),
('Que signifie "complexité algorithmique" ?', 'L'évaluation du temps ou de l'espace nécessaires pour exécuter un algorithme.'),
('Quel est le rôle d'un tableau (array) dans un algorithme ?', 'Stocker plusieurs valeurs du même type sous un même nom.'),
('Qu'est-ce qu'une pile (stack) ?', 'Une structure de données où le dernier élément ajouté est le premier à sortir (LIFO).'),
('Qu'est-ce qu'une file (queue) ?', 'Une structure de données où le premier élément ajouté est le premier à sortir (FIFO).'),
('Quelle est la différence entre tri par insertion et tri à bulles ?', 'Tri par insertion insère chaque élément à sa place, tri à bulles échange les éléments adjacents.'),
('Qu'est-ce qu'une condition "if-else" ?', 'Une structure qui exécute un bloc si la condition est vraie et un autre bloc sinon.'),
('Qu'est-ce que la récursivité ?', 'Quand une fonction s'appelle elle-même pour résoudre un problème.'),
('Qu'est-ce qu'un algorithme de recherche linéaire ?', 'Chercher un élément dans une liste en vérifiant un par un tous les éléments.'),
('Qu'est-ce qu'un algorithme de recherche binaire ?', 'Chercher dans une liste triée en divisant la liste par deux à chaque étape.'),
('Qu'est-ce qu'une complexité en O(n) ?', 'Le temps d'exécution augmente proportionnellement à la taille des données.'),
('Qu'est-ce qu'une structure de données ?', 'Une organisation particulière des données pour faciliter leur manipulation.'),
('Qu'est-ce qu'une liste chaînée ?', 'Une suite d'éléments où chaque élément pointe vers le suivant.'),
('Qu'est-ce qu'un algorithme glouton (greedy) ?', 'Un algorithme qui fait le choix le plus optimal à chaque étape.');

CREATE TABLE quiz_metiers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO quiz_metiers (question, answer) VALUES
('Quel métier conçoit et développe des logiciels ?', 'Développeur / Programmeur.'),
('Qui s'occupe de l'installation et de la maintenance des réseaux informatiques ?', 'Administrateur réseau.'),
('Quel professionnel protège les systèmes informatiques contre les cyberattaques ?', 'Expert en cybersécurité.'),
('Qui analyse des données pour en tirer des informations utiles ?', 'Data analyst.'),
('Quel métier consiste à créer des applications mobiles ?', 'Développeur mobile.'),
('Qui conçoit l'architecture technique des systèmes informatiques ?', 'Architecte informatique.'),
('Qui teste les logiciels pour détecter les bugs ?', 'Testeur logiciel / QA engineer.'),
('Quel métier consiste à gérer les bases de données ?', 'Administrateur base de données (DBA).'),
('Qui développe des sites web interactifs et dynamiques ?', 'Développeur web.'),
('Qui assure le support technique auprès des utilisateurs ?', 'Technicien support informatique.'),
('Quel métier utilise l'intelligence artificielle pour résoudre des problèmes ?', 'Ingénieur en intelligence artificielle / Machine Learning engineer.'),
('Qui gère la sécurité et la confidentialité des données ?', 'Responsable sécurité des systèmes d'information (RSSI).'),
('Qui transforme de grandes quantités de données brutes en informations exploitables ?', 'Data scientist.'),
('Qui crée des interfaces utilisateur attractives et ergonomiques ?', 'Designer UX/UI.'),
('Quel métier conçoit et supervise l'architecture des systèmes cloud ?', 'Architecte cloud.'),
('Qui gère le déploiement et le fonctionnement des applications sur les serveurs ?', 'DevOps engineer.'),
('Qui s'occupe de l'intelligence économique et de l'analyse des systèmes d'information ?', 'Analyste SI.'),
('Qui conçoit des jeux vidéo et leur logique ?', 'Game designer / Développeur de jeux vidéo.'),
('Quel métier consiste à maintenir le matériel informatique et les périphériques ?', 'Technicien informatique / Technicien matériel.'),
('Qui coordonne des projets informatiques et gère les équipes ?', 'Chef de projet informatique.');

CREATE TABLE quiz_logique (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO quiz_logique (question, answer) VALUES
('Si tous les chats sont des animaux et que Félix est un chat, Félix est-il un animal ?', 'Oui.'),
('Quel nombre complète la série : 2, 4, 8, 16, … ?', '32.'),
('Si A implique B et B est vrai, peut-on conclure que A est vrai ?', 'Non, ce n'est pas nécessairement vrai.'),
('Quelle est la négation de "Tous les oiseaux volent" ?', 'Il existe au moins un oiseau qui ne vole pas.'),
('Si aujourd'hui il pleut, alors je prends mon parapluie. Il pleut. Que fais-je ?', 'Je prends mon parapluie.'),
('Complétez la suite logique : 1, 1, 2, 3, 5, 8, …', '13 (suite de Fibonacci).'),
('Si trois crayons coûtent 6 euros, combien coûtent 5 crayons au même prix ?', '10 euros.'),
('Trouvez l'intrus : 2, 3, 5, 7, 9, 11', '9 (ce n'est pas un nombre premier).'),
('Si A est plus grand que B et B est plus grand que C, qui est le plus petit ?', 'C.'),
('Quel nombre complète la série : 3, 6, 12, 24, …', '48.'),
('Si je lance deux dés, quelle est la probabilité d'obtenir un total de 7 ?', '6/36 ou 1/6.'),
('Résolvez l'énigme : Je suis plus grand que Dieu, plus mauvais que le diable, les pauvres m'ont, les riches en ont besoin. Qui suis-je ?', 'Rien.'),
('Complétez : Si tous les A sont B, et certains B sont C, alors certains A sont-ils C ?', 'Pas forcément.'),
('Trouvez le mot manquant : chat est à chaton ce que chien est à …', 'Chiot.'),
('Quel nombre manque : 2, 5, 10, 17, …', '26 (ajouter 3, 5, 7, 9…).'),
('Si Pierre est plus âgé que Paul et Paul est plus âgé que Marie, qui est le plus âgé ?', 'Pierre.'),
('Complétez la suite : 1, 4, 9, 16, …', '25 (nombres carrés).'),
('Si deux trains partent en même temps à la même vitesse dans des directions opposées, que se passe-t-il par rapport à leur distance ?', 'La distance entre eux augmente à la somme de leurs vitesses.'),
('Quel est le prochain élément de la série : J, F, M, A, M, …', 'J (mois de l'année : Juin).'),
('Résolvez l'énigme : Un fermier a 17 moutons et tous sauf 9 meurent. Combien lui reste-t-il de moutons ?', '9.');

CREATE TABLE quiz_culture (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO quiz_culture (question, answer) VALUES
('Quelle est la capitale de l'Espagne ?', 'Madrid.'),
('Qui a peint la Joconde ?', 'Léonard de Vinci.'),
('Quel est le plus grand océan du monde ?', 'L'océan Pacifique.'),
('En quelle année l'homme a-t-il marché sur la Lune pour la première fois ?', '1969.'),
('Quel pays est surnommé le pays du Soleil-Levant ?', 'Le Japon.'),
('Qui a écrit "Les Misérables" ?', 'Victor Hugo.'),
('Quelle est la langue officielle du Brésil ?', 'Le portugais.'),
('Quel est l'élément chimique dont le symbole est O ?', 'L'oxygène.'),
('Quelle est la plus grande planète du système solaire ?', 'Jupiter.'),
('Quel inventeur a créé le téléphone ?', 'Alexander Graham Bell.'),
('Quel pays a inventé les Jeux Olympiques ?', 'La Grèce.'),
('Quelle est la monnaie du Royaume-Uni ?', 'La livre sterling.'),
('Qui est l'auteur de "Roméo et Juliette" ?', 'William Shakespeare.'),
('Quelle est la capitale de l'Australie ?', 'Canberra.'),
('Quel est le plus long fleuve du monde ?', 'Le Nil (ou l'Amazone selon certains critères).'),
('Qui a développé la théorie de la relativité ?', 'Albert Einstein.'),
('Quel est le pays le plus peuplé du monde ?', 'La Chine.'),
('Combien de continents existe-t-il sur Terre ?', '7.'),
('Quel animal est connu pour sa lenteur et sa carapace ?', 'La tortue.'),
('Quel est le symbole chimique de l'or ?', 'Au.');
CREATE TABLE quiz_anglais (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    answer TEXT NOT NULL
);

INSERT INTO quiz_anglais (question, answer) VALUES
('Comment dit-on "Bonjour" en anglais ?', 'Hello.'),
('Comment dit-on "Merci" en anglais ?', 'Thank you.'),
('Que signifie "Good morning" ?', 'Bonjour (le matin).'),
('Comment dit-on "Je m'appelle Othmane" en anglais ?', 'My name is Othmane.'),
('Que signifie "I love you" ?', 'Je t'aime.'),
('Comment dit-on "Au revoir" en anglais ?', 'Goodbye.'),
('Que signifie "See you later" ?', 'À plus tard.'),
('Comment dit-on "Je suis étudiant" en anglais ?', 'I am a student.'),
('Que signifie "What time is it ?" ?', 'Quelle heure est-il ?'),
('Comment dit-on "J'ai faim" en anglais ?', 'I am hungry.'),
('Que signifie "Where is the bathroom ?" ?', 'Où sont les toilettes ?'),
('Comment dit-on "Je veux un café" en anglais ?', 'I want a coffee.'),
('Que signifie "How are you ?" ?', 'Comment ça va ?'),
('Comment dit-on "Je ne comprends pas" en anglais ?', 'I don't understand.'),
('Que signifie "Happy birthday" ?', 'Joyeux anniversaire.'),
('Comment dit-on "Bonne nuit" en anglais ?', 'Good night.'),
('Que signifie "I like reading books" ?', 'J'aime lire des livres.'),
('Comment dit-on "Excusez-moi" en anglais ?', 'Excuse me.'),
('Que signifie "Can you help me ?" ?', 'Pouvez-vous m'aider ?'),
('Comment dit-on "Je suis fatigué" en anglais ?', 'I am tired.');



