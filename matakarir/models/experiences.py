# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.http import Response
from odoo.exceptions import ValidationError, UserError
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *
from odoo.tools.translate import _

class JobLevel(models.Model):
    _name = 'matakarir.joblevel'
    _description = 'Job Levels'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Job Level', translate=True)

class EmploymentStatus(models.Model):
    _name = 'matakarir.employmentstatus'
    _description = 'Employment Status'
    _order = 'sequence'

    sequence = fields.Integer('Sequence')
    name = fields.Char('Employment Status', translate=True)

class Experience(models.Model):
    _name = 'matakarir.experience'
    _description = 'Experiences'
    _order = "since"

    partner_id = fields.Many2one('res.partner', readonly=True)
    company_id = fields.Many2one('res.partner', required=True, domain=[('is_company', '=', True)])
    department_id = fields.Many2one('hr.department', string='Job Department', ondelete='restrict')
    level_id = fields.Many2one('matakarir.joblevel', string='Job Level', ondelete='restrict')
    industry_id = fields.Many2one('res.partner.industry', related="company_id.industry_id")
    e_status_id = fields.Many2one('matakarir.employmentstatus', string='Employment Status', ondelete='restrict')

    name = fields.Char('Company Name', related='company_id.name')
    job_name = fields.Char('Job Name', required=True)
    description = fields.Text('Job Description')
    since = fields.Date('Since')
    until = fields.Date('Until')
    status = fields.Selection([('quit', 'Quit'), 
                               ('work', 'Work')], 'Status')
    quit_reason = fields.Text('Quit Reasons')
    achievement = fields.Text('Achievements')
    salary = fields.Integer('Salary')
    allowance = fields.Integer('Allowance')
    bonus = fields.Integer('Bonus')
