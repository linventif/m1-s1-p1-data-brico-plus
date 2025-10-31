# -*- coding: utf-8 -*-
"""
Peuplement réaliste de la BD Brico Plus.
- Environ 50 lignes par table (les tables d'énumération ont leur taille "naturelle").
- 70% des adresses en Haute-Garonne (31xxx), 30% ailleurs en France.
- Conçu pour Oracle 23c Free (service name, pas SID).
"""

from pathlib import Path
import os
import sys
import random
import string
import datetime as dt
import oracledb

# ---------- Chargement du .env ----------
try:
    from dotenv import load_dotenv
except ImportError:
    sys.stderr.write("❌ Erreur : le module python-dotenv est requis. Installe-le avec:\n")
    sys.stderr.write("   pip install python-dotenv\n")
    sys.exit(1)

HERE = Path(__file__).resolve().parent
default_env_path = HERE.parent / ".env"
ENV_PATH = Path(os.getenv("ENV_FILE", str(default_env_path)))

if not ENV_PATH.exists():
    sys.stderr.write(f"❌ Fichier .env introuvable : {ENV_PATH}\n")
    sys.stderr.write("Place un fichier .env à la racine du projet ou définis ENV_FILE=/chemin/.env\n")
    sys.exit(1)

load_dotenv(dotenv_path=str(ENV_PATH), override=False)

# ---------- Vérification des variables obligatoires ----------
required_vars = ["ORACLE_HOST", "ORACLE_PORT", "ORACLE_SERVICE", "ORACLE_USER", "ORACLE_PASS"]
missing = [v for v in required_vars if not os.getenv(v)]
if missing:
    sys.stderr.write("❌ Variables manquantes dans .env : " + ", ".join(missing) + "\n")
    sys.stderr.write("Exemple minimal :\n"
                     "ORACLE_HOST=90.103.29.148\n"
                     "ORACLE_PORT=15210\n"
                     "ORACLE_SERVICE=FREEPDB1\n"
                     "ORACLE_USER=PROJET_BRICO_PLUS\n"
                     "ORACLE_PASS=BricoPlus123\n")
    sys.exit(1)

# ---------- Configuration Oracle ----------
HOST = os.getenv("ORACLE_HOST")
PORT = int(os.getenv("ORACLE_PORT"))
SERVICE = os.getenv("ORACLE_SERVICE")
USER = os.getenv("ORACLE_USER")
PASS = os.getenv("ORACLE_PASS")

DSN = oracledb.makedsn(HOST, PORT, service_name=SERVICE)
random.seed(31)  # reproductible

print(f"✅ Fichier .env chargé depuis : {ENV_PATH}")
print(f"→ Connexion prévue : {USER}@{HOST}:{PORT}/{SERVICE}\n")

# -----------------------
# RÉFÉRENTIELS FRANCE
# -----------------------
# Villes Haute-Garonne (70% des cas)
HG_CITIES = [
    ("Toulouse", "31000"), ("Toulouse", "31100"), ("Toulouse", "31200"), ("Toulouse", "31300"),
    ("Toulouse", "31400"), ("Toulouse", "31500"), ("Blagnac", "31700"), ("Colomiers", "31770"),
    ("Tournefeuille", "31170"), ("Balma", "31130"), ("Muret", "31600"), ("Ramonville-Saint-Agne", "31520"),
    ("Saint-Gaudens", "31800"), ("L'Union", "31240"), ("Cugnaux", "31270"), ("Labège", "31670"),
    ("Plaisance-du-Touch", "31830"), ("Castanet-Tolosan", "31320"), ("Fronton", "31620"), ("Grenade", "31330")
]

# Villes hors HG (30% des cas)
FR_CITIES = [
    ("Bordeaux", "33000"), ("Paris", "75011"), ("Lyon", "69007"), ("Marseille", "13008"),
    ("Lille", "59800"), ("Nantes", "44000"), ("Rennes", "35000"), ("Strasbourg", "67000"),
    ("Montpellier", "34000"), ("Nice", "06000"), ("Dijon", "21000"), ("Grenoble", "38000"),
    ("Le Mans", "72000"), ("Tours", "37000"), ("Brest", "29200"), ("Clermont-Ferrand", "63000")
]

# Téléphones : 05 pour sud-ouest (HG), sinon 01/02/03/04/05/09
def phone(hg=False):
    if hg:
        pref = "05"
    else:
        pref = random.choice(["01", "02", "03", "04", "05", "09"])
    return pref + "".join(random.choices(string.digits, k=8))

