# -*- coding: utf-8 -*-
{
    'name': "OAuth2 Provider for Odoo API",
    'summary': 'Use Odoo as OAuth2 provider for API access',
    'description': """
Use Odoo as OAuth2 provider for API access
    """,
    'author': "Aung Min Soe",
    'website': "https://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/oauth_root_menu.xml',
        'views/oauth_view.xml'
        
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
}

