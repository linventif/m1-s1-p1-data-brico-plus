#!/bin/bash
set -e

# === Oracle 23c Free Installer Script for Ubuntu 24.04 (Proxmox-compatible) ===

ORACLE_USER="PROJET_BRICO_PLUS"
ORACLE_PASS="BricoPlus123"
DEB_FILE="/tmp/oracle-database-free-23c.deb"
LOG_FILE="/var/log/oracle_install.log"

echo "=== 🧱 Updating system ==="
sudo apt update -y && sudo apt install -y wget net-tools unzip libaio1t64

echo "=== 📦 Downloading Oracle Database 23c Free .deb ==="
wget -O "$DEB_FILE" https://objectstorage.eu-frankfurt-1.oraclecloud.com/n/axjz2ybxq1bd/b/free23c/o/oracle-database-free-23c-1.0-1-linux.x64.deb

echo "=== 💿 Installing Oracle Database 23c Free ==="
sudo dpkg -i "$DEB_FILE" || sudo apt -f install -y

echo "=== ⚙️ Configuring Oracle (first-time setup) ==="
sudo /etc/init.d/oracle-free-23c configure | tee "$LOG_FILE"

echo "=== ✅ Oracle Database installed successfully ==="

# --- CREATE USER AND GRANT PRIVILEGES ---
echo "=== 👤 Creating application user $ORACLE_USER ==="

sudo -u oracle bash <<EOF
source /opt/oracle/product/23c/dbhomeFree/bin/oraenv <<< "FREE"
sqlplus / as sysdba <<SQL
WHENEVER SQLERROR EXIT SQL.SQLCODE;
CREATE USER $ORACLE_USER IDENTIFIED BY "$ORACLE_PASS";
GRANT CONNECT, RESOURCE, DBA TO $ORACLE_USER;
ALTER USER $ORACLE_USER QUOTA UNLIMITED ON USERS;
EXIT;
SQL
EOF

echo "=== 🧠 Oracle user $ORACLE_USER created successfully ==="
echo "=== 🔗 Connection info ==="
echo ""
echo "Host: $(hostname -I | awk '{print $1}')"
echo "Port: 1521"
echo "Service: FREEPDB1"
echo "User: $ORACLE_USER"
echo "Password: $ORACLE_PASS"
echo ""
echo "JDBC URL:"
echo "jdbc:oracle:thin:@//$(hostname -I | awk '{print $1}'):1521/FREEPDB1"
echo ""
echo "=== 🚀 Oracle 23c Free is ready ==="
echo "To start Oracle automatically on boot, run: sudo systemctl enable oracle-free-23c"
