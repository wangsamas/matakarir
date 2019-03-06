# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import werkzeug
from math import ceil
from datetime import date, datetime, timedelta
from dateutil.relativedelta import *

from odoo import fields, http, SUPERUSER_ID
from odoo.http import request
from odoo.tools import ustr
from odoo.addons.http_routing.models.ir_http import slug

_logger = logging.getLogger(__name__)


class ApplyVacancy(http.Controller):
    _message_per_page = 10
    
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

    def _calculate_experience_age(self, b=None, **kwargs):
        if b.status=='work':
            if b.since:
                delta = relativedelta(datetime.now(),fields.Datetime.from_string(b.since))
                age = float(delta.years + delta.months/12 + delta.days/365)
        else:
            if b.since and b.until:
                delta = relativedelta(fields.Datetime.from_string(b.until),fields.Datetime.from_string(b.since))
                age = float(delta.years + delta.months/12 + delta.days/365)
        return age

    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>'], type='http', auth="user", website=True)
    def apply(self, vacancy, **kwargs):
        partner = request.env.user.partner_id
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        request.env['hr_apply.tryapply'].sudo().search([("job_id","=",vacancy.id), ("partner_id","=",partner.id)]).unlink()
        
        if not partner.street or not partner.email or not partner.description:
            request.env['hr_apply.tryapply'].create({'partner_id': partner.id,'job_id': vacancy.id})
            return request.redirect('/edit/informations/%s' % slug(vacancy))
        
        if not partner.identification_no or not partner.alias_id or not partner.alias_id.street:
            request.env['hr_apply.tryapply'].create({'partner_id': partner.id,'job_id': vacancy.id})
            return request.redirect('/edit/identity/%s' % slug(vacancy))
        
        if not partner.birthday or not partner.gender or not partner.marital:
            request.env['hr_apply.tryapply'].create({'partner_id': partner.id,'job_id': vacancy.id})
            return request.redirect('/edit/otherinfo/%s' % slug(vacancy))

        application = request.env['hr_apply.applicant'].sudo().search([("job_id","=",vacancy.id), ("partner_id","=",partner.id)])
        if application:
            application.update({
                    'name': partner.name,
                    'partner_id': partner.id,
                    'job_id': vacancy.id,
                    'job_owner_id': vacancy.user_id.id,
                    'create_date': datetime.now(),
            })
        if not application:
            application = request.env['hr_apply.applicant'].create({
                'name': partner.name,
                'partner_id': partner.id,
                'job_id': vacancy.id,
                'job_owner_id': vacancy.user_id.id,
                'create_date': datetime.now(),
            })

        criteria_total = 0
        criteria_match = 0
        qualification_total = 0
        qualification_match = 0
        match = 0
        
        if vacancy.criteria_ids:
            for criteria in vacancy.criteria_ids:
                match = 0
                for score in partner.classification_score_ids:
                    if criteria.classification_method_id == score.classification_method_id:
                        match += 1
                if match == 0:
                    questionaire = request.env['questionaire.questionaire'].search([("classification_method_id","=",criteria.classification_method_id.id)])
                    vals = {'questionaire_id': questionaire.id}
                    UserInput = request.env['questionaire.user_input']
                    if request.website.user_id != request.env.user:
                        vals['partner_id'] = request.env.user.partner_id.id
                    user_input = UserInput.create(vals)
                    request.env['hr_apply.tryapply'].create({'partner_id': partner.id,'job_id': vacancy.id})
                    return request.redirect('/apply/vacancy/%s/questionaire/fill/%s/%s' % (vacancy.id, questionaire.id, user_input.token))

        request.env['hr_apply.criteriascore'].sudo().search([('applicant_id','=',application.id)]).unlink()
        if vacancy.criteria_ids:
            for criteria in vacancy.criteria_ids:
                criteria_total += 2
                for score in partner.classification_score_ids:
                    if score.classification_id == criteria.classification_id:
                        if score.score >= criteria.classification_method_id.excellent_score:
                            match = 2
                        elif score.score <= criteria.classification_method_id.poor_score:
                            match = 0
                        else:
                            match = 1
                request.env['hr_apply.criteriascore'].create({
                    'partner_id': partner.id,
                    'criteria_id': criteria.id,
                    'applicant_id': application.id,
                    'score': match})
                criteria_match += match

        if vacancy.min_age or vacancy.max_age:
            qualification_total += 1
            applicant_age = int(relativedelta(datetime.now(),fields.Datetime.from_string(partner.birthday)).years)
            application['applicant_age'] = applicant_age
            qualified_age = True
            
            if vacancy.min_age:
                if applicant_age < int(vacancy.min_age):
                    qualified_age = False
            if vacancy.max_age:
                if applicant_age > int(vacancy.max_age):
                    qualified_age = False
            application['qualified_age']=qualified_age
            if qualified_age == True:
                qualification_match += 1
        
        if vacancy.ethnic_id:
            qualification_total += 1
            if vacancy.ethnic_id == partner.ethnic_id:
                application['qualified_ethnic']=True
                qualification_match += 1
            else:
                application['qualified_ethnic']=False
            
        if vacancy.religion_id:
            qualification_total += 1
            if vacancy.religion_id == partner.religion_id:
                application['qualified_religion']=True
                qualification_match += 1
            else:
                application['qualified_religion']=False
        
        if vacancy.country_id:
            qualification_total += 1
            if vacancy.country_id == partner.country_id:
                application['qualified_country']=True
                qualification_match += 1
            else:
                application['qualified_country']=False
        
        if vacancy.state_id:
            qualification_total += 1
            if vacancy.state_id == partner.state_id:
                application['qualified_state']=True
                qualification_match += 1
            else:
                application['qualified_state']=False
        
        if vacancy.city_id:
            qualification_total += 1
            if vacancy.city_id == partner.city_id:
                application['qualified_city']=True
                qualification_match += 1
            else:
                application['qualified_city']=False
        
        if vacancy.district_id:
            qualification_total += 1
            if vacancy.district_id == partner.district_id:
                application['qualified_district']=True
                qualification_match += 1
            else:
                application['qualified_district']=False
        
        if vacancy.village_id:
            qualification_total += 1
            if vacancy.village_id == partner.village_id:
                application['qualified_village']=True
                qualification_match += 1
            else:
                application['qualified_village']=False
        
        if vacancy.area_id:
            qualification_total += 1
            if vacancy.area_id == partner.area_id:
                application['qualified_area']=True
                qualification_match += 1
            else:
                application['qualified_area']=False
        
        application.qualified_tool_ids.unlink()
        if vacancy.required_tools_ids:
            for a in vacancy.required_tools_ids:
                qualification_total += 1
                qualified_tool_id = request.env['hr_apply.qualified_tools'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.tools_ids:
                    if a.object_id == b.tooltype_id:
                        qualified_tool_id['qualified'] = True
                        qualification_match += 1
                        break
                    
        application.qualified_certificate_ids.unlink()
        if vacancy.required_certificate_ids:
            for a in vacancy.required_certificate_ids:
                qualification_total += 1
                qualified_certificate_id = request.env['hr_apply.qualified_certificate'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.certificate_ids:
                    if a.object_id == b.certificate_id:
                        qualified_certificate_id['qualified'] = True
                        qualification_match += 1
                        break

        application.qualified_lisence_ids.unlink()
        if vacancy.required_lisence_ids:
            for a in vacancy.required_lisence_ids:
                qualification_total += 1
                qualified_lisence_id = request.env['hr_apply.qualified_lisence'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.lisence_ids:
                    if a.object_id == b.lisence_id:
                        qualified_lisence_id['qualified'] = True
                        qualification_match += 1
                        break

        application.qualified_driving_lisence_ids.unlink()
        if vacancy.required_driving_lisence_ids:
            for a in vacancy.required_driving_lisence_ids:
                qualification_total += 1
                qualified_driving_lisence_id = request.env['hr_apply.qualified_driving_lisence'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.driving_lisence_ids:
                    if a.object_id == b.lisence_type_id:
                        qualified_driving_lisence_id['qualified'] = True
                        qualification_match += 1
                        break

        application.qualified_skill_ids.unlink()
        if vacancy.required_skill_ids:
            for a in vacancy.required_skill_ids:
                qualification_total += 1
                qualified_skill_id = request.env['hr_apply.qualified_skill'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.skill_ids:
                    if a.object_id == b.skill_id:
                        qualified_skill_id['qualified'] = True
                        qualification_match += 1
                        break

        application.qualified_langskill_ids.unlink()
        if vacancy.required_langskill_ids:
            for a in vacancy.required_langskill_ids:
                qualification_total += 1
                qualified_langskill_id = request.env['hr_apply.qualified_langskill'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.langskill_ids:
                    if a.object_id == b.language_id:
                        qualified_langskill_id['qualified'] = True
                        qualification_match += 1
                        break

        application.qualified_comskill_ids.unlink()
        if vacancy.required_comskill_ids:
            for a in vacancy.required_comskill_ids:
                qualification_total += 1
                qualified_comskill_id = request.env['hr_apply.qualified_comskill'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.comskill_ids:
                    if a.object_id == b.language_id:
                        qualified_comskill_id['qualified'] = True
                        qualification_match += 1
                        break
        
        application.qualified_school_ids.unlink()
        if vacancy.required_school_ids:
            qualification_total += 1
            for a in vacancy.required_school_ids:
                qualified_school_id = request.env['hr_apply.qualified_school'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.school_ids:
                    if a.object_id == b.stage_id:
                        qualified_school_id['qualified'] = True
                        break
            for c in application.qualified_school_ids:
                if c.qualified == True:
                    qualification_match += 1
                    break
        
        application.qualified_university_ids.unlink()
        if vacancy.required_university_ids:
            qualification_total += 1
            for a in vacancy.required_university_ids:
                qualified_university_id = request.env['hr_apply.qualified_university'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.university_ids:
                    if a.degree_id:
                        if a.degree_id == b.degree_id:
                            if a.faculty_id:
                                if a.faculty_id == b.faculty_id:
                                    if a.major_id:
                                        if a.major_id == b.major_id:
                                            qualified_university_id['qualified'] = True
                                            break
                                        else:
                                            qualified_university_id['qualified'] = False
                                            break
                                    else:
                                        qualified_university_id['qualified'] = True
                                        break
                                else:
                                    qualified_university_id['qualified'] = False
                                    break
                            else:
                                qualified_university_id['qualified'] = True
                                break
                        else:
                            qualified_university_id['qualified'] = False
                            break
                    if a.faculty_id:
                        if a.faculty_id == b.faculty_id:
                            if a.major_id:
                                if a.major_id == b.major_id:
                                    qualified_university_id['qualified'] = True
                                    break
                                else:
                                    qualified_university_id['qualified'] = False
                                    break
                            else:
                                qualified_university_id['qualified'] = True
                                break
                        else:
                            qualified_university_id['qualified'] = False
                            break
            for c in application.qualified_university_ids:
                if c.qualified == True:
                    qualification_match += 1
                    break

        application.qualified_experience_ids.unlink()
        if vacancy.required_experience_ids:
            qualification_total += 1
            for a in vacancy.required_experience_ids:
                qualified_experience_id = request.env['hr_apply.qualified_experience'].create({
                    'applicant_id': application.id,
                    'object_id': a.id,
                })
                for b in partner.experience_ids:
                    if a.joblevel_id:
                        if a.joblevel_id == b.level_id:
                            if a.department_id:
                                if a.department_id == b.department_id:
                                    if a.industry_id:
                                        if a.industry_id == b.industry_id:
                                            qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                                    else:
                                        qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                            elif a.industry_id:
                                if a.industry_id == b.industry_id:
                                    qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                            else:
                                qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                    elif a.department_id:
                        if a.department_id == b.department_id:
                            if a.industry_id:
                                if a.industry_id == b.industry_id:
                                    qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                            else:
                                qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                    elif a.industry_id:
                        if a.industry_id == b.industry_id:
                            qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                    else:
                        qualified_experience_id['age'] += self._calculate_experience_age(b=b)
                if qualified_experience_id['age'] > a.min_exp:
                    qualified_experience_id['qualified'] = True            
            for c in application.qualified_experience_ids:
                if c.qualified == True:
                    qualification_match += 1
                    break

        if qualification_total == 0:
            qualification_score = 100
        else:
            qualification_score = qualification_match / qualification_total * 100

        if criteria_total == 0:
            criteria_score = 100
        else:
            criteria_score = criteria_match / criteria_total * 100

        total_score = qualification_score * criteria_score / 100

        application['qualification_score'] = qualification_score
        application['criteria_score'] = criteria_score
        application['total_score'] = total_score
        application['status'] = 'draft'

        domain = [("application_id", "=", application.id)]
        messages = request.env['hr_apply.interview']
        total = messages.search_count(domain)
        pager = request.website.pager(
            url=('/application/%s' % (application.id)),
            total=total,
            page=1,
            step=self._message_per_page,
        )
        interview_ids = messages.search(domain, offset=(0) * self._message_per_page, limit=self._message_per_page)
        
        values = {
            'partner_id': partner,
            'application': application,
            'vacancy': vacancy,
            'partner': partner,
            'interview_ids': interview_ids,
            'pager': pager,
        }
        
        return request.render("hr_apply.application_form", values)

    @http.route(['/application/<model("hr_apply.applicant"):application>',
                '/application/<model("hr_apply.applicant"):application>/page/<int:page>',], type='http', auth="user", website=True)
    def view_application(self, application, page=1, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id or application.job_partner_id == partner_id:
            if application.job_partner_id == partner_id and application['status'] == 'sent':
                application['status'] = 'viewed'

            domain = [("application_id", "=", application.id)]
            messages = request.env['hr_apply.interview']
            total = messages.search_count(domain)
            pager = request.website.pager(
                url=('/application/%s' % (application.id)),
                total=total,
                page=page,
                step=self._message_per_page,
            )
            interview_ids = messages.search(domain, offset=(page - 1) * self._message_per_page, limit=self._message_per_page)
        
            values = {
                'partner_id': partner_id,
                'application': application,
                'vacancy': application.job_id,
                'partner': application.partner_id,
                'interview_ids': interview_ids,
                'pager': pager,
            }
            return request.render("hr_apply.application_form", values)
        else:
            return request.redirect('/my/home')
        
    @http.route(['/edit/otherinfo/new/<string:word>'], type='http', auth='user', website=True)
    def edit_other_info_word(self, word, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        values.update({
            'religions': request.env['res.religion'].sudo().search([]),
            'ethnics': request.env['res.ethnic'].sudo().search([]),
            'partner_id': partner_id,
            'object': partner_id,
            'word': word
        })
        return request.render("hr_apply.edit_other_info", values)

    @http.route(['/edit/otherinfo/<model("hr.job"):vacancy>'], type='http', auth='user', website=True)
    def edit_other_info(self, vacancy, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        values.update({
            'religions': request.env['res.religion'].sudo().search([]),
            'ethnics': request.env['res.ethnic'].sudo().search([]),
            'partner_id': partner_id,
            'object': partner_id,
            'vacancy': vacancy
        })
        return request.render("hr_apply.edit_other_info", values)

    @http.route('/submit/otherinfo', type='http', auth="user", methods=['POST'], website=True)
    def submit_other_info(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        partner_id = request.env.user.partner_id

        if kwargs.get('country_name'):
            country_id = request.env['res.country'].create({'name': kwargs.get('country_name')})
        elif kwargs.get('country'):
            country_id = request.env['res.country'].search([("id","=",kwargs.get('country'))])
        else:
            country_id = None

        if country_id:
            partner_id['birth_country_id'] = country_id
            if kwargs.get('state_name'):
                state_id = request.env['res.country.state'].create({
                    'name': kwargs.get('country_name'), 'country_id':country_id.id})
            elif kwargs.get('state'):
                state_id = request.env['res.country.state'].search([("id","=",kwargs.get('state'))])
            else:
                state_id = None
            
            if state_id:
                partner_id['birth_state_id'] = state_id
                if kwargs.get('city_name'):
                    city_id = request.env['res.city'].create({
                        'name': kwargs.get('city_name'), 'state_id':state_id.id})
                elif kwargs.get('city'):
                    city_id = request.env['res.city'].search([("id","=",kwargs.get('city'))])
                else:
                    city_id = None
                if city_id:
                    partner_id['birth_city_id'] = city_id
                
        if kwargs.get('citizen_name'):
            citizenship_id = request.env['res.country'].create({'name': kwargs.get('citizen_name')})
        elif kwargs.get('citizenship'):
            citizenship_id = request.env['res.country'].search([("id","=",kwargs.get('citizenship'))])
        else:
            citizenship_id = None
        if citizenship_id:
            partner_id['citizenship_id'] = citizenship_id

        if kwargs.get('religion_name'):
            religion_id = request.env['res.religion'].create({'name': kwargs.get('religion_name')})
        elif kwargs.get('religion'):
            religion_id = request.env['res.religion'].search([("id","=",kwargs.get('religion'))])
        else:
            religion_id = None
        if religion_id:
            partner_id['religion_id'] = religion_id

        if kwargs.get('ethnic_name'):
            ethnic_id = request.env['res.ethnic'].create({'name': kwargs.get('ethnic_name')})
        elif kwargs.get('ethnic'):
            ethnic_id = request.env['res.ethnic'].search([("id","=",kwargs.get('ethnic'))])
        else:
            ethnic_id = None
        if ethnic_id:
            partner_id['ethnic_id'] = ethnic_id

        if kwargs.get('birthday'):
            try:
                partner_id['birthday'] =  kwargs.get('birthday')
            except ValueError:
                error_fields.append(birthday)

        partner_id.update({
            'gender': kwargs.get('gender'),
            'marital': kwargs.get('marital'),
            'dependents': kwargs.get('dependents'),
            'height': kwargs.get('height'),
            'weight': kwargs.get('weight'),
            'blood': kwargs.get('blood'),
            'smoker': kwargs.get('smoker'),
        })
        if kwargs.get('word') == 'vacancy':
            return request.redirect('/new/vacancy')
        else:
            return request.redirect('/apply/vacancy/%s' % slug(vacancy))
    
    @http.route(['/edit/identity/new/<string:word>'], type='http', auth='user', website=True)
    def edit_identity_word(self, word, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'object': partner_id.alias_id,
            'word': word
        })
        return request.render("hr_apply.edit_my_identity", values)

    @http.route(['/edit/identity/<model("hr.job"):vacancy>'], type='http', auth='user', website=True)
    def edit_identity(self, vacancy, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        values.update({
            'partner_id': partner_id,
            'object': partner_id.alias_id,
            'vacancy': vacancy
        })
        return request.render("hr_apply.edit_my_identity", values)

    @http.route('/submit/identity', type='http', auth="user", methods=['POST'], website=True)
    def submit_identity(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        partner = request.env.user.partner_id
        partner_id = partner.alias_id
        self.save_area_value(partner_id, **kwargs)
        partner_id['street'] = kwargs.get('street')
        partner_id['street2'] = kwargs.get('street2')
        partner_id['address_status'] = kwargs.get('address_status')
        partner_id['phone'] = kwargs.get('phone')
        
        partner.update({
            'identification_no': kwargs.get('identification_no'),
            'sinid': kwargs.get('sinid'),
            'ssnid': kwargs.get('ssnid'),
            'passport_no': kwargs.get('passport_no'),
            'visa_no': kwargs.get('visa_no'),
            'permit_no': kwargs.get('permit_no'),
        })
        if kwargs.get('word') == 'vacancy':
            return request.redirect('/new/vacancy')
        else:
            return request.redirect('/apply/vacancy/%s' % slug(vacancy))
    
    @http.route(['/edit/informations/new/<string:word>'], type='http', auth='user', website=True)
    def edit_info_word(self, word, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        values.update({
            'partner_id': partner_id,
            'object': partner_id,
            'word': word
        })
        return request.render("hr_apply.edit_my_info", values)
    
    @http.route(['/edit/informations/<model("hr.job"):vacancy>'], type='http', auth='user', website=True)
    def edit_info(self, vacancy, **kwargs):
        partner_id = request.env.user.partner_id
        values = self._prepare_area_values()
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        values.update({
            'partner_id': partner_id,
            'object': partner_id,
            'vacancy': vacancy
        })
        return request.render("hr_apply.edit_my_info", values)
    
    @http.route('/submit/informations', type='http', auth="user", methods=['POST'], website=True)
    def submit_info(self, **kwargs):
        vacancy = request.env['hr.job'].sudo().search([("id","=",kwargs.get('vacancy'))])
        partner_id = request.env.user.partner_id
        self.save_area_value(partner_id, **kwargs)

        if kwargs.get('name'):
            if partner_id.alias_id:
                partner_id.alias_id['name'] = kwargs.get('name')
            else:
                alias_id = request.env['res.partner'].create({'name': kwargs.get('name')})
                partner_id['alias_id'] = alias_id

        partner_id.update({
            'name': kwargs.get('nickname'),
            'description': kwargs.get('description'),
            'street': kwargs.get('street'),
            'street2': kwargs.get('street2'),
            'phone': kwargs.get('phone'),
            'mobile': kwargs.get('mobile'),
            'email': kwargs.get('email'),
            'address_status': kwargs.get('address_status'),
        })
        if kwargs.get('word') == 'vacancy':
            return request.redirect('/new/vacancy')
        else:
            return request.redirect('/apply/vacancy/%s' % slug(vacancy))

    @http.route(['/submit/application/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def submit_application(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id:
            application.send_new_application_email()
            application['status'] = 'sent'
            return request.redirect('/application/%s' % slug(application))
        else:
            return request.redirect('/my/home')
            
    @http.route(['/cancel/application/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def cancel_application(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id:
            application['status'] = 'canceled'
            return request.redirect('/my/activities')
        else:
            return request.redirect('/my/home')
            
    @http.route(['/hire/application/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def hire_application(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.job_partner_id == partner_id:
            job = application.job_id
            partner = application.partner_id
            experience = request.env['matakarir.experience'].create({
                'partner_id': partner.id,
                'company_id': job.employer_id.id,
                'job_name': job.name,
                'since': datetime.now(),
                'status': 'work',
                })
            if job.department_id:
                experience['department_id'] = job.department_id.id
            if job.level_id:
                experience['level_id'] = job.level_id.id
            if job.industry_id:
                experience['industry_id'] = job.industry_id.id
            if job.e_status_id:
                experience['e_status_id'] = job.e_status_id.id
            application.send_hired_email()
            application['status'] = 'hired'
            job['no_of_recruitment'] -= 1
            return request.redirect(request.httprequest.referrer)
        else:
            return request.redirect('/my/home')
            
    @http.route(['/call/application/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def call_application(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id:
            application['status'] = 'called'
            return request.redirect(request.httprequest.referrer)
        else:
            return request.redirect('/my/home')
            
    @http.route(['/reject/application/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def reject_application(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.job_partner_id == partner_id:
            application.send_rejection_email()
            application['status'] = 'rejected'
            return request.redirect('/my/activities')
        else:
            return request.redirect('/my/home')
            
    @http.route(['/submit/interview/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def submit_interview(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id or application.job_partner_id == partner_id:
            if application.job_partner_id == partner_id:
                application['status'] = 'called'
                application.send_employer_response_email()
            if application.job_partner_id == partner_id:            
                application.send_applicant_response_email()
            request.env['hr_apply.interview'].create({
                'application_id': application.id,
                'writer_id': partner_id.id,
                'write_date': datetime.now(),
                'message': kwargs.get('message'),
            })
            return request.redirect('/application/%s' % slug(application))
        else:
            return request.redirect('/my/home')
            
    @http.route(['/applicant/<model("hr_apply.applicant"):application>'], type='http', auth="user", website=True)
    def view_applicant(self, application, **kwargs):
        partner_id = request.env.user.partner_id
        method_categories = request.env['questionaire.classification_method_category'].sudo().search([])
        application = request.env['hr_apply.applicant'].sudo().search([("id","=",application.id)])
        if application.partner_id == partner_id or application.job_partner_id == partner_id:
            values = {
                'method_categories': method_categories,
                'partner_id': partner_id,
                'application': application,
                'vacancy': application.job_id,
                'partner': application.partner_id,
            }
            return request.render("hr_apply.applicant_profile", values)
        else:
            return request.redirect('/my/home')
        
