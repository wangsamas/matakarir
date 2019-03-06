# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class CertificatePublisher(models.Model):
    _name = 'matakarir.certificatepublisher'
    _description = 'Certificate Publisher'
    _order = "name"

    name = fields.Char('Certificate Name', required=True)
    publisher_id = fields.Many2one('res.partner', required=True, domain=[('is_company', '=', True)])
    country_id = fields.Many2one('res.country', related='publisher_id.country_id')

class MyCertificate(models.Model):
    _name = 'matakarir.certificate'
    _description = 'Certificates'
    _order = "since"

    partner_id = fields.Many2one('res.partner', readonly=True)
    certificate_id = fields.Many2one('matakarir.certificatepublisher', required=True)

    name = fields.Char('Certificate Publisher', related='certificate_id.name')
    number = fields.Char('Lisence Number')
    since = fields.Date('Since')
