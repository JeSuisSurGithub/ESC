# ESC
![logo](/img/esc_ratio_43_2000px.png)

## Comment ça marche ?
### Organisation du code
+ Toute les pages html ont un script du même nom mais peuvent parfois partager les feuilles de style
* Toute les requêtes au serveur passent par api.js et les fonctions d'utilité générales sont aussi dedans
+ Toute la logique de la barre de navigation se trouve dans navbar.js
* Les scripts init_db.sh init.sql et ajout_compte.py servent à initialiser la base de données
+ Le code du serveur se trouve à la racine
* Les communications entre le frontend et le backend se font via le format json et des interfaces GET et POST, l'intégrité des informations communiquées est assurée par une table des code de statut définie dans erreurs.py et au début de api.js. Ils définissent aussi les messages d'erreur à afficher. Les codes de statut positifs signalent qu'il y'a pas eu d'erreur et ceux négatif signalent qu'il y'en a eu.

### Exemple de fonctionnement pour l'emprunt
1. Vous cliquez sur emprunt
2. Vous êtes redirigé vers la page d'attente nfc.html qui demande au serveur de lire le capteur avec un timeout de 10s
3. Une fois que le temps soit écoulé ou qu'une carte soit scannée la page redirige vers la page d'origine en lui retransmettant l'UID de la carte NFC ainsi que l'action originellement souhaitée c'est à dire ici l'emprunt
4. La page va ainsi demander au serveur le livre avec l'UID correspondant
5. Si il y'a eu un résultat alors la page va effectuer une requête d'emprunt au serveur en spécifiant l'ID du livre
6. Enfin si le livre est disponible et que l'utilisateur est connecté, l'emprunt est marqué dans la BDD et l'utilisateur en est informé grâce au code statuts

### Schéma
![logo](/fonctionnement.png)

## Guide d'installation
1.  Installer git et python3 avec `sudo apt install git python3`
2.  Activer la communication SPI avec `raspi-config`
2.  Suivre les instructions pour installer [SPI-Py](https://github.com/lthiery/SPI-Py)
3.  Cloner le dépot `git clone https://github.com/JeSuisSurGithub/ESC`
4.  Installer les libraries nécessaires `pip install -r requirements.txt`
5.  Initialiser la base de données `cd db && ./init_db.sh && cd ..`
6.  Lancer le serveur `./main.py`

## A faire!
- [ ] Redirection préventive de garde

## Fini
- [X] Inscription (Page, en commun avec connexion)
- [X] Connexion (Page, en commun avec inscription)
- [X] Emprunt (Page/Bouton, en commun avec retour)
- [X] Retour (Page/Bouton, en commun avec emprunt)
- [X] Deconnexion (Bouton)
- [X] Desinscription (Formulaire)
- [X] Ajout livre par admin (Formulaire)
- [X] Retrait livre par admin (Bouton)
- [X] Accueil (Page)
