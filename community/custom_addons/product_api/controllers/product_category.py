import json
from odoo import http
from odoo.http import request

class ProductCategoryApi(http.Controller):

    @http.route('/api/v1/product-categories', type='http', auth='public', methods=['GET'], csrf=False)
    def get_product_categories(self, search=None, searchField=None, **kwargs):

        domain = []

        if search:
            search = search.strip()

            if searchField == "parentCategory":
                domain = [("parent_id.name", "ilike", search)]
            else:
                domain = ["|",
                    ("name", "ilike", search),
                    ("complete_name", "ilike", search)
                ]

        categories = request.env['product.category'].sudo().search_read(
            domain,
            fields=[
                "id",
                "name",
                "complete_name",
                "parent_id",
            ]
        )

        result = []
        for category in categories:
            result.append({
                "id": category["id"],
                "name": category["name"],
                "completeName": category["complete_name"],
                "parentId": category["parent_id"][0] if category["parent_id"] else None,
            })

        return request.make_response(
            json.dumps(result),
            headers=[('Content-Type', 'application/json')]
        )