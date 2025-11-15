import sqlite3



def get_categories():
    # Connexion à la base de données
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM category")
    categories = cur.fetchall()
    con.close()
    return categories
print(get_categories())

def get_questions():
    con = sqlite3.connect("tutorial.db")
    cur =con.cursor()
    cur.execute("SELECT * FROM QUESTIONS")
    questions = cur.fetchall()
    con.close()
    return questions

def get_questions_by_category(name_category):
    con = sqlite3.connect("tutorial.db")
    cur = con.cursor()
    cur.execute("""
        SELECT q.id_question, q.texte_question
        FROM question q
        JOIN category c ON q.id_category = c.id_category
        WHERE c.name_category = ?
    """, (name_category,))
    question = cur.fetchall()
    con.close()
    return question

get_questions_by_category()


