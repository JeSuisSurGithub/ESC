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



































