# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

class Criteria(models.Model):
    _name = 'hr_apply.criteria'
    _description = 'Criteria for the job'

    classification_id = fields.Many2one('questionaire.classification', string='Classification', ondelete='restrict')
    job_id = fields.Many2one('hr.job', string='Job', ondelete='restrict')
    classification_method_id = fields.Many2one('questionaire.classification_method', ondelete='restrict')        
        
class CriteriaScore(models.Model):
    _name = 'hr_apply.criteriascore'
    _description = 'Criteria score of applicant'
    
    criteria_id = fields.Many2one('hr_apply.criteria')
    applicant_id = fields.Many2one('hr_apply.applicant')
    partner_id = fields.Many2one('res.partner')
    score = fields.Integer('Criteria Score')

class TryApply(models.Model):
    _name = 'hr_apply.tryapply'
    _description = 'failed apply'
    
    job_id = fields.Many2one('hr.job', string='Job')
    partner_id = fields.Many2one('res.partner')
    
class Number(models.Model):
    _name = 'hr_apply.number'
    _description = 'Number'
    _order = 'name'
    
    name = fields.Integer('Number', required=True, index=True)    

class Million(models.Model):
    _name = 'hr_apply.million'
    _description = 'Million'
    _order = 'name'
    
    name = fields.Integer('Million', required=True, index=True)    

class Duration(models.Model):
    _name = 'hr_apply.duration'
    _description = 'Duration'
    _order = 'sequence'
    
    sequence = fields.Integer('Sequence', required=True, index=True)    
    name = fields.Char(string='Wage Duration', required=True, index=True, translate=True)