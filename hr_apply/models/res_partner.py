# -*- coding: utf-8 -*-
import werkzeug

from odoo import api, fields, models

def urlplus(url, params):
    return werkzeug.Href(url)(params or None)

class Partner(models.Model):
    _inherit = "res.partner"
    
    my_application_ids = fields.One2many('hr_apply.applicant', 'partner_id', string="My Applications")
    my_vacancy_ids = fields.One2many('hr.job', 'poster_id', string="My Vacancies")
    failed_application_ids = fields.One2many('hr_apply.tryapply', 'partner_id', string="Unfinished Applications")
    
    working_company_ids = fields.One2many('res.partner', compute='_compute_working_company_ids')

    max_vacancy = fields.Integer(string='Maximum Vacancy Allowed')
    vacancies = fields.Integer(string='Active Vacancies', compute='_compute_vacancies')
    allow_vacancy_post = fields.Boolean('Allow to post vacancy', default=True)

    @api.depends('experience_ids', 'experience_ids.company_id')
    def _compute_working_company_ids(self):
        for c in self:
            c.working_company_ids = c.experience_ids.search([('partner_id','=',c.id),('status','=','work')]).mapped('company_id')

    @api.depends('my_vacancy_ids')
    def _compute_vacancies(self):
        for partner in self:
            partner.vacancies = len(partner.my_vacancy_ids)    

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
