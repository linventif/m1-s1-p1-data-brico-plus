TYPEU = ["chaine assemblage", "scierie", "métallurgie", "fonderie"]

GAMMES = [
    "jardin et piscine", "mobilier intérieur", "plomberie et chauffage", "salle de bain et WC",
    "luminaire", "électricité et domotique", "quincaillerie", "cuisine",
    "peinture et droguerie", "carrelage et parquet", "matériaux de construction"
]

DEPTS = ["fabrication", "assemblage", "RH", "expédition", "logistique", "direction", "finance"]

PV_TYPES = ["GSB", "Brico-Express"]

PV_NAMES = {
    "GSB": [
        "Brico Dépôt", "Leroy Merlin", "Castorama", "Weldom", "Bricomarché",
        "Point P", "Gedimat", "BigMat", "Brico Pro", "Mr.Bricolage",
        "Bricoman", "Brico Cash", "La Plateforme du Bâtiment", "Brico Leclerc",
        "Brico Centre", "Entrepôt du Bricolage", "Brico Arche", "King Jouet Bricolage"
    ],
    "Brico-Express": [
        "Brico Express"
    ]
}

# Bases
QUALIFICATIONS_PROBABILITIES = {
    3: 0.20,  # CAP, BEP
    4: 0.30,  # Bac Pro, BP, Bac
    5: 0.20,  # BTS, DUT
    6: 0.15,  # Licence Pro, BUT, Licence
    7: 0.10,   # Master
    8: 0.05,   # Doctorat
}

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


