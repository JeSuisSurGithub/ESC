import nfc

def lire_tag_nfc():
    with nfc.ContactlessFrontend() as clf:
        print("Attente d'une carte NFC...")
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        print(f"Carte détectée avec UID : {tag.uid}")
        return tag

def ecrire_sur_tag_nfc(tag, data):
    print("Écriture sur le tag NFC...")
    # Vous pouvez personnaliser cette partie pour écrire des données spécifiques sur le tag
    # Par exemple, si le tag est de type 2 (MIFARE Ultralight), vous pouvez utiliser la fonction write()
    if isinstance(tag, nfc.tag.tt2.Type2Tag):
        tag.write(data)
        print("Données écrites avec succès sur le tag.")
    else:
        print("Impossible d'écrire sur le tag. Type de tag non pris en charge.")


#Dans le fichier principale exemple d'utilisation 

from lecture_ecriture_tag_nfc import lire_tag_nfc, ecrire_sur_tag_nfc

# Utiliser les fonctions
tag = lire_tag_nfc()

if tag:
    donnees_a_ecrire = b"Bonjour, NFC!"
    ecrire_sur_tag_nfc(tag, donnees_a_ecrire)