def pick_city(hg_bias=True):
    if hg_bias and random.random() < 0.7:
        return random.choice(HG_CITIES)
    return random.choice(FR_CITIES)

# Rues factices
def street():
    types = ["Rue", "Avenue", "Boulevard", "Allée", "Chemin", "Impasse", "Place"]
    noms = ["Victor-Hugo", "de la République", "des Lilas", "du 14-Juillet", "Jean-Jaurès",
            "de la Liberté", "des Acacias", "des Forges", "Pasteur", "des Écoles"]
    return f"{random.randint(1, 220)} {random.choice(types)} {random.choice(noms)}"

# -----------------------
# ÉNUMÉRATIONS (Sujet)
# -----------------------
# TYPEU (NomTU) : chaine assemblage, scierie, métallurgie, fonderie (enum)
# Correspond exactement à la contrainte CHK_TYPEU_NOMTU_ENUM
TYPEU = ["chaine assemblage", "scierie", "métallurgie", "fonderie"]

# GAMME (Code GXX et libellé) - Doit correspondre exactement à l'enum de la DB
GAMMES = [
    "jardin et piscine", "mobilier intérieur", "plomberie et chauffage", "salle de bain et WC",
    "luminaire, électricité et domotique", "quincaillerie", "cuisine",
    "peinture et droguerie", "carrelage et parquet", "matériaux de construction"
]
# NB: 10 gammes correspondant exactement à l'enum de la contrainte CHK_GAMME_NOMG_ENUM

# DEPARTEMENTS (NomD) : fabrication, assemblage, RH, expédition, logistique, direction, finance  :contentReference[oaicite:4]{index=4}
DEPTS = ["fabrication", "assemblage", "RH", "expédition", "logistique", "direction", "finance"]

# POINTS_DE_VENTE TypePV : GSB, Brico-Express  :contentReference[oaicite:5]{index=5}
PV_TYPES = ["GSB", "Brico-Express"]

# -----------------------
# VOLUMÉTRIE VISÉE (données réduites mais beaucoup d'associations)
# -----------------------
N_EMP = 50  # 50 employés
N_QUALIF = 50  # 50 qualifications
N_USINES = 15  # 15 usines
N_PV = 50  # 50 points de vente
N_PRODUITS = 100  # 100 produits

# Calendriers (~50 lignes)
N_CAL1 = 50  # DATEFAB
N_CAL2 = 50  # DATEDEBUTDIR
# CAL3 = 200 couples (mois, année) <= année courante
# CAL4 = 200 années (<= année courante)
YEAR_NOW = dt.date.today().year
MONTH_NOW = dt.date.today().month

# Construit 50 (mois, année) en remontant depuis l'année courante
cal3 = []
y, m = YEAR_NOW, MONTH_NOW
for _ in range(60):  # génére assez, on tronquera à 50
    cal3.append((m, y))
    m -= 1
    if m == 0:
        m = 12
        y -= 1
cal3 = cal3[:50]

# 200 années : 1985 .. 2025 (plage réaliste pour l'entreprise)
cal4 = list(range(1985, 2026))  # 1985 à 2025 inclus

# 50 dates <= aujourd'hui pour CAL1 & CAL2
def sample_dates(n):
    base = dt.date(YEAR_NOW-1, 1, 1)
    last = dt.date.today()
    span = (last - base).days
    seen = set()
    out = []
    while len(out) < n:
        d = base + dt.timedelta(days=random.randint(0, max(span, 1)))
        if d <= last and d not in seen:
            seen.add(d)
            out.append(d)
    out.sort()
    return out

cal1_dates = sample_dates(N_CAL1)
cal2_dates = sample_dates(N_CAL2)

# -----------------------
# GÉNÉRATION DES DONNÉES
# -----------------------
def gen_employes(n=N_EMP):
    rows = []
    for code in range(1, n+1):
        nom = random.choice([
            "Martin", "Bernard", "Thomas", "Petit", "Robert", "Richard", "Durand", "Dubois",
            "Moreau", "Laurent", "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David", "Foxy"
        ])
        prenom = random.choice([
            "Lucas", "Louis", "Hugo", "Arthur", "Jules", "Adam", "Léo", "Noah",
            "Emma", "Louise", "Chloé", "Lina", "Mia", "Anna", "Zoé", "Léa"
        ])
        vpers, cppers = pick_city(True)
        vpro, cppro = pick_city(True)
        # Ne pas inclure CODEE car c'est GENERATED ALWAYS AS IDENTITY
        rows.append((
            nom, prenom,
            street(), cppers, vpers,
            street(), cppro, vpro,
            phone(hg=True), phone(hg=True)
        ))
    return rows

