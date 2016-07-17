# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Ashram Maintenance Management',
    'version' : '0.1',
    'author' : 'Sree Hari Nagaralu',
    'sequence': 165,
    'category': 'Managing vehicles and contracts',
    'website' : 'https://www.odoo.com/page/maint',
    'summary' : 'Facilities, land, maintenance, leasing, insurances, costs, Visitors',
    'description' : """
Facilities, land, maintenenace, leasing, insurances, cost
=========================================================
With this module, Odoo helps you managing all your Ashrams/Facilities, the
contracts associated to those Ashrams as well as services, repair
entries, costs and many other features necessary to the management 
of your facilities

Main Features
-------------
* Add facilities to your Ashrams
* Manage contracts for vehicles
* Reminder when a contract reach its expiration date
* Add services, fuel log entry, odometer values for all vehicles
* Show all costs associated to a vehicle or to a type of service
* Analysis graph for costs
""",
    'depends' : [
        'base',
        'mail',
    ],
    'data' : [
        'security/maint_security.xml',
        'security/ir.model.access.csv',
        'maint_view.xml',
        'maint_cars.xml',
        'maint_data.xml',
        'maint_board_view.xml',
    ],

    'demo': ['maint_demo.xml'],

    'installable' : True,
    'application' : True,
}
