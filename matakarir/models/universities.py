# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class UniversityDegree(models.Model):
    _name = 'matakarir.universitydegree'
    _description = 'University Degree'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    name = fields.Char('University Degree', translate=True)

class Faculty(models.Model):
    _name = 'matakarir.faculty'
    _description = 'Faculty'
    _order = 'name'

    name = fields.Char('Faculty', translate=True)
    major_ids = fields.One2many('matakarir.facultymajor', 'faculty_id', string='Major')

class FacultyMajor(models.Model):
    _name = 'matakarir.facultymajor'
    _description = 'Faculty Major'
    _order = 'name'

    name = fields.Char('Major', translate=True)
    faculty_id = fields.Many2one('matakarir.faculty', string='Faculty', ondelete='restrict')
    _sql_constraints = [
        ('name_uniq', 'unique(faculty_id, name)', 'The name of the major must be unique by faculty !')
    ]

class University(models.Model):
    _name = 'matakarir.university'
    _description = 'University'
    _order = "since"

    partner_id = fields.Many2one('res.partner', readonly=True)
    university_id = fields.Many2one('res.partner', required=True, domain=[('is_university', '=', True)])
    faculty_id = fields.Many2one('matakarir.faculty', string='Faculty', ondelete='restrict')
    major_id = fields.Many2one('matakarir.facultymajor', string='Major', ondelete='restrict')
    degree_id = fields.Many2one('matakarir.universitydegree', string='Gelar', ondelete='restrict')
    
    name = fields.Char('Nama Universitas', related='university_id.name')
    since = fields.Date('Since')
    until = fields.Date('Until')
    status = fields.Selection([('graduate', 'Graduate'), 
                               ('drop', 'Drop'), 
                               ('progress', 'Progress')], 'Status')
    score = fields.Float('Score')
    schollarship = fields.Boolean('Schollarship')