def gen_qualifs(n=N_QUALIF):
    rows = []
    for code in range(1, n+1):
        nom = random.choice([
            "Vendeur", "Chef d'équipe", "Opérateur", "Magasinier", "Technicien",
            "Responsable RH", "Contrôleur qualité", "Acheteur", "Comptable", "Électricien",
            "Plombier", "Carreleur", "Peintre", "Soudeur", "Monteur", "Chargé logistique"
        ]) + f" {random.randint(1,9)}"
        taux = round(random.uniform(11.5, 28.0), 2)  # €/h
        # Ne pas inclure CODEQ car c'est GENERATED ALWAYS AS IDENTITY
        rows.append((nom, taux, None))
    # Note: On ne peut plus créer les liens "complétée par" facilement sans connaître les IDs générés
    return rows

def gen_usines(n=N_USINES):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        nom_usine = f"Usine {city} {code}"

        # Ne pas inclure CODEU car c'est GENERATED ALWAYS AS IDENTITY
        rows.append((nom_usine, street(), cp, city, phone(hg=cp.startswith("31"))))
    return rows

def gen_typeu():
    rows = []
    for i, nom in enumerate(TYPEU, start=1):
        # Ne pas inclure CODETU car c'est GENERATED ALWAYS AS IDENTITY
        rows.append((nom,))
    return rows

def gen_gammes():
    rows = []
    for i, nom in enumerate(GAMMES, start=1):
        codeg = f"G{str(i).zfill(2)}"  # GXX  :contentReference[oaicite:9]{index=9}
        rows.append((codeg, nom))
    return rows

def gen_departements(usines):
    rows = []
    code = 1
    for u in usines:
        nb = random.randint(3, 6)  # plusieurs départements par usine
        noms = random.sample(DEPTS, k=nb)
        for nom in noms:
            rows.append((code, nom, u[0]))
            code += 1
    return rows

def gen_departements_with_ids(usines_with_ids):
    """Génère des départements en utilisant les vrais IDs d'usines"""
    rows = []
    for u_id, u_nom in usines_with_ids:
        nb = random.randint(3, 6)  # plusieurs départements par usine
        noms = random.sample(DEPTS, k=nb)
        for nom in noms:
            rows.append((nom, u_id))
    return rows

def gen_points_vente(n=N_PV):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        # NOMPV doit être dans ('GSB','Brico-Express') selon la contrainte de la DB
        nompv = random.choices(PV_TYPES, weights=[0.6, 0.4])[0]  # un peu plus de GSB
        # Ne pas inclure CODEPV car c'est GENERATED ALWAYS AS IDENTITY
        rows.append((
            nompv,  # NOMPV respecte maintenant la contrainte
            street(), cp, city, phone(hg=cp.startswith("31")),
            f"Type {nompv}"))  # TYPEPV comme description
    return rows

# -----------------------
# PRODUITS PAR TYPE D'USINE (pour réalisme)
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

def gen_produits(n=N_PRODUITS):
    """Génère des produits réalistes selon les types d'usines"""
    rows = []
    code = 1

    # Répartit les produits entre les types d'usines
    produits_par_type_usine = n // len(TYPEU)  # ~100 produits par type d'usine

    for type_usine in TYPEU:
        if type_usine not in PRODUITS_PAR_TYPE:
            continue

        # Pour chaque gamme de ce type d'usine
        for gamme_nom, produits_base in PRODUITS_PAR_TYPE[type_usine].items():
            # Trouve le code de la gamme
            codeg = None
            for i, g_nom in enumerate(GAMMES, start=1):
                if g_nom == gamme_nom:
                    codeg = f"G{str(i).zfill(2)}"
                    break

            if not codeg:
                continue

            # Génère plusieurs variantes de chaque produit de base
            for produit_base in produits_base:
                if code > n:
                    break

                # Variantes avec marques et modèles
                marques = ["ProLine", "MaisonPro", "BuildX", "Crafto", "Lumina", "AquaFix",
                          "TechMax", "HomeStyle", "PowerTool", "QualityPlus"]

                for i in range(min(3, (n - code + 1))):  # 1-3 variantes par produit
                    if code > n:
                        break
                    marque = random.choice(marques)
                    modele = random.randint(100, 999)
                    nom_final = f"{produit_base} {modele}"

                    # Ne pas inclure CODEP car c'est GENERATED ALWAYS AS IDENTITY
                    rows.append((nom_final, marque, codeg))
                    code += 1

    # Complete avec des produits génériques si nécessaire
    while len(rows) < n:
        nom = f"Produit générique {random.randint(1000, 9999)}"
        marque = random.choice(["Generic", "Standard", "Basic"])
        codeg = f"G{random.randint(1, len(GAMMES)):02d}"  # Ajusté pour 10 gammes
        rows.append((nom, marque, codeg))

    return rows[:n]

