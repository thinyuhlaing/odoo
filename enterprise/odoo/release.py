# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

RELEASE_LEVELS = [ALPHA, BETA, RELEASE_CANDIDATE, FINAL] = ['alpha', 'beta', 'candidate', 'final']
RELEASE_LEVELS_DISPLAY = {ALPHA: ALPHA,
                          BETA: BETA,
                          RELEASE_CANDIDATE: 'rc',
                          FINAL: ''}

# version_info format: (MAJOR, MINOR, MICRO, RELEASE_LEVEL, SERIAL)
# inspired by Python's own sys.version_info, in order to be
# properly comparable using normal operators, for example:
#  (6,1,0,'beta',0) < (6,1,0,'candidate',1) < (6,1,0,'candidate',2)
#  (6,1,0,'candidate',2) < (6,1,0,'final',0) < (6,1,2,'final',0)
version_info = (18, 0, 0, FINAL, 0, '')
version = '.'.join(str(s) for s in version_info[:2]) + RELEASE_LEVELS_DISPLAY[version_info[3]] + str(version_info[4] or '') + version_info[5]
series = serie = major_version = '.'.join(str(s) for s in version_info[:2])

product_name = 'Odoo'
description = 'Odoo Server'
long_desc = '''Odoo is a complete ERP and CRM. The main features are accounting (analytic
and financial), stock management, sales and purchases management, tasks
automation, marketing campaigns, help desk, POS, etc. Technical features include
a distributed server, an object database, a dynamic GUI,
customizable reports, and XML-RPC interfaces.
'''
classifiers = """Development Status :: 5 - Production/Stable
License :: OSI Approved :: GNU Lesser General Public License v3

Programming Language :: Python
"""
url = 'https://www.odoo.com'
author = 'OpenERP S.A.'
author_email = 'info@odoo.com'
license = 'LGPL-3'

nt_service_name = "odoo-server-" + series.replace('~','-')

version += '+e-20250703'

repos_heads = {'odoo': 'bc4f21afa911e76ceafe581b5af03501a3e2a6cd', 'enterprise': '6f96858d9547e88d0ef43c865553367ff6aec445', 'design-themes': '991be362794fdbf5fe59bb03ee8f1ca2cace53b5'}
