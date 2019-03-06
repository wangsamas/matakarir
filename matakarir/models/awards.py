# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class MyAward(models.Model):
    _name = 'matakarir.award'
    _description = 'Awards'
    _order = "since"

    partner_id = fields.Many2one('res.partner', readonly=True)
    awarder_id = fields.Many2one('res.partner', required=True, domain=[('is_company', '=', True)])
    name = fields.Char('Awarder Name', related='awarder_id.name')
    title = fields.Char('Award Title', required=True)
    since = fields.Date('Since')