def gen_posseder(employes, qualifs):
    rows = []
    for e in employes:
        qset = random.sample(qualifs, k=random.randint(2, 5))  # Beaucoup de qualifications par employé
        for q in qset:
            rows.append((e[0], q[0]))
    # Garder beaucoup d'associations
    return rows[:max(500, len(rows))]

def gen_assembler(produits):
    rows = []
    used = set()
    for _ in range(500):  # Beaucoup d'assemblages
        a, b = random.sample(produits, 2)
        if a[0] == b[0]:
            continue
        key = (a[0], b[0])
        if key in used:
            continue
        used.add(key)
        rows.append((a[0], b[0], random.randint(1, 10)))  # Quantités plus variées
    return rows

def gen_calendriers():
    # CAL1: DATEFAB, CAL2: DATEDEBUTDIR, CAL3: (MOIS, ANNEE), CAL4: ANNEE
    cal1 = [(d,) for d in cal1_dates]
    cal2 = [(d,) for d in cal2_dates]
    cal3_rows = [(m, y) for (m, y) in cal3]
    cal4_rows = [(y,) for y in cal4]
    return cal1, cal2, cal3_rows, cal4_rows

def gen_avoir_type(usines, typeu):
    rows = []
    for u in usines:
        # chaque usine a 1 à 2 types
        for t in random.sample(typeu, k=random.randint(1, min(2, len(typeu)))):
            rows.append((u[0], t[0]))
    return rows

def gen_diriger(employes, departements):
    rows = []
    for _ in range(500):  # Beaucoup d'associations
        e = random.choice(employes)[0]
        d = random.choice(departements)[0]
        date = random.choice(cal2_dates)
        rows.append((e, d, date))
    # unique par PK (CODEE, CODED, DATEDEBUTDIR) => dédoublonne
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_autoriser(qualifs, departements):
    rows = []
    for d in random.sample(departements, k=min(500, len(departements))):
        for q in random.sample(qualifs, k=random.randint(3, 8)):  # Beaucoup d'autorisations par département
            rows.append((q[0], d[0]))
    return rows[:500]

def gen_fabriquer(usines, produits):
    """Génère des fabrications réalistes selon les types d'usines"""
    rows = []
    used = set()
    # 70% des fabrications hors HG pour servir la requête 5 (vendus en HG mais fabriqués ailleurs)
    ext_usines = [u for u in usines if not str(u[3]).startswith("31")]
    loc_usines = [u for u in usines if str(u[3]).startswith("31")]

    # Obtient les types d'usines pour faire des associations réalistes
    typeu_data = gen_typeu()
    avoir_type_data = gen_avoir_type(usines, typeu_data)

    # Crée un mapping usine -> types
    usine_types = {}
    for codeu, codetu in avoir_type_data:
        if codeu not in usine_types:
            usine_types[codeu] = []
        type_nom = typeu_data[codetu-1][1]  # Récupère le nom du type
        usine_types[codeu].append(type_nom)

    attempts = 0
    max_attempts = 2000  # Moins d'essais
    target_records = 500  # Beaucoup d'associations

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1

        # Choix de l'usine
        if ext_usines and random.random() < 0.7:
            u = random.choice(ext_usines)
        else:
            u = random.choice(loc_usines or usines)

        # Vérifie que l'usine a des types associés
        if u[0] not in usine_types:
            continue

        # Choix d'un produit compatible avec les types de l'usine
        produit_compatible = None
        for _ in range(50):  # Essais pour trouver un produit compatible
            p = random.choice(produits)
            # Vérifie si le produit peut être fabriqué par cette usine
            if est_produit_compatible_usine(p, usine_types[u[0]]):
                produit_compatible = p
                break

        if not produit_compatible:
            # Si aucun produit compatible, prend un produit au hasard (cas d'exception)
            produit_compatible = random.choice(produits)

        d = random.choice(cal1_dates)

        # Vérifie l'unicité de la combinaison (CODEU, CODEP, DATEFAB)
        key = (u[0], produit_compatible[0], d)
        if key not in used:
            used.add(key)
            q = random.randint(10, 500)  # Quantités plus importantes
            rows.append((u[0], produit_compatible[0], d, q))

    return rows

