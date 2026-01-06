from odoo import models, fields, api
import hashlib
import secrets

class UserAccessApi(models.Model):
    _name = 'user.access.api'
    _description = 'API User Access'

    name = fields.Char(string="Username", required=True)
    password = fields.Char(string="Password", required=True)
    password_hash = fields.Char(string="Password Hash", readonly=True)
    client_id = fields.Char(string="Client ID", default=lambda self: secrets.token_hex(8), readonly=True, copy=False)
    client_secret = fields.Char(string="Client Secret", default=lambda self: secrets.token_hex(16), readonly=True, copy=False)

    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        # Auto-generate password hash
        if 'password' in vals:
            vals['password_hash'] = hashlib.sha256(vals['password'].encode()).hexdigest()

        # Auto-generate client_id and client_secret
        if not vals.get('client_id'):
            vals['client_id'] = secrets.token_hex(8)  # 16-char random ID
        if not vals.get('client_secret'):
            vals['client_secret'] = secrets.token_hex(16)  # 32-char secret

        return super().create(vals)

    def write(self, vals):
        # Update hash if password changes
        if 'password' in vals:
            vals['password_hash'] = hashlib.sha256(vals['password'].encode()).hexdigest()
        return super().write(vals)
