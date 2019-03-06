# See LICENSE file for full copyright and licensing details.

{
    'name': 'Applicant Matakarir',
    'version': '11.0.0.1.0',
    'category': 'Human Resources',
    'summary': 'Matakarir Applicant',
    "author": "Kusuma Ruslan",
    "website": "http://www.matakarir.com",
    'depends': ['document', 'matakarir', 'questionaire'],
    'data': [
        'data/hr_apply.million.csv',
        'data/hr_apply.number.csv',
        'data/hr_apply.duration.csv',
        'security/ir.model.access.csv',
        'views/apply_template.xml',
        'views/company_template.xml',
        'views/emails.xml',
        'views/model_views.xml',
        'views/my_activities_template.xml',
        'views/new_vacancy_template.xml',
        'views/vacancy_list_template.xml',
        'views/questionaire_template.xml',
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
}