def est_produit_compatible_usine(produit, types_usine):
    """Vérifie si un produit peut être fabriqué par les types d'usine donnés"""
    # Récupère le code de gamme du produit
    codeg = produit[3]

    # Trouve le nom de la gamme
    gamme_nom = None
    for i, g_nom in enumerate(GAMMES, start=1):
        if f"G{str(i).zfill(2)}" == codeg:
            gamme_nom = g_nom
            break

    if not gamme_nom:
        return True  # Si gamme inconnue, accepte par défaut

    # Vérifie si au moins un type d'usine peut fabriquer cette gamme
    for type_usine in types_usine:
        if type_usine in PRODUITS_PAR_TYPE and gamme_nom in PRODUITS_PAR_TYPE[type_usine]:
            return True

    return False

def gen_responsable(employes, gammes):
    rows = []
    # S'assurer que 2024 et 2025 sont inclus + autres années aléatoires
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for _ in range(500):  # Beaucoup d'associations
        e = random.choice(employes)[0]
        g = random.choice(gammes)[0]
        y = random.choice(years)
        rows.append((e, g, y))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_payer2(gammes):
    rows = []
    # Couvrir TOUTES les années 1985-2025 avec 2-10 enregistrements par année
    all_years = list(range(1985, 2026))  # Toutes les années de 1985 à 2025

    for year in all_years:
        # 2-10 enregistrements par année (gammes aléatoires)
        num_records = random.randint(2, 10)
        selected_gammes = random.sample(gammes, k=min(num_records, len(gammes)))

        for g in selected_gammes:
            indice = round(random.uniform(0.01, 0.99), 2)  # Entre 0 et 1 exclus selon contrainte
            rows.append((g[0], year, indice))

    return rows

def gen_facturer(produits):
    rows = []
    for p in produits:
        # Beaucoup de facturations par produit
        for (m, y) in random.sample(cal3, k=random.randint(4, 12)):
            pu = round(random.uniform(2.0, 2500.0), 2)  # Plus de variabilité de prix
            rows.append((p[0], m, y, pu))
    return rows[:500]

def gen_vendre(employes, pvs, produits):
    rows = []
    used = set()
    # Pour satisfaire la requête 1 : aucune vente Brico-Express pour une gamme donnée (ex: quincaillerie)
    # -> On évite de vendre des produits de la gamme "quincaillerie" en Brico-Express
    quinca_code = None
    for i, g in enumerate(GAMMES, start=1):
        if g == "quincaillerie":
            quinca_code = f"G{str(i).zfill(2)}"
            break

    attempts = 0
    max_attempts = 5000  # Moins d'essais
    target_records = 500  # Beaucoup d'associations

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes)[0]
        pv = random.choice(pvs)
        p = random.choice(produits)
        # règle pour Brico-Express & quincaillerie - pv[1] est maintenant NOMPV
        if pv[1] == "Brico-Express" and p[3] == quinca_code:
            continue
        (m, y) = random.choice(cal3)

        # Vérifie l'unicité de la combinaison (CODEE, CODEPV, CODEP, MOIS, ANNEE)
        key = (e, pv[0], p[0], m, y)
        if key not in used:
            used.add(key)
            q = random.randint(1, 100)  # Quantités plus importantes
            rows.append((e, pv[0], p[0], m, y, q))

    return rows

def gen_payer1(employes):
    rows = []
    # S'assurer que 2024 et 2025 sont inclus + autres années aléatoires
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for e in employes:
        for y in years:
            fixe = round(random.uniform(1200, 5000), 2)  # Plus de variabilité salariale
            idx = random.randint(1, 15)  # Indices plus variés
            rows.append((e[0], y, fixe, idx))
    return rows[:1000]  # Beaucoup d'associations

def gen_travailler_usine(employes, departements):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000  # Moins d'essais
    target_records = 500  # Beaucoup d'associations

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes)[0]
        d = random.choice(departements)[0]
        (m, y) = random.choice(cal3)

        # Vérifie l'unicité de la combinaison (CODEE, CODED, MOIS, ANNEE)
        key = (e, d, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(5, 200), 2)  # Plus de variabilité d'heures
            rows.append((e, d, m, y, hrs))

    return rows

def gen_travailler_pv(employes, pvs):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000  # Moins d'essais
    target_records = 500  # Beaucoup d'associations

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes)[0]
        pv = random.choice(pvs)[0]
        (m, y) = random.choice(cal3)

        # Vérifie l'unicité de la combinaison (CODEE, CODEPV, MOIS, ANNEE)
        key = (e, pv, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(3, 180), 2)  # Plus de variabilité d'heures
            rows.append((e, pv, m, y, hrs))

    return rows

