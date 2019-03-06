# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class LisencePublisher(models.Model):
    _name = 'matakarir.lisencepublisher'
    _description = 'Lisence Publisher'
    _order = "name"

    name = fields.Char('Lisence Name', required=True)
    publisher_id = fields.Many2one('res.partner', required=True, domain=[('is_company', '=', True)])
    country_id = fields.Many2one('res.country', related='publisher_id.country_id')

class MyLisence(models.Model):
    _name = 'matakarir.lisence'
    _description = 'Licences'
    _order = "since"

    partner_id = fields.Many2one('res.partner', readonly=True)
    lisence_id = fields.Many2one('matakarir.lisencepublisher', required=True)
    
    name = fields.Char('Lisence Publisher', related='lisence_id.name')
    number = fields.Char('Lisence Number')
    status = fields.Selection([('expired', 'Expired'), 
                               ('valid', 'Valid'), 
                               ('progress', 'On Progress')], 'Lisence Status')
    since = fields.Date('Since')
    until = fields.Date('Until')
