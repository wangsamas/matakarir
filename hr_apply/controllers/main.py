# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import werkzeug
from datetime import datetime
from math import ceil

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)


class MyVacanciesPortal(http.Controller):
    _vacancies_per_page = 20
    _activities_per_page = 10
	
    @http.route(['/my/activities',
                 '/my/activities/v/page/<int:v_page>',
                 '/my/activities/a/page/<int:a_page>',
                ], type='http', auth="user", website=True)
    def activities(self, v_page=1, a_page=1, **kwargs):
        partner = request.env.user.partner_id
        vacancy_domain = [("poster_id", "=", partner.id)]
        application_domain = [("partner_id", "=", partner.id), ("status", "not in", ["canceled"])]
#        application_domain += [("status", "not in", "canceled")]
#        application_ids = request.env['hr_apply.applicant'].sudo().search([("partner_id", "=", partner.id), ("status", "not in", ["canceled"])])

        vacancies = request.env['hr.job']
        total_vacancy = vacancies.search_count(vacancy_domain)
        v_pager = request.website.pager(
            url='/my/activities/v',
            total=total_vacancy,
            page=v_page,
            step=self._activities_per_page,
        )
        vacancy_ids = vacancies.search(vacancy_domain, offset=(v_page - 1) * self._activities_per_page, limit=self._activities_per_page)

        applications = request.env['hr_apply.applicant']
        total_application = applications.search_count(application_domain)
        a_pager = request.website.pager(
            url='/my/activities/a',
            total=total_application,
            page=a_page,
            step=self._activities_per_page,
        )
        application_ids = applications.search(application_domain, offset=(a_page - 1) * self._activities_per_page, limit=self._activities_per_page)

        values ={
            'partner': partner,
            'company_ids': partner.working_company_ids,
            'vacancy_ids': vacancy_ids,
            'application_ids': application_ids,
            'v_pager': v_pager,
            'a_pager': a_pager,
            'page_name': 'my_activities',
        }
        return request.render("hr_apply.my_activites", values)

    @http.route(['/profile/<model("res.partner"):company_id>',
                '/profile/<model("res.partner"):company_id>/page/<int:page>',], type='http', auth="public", website=True, csrf=False)
    def profile(self, company_id, page=1, **kwargs):
        user = request.env.user
        company = request.env['res.partner'].sudo().search([("id","=",company_id.id)])
        if company.is_company == False:
            return request.redirect('/')
        domain = [("employer_id","=",company.id)]
        vacancies = request.env['hr.job']
        total = vacancies.search_count(domain)
        pager = request.website.pager(
            url=('/profile/%s' % (company.id)),
            total=total,
            page=page,
            step=self._vacancies_per_page,
        )
        jobs = vacancies.search(domain, offset=(page - 1) * self._vacancies_per_page, limit=self._vacancies_per_page)
        values ={
            'user': user,
            'company': company,
            'jobs': jobs,
            'pager': pager,
        }
        return request.render("hr_apply.show_company", values)

    @http.route(['/vacancy/<model("hr.job"):job>'], type='http', auth="public", website=True, csrf=False)
    def vacancy(self, job, **kwargs):
        user = request.env.user
        vacancy = request.env['hr.job'].sudo().search([("id","=",job.id)])
        vacancy['views'] += 1
        company = vacancy.employer_id
        values ={
            'user': user,
            'company': company,
            'vacancy': vacancy,
        }
        return request.render("hr_apply.show_vacancy", values)

    @http.route(['/vacancies',
                 '/vacancies/page/<int:page>',
                 '/search/job/<string:search>',
                 '/cari/kerja/<string:search>',
                ], type='http', auth="public", website=True, csrf=False)
    def vacancies(self, page=1, search='', sorting=None, **kwargs):
        user = request.env.user
        AllVacancies = request.env['hr.job']
        domain = [('no_of_recruitment','>',0)]
        url_args = {}
        values = {}
        if search:
            search = search.replace('.',' ')
            url_args['search'] = search
            values['search'] = search
            for srch in search.split(" "):
                domain += ['|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', '|', 
                           ('name', 'ilike', srch), 
                           ('description', 'ilike', srch), 
                           ('tasks', 'ilike', srch), 
                           ('country_id.name', 'ilike', srch), 
                           ('state_id.name', 'ilike', srch), 
                           ('city_id.name', 'ilike', srch), 
                           ('district_id.name', 'ilike', srch), 
                           ('village_id.name', 'ilike', srch), 
                           ('area_id.name', 'ilike', srch), 
                           ('industry_id.name', 'ilike', srch), 
                           ('department_id.name', 'ilike', srch), 
                           ('level_id.name', 'ilike', srch), 
                           ('e_status_id.name', 'ilike', srch), 
                           ('employer_id.name', 'ilike', srch)]

        if kwargs.get('country'):
            country = request.env['res.country'].sudo().search([('id','=',kwargs.get('country'))])
            url_args['country_id'] = country.id
            values['country_id'] = country.id
            domain += [('country_id', '=', country.id)]
            
        if kwargs.get('state'):
            state = request.env['res.country.state'].sudo().search([('id','=',kwargs.get('state'))])
            url_args['state_id'] = state.id
            values['state_id'] = state.id
            domain += [('state_id.id', '=', state.id)]
            
        if kwargs.get('city'):
            city = request.env['res.city'].sudo().search([('id','=',kwargs.get('city'))])
            url_args['city_id'] = city.id
            values['city_id'] = city.id
            domain += [('city_id.id', '=', city.id)]
            
        if kwargs.get('district'):
            district = request.env['res.district'].sudo().search([('id','=',kwargs.get('district'))])
            url_args['district_id'] = district.id
            values['district_id'] = district.id
            domain += [('district_id.id', '=', district.id)]
            
        if kwargs.get('village'):
            village = request.env['res.village'].sudo().search([('id','=',kwargs.get('village'))])
            url_args['village_id'] = village.id
            values['village_id'] = village.id
            domain += [('village_id.id', '=', village.id)]
            
        if kwargs.get('area'):
            area = request.env['res.area'].sudo().search([('id','=',kwargs.get('area'))])
            url_args['area_id'] = area.id
            values['area_id'] = area.id
            domain += [('area_id.id', '=', area.id)]
            
        if kwargs.get('company'):
            company = request.env['res.partner'].sudo().search([('id','=',kwargs.get('company'))])
            url_args['company_id'] = company.id
            values['company_id'] = company.id
            domain += [('company_id.id', '=', company.id)]
            
        if kwargs.get('level'):
            level = request.env['matakarir.joblevel'].sudo().search([('id','=',kwargs.get('level'))])
            url_args['level_id'] = level.id
            values['level_id'] = level.id
            domain += [('level_id.id', '=', level.id)]
            
        if kwargs.get('department'):
            department = request.env['hr.department'].sudo().search([('id','=',kwargs.get('department'))])
            url_args['department_id'] = department.id
            values['department_id'] = department.id
            domain += [('department_id.id', '=', department.id)]
            
        if kwargs.get('industry'):
            industry = request.env['res.partner.industry'].sudo().search([('id','=',kwargs.get('industry'))])
            url_args['industry_id'] = industry.id
            values['industry_id'] = industry.id
            domain += [('industry_id.id', '=', industry.id)]
            
        if kwargs.get('e_status'):
            e_status = request.env['matakarir.employmentstatus'].sudo().search([('id','=',kwargs.get('e_status'))])
            url_args['e_status_id'] = e_status.id
            values['e_status_id'] = e_status.id
            domain += [('e_status_id.id', '=', e_status.id)]
            
        if kwargs.get('salary_currency'):
            salary_currency = request.env['res.currency'].sudo().search([('id','=',kwargs.get('salary_currency'))])
            url_args['salary_currency_id'] = salary_currency.id
            values['salary_currency_id'] = salary_currency.id
            domain += [('salary_currency_id.id', '=', salary_currency.id)]
            
        if kwargs.get('salary_duration'):
            salary_duration = request.env['hr_apply.duration'].sudo().search([('id','=',kwargs.get('salary_duration'))])
            url_args['salary_duration_id'] = salary_duration.id
            values['salary_duration_id'] = salary_duration.id
            domain += [('salary_duration_id.id', '=', salary_duration.id)]
            
        if kwargs.get('salary'):
            salary = request.env['hr_apply.million'].sudo().search([('id','=',kwargs.get('salary'))])
            url_args['salary_id'] = salary.id
            values['salary_id'] = salary.id
            domain += [('min_salary', '<=', int(salary.name)), ('max_salary', '>=', int(salary.name))]
            
        if kwargs.get('age'):
            age = request.env['hr_apply.number'].sudo().search([('id','=',kwargs.get('age'))])
            url_args['age_id'] = age.id
            values['age_id'] = age.id
            domain += [('min_age', '<=', int(age.name)), ('max_age', '>=', int(age.name))]
           
        if sorting:
            # check that sorting is valid
            # retro-compatibily for V8 and google links
            try:
                AllVacancies._generate_order_by(sorting, None)
                url_args['sorting'] = sorting
            except ValueError:
                sorting = False

        total = AllVacancies.search_count(domain)
        pager = request.website.pager(
            url='/vacancies',
            total=total,
            page=page,
            step=self._vacancies_per_page,
            url_args=url_args,
        )
        vacancies = AllVacancies.search(domain, offset=(page - 1) * self._vacancies_per_page, limit=self._vacancies_per_page, order=sorting)

        countries = request.env['res.country'].sudo().search([('id','in',vacancies.mapped('country_id.id'))])
        states = request.env['res.country.state'].sudo().search([('id','in',vacancies.mapped('state_id.id'))])
        cities = request.env['res.city'].sudo().search([('id','in',vacancies.mapped('city_id.id'))])
        districts = request.env['res.district'].sudo().search([('id','in',vacancies.mapped('district_id.id'))])
        villages = request.env['res.village'].sudo().search([('id','in',vacancies.mapped('village_id.id'))])
        areas = request.env['res.area'].sudo().search([('id','in',vacancies.mapped('area_id.id'))])
        companies = request.env['res.partner'].sudo().search([('id','in',vacancies.mapped('employer_id.id'))])
        companies = [j for j in companies if j.is_company == True]
        currencies = request.env['res.currency'].sudo().search([('id','in',vacancies.mapped('currency_id.id'))])
        durations = request.env['hr_apply.duration'].sudo().search([('id','in',vacancies.mapped('duration_id.id'))])
        salaries = request.env['hr_apply.million'].sudo().search([])
        ages = request.env['hr_apply.number'].sudo().search([])
        e_statuses = request.env['matakarir.employmentstatus'].sudo().search([('id','in',vacancies.mapped('e_status_id.id'))])
        levels = request.env['matakarir.joblevel'].sudo().search([('id','in',vacancies.mapped('level_id.id'))])
        departments = request.env['hr.department'].sudo().search([('id','in',vacancies.mapped('department_id.id'))])
        industries = request.env['res.partner.industry'].sudo().search([('id','in',vacancies.mapped('industry_id.id'))])
        
        values.update({
            'user': user,
            'vacancies': vacancies,
            'sorting': sorting,
            'pager': pager,
            'countries': countries,
            'states': states,
            'cities': cities,
            'districts': districts,
            'villages': villages,
            'areas': areas,
            'companies': companies,
            'currencies': currencies,
            'durations': durations,
            'salaries': salaries,
            'ages': ages,
            'industries': industries,
            'e_statuses': e_statuses,
            'levels': levels,
            'departments': departments,
        })
        return request.render("hr_apply.vacancies", values)
        
    @http.route(['/jobmeta'], type='http', auth="public", website=True, csrf=False)
    def jobmeta(self, **kwargs):
        jobs = request.env['hr.job'].sudo().search([])
        for job in jobs:
            job['website_meta_title'] = job.name
            job['website_meta_keywords'] = job.name and job.employer_id.name
            job['website_meta_description'] = job.description
        return request.redirect('/')
    
    