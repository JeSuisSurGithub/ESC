CREATE TABLE utilisateur(
    id INT AUTO_INCREMENT,
    nom VARCHAR(32) NOT NULL,
    prenom VARCHAR(32) NOT NULL,
    email VARCHAR(32) NOT NULL,
    date_naissance DATE NOT NULL,
    sexe VARCHAR(16) NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE livre(
    id INT AUTO_INCREMENT,
    titre VARCHAR(32) NOT NULL,
    genre VARCHAR(32) NOT NULL,
    data_parution DATE NOT NULL,
    rayon VARCHAR(16) NOT NULL,
    PRIMARY KEY (id),
);

CREATE TABLE emprunts(
    id INT AUTO_INCREMENT NOT NULL,
    id_u INT NOT NULL,
    id_l INT NOT NULL,
    date_emprunt DATE NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (id_u) REFERENCES utilisateur(id),
    FOREIGN KEY (id_l) REFERENCES livre(id),
);