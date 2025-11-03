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
# ZONES ET ADRESSES
# -----------------------
ZONES = [
    "Grand Est",
    "Nouvelle-Aquitaine",
    "Auvergne-Rhône-Alpes",
    "Bourgogne-Franche-Comté",
    "Hauts-de-France",
    "Occitanie",
    "Normandie",
    "Centre-Val de Loire",
    "Pays de la Loire",
    "Bretagne",
    "Île-de-France",
    "Provence-Alpes-Côte d'Azur",
    "Corse",
    "La Réunion",
    "Guadeloupe"
]

ADRESSES_PAR_ZONE = {
    "Grand Est": [
        "12 Rue des Tanneurs, 67000 Strasbourg",
        "25 Boulevard Lundy, 51100 Reims",
        "8 Rue du Grand Cerf, 57000 Metz",
        "14 Avenue de Boufflers, 54000 Nancy",
        "3 Rue des Clefs, 68000 Colmar"
    ],
    "Nouvelle-Aquitaine": [
        "18 Cours de l'Intendance, 33000 Bordeaux",
        "42 Boulevard de Fleurus, 87000 Limoges",
        "7 Rue du Marché Notre-Dame, 86000 Poitiers",
        "15 Quai Georges Simenon, 17000 La Rochelle",
        "9 Avenue du Général de Gaulle, 64000 Pau",
        "22 Rue Port-Neuf, 64100 Bayonne",
        "5 Place Bugeaud, 24000 Périgueux"
    ],
    "Auvergne-Rhône-Alpes": [
        "10 Rue de la République, 69002 Lyon",
        "25 Boulevard Lafayette, 63000 Clermont-Ferrand",
        "18 Rue Lesdiguières, 38000 Grenoble",
        "7 Rue du Grand Moulin, 42000 Saint-Étienne",
        "12 Avenue d'Albigny, 74000 Annecy",
        "5 Rue Croix-d'Or, 73000 Chambéry",
        "9 Boulevard Maurice Clerc, 26000 Valence",
        "14 Rue Marchande, 38200 Vienne",
        "6 Rue du 4 Septembre, 01000 Bourg-en-Bresse",
        "3 Place du Plot, 43000 Le Puy-en-Velay",
        "8 Rue Barathon, 03100 Montluçon"
    ],
    "Bourgogne-Franche-Comté": [
        "15 Rue de la Liberté, 21000 Dijon",
        "8 Quai Veil Picard, 25000 Besançon",
        "12 Rue Jean Jaurès, 90000 Belfort",
        "5 Rue du Port, 71100 Chalon-sur-Saône",
        "20 Boulevard Vauban, 89000 Auxerre",
        "3 Rue du Château, 25200 Montbéliard",
        "7 Avenue François Mitterrand, 58000 Nevers"
    ],
    "Hauts-de-France": [
        "10 Place du Général de Gaulle, 59000 Lille",
        "5 Rue de la République, 80000 Amiens",
        "12 Boulevard Gambetta, 59100 Roubaix",
        "7 Avenue du Général Leclerc, 59200 Tourcoing",
        "3 Quai de la Citadelle, 59140 Dunkerque",
        "18 Rue Royale, 62100 Calais",
        "6 Rue de Famars, 59300 Valenciennes",
        "14 Rue de la Sous-Préfecture, 60000 Beauvais",
        "8 Boulevard Faidherbe, 02100 Saint-Quentin"
    ],
    "Occitanie": [
        "12 Rue du Taur, 31000 Toulouse",
        "18 Avenue du Président Wilson, 34000 Montpellier",
        "5 Rue de l'Horloge, 30000 Nîmes",
        "10 Boulevard Clemenceau, 66000 Perpignan",
        "7 Avenue Général Leclerc, 34500 Béziers",
        "3 Rue Jean Jaurès, 11100 Narbonne",
        "14 Rue de Verdun, 11000 Carcassonne",
        "9 Boulevard Jean Jaurès, 81000 Albi",
        "6 Rue des Fontaines, 82000 Montauban",
        "8 Avenue de la Marne, 65000 Tarbes",
        "11 Rue des Jardins, 12000 Rodez",
        "4 Place Urbain V, 48000 Mende",
        "15 Rue Gambetta, 46000 Cahors"
    ],
    "Normandie": [
        "10 Rue Jeanne d'Arc, 76000 Rouen",
        "12 Boulevard Bertrand, 14000 Caen",
        "5 Quai de Southampton, 76600 Le Havre",
        "8 Rue de la République, 50100 Cherbourg-en-Cotentin",
        "7 Rue du Général Leclerc, 27000 Évreux",
        "3 Avenue Carnot, 61000 Alençon",
        "14 Rue Saint-Michel, 14100 Lisieux"
    ],
    "Centre-Val de Loire": [
        "15 Rue Jeanne d'Arc, 45000 Orléans",
        "12 Boulevard Béranger, 37000 Tours",
        "7 Rue Grande, 18000 Bourges",
        "5 Avenue Marcel Proust, 28000 Chartres",
        "8 Rue du Château, 41000 Blois",
        "10 Boulevard de la République, 36000 Châteauroux",
        "3 Rue des Écoles, 18100 Vierzon",
        "14 Rue Saint-Michel, 45200 Montargis"
    ],
    "Pays de la Loire": [
        "10 Rue Crébillon, 44000 Nantes",
        "12 Boulevard du Roi René, 49000 Angers",
        "5 Rue de l'Éperon, 72000 Le Mans",
        "8 Avenue Robert Buron, 53000 Laval",
        "3 Quai de Saint-Nazaire, 44600 Saint-Nazaire",
        "14 Rue des Halles, 49300 Cholet",
        "7 Avenue de Gaulle, 85000 La Roche-sur-Yon",
        "6 Rue Franklin Roosevelt, 49400 Saumur",
        "9 Boulevard Clemenceau, 85100 Les Sables-d'Olonne"
    ],
    "Bretagne": [
        "Place de la Mairie, 35000 Rennes",
        "Place de la Liberté, 29200 Brest",
        "Parc du Chêne, 56100 Lorient",
        "Place Saint-Corentin, 29000 Quimper",
        "Place des Lices, 56000 Vannes",
        "Grand'Place, 35400 Saint-Malo",
        "Place du Maréchal Foch, 22000 Saint-Brieuc",
        "Place Charles de Gaulle, 35300 Fougères",
        "Place du Centre, 22300 Lannion",
        "Place Duclos, 22100 Dinan"
    ],
    "Île-de-France": [
        "81 rue de Reuilly, 75012 Paris",
        "110 rue Cambronne, 75015 Paris",
        "125 rue Paul Vaillant Couturier, 94140 Alfortville",
        "38 avenue Outrebon, 93250 Villemomble",
        "160 avenue du Général de Gaulle, 77270 Villeparisis",
        "5B rue Montagne Mons, 91200 Athis-Mons",
        "54 Grande Rue, 91290 Arpajon",
        "15 Grande Rue, 91580 Étréchy",
        "17 bis rue Aristide Briand, 91150 Étampes",
        "94 rue de Tolbiac, 75013 Paris",
        "9 rue du Maréchal Foch, 78250 Meulan-en-Yvelines",
        "8 avenue du Maréchal Joffre, 92000 Nanterre",
        "51 rue Cler, 75007 Paris",
        "57 boulevard Rouget de l'Isle, 93100 Montreuil",
        "125 bis boulevard de la Boissière, 93100 Montreuil"
    ],
    "Provence-Alpes-Côte d'Azur": [
        "61-63 Avenue Simone Veil, 06200 Nice",
        "455 Promenade des Anglais, 06200 Nice",
        "5 Rue du Congrès, 06000 Nice",
        "21 Rue d'Angleterre, 06000 Nice",
        "3 Rue Château Briand, Domaine des Oliviers, 06150 Cannes",
        "90 Boulevard Carnot, 06400 Cannes",
        "259 Avenue de Grasse, 06400 Cannes",
        "47 Chemin du Devens, 06150 Cannes",
        "159 Avenue du Docteur Bernard Foussier, 04100 Manosque",
        "Rue Léon Foucault, Parc de la Duranne, 13290 Aix-en-Provence",
        "Place de l'Hôtel-de-Ville, 13000 Aix-en-Provence",
        "2 Cours des Arts et Métiers, 13617 Aix-en-Provence",
        "9 Avenue Valéry Giscard d'Estaing, 06200 Nice",
        "215 Rue de la Coquillade, Eole Parc, 13540 Aix-en-Provence"
    ],
    "Corse": [
        "5 Rue Fesch, 20000 Ajaccio",
        "12 Boulevard Paoli, 20200 Bastia",
        "8 Rue Emmanuel Arène, 20250 Corte",
        "15 Avenue de la Plage, 20137 Porto-Vecchio",
        "3 Quai Landry, 20260 Calvi",
        "7 Rue du Général Leclerc, 20100 Sartène",
        "2 Rue du Gouverneur, 20169 Bonifacio"
    ],
    "La Réunion": [
        "10 Rue de Paris, 97400 Saint-Denis",
        "15 Boulevard du Front de Mer, 97410 Saint-Pierre",
        "8 Rue des Hibiscus, 97460 Saint-Paul",
        "5 Avenue des Camélias, 97430 Le Tampon",
        "12 Rue du Général de Gaulle, 97440 Saint-André",
        "7 Boulevard des Sources, 97450 Saint-Louis",
        "3 Rue des Fleurs, 97470 Saint-Benoît",
        "14 Avenue de la Plage, 97438 Sainte-Marie",
        "9 Rue des Thermes, 97413 Cilaos"
    ],
    "Guadeloupe": [
        "12 Rue Schoelcher, 97100 Basse-Terre",
        "8 Avenue de la Liberté, 97110 Pointe-à-Pitre",
        "5 Boulevard de l'Europe, 97118 Sainte-Anne",
        "10 Rue Victor Hugo, 97160 Le Gosier",
        "7 Rue de la République, 97115 Capesterre-Belle-Eau",
        "3 Rue des Palmiers, 97122 Baie-Mahault",
        "14 Avenue des Caraïbes, 97190 Saint-François",
        "9 Rue de l'Église, 97140 Petit-Bourg",
        "6 Rue du Marché, 97113 Gourbeyre",
        "11 Rue de la Plage, 97170 Saint-Claude",
        "2 Rue des Bougainvilliers, 97120 Le Moule"
    ]
}

