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

class Job(models.Model):
    _name = "hr.job"
    _inherit = ['hr.job', 'website.seo.metadata']
    _order = "write_date desc"

    name = fields.Char(string='Job Position', required=True, index=False, translate=False)
    description = fields.Text('Job Description')
    tasks = fields.Text('Tasks of this job')

    employer_id = fields.Many2one('res.partner', required=True, domain=[('is_company', '=', True)])
    poster_id = fields.Many2one('res.partner', related='user_id.partner_id')
    industry_id = fields.Many2one('res.partner.industry', string='Employer Industry')
    department_id = fields.Many2one('hr.department', string='Job Department', ondelete='restrict')
    level_id = fields.Many2one('matakarir.joblevel', string='Job Level', ondelete='restrict')
    e_status_id = fields.Many2one('matakarir.employmentstatus', string='Employment Status', ondelete='restrict')
    min_age = fields.Integer(string='Minimum Age')
    max_age = fields.Integer(string='Maximum Age')
    min_salary = fields.Integer(string='Minimum Salary')
    max_salary = fields.Integer(string='Maximum Salary')
    duration_id = fields.Many2one('hr_apply.duration', string='Salary Duration', ondelete='restrict')
    currency_id = fields.Many2one('res.currency', string='Salary Currency', ondelete='restrict')
    zipcode_id = fields.Many2one('res.zipcode', string='Zip Code', ondelete='restrict')
    area_id = fields.Many2one('res.area', string='Area', ondelete='restrict')
    village_id = fields.Many2one('res.village', string='Village', ondelete='restrict')
    district_id = fields.Many2one('res.district', string='District', ondelete='restrict')
    city_id = fields.Many2one('res.city', string='City Regency', ondelete='restrict')
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')    
    ethnic_id = fields.Many2one('res.ethnic', string='Ethnic', ondelete='restrict')
    religion_id = fields.Many2one('res.religion', string='Religion', ondelete='restrict')
    
    applicant_ids = fields.One2many('hr_apply.applicant', 'job_id', string='Applicants', ondelete='cascade', domain=[('status','not in',['draft', 'rejected', 'canceled'])])
    criteria_ids = fields.One2many('hr_apply.criteria', 'job_id', string='Classification Criteria', ondelete='cascade')
    classification_ids = fields.One2many('questionaire.classification', compute='_compute_classification_ids')

    required_experience_ids = fields.One2many('hr_apply.required_experience', 'job_id', string='Required Experiences', ondelete='cascade')
    required_university_ids = fields.One2many('hr_apply.required_university', 'job_id', string='Required Universities', ondelete='cascade')
    required_school_ids = fields.One2many('hr_apply.required_school', 'job_id', string='Required Schools', ondelete='cascade')

    required_skill_ids = fields.One2many('hr_apply.required_skill', 'job_id', string='Required Skills', ondelete='cascade')
    required_langskill_ids = fields.One2many('hr_apply.required_langskill', 'job_id', string='Required Language Skills', ondelete='cascade')
    required_comskill_ids = fields.One2many('hr_apply.required_comskill', 'job_id', string='Required Computer Skills', ondelete='cascade')
    required_driving_lisence_ids = fields.One2many('hr_apply.required_driving_lisence', 'job_id', string='Required Driving Lisences', ondelete='cascade')
    required_lisence_ids = fields.One2many('hr_apply.required_lisence', 'job_id', string='Required Lisences', ondelete='cascade')
    required_certificate_ids = fields.One2many('hr_apply.required_certificate', 'job_id', string='Required Certificates', ondelete='cascade')
    required_tools_ids = fields.One2many('hr_apply.required_tools', 'job_id', string='Required Tools', ondelete='cascade')

    close_date = fields.Datetime("Vacancy closing date", readonly=True)
    abuse_report_ids = fields.One2many('hr_apply.abuse_report', 'job_id', string='Abuse Report Ids', ondelete='cascade')
    abuse_reports = fields.Integer(string='Abuse Reports', compute='_compute_abuse_reports')
    applicants = fields.Integer(string='Number of Applicants', compute='_compute_applicants')
    views = fields.Integer(string='Number of Views', default=0)

    def _default_website_meta(self):
        res = super(Job, self)._default_website_meta()
        res['default_opengraph']['og:description'] = res['default_twitter']['twitter:description'] = self.description
        res['default_opengraph']['og:title'] = res['default_twitter']['twitter:title'] = self.name
        res['default_twitter']['twitter:card'] = 'Vacancy'
        return res

    @api.depends('criteria_ids', 'criteria_ids.classification_id')
    def _compute_classification_ids(self):
        for c in self:
            c.classification_ids = c.criteria_ids.mapped('classification_id')

    @api.depends('abuse_report_ids')
    def _compute_abuse_reports(self):
        for job in self:
            job.abuse_reports = len(job.abuse_report_ids)

    @api.depends('applicant_ids')
    def _compute_applicants(self):
        for job in self:
            job.applicants = len(job.applicant_ids)

    @api.one
    def send_new_vacancy_email(self):
        if not self.user_id.email:
            return False
        email_template = self.env.ref('hr_apply.new_vacancy')
        if email_template:
            email_template.sudo().send_mail(self.id, force_send=True)
        return True
    
    @api.one
    def send_test_email(self):
        email_template = self.env.ref('hr_apply.testingmail')
        local_context = self.env.context.copy()
        if email_template:
            local_context['hr_user'] = 'Budi'
            email_template.sudo().with_context(local_context).send_mail(self.id, force_send=True)
        return True
    
    @api.onchange('zipcode_id')
    def _onchange_zipcode_id(self):
        if self.zipcode_id:
            self.zip = self.zipcode_id.name
            self.area_id = self.zipcode_id.area_id
            self.village_id = self.area_id.village_id
            self.district_id = self.village_id.district_id
            self.city_id = self.district_id.city_id
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.state_id.country_id

    @api.onchange('area_id')
    def _onchange_area_id(self):
        if self.area_id:
            self.village_id = self.area_id.village_id
            self.district_id = self.village_id.district_id
            self.city_id = self.district_id.city_id
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.state_id.country_id

    @api.onchange('village_id')
    def _onchange_village_id(self):
        if self.village_id:
            self.district_id = self.village_id.district_id
            self.city_id = self.district_id.city_id
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.state_id.country_id
            return {'domain': {'zipcode_id': [('village_id', '=', self.village_id.id)]}}
        else:
            return {'domain': {'zipcode_id': []}}

    @api.onchange('district_id')
    def _onchange_district_id(self):
        if self.district_id:
            self.city_id = self.district_id.city_id
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.state_id.country_id
            return {'domain': {'village_id': [('district_id', '=', self.district_id.id)]}}
        else:
            return {'domain': {'village_id': []}}

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id:
            self.city = self.city_id.name
            self.state_id = self.city_id.state_id
            self.country_id = self.city_id.state_id.country_id
            return {'domain': {'district_id': [('city_id', '=', self.city_id.id)]}}
        else:
            return {'domain': {'district_id': []}}

    @api.multi
    def google_map_img(self, zoom=8, width=600, height=100):
        google_maps_api_key = self.env['ir.config_parameter'].sudo().get_param('google_maps_api_key')
        if not google_maps_api_key:
            return False
        params = {
            'center': '%s, %s, %s, %s, %s, %s' % (self.country_id and self.country_id.name_get()[0][1] or '',
                                         self.state_id and self.state_id.name_get()[0][1] or '',
                                         self.city_id and self.city_id.name_get()[0][1] or '',
                                         self.district_id and self.district_id.name_get()[0][1] or '',
                                         self.village_id and self.village_id.name_get()[0][1] or '',
                                         self.area_id and self.area_id.name_get()[0][1] or '',
                                        ),
            'size': "%sx%s" % (width, height),
            'zoom': zoom,
            'key': google_maps_api_key,
        }
        return urlplus('//maps.googleapis.com/maps/api/staticmap', params)

    @api.multi
    def google_map_link(self, zoom=10):
        params = {
            'q': '%s, %s, %s, %s, %s, %s' % (self.country_id and self.country_id.name_get()[0][1] or '',
                                     self.state_id and self.state_id.name_get()[0][1] or '',
                                     self.city_id and self.city_id.name_get()[0][1] or '',
                                     self.district_id and self.district_id.name_get()[0][1] or '',
                                     self.village_id and self.village_id.name_get()[0][1] or '',
                                     self.area_id and self.area_id.name_get()[0][1] or '',
                                   ),
            'z': zoom,
        }
        return urlplus('https://maps.google.com/maps', params)

    @api.onchange('name')
    def _onchange_name(self):
        self.website_meta_title = self.name
        self.website_meta_keywords = self.name and self.employer_id.name
        
    @api.onchange('description')
    def _onchange_description(self):
        self.website_meta_description = self.description

