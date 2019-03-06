# -*- coding: utf-8 -*-

import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr
from odoo.addons.http_routing.models.ir_http import slug

class activities(http.Controller):
    _application_per_page = 20

    def no_area(self, partner_id=None, **kwargs):
        zipcode_id = None
        partner_id['zipcode_id'] = zipcode_id
        return
    
    def no_village(self, partner_id=None, **kwargs):
        self.no_area(partner_id=partner_id)
        area_id = None
        partner_id['area_id'] = area_id
        return
    
    def no_district(self, partner_id=None, **kwargs):
        self.no_village(partner_id=partner_id)
        village_id = None
        partner_id['village_id'] = village_id
        return
    
    def no_city(self, partner_id=None, **kwargs):
        self.no_district(partner_id=partner_id)
        district_id = None
        partner_id['district_id'] = district_id
        return
    
    def no_state(self, partner_id=None, **kwargs):
        self.no_city(partner_id=partner_id)
        city_id = None
        partner_id['city_id'] = city_id
        return
        
    def no_country(self, partner_id=None, **kwargs):
        self.no_state(partner_id=partner_id)
        state_id = None
        partner_id['state_id'] = state_id
        return
    
    def save_area_value(self, partner_id=None, **kwargs):
        if kwargs.get('country_name'):
            country_id = request.env['res.country'].create({'name': kwargs.get('country_name')})
        elif kwargs.get('country'):
            country_id = request.env['res.country'].search([("id","=",kwargs.get('country'))])
        else:
            country_id = None

        if country_id:
            if kwargs.get('state_name'):
                state_id = request.env['res.country.state'].create({
                    'name': kwargs.get('country_name'), 'country_id':country_id.id})
            elif kwargs.get('state'):
                state_id = request.env['res.country.state'].search([("id","=",kwargs.get('state'))])
            else:
                state_id = None
            
            if state_id:
                if kwargs.get('city_name'):
                    city_id = request.env['res.city'].create({
                        'name': kwargs.get('city_name'), 'state_id':state_id.id})
                elif kwargs.get('city'):
                    city_id = request.env['res.city'].search([("id","=",kwargs.get('city'))])
                else:
                    city_id = None

                if city_id:
                    if kwargs.get('district_name'):
                        district_id = request.env['res.district'].create({
                            'name': kwargs.get('district_name'), 'city_id':city_id.id})
                    elif kwargs.get('district'):
                        district_id = request.env['res.district'].search([("id","=",kwargs.get('district'))])
                    else:
                        district_id = None
                        
                    if district_id:
                        if kwargs.get('village_name'):
                            village_id = request.env['res.village'].create({
                                'name': kwargs.get('village_name'), 'district_id':district_id.id})
                        elif kwargs.get('village'):
                            village_id = request.env['res.village'].search([("id","=",kwargs.get('village'))])
                        else:
                            village_id = None
                            
                        if village_id:
                            if kwargs.get('area_name'):
                                area_id = request.env['res.area'].create({
                                    'name': kwargs.get('area_name'), 'village_id':village_id.id})
                            elif kwargs.get('area'):
                                area_id = request.env['res.area'].search([("id","=",kwargs.get('area'))])
                            else:
                                area_id = None
                                
                            if area_id:
                                if kwargs.get('zipcode_name'):
                                    zipcode_id = request.env['res.zipcode'].create({
                                        'name': kwargs.get('zipcode_name'), 'area_id':area_id.id})
                                elif kwargs.get('zipcode'):
                                    zipcode_id = request.env['res.zipcode'].search([("id","=",kwargs.get('zipcode'))])
                                else:
                                    zipcode_id = None
                                partner_id['zipcode_id'] = zipcode_id
                                partner_id._onchange_zipcode_id()
                            else:
                                self.no_area(partner_id=partner_id)
                            partner_id['area_id'] = area_id
                            partner_id._onchange_area_id()
                        else:
                            self.no_village(partner_id=partner_id)
                        partner_id['village_id'] = village_id
                        partner_id._onchange_village_id()
                    else:
                        self.no_district(partner_id=partner_id)
                    partner_id['district_id'] = district_id
                    partner_id._onchange_district_id()
                else:
                    self.no_city(partner_id=partner_id)
                partner_id['city_id'] = city_id
                partner_id._onchange_city_id()
            else:
                self.no_state(partner_id=partner_id)
            partner_id['state_id'] = state_id
        else:
            self.no_country(partner_id=partner_id)
        partner_id['country_id'] = country_id
        return
    
    def _prepare_area_values(self, **kwargs):
        values = {
            'countries': request.env['res.country'].sudo().search([]),
            'states': request.env['res.country.state'].sudo().search([]),
            'cities': request.env['res.city'].sudo().search([]),
            'districts': request.env['res.district'].sudo().search([]),
            'villages': request.env['res.village'].sudo().search([]),
            'areas': request.env['res.area'].sudo().search([]),
            'zipcodes': request.env['res.zipcode'].sudo().search([]),
        }
        return values
        
    @http.route(['/new/company/<string:word>'], type='http', auth='user', website=True)
    def new_workingcompany_vacancy(self, word, **kwargs):
        partner_id = request.env.user.partner_id
        companies = request.env['res.partner'].sudo().search([])
        companies = [j for j in companies if j.is_company]
        values = self._prepare_area_values()
        values.update({
            'word': word,
            'partner_id': partner_id,
            'companies': companies,
            'departments': request.env['hr.department'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'e_statuses': request.env['matakarir.employmentstatus'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
            'companytypes': request.env['res.companytype'].sudo().search([]),
        })
        return request.render("hr_apply.working_company", values)

    @http.route(['/new/company'], type='http', auth='user', website=True)
    def new_workingcompany(self, **kwargs):
        partner_id = request.env.user.partner_id
        companies = request.env['res.partner'].sudo().search([])
        companies = [j for j in companies if j.is_company]
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'companies': companies,
            'departments': request.env['hr.department'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'e_statuses': request.env['matakarir.employmentstatus'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
            'companytypes': request.env['res.companytype'].sudo().search([]),
        })
        return request.render("hr_apply.working_company", values)

    @http.route(['/edit/company/<model("res.partner"):workingcompany>'], type='http', auth='user', website=True)
    def edit_workingcompany(self, workingcompany, **kwargs):
        partner_id = request.env.user.partner_id
        experience_id = request.env['matakarir.experience'].sudo().search([("partner_id","=",partner_id.id), ("company_id","=",workingcompany.id)])
        if not experience_id:
            return request.redirect('/my/home')
        companies = request.env['res.partner'].sudo().search([])
        companies = [j for j in companies if j.is_company == True]
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'experience_id': experience_id,
            'object': experience_id.company_id,
            'companies': companies,
            'departments': request.env['hr.department'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'e_statuses': request.env['matakarir.employmentstatus'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
            'companytypes': request.env['res.companytype'].sudo().search([]),
        })
        return request.render("hr_apply.working_company", values)

    @http.route('/save/company', type='http', auth="user", methods=['POST'], website=True)
    def save_workingcompany(self, **kwargs):
        partner = request.env.user.partner_id

        if kwargs.get('level_name'):
            level_id = request.env['matakarir.joblevel'].create({'name': kwargs.get('level_name')})
        elif kwargs.get('level'):
            level_id = request.env['matakarir.joblevel'].search([("id","=",kwargs.get('level'))])
        else:
            level_id = None
            
        if kwargs.get('department_name'):
            department_id = request.env['hr.department'].create({'name': kwargs.get('department_name')})
        elif kwargs.get('department'):
            department_id = request.env['hr.department'].search([("id","=",kwargs.get('department'))])
        else:
            department_id = None
            
        if kwargs.get('e_status_name'):
            e_status_id = request.env['matakarir.employmentstatus'].create({'name': kwargs.get('e_status_name')})
        elif kwargs.get('e_status'):
            e_status_id = request.env['matakarir.employmentstatus'].search([("id","=",kwargs.get('e_status'))])
        else:
            e_status_id = None
            
        if kwargs.get('industry_name'):
            industry_id = request.env['res.partner.industry'].create({'name': kwargs.get('industry_name')})
        elif kwargs.get('industry'):
            industry_id = request.env['res.partner.industry'].search([("id","=",kwargs.get('industry'))])
        else:
            industry_id = None
            
        if kwargs.get('companytype_name'):
            companytype_id = request.env['res.companytype'].create({'name': kwargs.get('companytype_name')})
        elif kwargs.get('companytype'):
            companytype_id = request.env['res.companytype'].search([("id","=",kwargs.get('companytype'))])
        else:
            companytype_id = None

        if kwargs.get('experience_id'):
            experience_id = request.env['matakarir.experience'].search([("id","=",kwargs.get('experience_id'))])
            partner_id = experience_id.company_id
        else:
            if kwargs.get('company_name'):
                partner_id = request.env['res.partner'].create({
                    'name': kwargs.get('company_name'), 
                    'street': kwargs.get('street'), 
                    'street2': kwargs.get('street2'), 
                    'website': kwargs.get('website'), 
                    'email': kwargs.get('email'), 
                    'phone': kwargs.get('phone'), 
                    'industry_id': industry_id, 
                    'companytype_id': companytype_id, 
                    'is_company': True})
            elif kwargs.get('company'):
                partner_id = request.env['res.partner'].search([("id","=",kwargs.get('company'))])
            else:
                return request.redirect(request.httprequest.referrer)            
            self.save_area_value(partner_id, **kwargs)
            experience_id = request.env['matakarir.experience'].create({
                'partner_id': partner.id,
                'company_id': partner_id.id,
                'job_name': kwargs.get('job_name'),
                'since': kwargs.get('since'),
            })
        experience_id.update({
            'department_id': department_id,
            'level_id': level_id,
            'e_status_id': e_status_id,
            'job_name': kwargs.get('job_name'),
            'description': kwargs.get('description'),
            'since': kwargs.get('since'),
            'status': 'work',
        })
        if kwargs.get('word') == 'vacancy':
            return request.redirect('/new/vacancy')
        else:
            return request.redirect('/my/activities')
    
    @http.route(['/delete/company/<model("res.partner"):workingcompany>'], type='http', auth='user', website=True)
    def del_workingcompany(self, workingcompany, **kwargs):
        partner_id = request.env.user.partner_id
        object_id = request.env['matakarir.experience'].sudo().search([("partner_id","=",partner_id.id), ("company_id","=",workingcompany.id)])
        if not object_id:
            return request.redirect('/my/home')
        object_id['status'] = 'quit'
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/new/vacancy'], type='http', auth='user', website=True)
    def new_vacancy(self, **kwargs):
        partner_id = request.env.user.partner_id
        
        if not partner_id.street or not partner_id.email or not partner_id.alias_id:
            return request.redirect('/edit/informations/new/vacancy')

        if not partner_id.identification_no or not partner_id.alias_id or not partner_id.alias_id.street:
            return request.redirect('/edit/identity/new/vacancy')

        if not partner_id.birthday or not partner_id.gender or not partner_id.marital:
            return request.redirect('/edit/otherinfo/new/vacancy')

        if not partner_id.working_company_ids:
            return request.redirect('/new/company/vacancy')

        companies = partner_id.working_company_ids
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'companies': companies,
            'departments': request.env['hr.department'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'e_statuses': request.env['matakarir.employmentstatus'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
            'numbers': request.env['hr_apply.number'].sudo().search([]),
            'millions': request.env['hr_apply.million'].sudo().search([]),
            'durations': request.env['hr_apply.duration'].sudo().search([]),
            'currencies': request.env['res.currency'].sudo().search([]),
            'durations': request.env['hr_apply.duration'].sudo().search([]),
            'ethnics': request.env['res.ethnic'].sudo().search([]),
            'religions': request.env['res.religion'].sudo().search([]),
            'is_public_user': request.env.user.id == request.website.user_id.id,
            'method_ids': request.env['questionaire.classification_method'].sudo().search([])
        })
        return request.render("hr_apply.my_vacancy", values)

    @http.route(['/edit/vacancy/<model("hr.job"):job>'], type='http', auth='user', website=True)
    def edit_vacancy(self, job, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy_id = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy_id.poster_id != partner_id:
            return request.redirect('/my/home')
        companies = partner_id.working_company_ids
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'vacancy_id': vacancy_id,
            'object': vacancy_id,
            'companies': companies,
            'criteria_ids':vacancy_id.criteria_ids,
            'departments': request.env['hr.department'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'e_statuses': request.env['matakarir.employmentstatus'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
            'numbers': request.env['hr_apply.number'].sudo().search([]),
            'millions': request.env['hr_apply.million'].sudo().search([]),
            'durations': request.env['hr_apply.duration'].sudo().search([]),
            'currencies': request.env['res.currency'].sudo().search([]),
            'durations': request.env['hr_apply.duration'].sudo().search([]),
            'ethnics': request.env['res.ethnic'].sudo().search([]),
            'religions': request.env['res.religion'].sudo().search([]),
            'is_public_user': request.env.user.id == request.website.user_id.id,
            'method_ids': request.env['questionaire.classification_method'].sudo().search([])
        })
        return request.render("hr_apply.my_vacancy", values)

    @http.route('/save/vacancy', type='http', auth="user", methods=['POST'], website=True)
    def save_vacancy(self, **kwargs):
        user = request.env.user
        partner = request.env.user.partner_id

        if kwargs.get('employer_company'):
            employer_id = request.env['res.partner'].search([("id","=",kwargs.get('employer_company'))])
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('name'):
            name = kwargs.get('name')
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('vacancy_id'):
            vacancy_id = request.env['hr.job'].search([("id","=",kwargs.get('vacancy_id'))])
            if vacancy_id.poster_id != partner:
                return request.redirect('/my/home')
        else:
            vacancy_id = request.env['hr.job'].create({
                'user_id': user.id,
                'name': name,
                'employer_id': employer_id.id,
            })

        if kwargs.get('industry_name'):
            industry_id = request.env['res.partner.industry'].create({'name': kwargs.get('industry_name')})
        elif kwargs.get('industry'):
            industry_id = request.env['res.partner.industry'].search([("id","=",kwargs.get('industry'))])
        else:
            industry_id = None

        if kwargs.get('department_name'):
            department_id = request.env['hr.department'].create({'name': kwargs.get('department_name')})
        elif kwargs.get('department'):
            department_id = request.env['hr.department'].search([("id","=",kwargs.get('department'))])
        else:
            department_id = None
            
        if kwargs.get('level_name'):
            level_id = request.env['matakarir.joblevel'].create({'name': kwargs.get('level_name')})
        elif kwargs.get('level'):
            level_id = request.env['matakarir.joblevel'].search([("id","=",kwargs.get('level'))])
        else:
            level_id = None
            
        if kwargs.get('e_status_name'):
            e_status_id = request.env['matakarir.employmentstatus'].create({'name': kwargs.get('e_status_name')})
        elif kwargs.get('e_status'):
            e_status_id = request.env['matakarir.employmentstatus'].search([("id","=",kwargs.get('e_status'))])
        else:
            e_status_id = None

        if kwargs.get('min_age'):
            min_age = request.env['hr_apply.number'].search([("id","=",kwargs.get('min_age'))])
            vacancy_id['min_age']=min_age.name
        else:
            vacancy_id['min_age']=None

        if kwargs.get('max_age'):
            max_age = request.env['hr_apply.number'].search([("id","=",kwargs.get('max_age'))])
            vacancy_id['max_age']=max_age.name
        else:
            vacancy_id['max_age']=None

        if kwargs.get('min_salary'):
            min_salary = request.env['hr_apply.million'].search([("id","=",kwargs.get('min_salary'))])
            vacancy_id['min_salary']=min_salary.name
        else:
            vacancy_id['min_salary']=None

        if kwargs.get('max_salary'):
            max_salary = request.env['hr_apply.million'].search([("id","=",kwargs.get('max_salary'))])
            vacancy_id['max_salary']=max_salary.name
        else:
            vacancy_id['max_salary']=None

        if kwargs.get('duration'):
            duration_id = request.env['hr_apply.duration'].search([("id","=",kwargs.get('duration'))])
        else:
            duration_id = None

        if kwargs.get('currency'):
            currency_id = request.env['res.currency'].search([("id","=",kwargs.get('currency'))])
        else:
            currency_id = None

        if kwargs.get('ethnic_name'):
            ethnic_id = request.env['res.ethnic'].create({'name': kwargs.get('ethnic_name')})
        elif kwargs.get('ethnic'):
            ethnic_id = request.env['res.ethnic'].search([("id","=",kwargs.get('ethnic'))])
        else:
            ethnic_id = None
            
        if kwargs.get('religion_name'):
            religion_id = request.env['res.religion'].create({'name': kwargs.get('religion_name')})
        elif kwargs.get('religion'):
            religion_id = request.env['res.religion'].search([("id","=",kwargs.get('religion'))])
        else:
            religion_id = None
        
        if kwargs.get('no_of_recruitment'):
            no_of_recruitment = request.env['hr_apply.number'].search([("id","=",kwargs.get('no_of_recruitment'))])
            vacancy_id['no_of_recruitment']=no_of_recruitment.name
        else:
            vacancy_id['no_of_recruitment']=1
            
        self.save_area_value(vacancy_id, **kwargs)
        vacancy_id.update({
            'name': name,
            'description': kwargs.get('description',False),
            'tasks': kwargs.get('tasks',False),
            'employer_id': employer_id,
            'industry_id': industry_id,
            'department_id': department_id,
            'level_id': level_id,
            'e_status_id': e_status_id,
            'duration_id': duration_id,
            'currency_id': currency_id,
            'ethnic_id': ethnic_id,
            'religion_id': religion_id,
            'close_date': kwargs.get('close_date',False),
        })
        
        request.env['hr_apply.criteria'].sudo().search([("job_id","=",vacancy_id.id)]).unlink()
        method_ids = request.env['questionaire.classification_method'].sudo().search([])
        for method in method_ids:
            answer_tag = "%s" % (method.id)
            request.env['hr_apply.criteria'].create({
                'classification_method_id': method.id,
                'classification_id': kwargs[answer_tag],
                'job_id': vacancy_id.id
            })

        if not kwargs.get('vacancy_id'):
            vacancy_id.send_new_vacancy_email()

        return request.redirect('/vacancy/%s' % slug(vacancy_id))
    
    @http.route(['/delete/vacancy/<model("hr.job"):job>'], type='http', auth='user', website=True)
    def del_vacancy(self, job, **kwargs):
        partner_id = request.env.user.partner_id
        object_id = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if object_id.poster_id != partner_id:
            return request.redirect('/my/home')
        object_id['website_published'] = False
        return request.redirect(request.httprequest.referrer)

    @http.route(['/vacancy/<model("hr.job"):job>/driving_lisence'], type='http', auth='user', website=True)
    def driving_lisence(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        v_objects = request.env['matakarir.drivinglisencetype'].sudo().search([("country_id","=",job.country_id.id)])
        values ={
            'vacancy': vacancy,
            'v_objects': v_objects,
        }
        return request.render("hr_apply.vacancy_driving_lisence", values)        

    @http.route(['/save/vacancy/driving_lisence'], type='http', auth='user', website=True)
    def save_driving_lisence(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('v_object_name'):
            driving_lisence_id = request.env['matakarir.drivinglisencetype'].create({'name': kwargs.get('v_object_name'), 'country_id': vacancy.country_id.id})
        elif kwargs.get('v_object_id'):
            driving_lisence_id = request.env['matakarir.drivinglisencetype'].search([("id","=",kwargs.get('v_object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_driving_lisence_ids = request.env['hr_apply.required_driving_lisence'].create({
            'job_id': vacancy.id,
            'object_id': driving_lisence_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/driving_lisence/<model("hr_apply.required_driving_lisence"):required_driving_lisence>'], type='http', auth='user', website=True)
    def remove_driving_lisence(self, job, required_driving_lisence, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_driving_lisence'].search([("id","=",required_driving_lisence.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/lisence'], type='http', auth='user', website=True)
    def lisence(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        level1s = request.env['res.country'].sudo().search([])
        level2s = request.env['res.partner'].sudo().search([])
        level2s = [j for j in level2s if j.is_company]
        level3s = request.env['matakarir.lisencepublisher'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'level1s': level1s,
            'level2s': level2s,
            'level3s': level3s,
        }
        return request.render("hr_apply.vacancy_lisence", values)        

    @http.route(['/save/vacancy/lisence'], type='http', auth='user', website=True)
    def save_lisence(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('level1_name'):
            level1_id = request.env['res.country'].create({'name': kwargs.get('level1_name')})
        elif kwargs.get('level1'):
            level1_id = request.env['res.country'].search([("id","=",kwargs.get('level1'))])
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('level2_name'):
            level2_id = request.env['res.partner'].create({
                'name': kwargs.get('level2_name'), 'country_id':level1_id.id})
        elif kwargs.get('level2'):
            level2_id = request.env['res.partner'].search([("id","=",kwargs.get('level2'))])
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('level3_name'):
            level3_id = request.env['matakarir.lisencepublisher'].create({
            'name': kwargs.get('level3_name'), 'publisher_id':level2_id.id})
        elif kwargs.get('level3'):
            level3_id = request.env['matakarir.lisencepublisher'].search([("id","=",kwargs.get('level3'))])
        else:
            return request.redirect(request.httprequest.referrer)
        required_lisence_ids = request.env['hr_apply.required_lisence'].create({
            'job_id': vacancy.id,
            'object_id': level3_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/lisence/<model("hr_apply.required_lisence"):required_lisence>'], type='http', auth='user', website=True)
    def remove_lisence(self, job, required_lisence, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_lisence'].search([("id","=",required_lisence.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/certificate'], type='http', auth='user', website=True)
    def certificate(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        level1s = request.env['res.country'].sudo().search([])
        level2s = request.env['res.partner'].sudo().search([])
        level2s = [j for j in level2s if j.is_company]
        level3s = request.env['matakarir.certificatepublisher'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'level1s': level1s,
            'level2s': level2s,
            'level3s': level3s,
        }
        return request.render("hr_apply.vacancy_certificate", values)        

    @http.route(['/save/vacancy/certificate'], type='http', auth='user', website=True)
    def save_certificate(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('level1_name'):
            level1_id = request.env['res.country'].create({'name': kwargs.get('level1_name')})
        elif kwargs.get('level1'):
            level1_id = request.env['res.country'].search([("id","=",kwargs.get('level1'))])
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('level2_name'):
            level2_id = request.env['res.partner'].create({
                'name': kwargs.get('level2_name'), 'country_id':level1_id.id})
        elif kwargs.get('level2'):
            level2_id = request.env['res.partner'].search([("id","=",kwargs.get('level2'))])
        else:
            return request.redirect(request.httprequest.referrer)

        if kwargs.get('level3_name'):
            level3_id = request.env['matakarir.certificatepublisher'].create({
            'name': kwargs.get('level3_name'), 'publisher_id':level2_id.id})
        elif kwargs.get('level3'):
            level3_id = request.env['matakarir.certificatepublisher'].search([("id","=",kwargs.get('level3'))])
        else:
            return request.redirect(request.httprequest.referrer)
        required_certificate_ids = request.env['hr_apply.required_certificate'].create({
            'job_id': vacancy.id,
            'object_id': level3_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/certificate/<model("hr_apply.required_certificate"):required_certificate>'], type='http', auth='user', website=True)
    def remove_certificate(self, job, required_certificate, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_certificate'].search([("id","=",required_certificate.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/skill'], type='http', auth='user', website=True)
    def skill(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        v_objects = request.env['res.skill'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'v_objects': v_objects,
        }
        return request.render("hr_apply.vacancy_skill", values)        

    @http.route(['/save/vacancy/skill'], type='http', auth='user', website=True)
    def save_skill(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('v_object_name'):
            skill_id = request.env['res.skill'].create({'name': kwargs.get('v_object_name'), 'country_id': vacancy.country_id.id})
        elif kwargs.get('v_object_id'):
            skill_id = request.env['res.skill'].search([("id","=",kwargs.get('v_object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_skill_ids = request.env['hr_apply.required_skill'].create({
            'job_id': vacancy.id,
            'object_id': skill_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/skill/<model("hr_apply.required_skill"):required_skill>'], type='http', auth='user', website=True)
    def remove_skill(self, job, required_skill, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_skill'].search([("id","=",required_skill.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/langskill'], type='http', auth='user', website=True)
    def langskill(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        v_objects = request.env['res.language'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'v_objects': v_objects,
        }
        return request.render("hr_apply.vacancy_langskill", values)        

    @http.route(['/save/vacancy/langskill'], type='http', auth='user', website=True)
    def save_langskill(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('v_object_name'):
            langskill_id = request.env['res.language'].create({'name': kwargs.get('v_object_name'), 'country_id': vacancy.country_id.id})
        elif kwargs.get('v_object_id'):
            langskill_id = request.env['res.language'].search([("id","=",kwargs.get('v_object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_langskill_ids = request.env['hr_apply.required_langskill'].create({
            'job_id': vacancy.id,
            'object_id': langskill_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/langskill/<model("hr_apply.required_langskill"):required_langskill>'], type='http', auth='user', website=True)
    def remove_langskill(self, job, required_langskill, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_langskill'].search([("id","=",required_langskill.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/comskill'], type='http', auth='user', website=True)
    def comskill(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        v_objects = request.env['res.computer'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'v_objects': v_objects,
        }
        return request.render("hr_apply.vacancy_comskill", values)        

    @http.route(['/save/vacancy/comskill'], type='http', auth='user', website=True)
    def save_comskill(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('v_object_name'):
            comskill_id = request.env['res.computer'].create({'name': kwargs.get('v_object_name'), 'country_id': vacancy.country_id.id})
        elif kwargs.get('v_object_id'):
            comskill_id = request.env['res.computer'].search([("id","=",kwargs.get('v_object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_comskill_ids = request.env['hr_apply.required_comskill'].create({
            'job_id': vacancy.id,
            'object_id': comskill_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/comskill/<model("hr_apply.required_comskill"):required_comskill>'], type='http', auth='user', website=True)
    def remove_comskill(self, job, required_comskill, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_comskill'].search([("id","=",required_comskill.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/tools'], type='http', auth='user', website=True)
    def tools(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        objects = request.env['matakarir.tooltype'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'objects': objects,
        }
        return request.render("hr_apply.vacancy_tools", values)        

    @http.route(['/save/vacancy/tools'], type='http', auth='user', website=True)
    def save_tools(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('object_name'):
            tooltype_id = request.env['matakarir.tooltype'].create({
                'name': kwargs.get('object_name')})
        elif kwargs.get('object_id'):
            tooltype_id = request.env['matakarir.tooltype'].search([("id","=",kwargs.get('object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_tools_ids = request.env['hr_apply.required_tools'].create({
            'job_id': vacancy.id,
            'object_id': tooltype_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/tools/<model("hr_apply.required_tools"):required_tools>'], type='http', auth='user', website=True)
    def remove_tools(self, job, required_tools, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_tools'].search([("id","=",required_tools.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/school'], type='http', auth='user', website=True)
    def school(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        v_objects = request.env['matakarir.schoolstage'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'v_objects': v_objects,
        }
        return request.render("hr_apply.vacancy_school", values)        

    @http.route(['/save/vacancy/school'], type='http', auth='user', website=True)
    def save_school(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('v_object_name'):
            school_id = request.env['matakarir.schoolstage'].create({'name': kwargs.get('v_object_name'), 'country_id': vacancy.country_id.id})
        elif kwargs.get('v_object_id'):
            school_id = request.env['matakarir.schoolstage'].search([("id","=",kwargs.get('v_object_id'))])
        else:
            return request.redirect(request.httprequest.referrer)
        
        required_school_ids = request.env['hr_apply.required_school'].create({
            'job_id': vacancy.id,
            'object_id': school_id.id,
        })
        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/school/<model("hr_apply.required_school"):required_school>'], type='http', auth='user', website=True)
    def remove_school(self, job, required_school, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_school'].search([("id","=",required_school.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/university'], type='http', auth='user', website=True)
    def university(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        degrees = request.env['matakarir.universitydegree'].sudo().search([])
        faculties = request.env['matakarir.faculty'].sudo().search([])
        majors = request.env['matakarir.facultymajor'].sudo().search([])
        values ={
            'vacancy': vacancy,
            'degrees': degrees,
            'faculties': faculties,
            'majors': majors,
        }
        return request.render("hr_apply.vacancy_university", values)        

    @http.route(['/save/vacancy/university'], type='http', auth='user', website=True)
    def save_university(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('degree_name'):
            degree_id = request.env['matakarir.universitydegree'].create({'name': kwargs.get('degree_name')})
        elif kwargs.get('degree_id'):
            degree_id = request.env['matakarir.universitydegree'].search([("id","=",kwargs.get('degree_id'))])
        else:
            degree_id = None
        
        if degree_id:
            required_university_id = request.env['hr_apply.required_university'].create({
                'job_id': vacancy.id,
                'degree_id': degree_id.id,
            })
        
        if kwargs.get('faculty_name'):
            faculty_id = request.env['matakarir.faculty'].create({'name': kwargs.get('faculty_name')})
        elif kwargs.get('faculty_id'):
            faculty_id = request.env['matakarir.faculty'].search([("id","=",kwargs.get('faculty_id'))])
        else:
            faculty_id = None
        
        if faculty_id:
            if required_university_id:
                required_university_id['faculty_id'] = faculty_id
            else:
                required_university_id = request.env['hr_apply.required_university'].create({
                    'job_id': vacancy.id,
                    'faculty_id': faculty_id.id,
                })
            if kwargs.get('major_name'):
                major_id = request.env['matakarir.facultymajor'].create({'name': kwargs.get('major_name'), 'faculty_id': faculty_id.id})
            elif kwargs.get('major_id'):
                major_id = request.env['matakarir.facultymajor'].search([("id","=",kwargs.get('major_id'))])
            else:
                major_id = None
        
            if major_id:
                required_university_id['major_id'] = major_id

        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/university/<model("hr_apply.required_university"):required_university>'], type='http', auth='user', website=True)
    def remove_university(self, job, required_university, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_university'].search([("id","=",required_university.id)]).unlink()
        return request.redirect(request.httprequest.referrer)

    @http.route(['/vacancy/<model("hr.job"):job>/experience'], type='http', auth='user', website=True)
    def experience(self, job, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        values ={
            'vacancy': vacancy,
            'numbers': request.env['hr_apply.number'].sudo().search([]),
            'levels': request.env['matakarir.joblevel'].sudo().search([]),
            'departments': request.env['hr.department'].sudo().search([]),
            'industries': request.env['res.partner.industry'].sudo().search([]),
        }
        return request.render("hr_apply.vacancy_experience", values)        

    @http.route(['/save/vacancy/experience'], type='http', auth='user', website=True)
    def save_experience(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        
        if kwargs.get('min_exp'):
            exp = request.env['hr_apply.number'].search([("id","=",kwargs.get('min_exp'))])
            required_experience_id = request.env['hr_apply.required_experience'].create({
                'job_id': vacancy.id,
                'min_exp': exp.name,
            })
        else:
            return request.redirect(request.httprequest.referrer)
        
        if kwargs.get('level_name'):
            level_id = request.env['matakarir.joblevel'].create({'name': kwargs.get('level_name')})
        elif kwargs.get('level_id'):
            level_id = request.env['matakarir.joblevel'].search([("id","=",kwargs.get('level_id'))])
        else:
            level_id=None
        if level_id:
            required_experience_id['joblevel_id'] = level_id

        if kwargs.get('department_name'):
            department_id = request.env['hr.department'].create({'name': kwargs.get('department_name')})
        elif kwargs.get('department_id'):
            department_id = request.env['hr.department'].search([("id","=",kwargs.get('department_id'))])
        else:
            department_id=None
        if department_id:
            required_experience_id['department_id'] = department_id

        if kwargs.get('industry_name'):
            industry_id = request.env['res.partner.industry'].create({'name': kwargs.get('industry_name')})
        elif kwargs.get('industry_id'):
            industry_id = request.env['res.partner.industry'].search([("id","=",kwargs.get('industry_id'))])
        else:
            industry_id=None
        if industry_id:
            required_experience_id['industry_id'] = industry_id

        return request.redirect(request.httprequest.referrer)    
    
    @http.route(['/remove/<model("hr.job"):job>/experience/<model("hr_apply.required_experience"):required_experience>'], type='http', auth='user', website=True)
    def remove_experience(self, job, required_experience, **kwargs):
        partner_id = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner_id:
            return request.redirect('/my/home')
        request.env['hr_apply.required_experience'].search([("id","=",required_experience.id)]).unlink()
        return request.redirect(request.httprequest.referrer)
        
    @http.route(['/vacancy/<model("hr.job"):job>/applicants',
                '/vacancy/<model("hr.job"):job>/applicants/page/<int:page>',], type='http', auth="user", website=True)
    def vacancy_applicants(self, job, page=1, **kwargs):
        partner = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        if vacancy.poster_id != partner:
            return request.redirect('/my/home')
        domain = [("job_id","=",vacancy.id), ('status','not in',['draft','rejected','canceled'])]
        applicants = request.env['hr_apply.applicant'].sudo().search([])
        total = applicants.search_count(domain)
        pager = request.website.pager(
            url=('/vacancy/%s/applicants' % (vacancy.id)),
            total=total,
            page=page,
            step=self._application_per_page,
        )
        applications = applicants.search(domain, offset=(page - 1) * self._application_per_page, limit=self._application_per_page)
        
        values = {
            'partner': partner,
            'vacancy': vacancy,
            'pager': pager,
            'applications': applications,
        }
        return request.render("hr_apply.applicant_list", values)
        
