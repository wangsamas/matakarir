# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64
import logging

from odoo import api, fields, models
from odoo import tools, _
from odoo.exceptions import ValidationError, AccessError
from odoo.modules.module import get_module_resource

_logger = logging.getLogger(__name__)

class RequiredExperiences(models.Model):
    _name = "hr_apply.required_experience"
    _description = "Required Experiences"

    job_id = fields.Many2one('hr.job')
    joblevel_id = fields.Many2one('matakarir.joblevel')
    department_id = fields.Many2one('hr.department')
    industry_id = fields.Many2one('res.partner.industry')
    min_exp = fields.Integer(string='Minimum Experience in Year')

class QualifiedExperiences(models.Model):
    _name = "hr_apply.qualified_experience"
    _description = "Qualified Experiences"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_experience')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    age = fields.Float('Age')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredUniversities(models.Model):
    _name = "hr_apply.required_university"
    _description = "Required Universities"

    job_id = fields.Many2one('hr.job')
    degree_id = fields.Many2one('matakarir.universitydegree')
    faculty_id = fields.Many2one('matakarir.faculty')
    major_id = fields.Many2one('matakarir.facultymajor')

class QualifiedUniversities(models.Model):
    _name = "hr_apply.qualified_university"
    _description = "Qualified Universities"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_university')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredSchools(models.Model):
    _name = "hr_apply.required_school"
    _description = "Required Schools"
    _order = "name"

    name = fields.Char(related='object_id.name')
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('matakarir.schoolstage')

class QualifiedSchools(models.Model):
    _name = "hr_apply.qualified_school"
    _description = "Qualified Schools"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_school')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredComputerSkills(models.Model):
    _name = "hr_apply.required_comskill"
    _description = "Required Computer Skills"
    _order = "name"
	
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('res.computer')
    name = fields.Char(related='object_id.name')

class QualifiedComputerSkills(models.Model):
    _name = "hr_apply.qualified_comskill"
    _description = "Qualified Computer Skills"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_comskill')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredLanguageSkills(models.Model):
    _name = "hr_apply.required_langskill"
    _description = "Required Language Skills"
    _order = "name"
	
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('res.language')
    name = fields.Char(related='object_id.name')

class QualifiedLanguageSkills(models.Model):
    _name = "hr_apply.qualified_langskill"
    _description = "Qualified Language Skills"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_langskill')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredSkills(models.Model):
    _name = "hr_apply.required_skill"
    _description = "Required Skills"
    _order = "name"

    name = fields.Char(related='object_id.name')
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('res.skill')

class QualifiedSkills(models.Model):
    _name = "hr_apply.qualified_skill"
    _description = "Qualified Skills"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_skill')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredDrivingLisences(models.Model):
    _name = "hr_apply.required_driving_lisence"
    _description = "Required Driving Lisences"
    _order = "name"
	
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('matakarir.drivinglisencetype')
    name = fields.Char(related='object_id.name')

class QualifiedDrivingLisences(models.Model):
    _name = "hr_apply.qualified_driving_lisence"
    _description = "Qualified Driving Lisences"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_driving_lisence')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredLisences(models.Model):
    _name = "hr_apply.required_lisence"
    _description = "Required Lisences"
    _order = "name"
	
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('matakarir.lisencepublisher')
    name = fields.Char(related='object_id.name')

class QualifiedLisences(models.Model):
    _name = "hr_apply.qualified_lisence"
    _description = "Qualified Lisences"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_lisence')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredCertificates(models.Model):
    _name = "hr_apply.required_certificate"
    _description = "Required Certificates"
    _order = "name"
	
    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('matakarir.certificatepublisher')
    name = fields.Char(related='object_id.name')

class QualifiedCertificates(models.Model):
    _name = "hr_apply.qualified_certificate"
    _description = "Qualified Certificates"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_certificate')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

class RequiredTools(models.Model):
    _name = "hr_apply.required_tools"
    _description = "Required Tools"
    _order = "name"

    job_id = fields.Many2one('hr.job')
    object_id = fields.Many2one('matakarir.tooltype')
    name = fields.Char(related='object_id.name')

class QualifiedTools(models.Model):
    _name = "hr_apply.qualified_tools"
    _description = "Qualified Tools"
    _order = "name"

    applicant_id = fields.Many2one('hr_apply.applicant')
    object_id = fields.Many2one('hr_apply.required_tools')
    job_id = fields.Many2one('hr.job', related='object_id.job_id')
    name = fields.Char(related='object_id.name')
    qualified = fields.Boolean('Qualified', default=False)

    
class AbuseReports(models.Model):
    _name = "hr_apply.abuse_report"
    _description = "Abuse Reports"

    job_id = fields.Many2one('hr.job')
    reporter_id = fields.Many2one('res.partner', string='Reporter')
    reason = fields.Char('Report Reason', required=True)

