# -*- coding: utf-8 -*-
"""
Constantes et référentiels de données
"""

import datetime as dt

# -----------------------
# RÉFÉRENTIELS FRANCE
# -----------------------
HG_CITIES = [
    ("Toulouse", "31000"), ("Toulouse", "31100"), ("Toulouse", "31200"), ("Toulouse", "31300"),
    ("Toulouse", "31400"), ("Toulouse", "31500"), ("Blagnac", "31700"), ("Colomiers", "31770"),
    ("Tournefeuille", "31170"), ("Balma", "31130"), ("Muret", "31600"), ("Ramonville-Saint-Agne", "31520"),
    ("Saint-Gaudens", "31800"), ("L'Union", "31240"), ("Cugnaux", "31270"), ("Labège", "31670"),
    ("Plaisance-du-Touch", "31830"), ("Castanet-Tolosan", "31320"), ("Fronton", "31620"), ("Grenade", "31330")
]

FR_CITIES = [
    ("Bordeaux", "33000"), ("Paris", "75011"), ("Lyon", "69007"), ("Marseille", "13008"),
    ("Lille", "59800"), ("Nantes", "44000"), ("Rennes", "35000"), ("Strasbourg", "67000"),
    ("Montpellier", "34000"), ("Nice", "06000"), ("Dijon", "21000"), ("Grenoble", "38000"),
    ("Le Mans", "72000"), ("Tours", "37000"), ("Brest", "29200"), ("Clermont-Ferrand", "63000")
]

# -----------------------
# ÉNUMÉRATIONS
# -----------------------
TYPEU = ["chaine assemblage", "scierie", "métallurgie", "fonderie"]

GAMMES = [
    "jardin et piscine", "mobilier intérieur", "plomberie et chauffage", "salle de bain et WC",
    "luminaire, électricité et domotique", "quincaillerie", "cuisine",
    "peinture et droguerie", "carrelage et parquet", "matériaux de construction"
]

DEPTS = ["fabrication", "assemblage", "RH", "expédition", "logistique", "direction", "finance"]

PV_TYPES = ["GSB", "Brico-Express"]

# -----------------------
# QUALIFICATIONS
# -----------------------
QUALIFICATIONS = {
    # Niveau: (Nom diplôme, taux min €/h, taux max €/h)
    3: [("CAP", 11.0, 15.0), ("BEP", 11.5, 15.0)],
    4: [("Bac Pro", 13.0, 17.0), ("BP", 14.0, 18.0), ("Bac", 13.0, 16.5)],
    5: [("BTS", 15.0, 22.0), ("DUT", 15.5, 22.0)],
    6: [("Licence Pro", 18.0, 24.0), ("BUT", 18.5, 25.0), ("Licence", 18.0, 23.5)],
    7: [("Master", 22.0, 30.0), ("Ingénieur", 24.0, 35.0)],
    8: [("Doctorat", 28.0, 40.0)]
}

# -----------------------
# VOLUMÉTRIE
# -----------------------
N_EMP = 50
N_QUALIF = 50
N_USINES = 15
N_PV = 50
N_PRODUITS = 100
N_CAL1 = 50
N_CAL2 = 50
YEAR_NOW = dt.date.today().year
MONTH_NOW = dt.date.today().month

