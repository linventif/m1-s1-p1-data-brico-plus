#!/bin/zsh
# Download patronymes.csv and prenom.csv if missing
patronymes_url="https://www.data.gouv.fr/fr/datasets/r/9ae80de2-a41e-4282-b9f8-61e6850ef449"
prenoms_url="https://www.data.gouv.fr/fr/datasets/r/4b13bbf2-4185-4143-92d3-8ed5d990b0fa"

if [ ! -s patronymes.csv ]; then
  echo "patronymes.csv missing or empty — downloading..."
  if command -v wget >/dev/null 2>&1; then
    wget -q -O patronymes.csv "$patronymes_url" || { echo "Download failed"; exit 1; }
  else
    curl -sSfL -o patronymes.csv "$patronymes_url" || { echo "Download failed"; exit 1; }
  fi
fi

if [ ! -s prenom.csv ]; then
  echo "prenom.csv missing or empty — downloading..."
  if command -v wget >/dev/null 2>&1; then
    wget -q -O prenom.csv "$prenoms_url" || { echo "Download failed"; exit 1; }
  else
    curl -sSfL -o prenom.csv "$prenoms_url" || { echo "Download failed"; exit 1; }
  fi
fi

# Sort patronymes.csv by count (descending), keep top 10000
head -n 1 patronymes.csv > patronymes-extract.csv
tail -n +2 patronymes.csv | sort -t',' -k2,2nr | head -n 10000 >> patronymes-extract.csv

# Sort prenom.csv by sum (descending), keep top 10000
head -n 1 prenom.csv > prenom-extract.csv
tail -n +2 prenom.csv | sort -t',' -k2,2nr | head -n 10000 >> prenom-extract.csv