# -----------------------
# FONCTIONS AVEC IDS GÉNÉRÉS AUTOMATIQUEMENT
# -----------------------

def gen_posseder_with_ids(employes_ids, qualifs_ids):
    rows = []
    for e_id in employes_ids:
        qset = random.sample(qualifs_ids, k=random.randint(2, 5))
        for q_id in qset:
            rows.append((e_id, q_id))
    return rows[:max(500, len(rows))]

def gen_assembler_with_ids(produits_ids):
    rows = []
    used = set()
    for _ in range(500):
        a, b = random.sample(produits_ids, 2)
        if a == b:
            continue
        key = (a, b)
        if key in used:
            continue
        used.add(key)
        rows.append((a, b, random.randint(1, 10)))
    return rows

def gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids):
    rows = []
    for u_id, u_nom in usines_with_ids:
        for t_id, t_nom in random.sample(typeu_with_ids, k=random.randint(1, min(2, len(typeu_with_ids)))):
            rows.append((u_id, t_id))
    return rows

def gen_diriger_with_ids(employes_ids, departements_ids):
    rows = []
    for _ in range(500):
        e = random.choice(employes_ids)
        d = random.choice(departements_ids)
        date = random.choice(cal2_dates)
        rows.append((e, d, date))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_autoriser_with_ids(qualifs_ids, departements_ids):
    rows = []
    for d in random.sample(departements_ids, k=min(500, len(departements_ids))):
        for q in random.sample(qualifs_ids, k=random.randint(3, 8)):
            rows.append((q, d))
    return rows[:500]

def gen_fabriquer_with_ids(usines_with_ids, produits_ids, typeu_with_ids):
    """Génère des fabrications réalistes avec les vrais IDs"""
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        u_id = random.choice([u[0] for u in usines_with_ids])
        p_id = random.choice(produits_ids)
        d = random.choice(cal1_dates)
        key = (u_id, p_id, d)
        if key not in used:
            used.add(key)
            q = random.randint(10, 500)
            rows.append((u_id, p_id, d, q))
    return rows

def gen_responsable_with_ids(employes_ids, gammes):
    rows = []
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for _ in range(500):
        e = random.choice(employes_ids)
        g = random.choice(gammes)[0]
        y = random.choice(years)
        rows.append((e, g, y))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:500]

def gen_facturer_with_ids(produits_ids):
    rows = []
    for p_id in produits_ids:
        for (m, y) in random.sample(cal3, k=random.randint(4, 12)):
            pu = round(random.uniform(2.0, 2500.0), 2)
            rows.append((p_id, m, y, pu))
    return rows[:500]

def gen_vendre_with_ids(employes_ids, pvs_ids, produits_ids):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 5000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        pv = random.choice(pvs_ids)
        p = random.choice(produits_ids)
        (m, y) = random.choice(cal3)
        key = (e, pv, p, m, y)
        if key not in used:
            used.add(key)
            q = random.randint(1, 100)
            rows.append((e, pv, p, m, y, q))
    return rows

def gen_payer1_with_ids(employes_ids):
    rows = []
    mandatory_years = [2024, 2025]
    other_years = random.sample([y for y in cal4 if y not in mandatory_years], k=min(15, len(cal4)-2))
    years = mandatory_years + other_years
    for e_id in employes_ids:
        for y in years:
            fixe = round(random.uniform(1200, 5000), 2)
            idx = random.randint(1, 15)
            rows.append((e_id, y, fixe, idx))
    return rows[:1000]

def gen_travailler_usine_with_ids(employes_ids, departements_ids):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        d = random.choice(departements_ids)
        (m, y) = random.choice(cal3)
        key = (e, d, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(5, 200), 2)
            rows.append((e, d, m, y, hrs))
    return rows

def gen_travailler_pv_with_ids(employes_ids, pvs_ids):
    rows = []
    used = set()
    attempts = 0
    max_attempts = 2000
    target_records = 500

    while len(rows) < target_records and attempts < max_attempts:
        attempts += 1
        e = random.choice(employes_ids)
        pv = random.choice(pvs_ids)
        (m, y) = random.choice(cal3)
        key = (e, pv, m, y)
        if key not in used:
            used.add(key)
            hrs = round(random.uniform(3, 180), 2)
            rows.append((e, pv, m, y, hrs))
    return rows

