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
# TYPEU (NomTU) : chaine assemblage, scierie, métallurgie, fonderie (enum)  :contentReference[oaicite:1]{index=1}
TYPEU = ["assemblage", "scierie", "métallurgie", "fonderie"]

# GAMME (Code GXX et libellé)  :contentReference[oaicite:2]{index=2}
GAMMES = [
    "jardin et piscine", "mobilier intérieur", "plomberie et chauffage", "salle de bain et WC",
    "luminaire", "électricité et domotique", "quincaillerie", "cuisine",
    "peinture et droguerie", "carrelage et parquet", "matériaux de construction", "outillage"
]
# NB: le sujet liste 11 libellés, on complète avec "outillage" pour arriver à 12 codes G01..G12.
# Le format de code attendu est GXX (ex: G01)  :contentReference[oaicite:3]{index=3}

# DEPARTEMENTS (NomD) : fabrication, assemblage, RH, expédition, logistique, direction, finance  :contentReference[oaicite:4]{index=4}
DEPTS = ["fabrication", "assemblage", "RH", "expédition", "logistique", "direction", "finance"]

# POINTS_DE_VENTE TypePV : GSB, Brico-Express  :contentReference[oaicite:5]{index=5}
PV_TYPES = ["GSB", "Brico-Express"]

# -----------------------
# VOLUMÉTRIE VISÉE
# -----------------------
N_EMP = 50
N_QUALIF = 50
N_USINES = 30
N_PV = 50
N_PRODUITS = 50

# Calendriers (~50 lignes)
N_CAL1 = 50  # DATEFAB
N_CAL2 = 50  # DATEDEBUTDIR
# CAL3 = 50 couples (mois, année) <= année courante  :contentReference[oaicite:6]{index=6}
# CAL4 = 50 années (<= année courante)
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

# 50 années : YEAR_NOW-49 .. YEAR_NOW (toutes <= année courante)  :contentReference[oaicite:7]{index=7}
cal4 = list(range(YEAR_NOW - 49, YEAR_NOW + 1))