# -----------------------
# ÉNUMÉRATIONS
# -----------------------
TYPEU = ["chaine assemblage", "scierie", "métallurgie", "fonderie"]

GAMMES = [
    "jardin et piscine", "mobilier intérieur", "plomberie et chauffage", "salle de bain et WC",
    "luminaire", "électricité et domotique", "quincaillerie", "cuisine",
    "peinture et droguerie", "carrelage et parquet", "matériaux de construction"
]

DEPTS = ["fabrication", "assemblage", "RH", "expédition", "logistique", "direction", "finance"]

PV_TYPES = ["GSB", "Brico-Express"]

# Noms réalistes pour les points de vente par type
PV_NAMES = {
    "GSB": [
        "Brico Dépôt", "Leroy Merlin", "Castorama", "Weldom", "Bricomarché",
        "Point P", "Gedimat", "BigMat", "Brico Pro", "Mr.Bricolage",
        "Bricoman", "Brico Cash", "La Plateforme du Bâtiment", "Brico Leclerc",
        "Brico Centre", "Entrepôt du Bricolage", "Brico Arche", "King Jouet Bricolage"
    ],
    "Brico-Express": [
        "Brico Minute", "Brico Shop", "Brico Corner", "Express Bricolage",
        "Brico Plus", "Quick Brico", "Brico Service", "Brico Direct",
        "Brico Rapide", "Brico Point", "Allo Brico", "Brico Store",
        "Brico Facile", "Flash Brico", "Brico Express +", "Top Brico"
    ]
}

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