# -----------------------
# NETTOYAGE DES DONNÉES
# -----------------------
def clear_all_data(cursor):
    """Vide toutes les tables dans l'ordre correct (dépendances)"""
    tables_to_clear = [
        # Relations d'abord (qui dépendent des entités)
        "TRAVAILLER_PT_VENTE",
        "TRAVAILLER_USINE",
        "PAYER1",
        "VENDRE",
        "FACTURER",
        "PAYER2",
        "RESPONSABLE",
        "FABRIQUER_ASSEMBLER1",
        "AUTORISER",
        "DIRIGER",
        "AVOIR_TYPE",
        "ASSEMBLER",
        "POSSEDER",
        # Entités ensuite
        "PRODUITS",
        "POINTS_DE_VENTE",
        "DEPARTEMENTS",
        "QUALIFICATIONS",
        "EMPLOYES",
        "USINES",
        "CALENDRIER4",
        "CALENDRIER3",
        "CALENDRIER2",
        "CALENDRIER1",
        "GAMME",
        "TYPEU"
    ]

    print("🧹 Nettoyage des données existantes...")
    for table in tables_to_clear:
        try:
            cursor.execute(f"DELETE FROM {table}")
            print(f"   ✓ {table} vidée")
        except Exception as e:
            print(f"   ⚠️  Erreur lors du nettoyage de {table}: {e}")

    print("🧹 Nettoyage terminé.\n")

