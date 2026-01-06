from odoo import http
from odoo.http import request
import hashlib, jwt, datetime, json

SECRET_KEY = "SuperSecretKey@2025"
JWT_ALGORITHM = "HS256"


class OAuthController(http.Controller):

    # ----------------------------
    # Token Endpoint (/oauth/token)
    # ----------------------------
    @http.route('/oauth/token', type='http', auth='none', methods=['POST'], csrf=False)
    def oauth_token(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
        except:
            return http.Response(json.dumps({'error': 'invalid_request'}), status=400, content_type='application/json')

        grant_type = data.get('grant_type')
        if grant_type != 'password':
            return http.Response(json.dumps({'error': 'unsupported_grant_type'}), status=400, content_type='application/json')

        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        username = data.get('username')
        password = data.get('password')

        if not all([client_id, client_secret, username, password]):
            return http.Response(json.dumps({'error': 'invalid_request'}), status=400, content_type='application/json')

        # Validate client
        client = request.env['user.access.api'].sudo().search([
            ('client_id', '=', client_id),
            ('client_secret', '=', client_secret),
            ('active', '=', True)
        ], limit=1)

        if not client:
            return http.Response(json.dumps({'error': 'invalid_client'}), status=401, content_type='application/json')

        # Validate user
        user = request.env['user.access.api'].sudo().search([
            ('name', '=', username),
            ('active', '=', True)
        ], limit=1)

        if not user:
            return http.Response(json.dumps({'error': 'invalid_grant'}), status=401, content_type='application/json')

        hashed = hashlib.sha256(password.encode()).hexdigest()
        if hashed != user.password_hash:
            return http.Response(json.dumps({'error': 'invalid_grant'}), status=401, content_type='application/json')

        # Generate access & refresh tokens
        access_payload = {
            'api_user_id': user.id,
            'username': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        access_token = jwt.encode(access_payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(access_token, bytes):
            access_token = access_token.decode('utf-8')

        refresh_payload = {
            'api_user_id': user.id,
            'type': 'refresh',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7)
        }
        refresh_token = jwt.encode(refresh_payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(refresh_token, bytes):
            refresh_token = refresh_token.decode('utf-8')

        return http.Response(json.dumps({
            'access_token': access_token,
            'token_type': 'Bearer',
            'expires_in': 7200, # 2 hours
            'refresh_token': refresh_token
        }), status=200, content_type='application/json')


    # ----------------------------
    # Refresh Token Endpoint
    # ----------------------------
    @http.route('/oauth/refresh', type='http', auth='none', methods=['POST'], csrf=False)
    def oauth_refresh(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
        except:
            return http.Response(json.dumps({'error': 'invalid_request'}), status=400, content_type='application/json')

        grant_type = data.get('grant_type')
        refresh_token = data.get('refresh_token')

        if grant_type != 'refresh_token' or not refresh_token:
            return http.Response(json.dumps({'error': 'invalid_request'}), status=400, content_type='application/json')

        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            if payload.get('type') != 'refresh':
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return http.Response(json.dumps({'error': 'token_expired'}), status=401, content_type='application/json')
        except jwt.InvalidTokenError:
            return http.Response(json.dumps({'error': 'invalid_token'}), status=401, content_type='application/json')

        user = request.env['user.access.api'].sudo().browse(payload['api_user_id'])
        if not user or not user.active:
            return http.Response(json.dumps({'error': 'invalid_user'}), status=401, content_type='application/json')

        new_access_payload = {
            'api_user_id': user.id,
            'username': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        new_access_token = jwt.encode(new_access_payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(new_access_token, bytes):
            new_access_token = new_access_token.decode('utf-8')

        return http.Response(json.dumps({
            'access_token': new_access_token,
            'token_type': 'Bearer',
            'expires_in': 7200
        }), status=200, content_type='application/json')


    # ----------------------------
    # Token Verification Helper
    # ----------------------------   check this point
    def verify_token(self, request):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return {'error': 'invalid_token'}

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            api_user = request.env['user.access.api'].sudo().browse(payload['api_user_id'])
            if not api_user or not api_user.active:
                return {'error': 'invalid_user'}
            return api_user
        except jwt.ExpiredSignatureError:
            return {'error': 'token_expired'}
        except jwt.InvalidTokenError:
            return {'error': 'invalid_token'}

    # ----------------------------
    # eg Protected Endpoint
    # ----------------------------
    @http.route('/api/me', type='http', auth='none', methods=['GET'], csrf=False)
    def api_me(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        return http.Response(json.dumps({
            'id': api_user.id,
            'username': api_user.name,
            'active': api_user.active
        }), status=200, content_type='application/json')


    # ======================================================
    #  CRUD: HR Employee Endpoints
    # ======================================================

    @http.route('/api/employees', type='http', auth='none', methods=['GET'], csrf=False)
    def get_employees(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        admin_user = request.env['res.users'].sudo().browse(1)  # admin user
        employees = request.env['hr.employee'].with_user(admin_user).sudo().search([])
        # response data employee route
        data = [{
            'id': emp.id,
            'name': emp.name,
            'work_email': emp.work_email,
            'job_title': emp.job_id.name if emp.job_id else '',
            'department': emp.department_id.name if emp.department_id else '',
            'work_phone': emp.work_phone,
            'mobile_phone': emp.mobile_phone,
            'pin': emp.pin
        } for emp in employees]

        return http.Response(json.dumps({'count': len(data), 'employees': data}),
                            status=200,
                            content_type='application/json')

    @http.route('/api/employees', type='http', auth='none', methods=['POST'], csrf=False)
    def create_employee(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        try:
            data = json.loads(request.httprequest.data)
        except:
            return http.Response(json.dumps({'error': 'invalid_json'}), status=400, content_type='application/json')
        # user ref id 
        admin_user = request.env['res.users'].sudo().browse(1)
        
        new_emp = request.env['hr.employee'].with_user(admin_user).sudo().create({
            'name': data.get('name'),
            'work_email': data.get('work_email'),
            'job_title': data.get('job_title'),
            'work_phone': data.get('work_phone')
        })

        return http.Response(json.dumps({'id': new_emp.id, 'message': 'Employee created'}), status=201, content_type='application/json')

    @http.route('/api/employees/<int:emp_id>', type='http', auth='none', methods=['PUT'], csrf=False)
    def update_employee(self, emp_id, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')
        admin_user = request.env['res.users'].sudo().browse(1)
        emp = request.env['hr.employee'].with_user(admin_user).sudo().browse(emp_id)
        if not emp.exists():
            return http.Response(json.dumps({'error': 'not_found'}), status=404, content_type='application/json')

        try:
            data = json.loads(request.httprequest.data)
        except:
            return http.Response(json.dumps({'error': 'invalid_json'}), status=400, content_type='application/json')

        emp.sudo().write({
            'name': data.get('name', emp.name),
            'work_email': data.get('work_email', emp.work_email),
            'job_title': data.get('job_title', emp.job_title),
            'work_phone': data.get('work_phone', emp.work_phone)
        })

        return http.Response(json.dumps({'message': 'Employee updated'}), status=200, content_type='application/json')

    @http.route('/api/employees/<int:emp_id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_employee(self, emp_id, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')
        admin_user = request.env['res.users'].sudo().browse(1)
        emp = request.env['hr.employee'].with_user(admin_user).sudo().browse(emp_id)
        if not emp.exists():
            return http.Response(json.dumps({'error': 'not_found'}), status=404, content_type='application/json')

        emp.sudo().unlink()
        return http.Response(json.dumps({'message': 'Employee deleted'}), status=200, content_type='application/json')
