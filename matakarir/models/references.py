# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class ReferenceType(models.Model):
    _name = 'matakarir.referencetype'
    _description = 'Reference Type'
    _order = 'name'
    
    name = fields.Char('Relation Name', required=True, translate=True)

class Reference(models.Model):
    _name = 'matakarir.reference'
    _description = 'Reference'
    _order = 'name'

    partner_id = fields.Many2one('res.partner', readonly=True)
    name = fields.Char('Reference Name', required=True)
    relation_id = fields.Many2one('matakarir.referencetype', string='Relation', required=True)
    phone = fields.Char('Phone Number', required=True)
    email = fields.Char('Email', required=True)
