# Odoo 15 Community Installation Guide

This guide documents the local macOS setup used for this checkout.

## Environment

- Odoo: 15.0 Community
- Python: 3.8.20 via pyenv
- PostgreSQL client/server: PostgreSQL 18.3 via Homebrew
- Project directory: `/Users/thinyu/bee/odoo/odoo15/community`
- Odoo config: `odoo.conf`
- HTTP port: `8099`

## 1. Install Python With pyenv

Install Python 3.8.20 if it is not already available:

```bash
pyenv install 3.8.20
```

Set the project Python:

```bash
cd /Users/thinyu/bee/odoo/odoo15/community
pyenv local 3.8.20
```

Verify:

```bash
python --version
```

Expected:

```text
Python 3.8.20
```

## 2. Create a Clean Virtual Environment

From the `community` directory:

```bash
rm -rf venv
python -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip setuptools wheel
```

## 3. Install Python Dependencies

Odoo 15's original `cryptography==2.6.1` pin does not build cleanly against modern Homebrew OpenSSL 3. Use this compatible wheel-based pair first:

```bash
python -m pip install "cryptography==3.4.8" "pyOpenSSL==20.0.1"
```

Then install the remaining Odoo requirements without the old crypto pins:

```bash
rg -v '^(cryptography|pyopenssl)' requirements.txt > /tmp/odoo15-requirements-no-crypto.txt
python -m pip install -r /tmp/odoo15-requirements-no-crypto.txt
```

Verify:

```bash
python -m pip check
python odoo-bin --version
```

Expected:

```text
No broken requirements found.
Odoo Server 15.0
```

## 4. Configure PostgreSQL

Start PostgreSQL 18:

```bash
brew services start postgresql@18
```

Create or update the Odoo database role:

```bash
createuser -s odoo
psql -d postgres -c "ALTER USER odoo WITH PASSWORD '296092';"
```

Verify PostgreSQL is reachable:

```bash
pg_isready -h localhost -p 5432
```

## 5. Configure Odoo

The local `odoo.conf` should include:

```ini
[options]
addons_path = /Users/thinyu/bee/odoo/odoo15/community/addons,/Users/thinyu/bee/odoo/odoo15/community/odoo/addons
db_user = odoo
db_password = 296092
db_host = localhost
db_port = 5432
xmlrpc_port = 8099
limit_memory_hard = 0
admin_passwd = odoo123
```

Notes:

- `limit_memory_hard = 0` avoids a macOS `resource.setrlimit` startup error.
- Both addon paths are required so Odoo can load core modules and Community apps.

## 6. Apply the PostgreSQL DSN Compatibility Fix

Modern PostgreSQL/libpq can return DSN strings with quoted values. Odoo 15's original parser splits on spaces and can fail on `/web/database/selector`.

In `odoo/sql_db.py`, `_dsn_to_dict` should be:

```python
def _dsn_to_dict(self, dsn):
    return psycopg2.extensions.parse_dsn(dsn)
```

This replaces the old manual split:

```python
return dict(value.split('=', 1) for value in dsn.strip().split())
```

## 7. Run Odoo

```bash
cd /Users/thinyu/bee/odoo/odoo15/community
source venv/bin/activate
python odoo-bin -c odoo.conf
```

Open:

```text
http://localhost:8099
```

## 8. Smoke Test

Check startup without keeping the server running:

```bash
python odoo-bin -c odoo.conf --stop-after-init
```

Check the database selector:

```bash
curl -I http://127.0.0.1:8099/web/database/selector
```

Expected HTTP status:

```text
200 OK
```

## Optional: Install wkhtmltopdf

Odoo can run without wkhtmltopdf, but PDF reports will show this warning:

```text
You need Wkhtmltopdf to print a pdf version of the reports.
```

Install it if PDF reports are needed.