# 50 dates <= aujourd’hui pour CAL1 & CAL2  :contentReference[oaicite:8]{index=8}
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
            "Moreau", "Laurent", "Simon", "Michel", "Lefebvre", "Leroy", "Roux", "David"
        ])
        prenom = random.choice([
            "Lucas", "Louis", "Hugo", "Arthur", "Jules", "Adam", "Léo", "Noah",
            "Emma", "Louise", "Chloé", "Lina", "Mia", "Anna", "Zoé", "Léa"
        ])
        vpers, cppers = pick_city(True)
        vpro, cppro = pick_city(True)
        rows.append((
            code, nom, prenom,
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
        rows.append((code, nom, taux, None))
    # Crée quelques liens de "complétée par" (réflexive 0,n <> 0,1)
    for i in range(2, min(n, 15)):
        rows[i-1] = (rows[i-1][0], rows[i-1][1], rows[i-1][2], random.randint(1, i-1))
    return rows

def gen_usines(n=N_USINES):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        rows.append((code,
                     f"Usine {city} {code}",
                     street(), cp, city, phone(hg=cp.startswith("31"))))
    return rows

def gen_typeu():
    rows = []
    for i, nom in enumerate(TYPEU, start=1):
        rows.append((i, nom))
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

def gen_points_vente(n=N_PV):
    rows = []
    for code in range(1, n+1):
        city, cp = pick_city(True)
        rows.append((code,
                     f"Brico {city} {code}",
                     street(), cp, city, phone(hg=cp.startswith("31")),
                     random.choices(PV_TYPES, weights=[0.6, 0.4])[0]))  # un peu plus de GSB
    return rows

def gen_produits(n=N_PRODUITS):
    rows = []
    for code in range(1, n+1):
        nom = random.choice([
            "Perceuse", "Peinture acrylique", "Câble électrique", "Mitigeur", "Panneau LED",
            "Tasseau bois", "Faïence murale", "Robinet thermostatique", "Visserie inox",
            "Parquet chêne", "Tondeuse", "Pompe piscine"
        ]) + f" {random.randint(100,999)}"
        marque = random.choice(["ProLine", "MaisonPro", "BuildX", "Crafto", "Lumina", "AquaFix"])
        codeg = gen_gammes()[random.randint(0, len(GAMMES)-1)][0]
        rows.append((code, nom, marque, codeg))
    return rows

def gen_posseder(employes, qualifs):
    rows = []
    for e in employes:
        qset = random.sample(qualifs, k=random.randint(1, 3))
        for q in qset:
            rows.append((e[0], q[0]))
    # 50 lignes min
    return rows[:max(50, len(rows))]

def gen_assembler(produits):
    rows = []
    used = set()
    for _ in range(50):
        a, b = random.sample(produits, 2)
        if a[0] == b[0]:
            continue
        key = (a[0], b[0])
        if key in used:
            continue
        used.add(key)
        rows.append((a[0], b[0], random.randint(1, 6)))
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
    for _ in range(50):
        e = random.choice(employes)[0]
        d = random.choice(departements)[0]
        date = random.choice(cal2_dates)
        rows.append((e, d, date))
    # unique par PK (CODEE, CODED, DATEDEBUTDIR) => dédoublonne
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:50]

def gen_autoriser(qualifs, departements):
    rows = []
    for d in random.sample(departements, k=min(50, len(departements))):
        for q in random.sample(qualifs, k=random.randint(2, 5)):
            rows.append((q[0], d[0]))
    return rows[:50]

def gen_fabriquer(usines, produits):
    rows = []
    # 70% des fabrications hors HG pour servir la requête 5 (vendus en HG mais fabriqués ailleurs)
    ext_usines = [u for u in usines if not str(u[3]).startswith("31")]
    loc_usines = [u for u in usines if str(u[3]).startswith("31")]
    for _ in range(50):
        if ext_usines and random.random() < 0.7:
            u = random.choice(ext_usines)
        else:
            u = random.choice(loc_usines or usines)
        p = random.choice(produits)
        d = random.choice(cal1_dates)
        q = random.randint(5, 300)
        rows.append((u[0], p[0], d, q))
    rows = list({(a, b, c, d) for (a, b, c, d) in rows})
    return rows[:50]

def gen_responsable(employes, gammes):
    rows = []
    years = random.sample(cal4, k=5)
    for _ in range(50):
        e = random.choice(employes)[0]
        g = random.choice(gammes)[0]
        y = random.choice(years)
        rows.append((e, g, y))
    rows = list({(a, b, c) for (a, b, c) in rows})
    return rows[:50]

def gen_payer2(gammes):
    rows = []
    years = random.sample(cal4, k=5)
    for g in gammes:
        for y in years:
            rows.append((g[0], y, round(random.uniform(0.05, 0.25), 2)))
    return rows[:50]

def gen_facturer(produits):
    rows = []
    for p in produits:
        for (m, y) in random.sample(cal3, k= random.randint(2, 6)):
            pu = round(random.uniform(4.0, 1500.0), 2)
            rows.append((p[0], m, y, pu))
    return rows[:50]

def gen_vendre(employes, pvs, produits):
    rows = []
    # Pour satisfaire la requête 1 : aucune vente Brico-Express pour une gamme donnée (ex: quincaillerie)
    # -> On évite de vendre des produits de la gamme "quincaillerie" en Brico-Express
    quinca_code = None
    for i, g in enumerate(GAMMES, start=1):
        if g == "quincaillerie":
            quinca_code = f"G{str(i).zfill(2)}"
            break

    for _ in range(200):
        e = random.choice(employes)[0]
        pv = random.choice(pvs)
        p = random.choice(produits)
        # règle pour Brico-Express & quincaillerie
        if pv[-1] == "Brico-Express" and p[3] == quinca_code:
            continue
        (m, y) = random.choice(cal3)
        q = random.randint(1, 50)
        rows.append((e, pv[0], p[0], m, y, q))
    rows = list({(a, b, c, d, e, f) for (a, b, c, d, e, f) in rows})
    return rows[:50]

def gen_payer1(employes):
    rows = []
    years = random.sample(cal4, k=5)
    for e in employes:
        for y in years:
            fixe = round(random.uniform(1300, 4200), 2)
            idx = random.randint(1, 10)
            rows.append((e[0], y, fixe, idx))
    return rows[:50]

def gen_travailler_usine(employes, departements):
    rows = []
    for _ in range(80):
        e = random.choice(employes)[0]
        d = random.choice(departements)[0]
        (m, y) = random.choice(cal3)
        hrs = round(random.uniform(10, 180), 2)
        rows.append((e, d, m, y, hrs))
    rows = list({(a, b, c, d, e) for (a, b, c, d, e) in rows})
    return rows[:50]

def gen_travailler_pv(employes, pvs):
    rows = []
    for _ in range(80):
        e = random.choice(employes)[0]
        pv = random.choice(pvs)[0]
        (m, y) = random.choice(cal3)
        hrs = round(random.uniform(5, 160), 2)
        rows.append((e, pv, m, y, hrs))
    rows = list({(a, b, c, d, e) for (a, b, c, d, e) in rows})
    return rows[:50]

# -----------------------
# INSERTS
# -----------------------
def main():
    print(f"Connecting to {USER}@{HOST}:{PORT}/{SERVICE} ...")
    with oracledb.connect(user=USER, password=PASS, dsn=DSN) as con:
        cur = con.cursor()

        # Parents
        typeu = gen_typeu()
        cur.executemany("INSERT INTO TYPEU(CODETU, NOMTU) VALUES (:1,:2)", typeu)

        gammes = gen_gammes()
        cur.executemany("INSERT INTO GAMME(CODEG, NOMG) VALUES (:1,:2)", gammes)

        cal1, cal2, cal3_rows, cal4_rows = gen_calendriers()
        cur.executemany("INSERT INTO CALENDRIER1(DATEFAB) VALUES (:1)", cal1)
        cur.executemany("INSERT INTO CALENDRIER2(DATEDEBUTDIR) VALUES (:1)", cal2)
        cur.executemany("INSERT INTO CALENDRIER3(MOIS, ANNEE) VALUES (:1,:2)", cal3_rows)
        cur.executemany("INSERT INTO CALENDRIER4(ANNEE) VALUES (:1)", cal4_rows)

        usines = gen_usines()
        cur.executemany("""INSERT INTO USINES(CODEU,NOMU,RUEU,CPOSTALU,VILLEU,TELU)
                           VALUES (:1,:2,:3,:4,:5,:6)""", usines)

        employes = gen_employes()
        cur.executemany("""INSERT INTO EMPLOYES
                           (CODEE,NOME,PRENOME,RUEPERSE,CPOSTALPERSE,VILLEPERSE,
                            RUEPROE,CPOSTALPROE,VILLEPROE,TELPERSE,TELPROE)
                           VALUES (:1,:2,:3,:4,:5,:6,:7,:8,:9,:10,:11)""", employes)

        qualifs = gen_qualifs()
        cur.executemany("""INSERT INTO QUALIFICATIONS
                           (CODEQ,NOMQ,TAUXMINQ,CODEQ_EST_COMPLETEE)
                           VALUES (:1,:2,:3,:4)""", qualifs)

        # Dépendants
        departements = gen_departements(usines)
        cur.executemany("""INSERT INTO DEPARTEMENTS(CODED,NOMD,CODEU) VALUES (:1,:2,:3)""", departements)

        pvs = gen_points_vente()
        cur.executemany("""INSERT INTO POINTS_DE_VENTE
                           (CODEPV,NOMPV,RUEPV,CPOSTALPV,VILLEPV,TELPV,TYPEPV)
                           VALUES (:1,:2,:3,:4,:5,:6,:7)""", pvs)

        produits = gen_produits()
        cur.executemany("""INSERT INTO PRODUITS(CODEP,NOMP,MARQUEP,CODEG) VALUES (:1,:2,:3,:4)""", produits)

        # Associations / faits
        posseder = gen_posseder(employes, qualifs)
        cur.executemany("INSERT INTO POSSEDER(CODEE,CODEQ) VALUES (:1,:2)", posseder)

        assembler = gen_assembler(produits)
        cur.executemany("""INSERT INTO ASSEMBLER(CODEP_EST_COMPOSE,CODEP_COMPOSE,QTE_ASSEMBL)
                           VALUES (:1,:2,:3)""", assembler)

        avoir_type = gen_avoir_type(usines, typeu)
        cur.executemany("INSERT INTO AVOIR_TYPE(CODEU,CODETU) VALUES (:1,:2)", avoir_type)

        diriger = gen_diriger(employes, departements)
        cur.executemany("""INSERT INTO DIRIGER(CODEE,CODED,DATEDEBUTDIR)
                           VALUES (:1,:2,:3)""", diriger)

        autoriser = gen_autoriser(qualifs, departements)
        cur.executemany("INSERT INTO AUTORISER(CODEQ,CODED) VALUES (:1,:2)", autoriser)

        fabriquer = gen_fabriquer(usines, produits)
        cur.executemany("""INSERT INTO FABRIQUER_ASSEMBLER1(CODEU,CODEP,DATEFAB,QTE_FAB)
                           VALUES (:1,:2,:3,:4)""", fabriquer)

        responsable = gen_responsable(employes, gammes)
        cur.executemany("""INSERT INTO RESPONSABLE(CODEE,CODEG,ANNEE)
                           VALUES (:1,:2,:3)""", responsable)

        payer2 = gen_payer2(gammes)
        cur.executemany("""INSERT INTO PAYER2(CODEG,ANNEE,INDICERETROCESSIONG)
                           VALUES (:1,:2,:3)""", payer2)

        facturer = gen_facturer(produits)
        cur.executemany("""INSERT INTO FACTURER(CODEP,MOIS,ANNEE,PRIXUNITP)
                           VALUES (:1,:2,:3,:4)""", facturer)

        vendre = gen_vendre(employes, pvs, produits)
        cur.executemany("""INSERT INTO VENDRE(CODEE,CODEPV,CODEP,MOIS,ANNEE,QTE_VENDUE)
                           VALUES (:1,:2,:3,:4,:5,:6)""", vendre)

        payer1 = gen_payer1(employes)
        cur.executemany("""INSERT INTO PAYER1(CODEE,ANNEE,FIXEMENSUELE,INDICESALE)
                           VALUES (:1,:2,:3,:4)""", payer1)

        trav_u = gen_travailler_usine(employes, departements)
        cur.executemany("""INSERT INTO TRAVAILLER_USINE(CODEE,CODED,MOIS,ANNEE,NBHEURES_U)
                           VALUES (:1,:2,:3,:4,:5)""", trav_u)

        trav_pv = gen_travailler_pv(employes, pvs)
        cur.executemany("""INSERT INTO TRAVAILLER_PT_VENTE(CODEE,CODEPV,MOIS,ANNEE,NBHEURES_PV)
                           VALUES (:1,:2,:3,:4,:5)""", trav_pv)

        con.commit()
        print("✅ Peuplement terminé.")

if __name__ == "__main__":
    main()
