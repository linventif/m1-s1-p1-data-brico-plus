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

# Bases
QUALIFICATIONS = {
    # Niveau: [(diplome_complet, salaire_min, salaire_max, base_diplome)]
    3: [
        # Bases
        ("CAP", 11.0, 15.0),
        ("BEP", 11.5, 15.0),
        # Spécialisations
        ("CAP Électricien", 11.5, 16.0, "CAP"),
        ("BEP Chaîne Assemblage", 11.5, 15.0, "BEP"),
        ("BEP Scierie", 11.5, 15.0, "BEP"),
        ("BEP Métallurgie", 11.5, 15.0, "BEP"),
        ("BEP Fonderie", 11.5, 15.0, "BEP"),
        ("BEP Fabrication", 11.5, 15.0, "BEP"),
        ("BEP Assemblage", 11.5, 15.0, "BEP"),
        ("BEP RH", 11.5, 15.0, "BEP"),
        ("BEP Expédition", 11.5, 15.0, "BEP"),
        ("BEP Logistique", 11.5, 15.0, "BEP"),
        ("BEP Direction", 11.5, 15.0, "BEP"),
        ("BEP Finance", 11.5, 15.0, "BEP"),
        ("CAP Chaîne Assemblage", 11.0, 15.0, "CAP"),
        ("CAP Scierie", 11.0, 15.0, "CAP"),
        ("CAP Métallurgie", 11.0, 15.0, "CAP"),
        ("CAP Fonderie", 11.0, 15.0, "CAP"),
        ("CAP Fabrication", 11.0, 15.0, "CAP"),
        ("CAP Assemblage", 11.0, 15.0, "CAP"),
        ("CAP RH", 11.0, 15.0, "CAP"),
        ("CAP Expédition", 11.0, 15.0, "CAP"),
        ("CAP Logistique", 11.0, 15.0, "CAP"),
        ("CAP Direction", 11.0, 15.0, "CAP"),
        ("CAP Finance", 11.0, 15.0, "CAP"),
    ],
    4: [
        # Bases
        ("Bac Pro", 13.0, 17.0),
        ("BP", 14.0, 18.0),
        ("Bac", 13.0, 16.5),
        # Spécialisations BP
        ("BP Chaîne Assemblage", 14.0, 18.0, "BP"),
        ("BP Scierie", 14.0, 18.0, "BP"),
        ("BP Métallurgie", 14.0, 18.0, "BP"),
        ("BP Fonderie", 14.0, 18.0, "BP"),
        ("BP Fabrication", 14.0, 18.0, "BP"),
        ("BP Assemblage", 14.0, 18.0, "BP"),
        ("BP RH", 14.0, 18.0, "BP"),
        ("BP Expédition", 14.0, 18.0, "BP"),
        ("BP Logistique", 14.0, 18.0, "BP"),
        ("BP Direction", 14.0, 18.0, "BP"),
        ("BP Finance", 14.0, 18.0, "BP"),
        # Spécialisations Bac Pro
        ("Bac Pro Électrotechnique", 13.5, 18.0, "Bac Pro"),
        ("Bac Pro Chaîne Assemblage", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Scierie", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Métallurgie", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Fonderie", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Fabrication", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Assemblage", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro RH", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Expédition", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Logistique", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Direction", 13.0, 17.0, "Bac Pro"),
        ("Bac Pro Finance", 13.0, 17.0, "Bac Pro"),
    ],
    5: [
        # Bases
        ("BTS", 15.0, 22.0),
        ("DUT", 15.5, 22.0),
        # Spécialisations
        ("DUT Chaîne Assemblage", 15.5, 22.0, "DUT"),
        ("DUT Scierie", 15.5, 22.0, "DUT"),
        ("DUT Métallurgie", 15.5, 22.0, "DUT"),
        ("DUT Fonderie", 15.5, 22.0, "DUT"),
        ("DUT Fabrication", 15.5, 22.0, "DUT"),
        ("DUT Assemblage", 15.5, 22.0, "DUT"),
        ("DUT RH", 15.5, 22.0, "DUT"),
        ("DUT Expédition", 15.5, 22.0, "DUT"),
        ("DUT Logistique", 15.5, 22.0, "DUT"),
        ("DUT Direction", 15.5, 22.0, "DUT"),
        ("DUT Finance", 15.5, 22.0, "DUT"),
        ("BTS Électrotechnique", 15.5, 23.0, "BTS"),
        ("BTS Chaîne Assemblage", 15.0, 22.0, "BTS"),
        ("BTS Scierie", 15.0, 22.0, "BTS"),
        ("BTS Métallurgie", 15.0, 22.0, "BTS"),
        ("BTS Fonderie", 15.0, 22.0, "BTS"),
        ("BTS Fabrication", 15.0, 22.0, "BTS"),
        ("BTS Assemblage", 15.0, 22.0, "BTS"),
        ("BTS RH", 15.0, 22.0, "BTS"),
        ("BTS Expédition", 15.0, 22.0, "BTS"),
        ("BTS Logistique", 15.0, 22.0, "BTS"),
        ("BTS Direction", 15.0, 22.0, "BTS"),
        ("BTS Finance", 15.0, 22.0, "BTS"),
    ],
    6: [
        # Bases
        ("Licence Pro", 18.0, 24.0),
        ("BUT", 18.5, 25.0),
        ("Licence", 18.0, 23.5),
        # Spécialisations Licence Pro
        ("Licence Pro Chaîne Assemblage", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Scierie", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Métallurgie", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Fonderie", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Fabrication", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Assemblage", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro RH", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Expédition", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Logistique", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Direction", 18.0, 24.0, "Licence Pro"),
        ("Licence Pro Finance", 18.0, 24.0, "Licence Pro"),
        # Spécialisations BUT
        ("BUT Chaîne Assemblage", 18.5, 25.0, "BUT"),
        ("BUT Scierie", 18.5, 25.0, "BUT"),
        ("BUT Métallurgie", 18.5, 25.0, "BUT"),
        ("BUT Fonderie", 18.5, 25.0, "BUT"),
        ("BUT Fabrication", 18.5, 25.0, "BUT"),
        ("BUT Assemblage", 18.5, 25.0, "BUT"),
        ("BUT RH", 18.5, 25.0, "BUT"),
        ("BUT Expédition", 18.5, 25.0, "BUT"),
        ("BUT Logistique", 18.5, 25.0, "BUT"),
        ("BUT Direction", 18.5, 25.0, "BUT"),
        ("BUT Finance", 18.5, 25.0, "BUT"),
        # Spécialisations Licence
        ("Licence Pro Métiers de l'Électricité", 18.5, 25.0, "Licence"),
        ("Licence Chaîne Assemblage", 18.0, 23.5, "Licence"),
        ("Licence Scierie", 18.0, 23.5, "Licence"),
        ("Licence Métallurgie", 18.0, 23.5, "Licence"),
        ("Licence Fonderie", 18.0, 23.5, "Licence"),
        ("Licence Fabrication", 18.0, 23.5, "Licence"),
        ("Licence Assemblage", 18.0, 23.5, "Licence"),
        ("Licence RH", 18.0, 23.5, "Licence"),
        ("Licence Expédition", 18.0, 23.5, "Licence"),
        ("Licence Logistique", 18.0, 23.5, "Licence"),
        ("Licence Direction", 18.0, 23.5, "Licence"),
        ("Licence Finance", 18.0, 23.5, "Licence"),
    ],
    7: [
        # Bases
        ("Master", 22.0, 30.0),
        ("Ingénieur", 24.0, 35.0),
        # Spécialisations
        ("Ingénieur Chaîne Assemblage", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Scierie", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Métallurgie", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Fonderie", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Fabrication", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Assemblage", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur RH", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Expédition", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Logistique", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Direction", 24.0, 35.0, "Ingénieur"),
        ("Ingénieur Finance", 24.0, 35.0, "Ingénieur"),
        ("Master Énergétique et Électrique", 23.0, 32.0, "Master"),
        ("Master Chaîne Assemblage", 22.0, 30.0, "Master"),
        ("Master Scierie", 22.0, 30.0, "Master"),
        ("Master Métallurgie", 22.0, 30.0, "Master"),
        ("Master Fonderie", 22.0, 30.0, "Master"),
        ("Master Fabrication", 22.0, 30.0, "Master"),
        ("Master Assemblage", 22.0, 30.0, "Master"),
        ("Master RH", 22.0, 30.0, "Master"),
        ("Master Expédition", 22.0, 30.0, "Master"),
        ("Master Logistique", 22.0, 30.0, "Master"),
        ("Master Direction", 22.0, 30.0, "Master"),
        ("Master Finance", 22.0, 30.0, "Master"),
    ],
    8: [
        # Bases
        ("Doctorat", 28.0, 40.0),
        # Spécialisations Doctorat
        ("Doctorat en Génie Électrique", 29.0, 42.0, "Doctorat"),
        ("Doctorat Chaîne Assemblage", 28.0, 40.0, "Doctorat"),
        ("Doctorat Scierie", 28.0, 40.0, "Doctorat"),
        ("Doctorat Métallurgie", 28.0, 40.0, "Doctorat"),
        ("Doctorat Fonderie", 28.0, 40.0, "Doctorat"),
        ("Doctorat Fabrication", 28.0, 40.0, "Doctorat"),
        ("Doctorat Assemblage", 28.0, 40.0, "Doctorat"),
        ("Doctorat RH", 28.0, 40.0, "Doctorat"),
        ("Doctorat Expédition", 28.0, 40.0, "Doctorat"),
        ("Doctorat Logistique", 28.0, 40.0, "Doctorat"),
        ("Doctorat Direction", 28.0, 40.0, "Doctorat"),
        ("Doctorat Finance", 28.0, 40.0, "Doctorat"),
    ],
}

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
# RECETTES DE PRODUITS
# Format: (nom_produit, gamme, type_usine)
# -----------------------
# create object product
class Product:
    def __init__(self, name, gamme, type_usine):
        self.name = name
        self.gamme = gamme
        self.type_usine = type_usine
        self.recettes = []


RECETTES_PRODUITS = [
    # Produits de chaine assemblage
    ("Tondeuse électrique", "jardin et piscine", "chaine assemblage"),
    ("Tondeuse thermique", "jardin et piscine", "chaine assemblage"),
    ("Coupe-bordures", "jardin et piscine", "chaine assemblage"),
    ("Taille-haie", "jardin et piscine", "chaine assemblage"),
    ("Souffleur", "jardin et piscine", "chaine assemblage"),
    ("Scarificateur", "jardin et piscine", "chaine assemblage"),
    ("Bineuse", "jardin et piscine", "chaine assemblage"),
    ("Pompe piscine", "jardin et piscine", "chaine assemblage"),
    ("Filtre piscine", "jardin et piscine", "chaine assemblage"),
    ("Robot piscine", "jardin et piscine", "chaine assemblage"),
    ("Échelle piscine", "jardin et piscine", "chaine assemblage"),
    ("Bâche piscine", "jardin et piscine", "chaine assemblage"),
    ("Alarme piscine", "jardin et piscine", "chaine assemblage"),
    ("Canapé d'angle", "mobilier intérieur", "chaine assemblage"),
    ("Fauteuil relax", "mobilier intérieur", "chaine assemblage"),
    ("Table basse", "mobilier intérieur", "chaine assemblage"),
    ("Bibliothèque", "mobilier intérieur", "chaine assemblage"),
    ("Armoire penderie", "mobilier intérieur", "chaine assemblage"),
    ("Commode", "mobilier intérieur", "chaine assemblage"),
    ("Table à manger", "mobilier intérieur", "chaine assemblage"),
    ("Chaises", "mobilier intérieur", "chaine assemblage"),
    ("Lit", "mobilier intérieur", "chaine assemblage"),
    ("Matelas", "mobilier intérieur", "chaine assemblage"),
    ("Sommier", "mobilier intérieur", "chaine assemblage"),
    ("Table de chevet", "mobilier intérieur", "chaine assemblage"),
    ("Bureau", "mobilier intérieur", "chaine assemblage"),
    ("Étagères", "mobilier intérieur", "chaine assemblage"),
    ("Perceuse visseuse", "matériaux de construction", "chaine assemblage"),
    ("Perceuse à percussion", "matériaux de construction", "chaine assemblage"),
    ("Visseuse impact", "matériaux de construction", "chaine assemblage"),
    ("Scie circulaire", "matériaux de construction", "chaine assemblage"),
    ("Scie sauteuse", "matériaux de construction", "chaine assemblage"),
    ("Ponceuse orbitale", "matériaux de construction", "chaine assemblage"),
    ("Ponceuse excentrique", "matériaux de construction", "chaine assemblage"),
    ("Défonceuse", "matériaux de construction", "chaine assemblage"),
    ("Raboteuse", "matériaux de construction", "chaine assemblage"),
    ("Meuleuse", "matériaux de construction", "chaine assemblage"),
    ("Perforateur", "matériaux de construction", "chaine assemblage"),
    ("Marteau piqueur", "matériaux de construction", "chaine assemblage"),
    ("Tableau électrique CA", "électricité et domotique", "chaine assemblage"),
    ("Disjoncteur CA", "électricité et domotique", "chaine assemblage"),
    ("Interrupteur différentiel CA", "électricité et domotique", "chaine assemblage"),
    ("Box domotique", "électricité et domotique", "chaine assemblage"),
    ("Prise connectée", "électricité et domotique", "chaine assemblage"),
    ("Interrupteur connecté", "électricité et domotique", "chaine assemblage"),
    ("Détecteur mouvement", "électricité et domotique", "chaine assemblage"),
    ("Caméra surveillance", "électricité et domotique", "chaine assemblage"),
    ("Portier vidéo", "électricité et domotique", "chaine assemblage"),

    # Produits de scierie
    ("Planche pin", "jardin et piscine", "scierie"),
    ("Planche chêne", "jardin et piscine", "scierie"),
    ("Lame terrasse", "jardin et piscine", "scierie"),
    ("Poteau bois", "jardin et piscine", "scierie"),
    ("Panneau bois", "jardin et piscine", "scierie"),
    ("Bardage bois", "jardin et piscine", "scierie"),
    ("Cloture bois", "jardin et piscine", "scierie"),
    ("Pergola bois", "jardin et piscine", "scierie"),
    ("Abri jardin", "jardin et piscine", "scierie"),
    ("Jardinière bois", "jardin et piscine", "scierie"),
    ("Bac à sable", "jardin et piscine", "scierie"),
    ("Balançoire", "jardin et piscine", "scierie"),
    ("Plan travail bois", "mobilier intérieur", "scierie"),
    ("Étagère pin", "mobilier intérieur", "scierie"),
    ("Étagère chêne", "mobilier intérieur", "scierie"),
    ("Planche étagère", "mobilier intérieur", "scierie"),
    ("Tasseau bois", "mobilier intérieur", "scierie"),
    ("Moulure bois", "mobilier intérieur", "scierie"),
    ("Corniche bois", "mobilier intérieur", "scierie"),
    ("Plinthe bois", "mobilier intérieur", "scierie"),
    ("Parquet massif", "mobilier intérieur", "scierie"),
    ("Parquet contrecollé", "mobilier intérieur", "scierie"),
    ("Stratifié", "mobilier intérieur", "scierie"),
    ("Lambris", "mobilier intérieur", "scierie"),
    ("Parquet chêne massif", "carrelage et parquet", "scierie"),
    ("Parquet hêtre", "carrelage et parquet", "scierie"),
    ("Parquet bambou", "carrelage et parquet", "scierie"),
    ("Parquet flottant", "carrelage et parquet", "scierie"),
    ("Lame PVC", "carrelage et parquet", "scierie"),
    ("Sol vinyle", "carrelage et parquet", "scierie"),
    ("Sous-couche parquet", "carrelage et parquet", "scierie"),
    ("Poutre bois", "matériaux de construction", "scierie"),
    ("Chevron", "matériaux de construction", "scierie"),
    ("Latte", "matériaux de construction", "scierie"),
    ("Madrier", "matériaux de construction", "scierie"),
    ("Planche coffrage", "matériaux de construction", "scierie"),
    ("OSB", "matériaux de construction", "scierie"),
    ("Contreplaqué", "matériaux de construction", "scierie"),
    ("Médium MDF", "matériaux de construction", "scierie"),
    ("Aggloméré", "matériaux de construction", "scierie"),
    ("Panneau OSB", "matériaux de construction", "scierie"),

    # Produits de métallurgie
    ("Vis inox", "quincaillerie", "métallurgie"),
    ("Boulon acier", "quincaillerie", "métallurgie"),
    ("Écrou", "quincaillerie", "métallurgie"),
    ("Rondelle", "quincaillerie", "métallurgie"),
    ("Clou", "quincaillerie", "métallurgie"),
    ("Pointe", "quincaillerie", "métallurgie"),
    ("Cheville", "quincaillerie", "métallurgie"),
    ("Tire-fond", "quincaillerie", "métallurgie"),
    ("Tige filetée", "quincaillerie", "métallurgie"),
    ("Chaîne acier", "quincaillerie", "métallurgie"),
    ("Câble acier", "quincaillerie", "métallurgie"),
    ("Serrure", "quincaillerie", "métallurgie"),
    ("Verrou", "quincaillerie", "métallurgie"),
    ("Cadenas", "quincaillerie", "métallurgie"),
    ("Gond", "quincaillerie", "métallurgie"),
    ("Paumelle", "quincaillerie", "métallurgie"),
    ("Charnière", "quincaillerie", "métallurgie"),
    ("Tube cuivre", "plomberie et chauffage", "métallurgie"),
    ("Raccord cuivre", "plomberie et chauffage", "métallurgie"),
    ("Tube PER", "plomberie et chauffage", "métallurgie"),
    ("Raccord PER", "plomberie et chauffage", "métallurgie"),
    ("Radiateur acier", "plomberie et chauffage", "métallurgie"),
    ("Radiateur fonte", "plomberie et chauffage", "métallurgie"),
    ("Collecteur chauffage", "plomberie et chauffage", "métallurgie"),
    ("Vanne d'arrêt", "plomberie et chauffage", "métallurgie"),
    ("Clapet anti-retour", "plomberie et chauffage", "métallurgie"),
    ("Détendeur gaz", "plomberie et chauffage", "métallurgie"),
    ("Gaine électrique", "électricité et domotique", "métallurgie"),
    ("Tube IRL", "électricité et domotique", "métallurgie"),
    ("Chemin câbles", "électricité et domotique", "métallurgie"),
    ("Goulottes", "électricité et domotique", "métallurgie"),
    ("Boîtier étanche", "électricité et domotique", "métallurgie"),
    ("Armoire électrique", "électricité et domotique", "métallurgie"),
    ("Rail DIN", "électricité et domotique", "métallurgie"),
    ("Borne connexion", "électricité et domotique", "métallurgie"),
    ("Clé plate", "matériaux de construction", "métallurgie"),
    ("Clé à pipe", "matériaux de construction", "métallurgie"),
    ("Tournevis", "matériaux de construction", "métallurgie"),
    ("Pince", "matériaux de construction", "métallurgie"),
    ("Serre-joint", "matériaux de construction", "métallurgie"),
    ("Étau", "matériaux de construction", "métallurgie"),
    ("Lime", "matériaux de construction", "métallurgie"),
    ("Râpe", "matériaux de construction", "métallurgie"),
    ("Burins", "matériaux de construction", "métallurgie"),
    ("Pointeau", "matériaux de construction", "métallurgie"),
    ("Compas", "matériaux de construction", "métallurgie"),

    # Produits de fonderie
    ("Mitigeur cuisine", "plomberie et chauffage", "fonderie"),
    ("Mitigeur douche", "plomberie et chauffage", "fonderie"),
    ("Robinet lavabo", "plomberie et chauffage", "fonderie"),
    ("Robinet évier", "plomberie et chauffage", "fonderie"),
    ("Douchette", "plomberie et chauffage", "fonderie"),
    ("Colonne douche", "plomberie et chauffage", "fonderie"),
    ("Bonde", "plomberie et chauffage", "fonderie"),
    ("Siphon", "plomberie et chauffage", "fonderie"),
    ("Collecteur fonte", "plomberie et chauffage", "fonderie"),
    ("Regard fonte", "plomberie et chauffage", "fonderie"),
    ("Bouche égout", "plomberie et chauffage", "fonderie"),
    ("Robinet baignoire", "salle de bain et WC", "fonderie"),
    ("Mitigeur thermostatique", "salle de bain et WC", "fonderie"),
    ("Pomme douche", "salle de bain et WC", "fonderie"),
    ("Flexible douche", "salle de bain et WC", "fonderie"),
    ("Barre douche", "salle de bain et WC", "fonderie"),
    ("Support douchette", "salle de bain et WC", "fonderie"),
    ("Évacuation douche", "salle de bain et WC", "fonderie"),
    ("Bonde baignoire", "salle de bain et WC", "fonderie"),
    ("Trop-plein", "salle de bain et WC", "fonderie"),
    ("Applique murale", "luminaire", "fonderie"),
    ("Suspension", "luminaire", "fonderie"),
    ("Lustre", "luminaire", "fonderie"),
    ("Spot encastrable", "luminaire", "fonderie"),
    ("Réglette LED", "luminaire", "fonderie"),
    ("Plafonnier", "luminaire", "fonderie"),
    ("Lampadaire", "luminaire", "fonderie"),
    ("Lampe bureau", "luminaire", "fonderie"),
    ("Projecteur LED", "luminaire", "fonderie"),
    ("Borne éclairage", "luminaire", "fonderie"),
    ("Balise LED", "luminaire", "fonderie"),
    ("Tableau électrique FO", "électricité et domotique", "fonderie"),
    ("Disjoncteur FO", "électricité et domotique", "fonderie"),
    ("Interrupteur différentiel FO", "électricité et domotique", "fonderie"),
    ("Box domotique FO", "électricité et domotique", "fonderie"),
    ("Prise connectée FO", "électricité et domotique", "fonderie"),
    ("Interrupteur connecté FO", "électricité et domotique", "fonderie"),
    ("Détecteur mouvement FO", "électricité et domotique", "fonderie"),
    ("Caméra surveillance FO", "électricité et domotique", "fonderie"),
    ("Portier vidéo FO", "électricité et domotique", "fonderie"),
    ("Poignée porte", "quincaillerie", "fonderie"),
    ("Béquille", "quincaillerie", "fonderie"),
    ("Crémone", "quincaillerie", "fonderie"),
    ("Espagnolette", "quincaillerie", "fonderie"),
    ("Ferme-porte", "quincaillerie", "fonderie"),
    ("Butée porte", "quincaillerie", "fonderie"),
    ("Heurtoir", "quincaillerie", "fonderie"),
    ("Boîte aux lettres", "quincaillerie", "fonderie"),
]