# marques{ gamme: [marque1, marque2, ...] }
MARQUES = {
    "jardin et piscine": [
        "Gardena", "Husqvarna", "Kärcher", "Bosch", "Makita", "Stihl", "Intex", "Bestway", "Gré", "Ubbink", "Aquazendo", "Ribiland", "Oase", "Claber", "Vilmorin"
    ],
    "mobilier intérieur": [
        "IKEA", "Conforama", "Maisons du Monde", "Habitat", "Alinéa", "Fly", "H&H", "Roche Bobois", "La Redoute", "Cuir Center", "Miliboo", "BoConcept", "Poltronesofà", "Ligne Roset", "Meubles Gautier"
    ],
    "plomberie et chauffage": [
        "Grohe", "Hansgrohe", "Jacob Delafon", "Franke", "Atlantic", "Thermor", "Saunier Duval", "Vaillant", "Ariston", "De Dietrich", "Chaffoteaux", "Fleck", "SFA", "Duravit", "Ideal Standard"
    ],
    "salle de bain et WC": [
        "Jacob Delafon", "Duravit", "Grohe", "Hansgrohe", "Ideal Standard", "Villeroy & Boch", "Allibert", "Geberit", "Porcher", "Laufen", "Roca", "SFA", "Leda", "Aquarine", "Lapeyre"
    ],
    "cuisine": [
        "Schmidt", "Mobalpa", "IKEA", "Cuisine Plus", "Cuisinella", "Arthur Bonnet", "Snaidero", "Leicht", "Bultaup", "Siemens", "Bosch", "Whirlpool", "Electrolux", "De Dietrich", "Brandt"
    ],
    "luminaire": [
        "Philips", "Osram", "Eglo", "Paulmann", "Lucide", "Artemide", "Faro Barcelona", "Massive", "Slamp", "Flos", "Kartell", "Luceplan", "Vibia", "Trio Lighting", "Mantra"
    ],
    "électricité et domotique": [
        "Legrand", "Schneider Electric", "Somfy", "Netatmo", "Delta Dore", "Bosch Smart Home", "Philips Hue", "Fibaro", "Nodon", "Gira", "Hager", "BTicino", "ABB", "Siemens", "Eaton"
    ],
    "quincaillerie": [
        "Stanley", "Facom", "Bosch", "Makita", "Dexter", "Wolfcraft", "Irwin", "Knipex", "Vachette", "Bricard", "Abus", "Securit", "Tesa", "Laperche", "Thirard"
    ],
    "peinture et droguerie": [
        "Dulux Valentine", "Ripolin", "V33", "Sikkens", "Tollens", "Blancolor", "Guittet", "Levis", "Luxens", "Hammerite", "Julien", "Bondex", "Oxi", "Béton Ciré", "Peintures 1825"
    ],
    "carrelage et parquet": [
        "Porcelanosa", "Marazzi", "Cotto d'Este", "Tarkett", "Gerflor", "Quick-Step", "BerryAlloc", "Pergo", "Lapeyre", "Castorama", "Leroy Merlin", "Saint Maclou", "Alsapan", "Parador", "Wicanders"
    ],
    "matériaux de construction": [
        "Lafarge", "Saint-Gobain", "Knauf", "Isover", "Placo", "Weber", "ParexLanko", "Siniat", "Rockwool", "Siporex", "Point P", "BigMat", "Gedimat", "Bricoman", "Brico Dépôt"
    ]
}
# produit(nom_produit, gamme, type_usine, [(composant, quantite), ...])
PRODUITS = [
    # Produits de chaine assemblage
    ("Tondeuse électrique", "jardin et piscine", "chaine assemblage", [("Vis inox", 20), ("Boulon acier", 10), ("Câble acier", 2)]),
    ("Tondeuse thermique", "jardin et piscine", "chaine assemblage", [("Vis inox", 25), ("Boulon acier", 15), ("Tube cuivre", 1)]),
    ("Coupe-bordures", "jardin et piscine", "chaine assemblage", [("Vis inox", 15), ("Câble acier", 1)]),
    ("Taille-haie", "jardin et piscine", "chaine assemblage", [("Vis inox", 18), ("Boulon acier", 8)]),
    ("Souffleur", "jardin et piscine", "chaine assemblage", [("Vis inox", 12), ("Tube PER", 1)]),
    ("Scarificateur", "jardin et piscine", "chaine assemblage", [("Vis inox", 30), ("Boulon acier", 20), ("Chaîne acier", 1)]),
    ("Bineuse", "jardin et piscine", "chaine assemblage", [("Vis inox", 16), ("Poignée porte", 2)]),
    ("Pompe piscine", "jardin et piscine", "chaine assemblage", [("Vis inox", 20), ("Boulon acier", 12), ("Tube cuivre", 2), ("Raccord cuivre", 4)]),
    ("Filtre piscine", "jardin et piscine", "chaine assemblage", [("Vis inox", 15), ("Tube PER", 3), ("Vanne d'arrêt", 2)]),
    ("Robot piscine", "jardin et piscine", "chaine assemblage", [("Vis inox", 40), ("Boulon acier", 20), ("Câble acier", 1)]),
    ("Échelle piscine", "jardin et piscine", "chaine assemblage", [("Tube cuivre", 6), ("Boulon acier", 24), ("Vis inox", 30)]),
    ("Bâche piscine", "jardin et piscine", "chaine assemblage", [("Chaîne acier", 4), ("Clou", 50)]),
    ("Alarme piscine", "jardin et piscine", "chaine assemblage", [("Vis inox", 10), ("Boîtier étanche", 1), ("Câble acier", 1)]),
    ("Canapé d'angle", "mobilier intérieur", "chaine assemblage", [("Planche pin", 10), ("Vis inox", 50), ("Boulon acier", 30)]),
    ("Fauteuil relax", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 6), ("Vis inox", 40), ("Boulon acier", 20)]),
    ("Table basse", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 4), ("Vis inox", 30), ("Paumelle", 4)]),
    ("Bibliothèque", "mobilier intérieur", "chaine assemblage", [("Planche pin", 15), ("Vis inox", 60), ("Cheville", 20)]),
    ("Armoire penderie", "mobilier intérieur", "chaine assemblage", [("Planche pin", 20), ("Vis inox", 80), ("Paumelle", 6), ("Poignée porte", 2)]),
    ("Commode", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 12), ("Vis inox", 50), ("Poignée porte", 4)]),
    ("Table à manger", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 8), ("Vis inox", 40), ("Boulon acier", 16)]),
    ("Chaises", "mobilier intérieur", "chaine assemblage", [("Planche pin", 4), ("Vis inox", 20), ("Boulon acier", 8)]),
    ("Lit", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 12), ("Vis inox", 60), ("Boulon acier", 40)]),
    ("Matelas", "mobilier intérieur", "chaine assemblage", []),
    ("Sommier", "mobilier intérieur", "chaine assemblage", [("Planche pin", 10), ("Vis inox", 40), ("Boulon acier", 30)]),
    ("Table de chevet", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 4), ("Vis inox", 20), ("Poignée porte", 1)]),
    ("Bureau", "mobilier intérieur", "chaine assemblage", [("Planche chêne", 8), ("Vis inox", 40), ("Boulon acier", 20), ("Poignée porte", 3)]),
    ("Étagères", "mobilier intérieur", "chaine assemblage", [("Planche pin", 6), ("Vis inox", 30), ("Cheville", 12)]),
    ("Perceuse visseuse", "matériaux de construction", "chaine assemblage", [("Vis inox", 15), ("Boulon acier", 10)]),
    ("Perceuse à percussion", "matériaux de construction", "chaine assemblage", [("Vis inox", 18), ("Boulon acier", 12)]),
    ("Visseuse impact", "matériaux de construction", "chaine assemblage", [("Vis inox", 20), ("Boulon acier", 15)]),
    ("Scie circulaire", "matériaux de construction", "chaine assemblage", [("Vis inox", 25), ("Boulon acier", 18)]),
    ("Scie sauteuse", "matériaux de construction", "chaine assemblage", [("Vis inox", 20), ("Boulon acier", 12)]),
    ("Ponceuse orbitale", "matériaux de construction", "chaine assemblage", [("Vis inox", 15), ("Boulon acier", 10)]),
    ("Ponceuse excentrique", "matériaux de construction", "chaine assemblage", [("Vis inox", 18), ("Boulon acier", 12)]),
    ("Défonceuse", "matériaux de construction", "chaine assemblage", [("Vis inox", 22), ("Boulon acier", 16)]),
    ("Raboteuse", "matériaux de construction", "chaine assemblage", [("Vis inox", 30), ("Boulon acier", 20)]),
    ("Meuleuse", "matériaux de construction", "chaine assemblage", [("Vis inox", 18), ("Boulon acier", 14)]),
    ("Perforateur", "matériaux de construction", "chaine assemblage", [("Vis inox", 25), ("Boulon acier", 18)]),
    ("Marteau piqueur", "matériaux de construction", "chaine assemblage", [("Vis inox", 30), ("Boulon acier", 25)]),
    ("Tableau électrique CA", "électricité et domotique", "chaine assemblage", [("Vis inox", 40), ("Rail DIN", 5), ("Borne connexion", 10)]),
    ("Disjoncteur CA", "électricité et domotique", "chaine assemblage", [("Vis inox", 8), ("Borne connexion", 2)]),
    ("Interrupteur différentiel CA", "électricité et domotique", "chaine assemblage", [("Vis inox", 10), ("Borne connexion", 3)]),
    ("Box domotique", "électricité et domotique", "chaine assemblage", [("Vis inox", 12), ("Boîtier étanche", 1), ("Borne connexion", 8)]),
    ("Prise connectée", "électricité et domotique", "chaine assemblage", [("Vis inox", 4), ("Borne connexion", 2)]),
    ("Interrupteur connecté", "électricité et domotique", "chaine assemblage", [("Vis inox", 4), ("Borne connexion", 2)]),
    ("Détecteur mouvement", "électricité et domotique", "chaine assemblage", [("Vis inox", 6), ("Boîtier étanche", 1)]),
    ("Caméra surveillance", "électricité et domotique", "chaine assemblage", [("Vis inox", 8), ("Boîtier étanche", 1), ("Câble acier", 1)]),
    ("Portier vidéo", "électricité et domotique", "chaine assemblage", [("Vis inox", 10), ("Boîtier étanche", 1), ("Borne connexion", 4)]),

    # Produits de scierie (pas de composants - matières premières)
    ("Planche pin", "jardin et piscine", "scierie", []),
    ("Planche chêne", "jardin et piscine", "scierie", []),
    ("Lame terrasse", "jardin et piscine", "scierie", []),
    ("Poteau bois", "jardin et piscine", "scierie", []),
    ("Panneau bois", "jardin et piscine", "scierie", []),
    ("Bardage bois", "jardin et piscine", "scierie", []),
    ("Cloture bois", "jardin et piscine", "scierie", []),
    ("Pergola bois", "jardin et piscine", "scierie", []),
    ("Abri jardin", "jardin et piscine", "scierie", []),
    ("Jardinière bois", "jardin et piscine", "scierie", []),
    ("Bac à sable", "jardin et piscine", "scierie", []),
    ("Balançoire", "jardin et piscine", "scierie", []),
    ("Plan travail bois", "mobilier intérieur", "scierie", []),
    ("Étagère pin", "mobilier intérieur", "scierie", []),
    ("Étagère chêne", "mobilier intérieur", "scierie", []),
    ("Planche étagère", "mobilier intérieur", "scierie", []),
    ("Tasseau bois", "mobilier intérieur", "scierie", []),
    ("Moulure bois", "mobilier intérieur", "scierie", []),
    ("Corniche bois", "mobilier intérieur", "scierie", []),
    ("Plinthe bois", "mobilier intérieur", "scierie", []),
    ("Parquet massif", "mobilier intérieur", "scierie", []),
    ("Parquet contrecollé", "mobilier intérieur", "scierie", []),
    ("Stratifié", "mobilier intérieur", "scierie", []),
    ("Lambris", "mobilier intérieur", "scierie", []),
    ("Parquet chêne massif", "carrelage et parquet", "scierie", []),
    ("Parquet hêtre", "carrelage et parquet", "scierie", []),
    ("Parquet bambou", "carrelage et parquet", "scierie", []),
    ("Parquet flottant", "carrelage et parquet", "scierie", []),
    ("Lame PVC", "carrelage et parquet", "scierie", []),
    ("Sol vinyle", "carrelage et parquet", "scierie", []),
    ("Sous-couche parquet", "carrelage et parquet", "scierie", []),
    ("Poutre bois", "matériaux de construction", "scierie", []),
    ("Chevron", "matériaux de construction", "scierie", []),
    ("Latte", "matériaux de construction", "scierie", []),
    ("Madrier", "matériaux de construction", "scierie", []),
    ("Planche coffrage", "matériaux de construction", "scierie", []),
    ("OSB", "matériaux de construction", "scierie", []),
    ("Contreplaqué", "matériaux de construction", "scierie", []),
    ("Médium MDF", "matériaux de construction", "scierie", []),
    ("Aggloméré", "matériaux de construction", "scierie", []),
    ("Panneau OSB", "matériaux de construction", "scierie", []),

    # Produits de métallurgie (pas de composants - matières premières)
    ("Vis inox", "quincaillerie", "métallurgie", []),
    ("Boulon acier", "quincaillerie", "métallurgie", []),
    ("Écrou", "quincaillerie", "métallurgie", []),
    ("Rondelle", "quincaillerie", "métallurgie", []),
    ("Clou", "quincaillerie", "métallurgie", []),
    ("Pointe", "quincaillerie", "métallurgie", []),
    ("Cheville", "quincaillerie", "métallurgie", []),
    ("Tire-fond", "quincaillerie", "métallurgie", []),
    ("Tige filetée", "quincaillerie", "métallurgie", []),
    ("Chaîne acier", "quincaillerie", "métallurgie", []),
    ("Câble acier", "quincaillerie", "métallurgie", []),
    ("Serrure", "quincaillerie", "métallurgie", []),
    ("Verrou", "quincaillerie", "métallurgie", []),
    ("Cadenas", "quincaillerie", "métallurgie", []),
    ("Gond", "quincaillerie", "métallurgie", []),
    ("Paumelle", "quincaillerie", "métallurgie", []),
    ("Charnière", "quincaillerie", "métallurgie", []),
    ("Tube cuivre", "plomberie et chauffage", "métallurgie", []),
    ("Raccord cuivre", "plomberie et chauffage", "métallurgie", []),
    ("Tube PER", "plomberie et chauffage", "métallurgie", []),
    ("Raccord PER", "plomberie et chauffage", "métallurgie", []),
    ("Radiateur acier", "plomberie et chauffage", "métallurgie", []),
    ("Radiateur fonte", "plomberie et chauffage", "métallurgie", []),
    ("Collecteur chauffage", "plomberie et chauffage", "métallurgie", []),
    ("Vanne d'arrêt", "plomberie et chauffage", "métallurgie", []),
    ("Clapet anti-retour", "plomberie et chauffage", "métallurgie", []),
    ("Détendeur gaz", "plomberie et chauffage", "métallurgie", []),
    ("Gaine électrique", "électricité et domotique", "métallurgie", []),
    ("Tube IRL", "électricité et domotique", "métallurgie", []),
    ("Chemin câbles", "électricité et domotique", "métallurgie", []),
    ("Goulottes", "électricité et domotique", "métallurgie", []),
    ("Boîtier étanche", "électricité et domotique", "métallurgie", []),
    ("Armoire électrique", "électricité et domotique", "métallurgie", []),
    ("Rail DIN", "électricité et domotique", "métallurgie", []),
    ("Borne connexion", "électricité et domotique", "métallurgie", []),
    ("Clé plate", "matériaux de construction", "métallurgie", []),
    ("Clé à pipe", "matériaux de construction", "métallurgie", []),
    ("Tournevis", "matériaux de construction", "métallurgie", []),
    ("Pince", "matériaux de construction", "métallurgie", []),
    ("Serre-joint", "matériaux de construction", "métallurgie", []),
    ("Étau", "matériaux de construction", "métallurgie", []),
    ("Lime", "matériaux de construction", "métallurgie", []),
    ("Râpe", "matériaux de construction", "métallurgie", []),
    ("Burins", "matériaux de construction", "métallurgie", []),
    ("Pointeau", "matériaux de construction", "métallurgie", []),
    ("Compas", "matériaux de construction", "métallurgie", []),

    # Produits de fonderie
    ("Mitigeur cuisine", "plomberie et chauffage", "fonderie", []),
    ("Mitigeur douche", "plomberie et chauffage", "fonderie", []),
    ("Robinet lavabo", "plomberie et chauffage", "fonderie", []),
    ("Robinet évier", "plomberie et chauffage", "fonderie", []),
    ("Douchette", "plomberie et chauffage", "fonderie", []),
    ("Colonne douche", "plomberie et chauffage", "fonderie", []),
    ("Bonde", "plomberie et chauffage", "fonderie", []),
    ("Siphon", "plomberie et chauffage", "fonderie", []),
    ("Collecteur fonte", "plomberie et chauffage", "fonderie", []),
    ("Regard fonte", "plomberie et chauffage", "fonderie", []),
    ("Bouche égout", "plomberie et chauffage", "fonderie", []),
    ("Robinet baignoire", "salle de bain et WC", "fonderie", []),
    ("Mitigeur thermostatique", "salle de bain et WC", "fonderie", []),
    ("Pomme douche", "salle de bain et WC", "fonderie", []),
    ("Flexible douche", "salle de bain et WC", "fonderie", []),
    ("Barre douche", "salle de bain et WC", "fonderie", []),
    ("Support douchette", "salle de bain et WC", "fonderie", []),
    ("Évacuation douche", "salle de bain et WC", "fonderie", []),
    ("Bonde baignoire", "salle de bain et WC", "fonderie", []),
    ("Trop-plein", "salle de bain et WC", "fonderie", []),
    ("Applique murale", "luminaire", "fonderie", []),
    ("Suspension", "luminaire", "fonderie", []),
    ("Lustre", "luminaire", "fonderie", []),
    ("Spot encastrable", "luminaire", "fonderie", []),
    ("Réglette LED", "luminaire", "fonderie", []),
    ("Plafonnier", "luminaire", "fonderie", []),
    ("Lampadaire", "luminaire", "fonderie", []),
    ("Lampe bureau", "luminaire", "fonderie", []),
    ("Projecteur LED", "luminaire", "fonderie", []),
    ("Borne éclairage", "luminaire", "fonderie", []),
    ("Balise LED", "luminaire", "fonderie", []),
    ("Tableau électrique FO", "électricité et domotique", "fonderie", []),
    ("Disjoncteur FO", "électricité et domotique", "fonderie", []),
    ("Interrupteur différentiel FO", "électricité et domotique", "fonderie", []),
    ("Box domotique FO", "électricité et domotique", "fonderie", []),
    ("Prise connectée FO", "électricité et domotique", "fonderie", []),
    ("Interrupteur connecté FO", "électricité et domotique", "fonderie", []),
    ("Détecteur mouvement FO", "électricité et domotique", "fonderie", []),
    ("Caméra surveillance FO", "électricité et domotique", "fonderie", []),
    ("Portier vidéo FO", "électricité et domotique", "fonderie", []),
    ("Poignée porte", "quincaillerie", "fonderie", []),
    ("Béquille", "quincaillerie", "fonderie", []),
    ("Crémone", "quincaillerie", "fonderie", []),
    ("Espagnolette", "quincaillerie", "fonderie", []),
    ("Ferme-porte", "quincaillerie", "fonderie", []),
    ("Butée porte", "quincaillerie", "fonderie", []),
    ("Heurtoir", "quincaillerie", "fonderie", []),
    ("Boîte aux lettres", "quincaillerie", "fonderie", []),
]