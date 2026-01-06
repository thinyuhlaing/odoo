Sure! Here's the full `README.md` content ready to copy and paste:

````markdown
# Odoo 18 Setup from Source

This guide explains how to set up **Odoo 18** from source using a Python virtual environment.

---

## 1️⃣ Prerequisites

Make sure the following are installed:

- Python 3.x
- PostgreSQL
- Git
- pip

---

## 2️⃣ Clone Odoo Source Code

```bash
git clone https://github.com/thinyuhlaing3/odoo
cd odoo
```
````

---

## 3️⃣ Create Python Virtual Environment

```bash
cd odoo
python3 -m venv venv
source venv/bin/activate
```

> This creates and activates a virtual environment named `venv`.

---

## 4️⃣ Install Python Requirements

```bash
pip install wheel
pip install -r requirements.txt
```

> Ensure all dependencies are installed before running Odoo.

---

## 5️⃣ Create Odoo Configuration File

Create a configuration file `odoo18.conf`:

```bash
sudo nano odoo18.conf
```

Paste the following (update paths and database credentials):

```
[options]
addons_path = /path/folder/odoo18/addons,/path/folder/odoo18/custom_addons
data_dir = /path/folder/odoo18/data
logfile = /path/folder/odoo18/odoo.log

db_user = myuser
db_password = mypassword
db_host = localhost
db_port = 5432
db_name = mydb

xmlrpc_port = 8069
```

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).

---

## 6️⃣ Run Odoo from Source

Activate the virtual environment if not already active:

```bash
source venv/bin/activate
```

Start Odoo:

```bash
python odoo-bin -c odoo18.conf
```

Optional: Install base module while running:

```bash
python odoo-bin -c odoo18.conf -d mydb -i base
```

---

## 7️⃣ Access Odoo

Open your browser and go to:

- Localhost: [http://localhost:8069](http://localhost:8069)
- Server IP: `http://YOUR_SERVER_IP:8069`

You should now see the Odoo 18 setup page.

---
