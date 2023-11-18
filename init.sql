CREATE TABLE UTILISATEUR(
    id INT UNIQUE AUTO_INCREMENT,
    nom VARCHAR(32) NOT NULL,
    prenom VARCHAR(32) NOT NULL,
    mdp VARCHAR(256) NOT NULL,
    email VARCHAR(32) NOT NULL,
    genre VARCHAR(16) NOT NULL,
    date_naissance DATE NOT NULL,
    grade INT,
    PRIMARY KEY (id),
);

CREATE TABLE LIVRE(
    id INT AUTO_INCREMENT,
    titre VARCHAR(32) NOT NULL,
    genre VARCHAR(32) NOT NULL,
    date_parution DATE NOT NULL,
    rayon VARCHAR(16) NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE EMPRUNTS(
    id INT AUTO_INCREMENT NOT NULL,
    id_u INT NOT NULL,
    id_l INT NOT NULL,
    date_emprunt DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_u) REFERENCES utilisateur(id),
    FOREIGN KEY (id_l) REFERENCES livre(id),
);