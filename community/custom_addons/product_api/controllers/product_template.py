import json
from odoo import http
from odoo.http import request

class ProductAPI(http.Controller):

    @http.route('/api/v1/products', type='http', auth='public', methods=['GET'], csrf=False)
    def get_products(self, **kwargs):

        products = request.env['product.template'].sudo().search_read(
            [],
            fields=[
                "id",
                "name",
                "categ_id",
                "list_price",
                "standard_price",
                "image_1920",
                "create_date",
                "write_date",
                "active",
            ]
        )

        result = []

        for product in products:
            category = product["categ_id"] if product["categ_id"] else [None, None]

            result.append({
                "id": product["id"],
                "name": product["name"],
                "categoryId": category[0],
                "categoryName": category[1],
                "salePrice": product["list_price"],
                "costPrice": product["standard_price"],
                # "imageUrl": (
                #     "data:image/png;base64," + product["image_1920"]
                #     if product["image_1920"] else None
                # ),
                "createdAt": product["create_date"].isoformat() if product["create_date"] else None,
                "updatedAt": product["write_date"].isoformat() if product["write_date"] else None,
                "isArchived": not product["active"],
            })

        return request.make_response(
            json.dumps(result),
            headers=[('Content-Type', 'application/json')]
        )