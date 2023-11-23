def ajouter_compte(mot_de_passe, nom, prenom, grade, email, date_de_naissance):
    try:
        cursor.execute('''INSERT INTO utilisateur (mot_de_passe, nom, prenom, grade, email, date_de_naissance)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                    (mot_de_passe, nom, prenom, grade, email, date_de_naissance))
    except:
        return ("echoueajoutecompte")

    conn.commit()
    return("Compte ajouté avec succès.")

def supprimer_compte(id):
    try:
        cursor.execute('''DELETE FROM utilisateur
         WHERE id=?''',
         (id))
    except:
        return("echouesupprimecompte")
    
    conn.commit()
    return("Compte supprimer avec succès.")


def verifier_mdp(mdp,email):
    try:
        cursor.execute('''SELECT COUNT(mdp) FROM utilisateur 
        WHERE  mdp==? and email==?''' ,(mdp,email))
        cursor.fetchone()
    except:
        return("verifiermotdepasseechoue")
    conn.commit()
    return("mdp verifie")

# Exécution de la requête SELECT
def obtenir_livre():
    try:
        cursor.execute('''SELECT id, titre, genre, date_de_parution FROM LIVRE''')
        # Récupération des résultats sous forme de dictionnaires
        results = []
        for row in cursor.fetchall():
            # Création d'un dictionnaire pour chaque ligne de résultat
            result_dict = {
                'id': row[0]
                'titre': row[1],
                'genre': row[2],
                'date_de_parution': row[3],
                }
            results.append(result_dict)
    except:
        return("echecobtentionlivre")
    return(results)


def livre_emprunte(id_u):
    try:
        cursor.execute('''SELECT id, titre, genre, date_parution,date_debut, date_fin
        FROM LIVRE JOIN EMPRUNT ON LIVRE.id==EMPRUNT.id_l WHERE id_u==?''',(id_u))
        results = []
        for row in cursor.fetchall():
            # Création d'un dictionnaire pour chaque ligne de résultat
            result_dict = {
                'id': row[0]
                'titre': row[1],
                'genre': row[2],
                'date_de_parution': row[3],
                'date_debut': row[4],
                'date_fin': row[5],
                }
            results.append(result_dict)
    except:
        return("livreemprunteechoue")
    return(results)
































