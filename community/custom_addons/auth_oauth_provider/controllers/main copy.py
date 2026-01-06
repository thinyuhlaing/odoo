from odoo import http
from odoo.http import request
import hashlib
import jwt
import datetime
import json

SECRET_KEY = "SuperSecretKey@2025"
JWT_ALGORITHM = "HS256"

class ApiController(http.Controller):

    # ------------------------
    # Login → Generate JWT Token
    # ------------------------
    @http.route('/api/auth/login', type='http', auth='none', methods=['POST'], csrf=False)
    def api_login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
        except:
            return json.dumps({'error':'Invalid JSON'})

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return json.dumps({'error': 'Missing username or password'})

        user = request.env['user.access.api'].sudo().search(
            [('name', '=', username), ('active', '=', True)], limit=1
        )
        if not user:
            return json.dumps({'error': 'Invalid username or password'})

        hashed = hashlib.sha256(password.encode()).hexdigest()
        if hashed != user.password_hash:
            return json.dumps({'error': 'Invalid username or password'})

        payload = {
            'api_user_id': user.id,
            'username': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return json.dumps({
            'success': True,
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': 7200
        })

    # ------------------------
    # Verify JWT Token (API-only)
    # ------------------------
    def verify_token(self, request):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return {'error': 'Missing or invalid Authorization header'}

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            api_user = request.env['user.access.api'].sudo().browse(payload['api_user_id'])
            if not api_user or not api_user.active:
                return {'error': 'Invalid user'}
            return api_user  # return API user directly
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

    # ------------------------
    # API Endpoint: Get Employees (no res.users needed)
    # ------------------------
    # @http.route('/api/employees', type='http', auth='none', methods=['GET'], csrf=False)
    # def api_employees(self, **kw):
    #     api_user = self.verify_token(request)
    #     if isinstance(api_user, dict):  # error
    #         return http.Response(json.dumps(api_user), status=401, content_type='application/json')

    #     # Use sudo() + no_access_rights context
    #     employees = request.env['hr.employee'].sudo().with_context(no_access_rights=True).search([])
    #     data = []
    #     for e in employees:
    #         data.append({
    #             'id': e.id,
    #             'name': e.name,
    #             'work_email': e.work_email,
    #             'work_phone': e.work_phone,
    #             'mobile_phone': e.mobile_phone,
    #             'job_title': e.job_id.name if e.job_id else '',
    #             'department': e.department_id.name if e.department_id else '',
    #         })

    #     return http.Response(
    #         json.dumps({'count': len(data), 'employees': data}),
    #         status=200,
    #         content_type='application/json'
    #     )

    @http.route('/api/employees', type='http', auth='none', methods=['GET'], csrf=False)
    def api_employees(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        admin_user = request.env['res.users'].sudo().browse(1)  # admin
        employees = request.env['hr.employee'].with_user(admin_user).sudo().search([])

        data = []
        # employees = request.env['hr.employee'].sudo().with_context(no_access_rights=True).search([])
        # data = []
        for e in employees:
            data.append({
                'id': e.id,
                'name': e.name,
                'work_email': e.work_email,
                'work_phone': e.work_phone,
                'mobile_phone': e.mobile_phone,
                'job_title': e.job_id.name if e.job_id else '',
                'department': e.department_id.name if e.department_id else '',
            })

        return http.Response(
            json.dumps({'count': len(data), 'employees': data}),
            status=200,
            content_type='application/json'
        )



# ------------------------------------------------------
# API END Point
# ------------------------------------------------------


from odoo import http
from odoo.http import request
import hashlib
import jwt
import datetime
import json

SECRET_KEY = "SuperSecretKey@2025"
JWT_ALGORITHM = "HS256"

class ApiController(http.Controller):

    
    # Login → Generate JWT Token
    # ------------------------
    @http.route('/api/auth/login', type='http', auth='none', methods=['POST'], csrf=False)
    def api_login(self, **kwargs):
        try:
            data = json.loads(request.httprequest.data)
        except:
            return json.dumps({'error':'Invalid JSON'})

        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return json.dumps({'error': 'Missing username or password'})

        user = request.env['user.access.api'].sudo().search(
            [('name', '=', username), ('active', '=', True)], limit=1
        )
        if not user:
            return json.dumps({'error': 'Invalid username or password'})

        hashed = hashlib.sha256(password.encode()).hexdigest()
        if hashed != user.password_hash:
            return json.dumps({'error': 'Invalid username or password'})

        payload = {
            'api_user_id': user.id,
            'username': user.name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return json.dumps({
            'success': True,
            'access_token': token,
            'token_type': 'Bearer',
            'expires_in': 7200
        })

    
    # Verify JWT Token
    
    def verify_token(self, request):
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return {'error': 'Missing or invalid Authorization header'}

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            api_user = request.env['user.access.api'].sudo().browse(payload['api_user_id'])
            if not api_user or not api_user.active:
                return {'error': 'Invalid user'}
            return api_user
        except jwt.ExpiredSignatureError:
            return {'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'error': 'Invalid token'}

    
    # GET Employees
    
    @http.route('/api/employees', type='http', auth='none', methods=['GET'], csrf=False)
    def api_employees(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        admin_user = request.env['res.users'].sudo().browse(1)
        employees = request.env['hr.employee'].with_user(admin_user).sudo().search([])

        data = []
        for e in employees:
            data.append({
                'id': e.id,
                'name': e.name,
                'work_email': e.work_email,
                'work_phone': e.work_phone,
                'mobile_phone': e.mobile_phone,
                'job_title': e.job_id.name if e.job_id else '',
                'department': e.department_id.name if e.department_id else '',
            })

        return http.Response(
            json.dumps({'count': len(data), 'employees': data}),
            status=200,
            content_type='application/json'
        )

    
    # POST → Create Employee
    
    @http.route('/api/employees', type='http', auth='none', methods=['POST'], csrf=False)
    def create_employee(self, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        try:
            data = json.loads(request.httprequest.data)
        except:
            return json.dumps({'error':'Invalid JSON'})

        admin_user = request.env['res.users'].sudo().browse(1)
        employee = request.env['hr.employee'].with_user(admin_user).sudo().create({
            'name': data.get('name'),
            'work_email': data.get('work_email'),
            'work_phone': data.get('work_phone'),
            'mobile_phone': data.get('mobile_phone'),
            
        })

        return http.Response(
            json.dumps({'success': True, 'id': employee.id}),
            status=201,
            content_type='application/json'
        )

    
    # PUT/PATCH → Update Employee
    
    @http.route('/api/employees/<int:emp_id>', type='http', auth='none', methods=['PUT','PATCH'], csrf=False)
    def update_employee(self, emp_id, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        try:
            data = json.loads(request.httprequest.data)
        except:
            return json.dumps({'error':'Invalid JSON'})

        admin_user = request.env['res.users'].sudo().browse(1)
        employee = request.env['hr.employee'].with_user(admin_user).sudo().browse(emp_id)
        if not employee.exists():
            return http.Response(json.dumps({'error': 'Employee not found'}), status=404, content_type='application/json')

        employee.sudo().write({
            'name': data.get('name', employee.name),
            'work_email': data.get('work_email', employee.work_email),
            'work_phone': data.get('work_phone', employee.work_phone),
            'mobile_phone': data.get('mobile_phone', employee.mobile_phone),
        })

        return http.Response(
            json.dumps({'success': True}),
            status=200,
            content_type='application/json'
        )

    
    # DELETE → Remove Employee
    
    @http.route('/api/employees/<int:emp_id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_employee(self, emp_id, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        admin_user = request.env['res.users'].sudo().browse(1)
        employee = request.env['hr.employee'].with_user(admin_user).sudo().browse(emp_id)
        if not employee.exists():
            return http.Response(json.dumps({'error': 'Employee not found'}), status=404, content_type='application/json')

        employee.sudo().unlink()
        return http.Response(
            json.dumps({'success': True}),
            status=200,
            content_type='application/json'
        )

    # for single employee
    @http.route('/api/employees/<int:employee_id>', type='http', auth='none', methods=['GET'], csrf=False)
    def api_employee_single(self, employee_id, **kw):
        api_user = self.verify_token(request)
        if isinstance(api_user, dict):
            return http.Response(json.dumps(api_user), status=401, content_type='application/json')

        admin_user = request.env['res.users'].sudo().browse(1)
        employee = request.env['hr.employee'].with_user(admin_user).sudo().browse(employee_id)
        
        if not employee.exists():
            return http.Response(json.dumps({'error': 'Employee not found'}),
                                status=404,
                                content_type='application/json')

        data = {
            'id': employee.id,
            'name': employee.name,
            'work_email': employee.work_email,
            'work_phone': employee.work_phone,
            'mobile_phone': employee.mobile_phone,
            'job_title': employee.job_id.name if employee.job_id else '',
            'department': employee.department_id.name if employee.department_id else '',
        }

        return http.Response(json.dumps(data), status=200, content_type='application/json')


# ------------------------------------------------------
# API END Point Session End
# ------------------------------------------------------