# -----------------------
# INSERTS
# -----------------------
def main():
    print(f"Connecting to {USER}@{HOST}:{PORT}/{SERVICE} ...")
    with oracledb.connect(user=USER, password=PASS, dsn=DSN) as con:
        cur = con.cursor()

        # Nettoyage des données existantes
        clear_all_data(cur)

        # Parents
        typeu = gen_typeu()
        cur.executemany("INSERT INTO TYPEU(NOMTU) VALUES (:1)", typeu)
        # Récupération des IDs générés pour TYPEU
        cur.execute("SELECT CODETU, NOMTU FROM TYPEU ORDER BY CODETU")
        typeu_with_ids = cur.fetchall()

        gammes = gen_gammes()
        cur.executemany("INSERT INTO GAMME(CODEG, NOMG) VALUES (:1,:2)", gammes)

        cal1, cal2, cal3_rows, cal4_rows = gen_calendriers()
        cur.executemany("INSERT INTO CALENDRIER1(DATEFAB) VALUES (:1)", cal1)
        cur.executemany("INSERT INTO CALENDRIER2(DATEDEBUTDIR) VALUES (:1)", cal2)
        cur.executemany("INSERT INTO CALENDRIER3(MOIS, ANNEE) VALUES (:1,:2)", cal3_rows)
        cur.executemany("INSERT INTO CALENDRIER4(ANNEE) VALUES (:1)", cal4_rows)

        usines = gen_usines()
        cur.executemany("""INSERT INTO USINES(NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                           VALUES (:1,:2,:3,:4,:5)""", usines)
        # Récupération des IDs générés pour USINES
        cur.execute("SELECT CODEU, NOMU FROM USINES ORDER BY CODEU")
        usines_with_ids = cur.fetchall()

        employes = gen_employes()
        cur.executemany("""INSERT INTO EMPLOYES
                           (NOME,PRENOME,RUEPERSE,CPOSTALPERSE,VILLEPERSE,
                            RUEPROE,CPOSTALPROE,VILLEPROE,TELPERSE,TELPROE)
                           VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10)""", employes)
        # Récupération des IDs générés pour EMPLOYES
        cur.execute("SELECT CODEE FROM EMPLOYES ORDER BY CODEE")
        employes_ids = [row[0] for row in cur.fetchall()]

        qualifs = gen_qualifs()
        cur.executemany("""INSERT INTO QUALIFICATIONS
                           (NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                           VALUES (:1,:2,:3)""", qualifs)
        # Récupération des IDs générés pour QUALIFICATIONS
        cur.execute("SELECT CODEQ FROM QUALIFICATIONS ORDER BY CODEQ")
        qualifs_ids = [row[0] for row in cur.fetchall()]

        # Dépendants - utilisation des IDs récupérés
        departements = gen_departements_with_ids(usines_with_ids)
        cur.executemany("""INSERT INTO DEPARTEMENTS(NOMD,CODEU) VALUES (:1,:2)""", departements)
        # Récupération des IDs générés pour DEPARTEMENTS
        cur.execute("SELECT CODED FROM DEPARTEMENTS ORDER BY CODED")
        departements_ids = [row[0] for row in cur.fetchall()]

        pvs = gen_points_vente()
        cur.executemany("""INSERT INTO POINTS_DE_VENTE
                           (NOMPV,RUEPV,CPOSTALPV,VILLEPV,TELPV,TYPEPV)
                           VALUES (:1,:2,:3,:4,:5,:6)""", pvs)
        # Récupération des IDs générés pour POINTS_DE_VENTE
        cur.execute("SELECT CODEPV FROM POINTS_DE_VENTE ORDER BY CODEPV")
        pvs_ids = [row[0] for row in cur.fetchall()]

        produits = gen_produits()
        cur.executemany("""INSERT INTO PRODUITS(NOMP,MARQUEP,CODEG) VALUES (:1,:2,:3)""", produits)
        # Récupération des IDs générés pour PRODUITS
        cur.execute("SELECT CODEP FROM PRODUITS ORDER BY CODEP")
        produits_ids = [row[0] for row in cur.fetchall()]

        # Associations / faits - utilisation des IDs récupérés
        posseder = gen_posseder_with_ids(employes_ids, qualifs_ids)
        cur.executemany("INSERT INTO POSSEDER(CODEE,CODEQ) VALUES (:1,:2)", posseder)

        assembler = gen_assembler_with_ids(produits_ids)
        cur.executemany("""INSERT INTO ASSEMBLER(CODEP_EST_COMPOSE,CODEP_COMPOSE,QTE_ASSEMBL)
                           VALUES (:1,:2,:3)""", assembler)

        avoir_type = gen_avoir_type_with_ids(usines_with_ids, typeu_with_ids)
        cur.executemany("INSERT INTO AVOIR_TYPE(CODEU,CODETU) VALUES (:1,:2)", avoir_type)

        diriger = gen_diriger_with_ids(employes_ids, departements_ids)
        cur.executemany("""INSERT INTO DIRIGER(CODEE,CODED,DATEDEBUTDIR)
                           VALUES (:1,:2,:3)""", diriger)

        autoriser = gen_autoriser_with_ids(qualifs_ids, departements_ids)
        cur.executemany("INSERT INTO AUTORISER(CODEQ,CODED) VALUES (:1,:2)", autoriser)

        fabriquer = gen_fabriquer_with_ids(usines_with_ids, produits_ids, typeu_with_ids)
        cur.executemany("""INSERT INTO FABRIQUER_ASSEMBLER1(CODEU,CODEP,DATEFAB,QTE_FAB)
                           VALUES (:1,:2,:3,:4)""", fabriquer)

        responsable = gen_responsable_with_ids(employes_ids, gammes)
        cur.executemany("""INSERT INTO RESPONSABLE(CODEE,CODEG,ANNEE)
                           VALUES (:1,:2,:3)""", responsable)

        payer2 = gen_payer2(gammes)
        cur.executemany("""INSERT INTO PAYER2(CODEG,ANNEE,INDICERETROCESSIONG)
                           VALUES (:1,:2,:3)""", payer2)

        facturer = gen_facturer_with_ids(produits_ids)
        cur.executemany("""INSERT INTO FACTURER(CODEP,MOIS,ANNEE,PRIXUNITP)
                           VALUES (:1,:2,:3,:4)""", facturer)

        vendre = gen_vendre_with_ids(employes_ids, pvs_ids, produits_ids)
        cur.executemany("""INSERT INTO VENDRE(CODEE,CODEPV,CODEP,MOIS,ANNEE,QTE_VENDUE)
                           VALUES (:1,:2,:3,:4,:5,:6)""", vendre)

        payer1 = gen_payer1_with_ids(employes_ids)
        cur.executemany("""INSERT INTO PAYER1(CODEE,ANNEE,FIXEMENSUELE,INDICESALE)
                           VALUES (:1,:2,:3,:4)""", payer1)

        trav_u = gen_travailler_usine_with_ids(employes_ids, departements_ids)
        cur.executemany("""INSERT INTO TRAVAILLER_USINE(CODEE,CODED,MOIS,ANNEE,NBHEURES_U)
                           VALUES (:1,:2,:3,:4,:5)""", trav_u)

        trav_pv = gen_travailler_pv_with_ids(employes_ids, pvs_ids)
        cur.executemany("""INSERT INTO TRAVAILLER_PT_VENTE(CODEE,CODEPV,MOIS,ANNEE,NBHEURES_PV)
                           VALUES (:1,:2,:3,:4,:5)""", trav_pv)

        con.commit()
        print("✅ Peuplement terminé.")

if __name__ == "__main__":
    main()
