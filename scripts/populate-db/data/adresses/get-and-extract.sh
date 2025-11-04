#!/bin/zsh

# Ensure we have the CSV (non-empty); if not, download and decompress
if [ ! -s ./adresses-france.csv ]; then
  echo "adresses-france.csv missing or empty — downloading..."
  url="https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/adresses-france.csv.gz"
  if command -v wget >/dev/null 2>&1; then
    wget -q -O adresses-france.csv.gz "$url" || { echo "Download failed"; exit 1; }
  else
    curl -sSfL -o adresses-france.csv.gz "$url" || { echo "Download failed"; exit 1; }
  fi
  if command -v gunzip >/dev/null 2>&1; then
    gunzip -f adresses-france.csv.gz || { echo "Decompression failed"; exit 1; }
  else
    gzip -d -f adresses-france.csv.gz || { echo "Decompression failed"; exit 1; }
  fi
fi

# Shuffle and extract 10000 random addresses
shuf -n 10000 adresses-france.csv > adresses-france-shuffle.csv

# Add header
echo "numero,nom_voie,code_postal,nom_commune" > adresses-france-extract.csv

# Keep only needed columns (numero, nom_voie, code_postal, nom_commune)
awk -F';' '{print $3 "," $5 "," $6 "," $8}' adresses-france-shuffle.csv >> adresses-france-extract.csv

# Clean up intermediate file
rm adresses-france-shuffle.csv