# -----------------------
# PRODUITS PAR TYPE D'USINE
# -----------------------
PRODUITS_PAR_TYPE = {
    "chaine assemblage": {
        "jardin et piscine": [
            "Tondeuse électrique", "Tondeuse thermique", "Coupe-bordures", "Taille-haie",
            "Souffleur", "Scarificateur", "Bineuse", "Pompe piscine", "Filtre piscine",
            "Robot piscine", "Échelle piscine", "Bâche piscine", "Alarme piscine"
        ],
        "mobilier intérieur": [
            "Canapé d'angle", "Fauteuil relax", "Table basse", "Bibliothèque",
            "Armoire penderie", "Commode", "Table à manger", "Chaises", "Lit",
            "Matelas", "Sommier", "Table de chevet", "Bureau", "Étagères"
        ],
        "matériaux de construction": [
            "Perceuse visseuse", "Perceuse à percussion", "Visseuse impact",
            "Scie circulaire", "Scie sauteuse", "Ponceuse orbitale", "Ponceuse excentrique",
            "Défonceuse", "Raboteuse", "Meuleuse", "Perforateur", "Marteau piqueur"
        ],
        "luminaire, électricité et domotique": [
            "Tableau électrique", "Disjoncteur", "Interrupteur différentiel",
            "Box domotique", "Prise connectée", "Interrupteur connecté",
            "Détecteur mouvement", "Caméra surveillance", "Portier vidéo"
        ]
    },
    "scierie": {
        "jardin et piscine": [
            "Planche pin", "Planche chêne", "Lame terrasse", "Poteau bois",
            "Panneau bois", "Bardage bois", "Cloture bois", "Pergola bois",
            "Abri jardin", "Jardinière bois", "Bac à sable", "Balançoire"
        ],
        "mobilier intérieur": [
            "Plan travail bois", "Étagère pin", "Étagère chêne", "Planche étagère",
            "Tasseau bois", "Moulure bois", "Corniche bois", "Plinthe bois",
            "Parquet massif", "Parquet contrecollé", "Stratifié", "Lambris"
        ],
        "carrelage et parquet": [
            "Parquet chêne massif", "Parquet hêtre", "Parquet bambou",
            "Parquet flottant", "Lame PVC", "Sol vinyle", "Sous-couche parquet"
        ],
        "matériaux de construction": [
            "Poutre bois", "Chevron", "Latte", "Madrier", "Planche coffrage",
            "OSB", "Contreplaqué", "Médium MDF", "Aggloméré", "Panneau OSB"
        ]
    },
    "métallurgie": {
        "quincaillerie": [
            "Vis inox", "Boulon acier", "Écrou", "Rondelle", "Clou", "Pointe",
            "Cheville", "Tire-fond", "Tige filetée", "Chaîne acier", "Câble acier",
            "Serrure", "Verrou", "Cadenas", "Gond", "Paumelle", "Charnière"
        ],
        "plomberie et chauffage": [
            "Tube cuivre", "Raccord cuivre", "Tube PER", "Raccord PER",
            "Radiateur acier", "Radiateur fonte", "Collecteur chauffage",
            "Vanne d'arrêt", "Clapet anti-retour", "Détendeur gaz"
        ],
        "luminaire, électricité et domotique": [
            "Gaine électrique", "Tube IRL", "Chemin câbles", "Goulottes",
            "Boîtier étanche", "Armoire électrique", "Rail DIN", "Borne connexion"
        ],
        "matériaux de construction": [
            "Clé plate", "Clé à pipe", "Tournevis", "Pince", "Serre-joint",
            "Étau", "Lime", "Râpe", "Burins", "Pointeau", "Compas"
        ]
    },
    "fonderie": {
        "plomberie et chauffage": [
            "Mitigeur cuisine", "Mitigeur douche", "Robinet lavabo",
            "Robinet évier", "Douchette", "Colonne douche", "Bonde",
            "Siphon", "Collecteur fonte", "Regard fonte", "Bouche égout"
        ],
        "salle de bain et WC": [
            "Robinet baignoire", "Mitigeur thermostatique", "Pomme douche",
            "Flexible douche", "Barre douche", "Support douchette",
            "Évacuation douche", "Bonde baignoire", "Trop-plein"
        ],
        "luminaire, électricité et domotique": [
            "Applique murale", "Suspension", "Lustre", "Spot encastrable",
            "Réglette LED", "Plafonnier", "Lampadaire", "Lampe bureau",
            "Projecteur LED", "Borne éclairage", "Balise LED"
        ],
        "quincaillerie": [
            "Poignée porte", "Béquille", "Crémone", "Espagnolette",
            "Ferme-porte", "Butée porte", "Heurtoir", "Boîte aux lettres"
        ]
    }
}
