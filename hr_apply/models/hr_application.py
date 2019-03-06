# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging
import werkzeug

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

def urlplus(url, params):
    return werkzeug.Href(url)(params or None)

class Interviews(models.Model):
    _name = "hr_apply.interview"
    _description = "Application Interview Questions"
    _order = "write_date desc"
    
    application_id = fields.Many2one('hr_apply.applicant', "Application", required=True)
    interviewer_id = fields.Many2one('res.partner', related="application_id.job_partner_id")
    applicant_id = fields.Many2one('res.partner', related="application_id.partner_id")
    write_date = fields.Datetime("Apply Date", readonly=True, index=True)
    writer_id = fields.Many2one('res.partner', "Writer", required=True)
    message = fields.Text('Message', required=True)
    
class JobApplicant(models.Model):
    _name = "hr_apply.applicant"
    _description = "Job Applicant"
    _inherit = ['mail.thread']
    _order = "criteria_score desc, qualification_score desc, create_date desc"
    
    partner_id = fields.Many2one('res.partner', "Applicant", required=True)
    job_id = fields.Many2one('hr.job', "Applied Job", required=True)
    job_owner_id = fields.Many2one('res.users')
    job_partner_id = fields.Many2one('res.partner', related ="job_owner_id.partner_id" )

    name = fields.Char(string='Job Position', required=True, index=True)
    description = fields.Text("Opening Letter")
    
    create_date = fields.Datetime("Apply Date", readonly=True, index=True)
    
    applicant_age = fields.Integer("Applicant Age")
    criteria_score = fields.Float("Criteria match in percent")
    qualification_score = fields.Float("Qualification match in percent")
    total_score = fields.Float("Total match in percent")
    probability = fields.Float("Probability")

    qualified_age = fields.Boolean('Aplicant age compare to requirement age', default=False)
    qualified_experience = fields.Boolean('Qualified Experience', default=False)
    qualified_ethnic = fields.Boolean('Qualified Ethnic', default=False)
    qualified_religion = fields.Boolean('Qualified Religion', default=False)
    qualified_country = fields.Boolean('Qualified Country', default=False)
    qualified_state = fields.Boolean('Qualified State', default=False)
    qualified_city = fields.Boolean('Qualified City', default=False)
    qualified_district = fields.Boolean('Qualified District', default=False)
    qualified_village = fields.Boolean('Qualified Village', default=False)
    qualified_area = fields.Boolean('Qualified Area', default=False)

    criteria_scores_ids = fields.One2many('hr_apply.criteriascore', 'applicant_id', ondelete='cascade')
    interview_ids = fields.One2many('hr_apply.interview', 'application_id', ondelete='cascade')

    qualified_experience_ids = fields.One2many('hr_apply.qualified_experience', 'applicant_id', string='Qualified Experiences', ondelete='cascade')
    qualified_university_ids = fields.One2many('hr_apply.qualified_university', 'applicant_id', string='Qualified Universities', ondelete='cascade')
    qualified_school_ids = fields.One2many('hr_apply.qualified_school', 'applicant_id', string='Qualified Schools', ondelete='cascade')

    qualified_skill_ids = fields.One2many('hr_apply.qualified_skill', 'applicant_id', string='Qualified Skills', ondelete='cascade')
    qualified_langskill_ids = fields.One2many('hr_apply.qualified_langskill', 'applicant_id', string='Qualified Language Skills', ondelete='cascade')
    qualified_comskill_ids = fields.One2many('hr_apply.qualified_comskill', 'applicant_id', string='Qualified Computer Skills', ondelete='cascade')
    qualified_driving_lisence_ids = fields.One2many('hr_apply.qualified_driving_lisence', 'applicant_id', string='Qualified Driving Lisences', ondelete='cascade')
    qualified_lisence_ids = fields.One2many('hr_apply.qualified_lisence', 'applicant_id', string='Qualified Lisences', ondelete='cascade')
    qualified_certificate_ids = fields.One2many('hr_apply.qualified_certificate', 'applicant_id', string='Qualified Certificates', ondelete='cascade')
    qualified_tool_ids = fields.One2many('hr_apply.qualified_tools', 'applicant_id', string='Qualified Tools', ondelete='cascade')
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('viewed', 'Viewed'),
        ('called', 'Called'),
        ('hired', 'Hired'),
        ('rejected', 'Rejected'),
        ('canceled', 'Canceled')
        ], string='Status', readonly=True, index=True, copy=False, default='draft', track_visibility='onchange')
    
    @api.one
    def send_new_application_email(self):
        if not self.job_owner_id.email:
            return False
        email_template = self.env.ref('hr_apply.email_applied')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True    

    @api.one
    def send_rejection_email(self):
        if not self.partner_id.email:
            return False
        email_template = self.env.ref('hr_apply.email_rejected')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True

    @api.one
    def send_hired_email(self):
        if not self.partner_id.email:
            return False
        email_template = self.env.ref('hr_apply.email_hired')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True
    
    @api.one
    def send_employer_response_email(self):
        if not self.partner_id.email:
            return False
        email_template = self.env.ref('hr_apply.email_employer_response')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True
    
    @api.one
    def send_applicant_response_email(self):
        if not self.job_owner_id.email:
            return False
        email_template = self.env.ref('hr_apply.email_applicant_response')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True
    
