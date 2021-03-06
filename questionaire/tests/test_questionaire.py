# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import random
import re
from collections import Counter
from itertools import product

from werkzeug import urls

from odoo import _
from odoo.addons.http_routing.models.ir_http import slug
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

class TestQuestionaire(TransactionCase):

    def setUp(self):
        super(TestQuestionaire, self).setUp()
        User = self.env['res.users'].with_context({'no_reset_password': True})
        (group_questionaire_user, group_employee) = (self.ref('questionaire.group_questionaire_user'), self.ref('base.group_user'))
        self.questionaire_manager = User.create({
            'name': 'Gustave Doré', 'login': 'Gustav','email': 'gustav.dore@example.com',
            'groups_id': [(6, 0, [self.ref('questionaire.group_questionaire_manager'), group_questionaire_user, group_employee])]})

        self.questionaire_user = User.create({
            'name': 'Lukas Peeters', 'login': 'Lukas', 'email': 'lukas.petters@example.com',
            'groups_id': [(6, 0, [group_questionaire_user, group_employee])]})

        self.user_public = User.create({
            'name': 'Wout Janssens', 'login': 'Wout', 'email': 'wout.janssens@example.com',
            'groups_id': [(6, 0, [self.ref('base.group_public')])]})

        self.questionaire1 = self.env['questionaire.questionaire'].sudo(self.questionaire_manager).create({'title': "S0", 'page_ids': [(0, 0, {'title': "P0"})]})
        self.page1 = self.questionaire1.page_ids[0]

    def test_00_create_minimal_questionaire(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({'page_id': self.page1.id, 'question': 'Q0'})
        self.assertEqual(self.questionaire1.title, "S0", msg="Title of the questionaire is somehow modified.")
        self.assertEqual(len(self.questionaire1.page_ids), 1, msg="Additional Pages are linked with the questionaire after creation.")
        self.assertEqual(self.page1.title, "P0", msg="Title of the page is somehow modified.")
        self.assertEqual(len(self.page1.question_ids), 1, msg="Additional questions are linked with the page after creation.")
        self.assertEqual(question.question, "Q0", msg="Title of the Question is somehow modified.")

    def test_01_question_type_validation_save_line_function(self):
        for (question_type, text) in self.env['questionaire.question']._fields['type'].selection:
            # Each question ype must have validation function.
            self.assertTrue(hasattr(self.env['questionaire.question'], 'validate_' + question_type), msg="Question must have a validation method in\
                the form of 'validate_' followed by the name of the type.")

            # Questionaire Input Lines must have validation function for each line.
            self.assertTrue(hasattr(self.env['questionaire.user_input_line'], 'save_line_' + question_type), msg="Inputline must have Save method in \
                the form of 'save_line_' followed by the name of the type.")

    def test_02_question_answer_required(self):
        for (question_type, text) in self.env['questionaire.question']._fields['type'].selection:
            # Blank value of field is not accepted for mandatory questions.
            if question_type == 'multiple_choice':
                question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
                    'page_id': self.page1.id, 'question': 'Q0', 'type': 'multiple_choice',
                    'constr_mandatory': True, 'constr_error_msg': 'Error',
                    'labels_ids': [(0, 0, {'value': "MChoice0", "quizz_mark": 0}), (0, 0, {'value': "MChoice1", "quizz_mark": 0})]})

            elif question_type == 'matrix':
                question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
                    'page_id': self.page1.id, 'question': 'Q0', 'type': 'matrix', 'matrix_subtype': 'simple',
                    'constr_mandatory': True, 'constr_error_msg': 'Error',
                    'labels_ids': [(0, 0, {'value': "Column0", "quizz_mark": 0}), (0, 0, {'value': "Column1", "quizz_mark": 0})],
                    'labels_ids_2': [(0, 0, {'value': "Row0", "quizz_mark": 0}), (0, 0, {'value': "Row1", "quizz_mark": 0})]})

            else:
                question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
                    'page_id': self.page1.id, 'question': 'Q0', 'type': question_type, 'constr_mandatory': True, 'constr_error_msg': 'Error'})
            answer_tag = '%s_%s_%s' % (self.questionaire1.id, self.page1.id, question.id)
            self.assertDictEqual({answer_tag: "Error"}, question.validate_question({answer_tag: ''}, answer_tag),
                msg=("Validation function for type %s is unable to generate error if it is mandatory and answer is blank." % question_type))

    def test_03_question_textbox(self):
        questions = [
            self.env['questionaire.question'].sudo(self.questionaire_manager).create({
                'page_id': self.page1.id, 'question': 'Q0', 'type': 'textbox', 'validation_email': True}),
            self.env['questionaire.question'].sudo(self.questionaire_manager).create({
                'page_id': self.page1.id, 'question': 'Q1', 'type': 'textbox', 'validation_required': True,
                'validation_length_min': 2, 'validation_length_max': 8, 'validation_error_msg': "Error"})]

        results = [('test @ testcom', _('This answer must be an email address')), ('t', 'Error')]
        for i in range(len(questions)):
            answer_tag = '%s_%s_%s' % (self.questionaire1.id, self.page1.id, questions[i].id)
            self.assertEqual(questions[i].validate_question({answer_tag: results[i][0]}, answer_tag), {answer_tag: results[i][1]}, msg="\
                Validation function for textbox is unable to notify if answer is violating the validation rules")

    def test_04_question_numerical_box(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
            'page_id': self.page1.id, 'question': 'Q0', 'type': 'numerical_box', 'validation_required': True,
            'validation_min_float_value': 2.1, 'validation_max_float_value': 3.0, 'validation_error_msg': "Error"})
        answer_tag = '%s_%s_%s' % (self.questionaire1.id, self.page1.id, question.id)
        results = [('aaa', _('This is not a number')), ('4.5', 'Error'), ('0.1', 'Error')]
        for i in range(len(results)):
            self.assertEqual(question.validate_question({answer_tag: results[i][0]}, answer_tag), {answer_tag: results[i][1]}, msg="\
                Validation function for type numerical_box is unable to notify if answer is violating the validation rules")

    def test_05_question_date(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
            'page_id': self.page1.id, 'question': 'Q0', 'type': 'date', 'validation_required': True,
            'validation_min_date': '2015-03-20', 'validation_max_date': '2015-03-25', 'validation_error_msg': "Error"})
        answer_tag = '%s_%s_%s' % (self.questionaire1.id, self.page1.id, question.id)
        results = [('2015-55-10', _('This is not a date')), ('2015-03-19', 'Error'), ('2015-03-26', 'Error')]
        for i in range(len(results)):
            self.assertEqual(question.validate_question({answer_tag: results[i][0]}, answer_tag), {answer_tag: results[i][1]}, msg="\
                Validation function for type date is unable to notify if answer is violating the validation rules")

    def test_06_questionaire_sharing(self):
        # Case-1: Executing action with correct data.
        correct_questionaire = self.env['questionaire.questionaire'].sudo(self.questionaire_manager).create({
            'title': "S0", 'stage_id': self.env['questionaire.stage'].search([('sequence', '=', 1)]).id,
            'page_ids': [(0, 0, {'title': "P0", 'question_ids': [(0, 0, {'question': "Q0", 'type': 'free_text'})]})]})
        action = correct_questionaire.action_send_questionaire()
        template = self.env.ref('questionaire.email_template_questionaire', raise_if_not_found=False)

        ctx = dict(
            self.env.context,
            default_model='questionaire.questionaire',
            default_res_id=correct_questionaire.id,
            default_questionaire_id=correct_questionaire.id,
            default_use_template=bool(template),
            default_template_id=template and template.id or False,
            default_composition_mode='comment')

        self.assertDictEqual(action, {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'questionaire.mail.compose.message',
            'target': 'new',
            'context': ctx,
        })

        # Case-2: Executing action with incorrect data.
        questionaires = [
            self.env['questionaire.questionaire'].sudo(self.questionaire_manager).create({  # Questionaire without any page or question.
                'title': "Test questionaire"}),
            self.env['questionaire.questionaire'].sudo(self.questionaire_manager).create({  # Closed Questionaire.
                'title': "S0", 'stage_id': self.env['questionaire.stage'].search([('closed', '=', True)]).id,  # Getting Closed stage id.
                'page_ids': [(0, 0, {'title': "P0", 'question_ids': [(0, 0, {'question': "Q0", 'type': 'free_text'})]})]})]
        for questionaire in questionaires:
            self.assertRaises(UserError, questionaire.action_send_questionaire)

    def test_07_questionaire_email_message(self):
        # Case-1: Executing send_mail with correct data.
        partner = self.env['res.partner'].create({'name': 'Marie De Cock', 'email': 'marie.de.cock@gmail.com'})
        questionaire_mail_message = self.env['questionaire.mail.compose.message'].sudo(self.questionaire_manager).create({
            'questionaire_id': self.questionaire1.id, 'public': 'email_public_link', 'body': '__URL__', 'partner_ids': [(4, partner.id)]})
        questionaire_mail_message.send_mail()

        # Case-2: Executing send_mail with incorrect data.
        mail_messages = [
            self.env['questionaire.mail.compose.message'].sudo(self.questionaire_manager).create({  # Mail Message without __URL__ in body.
                'questionaire_id': self.questionaire1.id, 'public': 'email_public_link'}),
            self.env['questionaire.mail.compose.message'].sudo(self.questionaire_manager).create({  # Mail Message without recipents.
                'questionaire_id': self.questionaire1.id, 'public': 'email_public_link', 'body': "__URL__"})]
        for message in mail_messages:
            self.assertRaises(UserError, message.send_mail)

    def test_08_questionaire_urls(self):
        def validate_url(url):
            """ Reference: https://github.com/django/django/blob/master/django/core/validators.py """
            url_regex = re.compile(
                r'^https?://'  # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
                r'localhost|'  # localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
                r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
                r'(?::\d+)?'  # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            return True if url_regex.match(url) else False

        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        urltypes = {'public': 'start', 'print': 'print', 'result': 'results'}
        for urltype, urltxt in urltypes.items():
            questionaire_url = getattr(self.questionaire1, urltype + '_url')
            questionaire_url_relative = getattr(self.questionaire1.with_context({'relative_url': True}), urltype + '_url')
            self.assertTrue(validate_url(questionaire_url))
            url = "questionaire/%s/%s" % (urltxt, slug(self.questionaire1))
            full_url = urls.url_join(base_url, url)
            self.assertEqual(full_url, questionaire_url)
            self.assertEqual('/' + url, questionaire_url_relative)
            if urltype == 'public':
                url_html = '<a href="%s">Click here to start questionaire</a>'
                self.assertEqual(url_html % full_url, getattr(self.questionaire1, urltype + '_url_html'), msg="Public URL is incorrect")
                self.assertEqual(url_html % ('/' + url), getattr(self.questionaire1.with_context({'relative_url': True}), urltype + '_url_html'), msg="Public URL is incorrect.")

    def test_09_answer_questionaire(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({'page_id': self.page1.id, 'question': 'Q0'})
        input_portal = self.env['questionaire.user_input'].sudo(self.questionaire_user).create({
            'questionaire_id': self.questionaire1.id,
            'partner_id': self.questionaire_user.partner_id.id,
            'user_input_line_ids': [(0, 0, {
                'skipped': False, 'answer_type': 'free_text', 'value_free_text': "Test Answer",
                'questionaire_id': self.questionaire1.id, 'question_id': question.id})]})

        input_public = self.env['questionaire.user_input'].sudo(self.user_public).create({
            'questionaire_id': self.questionaire1.id,
            'partner_id': self.questionaire_user.partner_id.id,
            'user_input_line_ids': [(0, 0, {
                'skipped': False, 'answer_type': 'free_text', 'value_free_text': "Test Answer",
                'questionaire_id': self.questionaire1.id, 'question_id': question.id})]})

        answers = [input_portal.user_input_line_ids[0], input_public.user_input_line_ids[0]]
        expected_values = {'answer_type': 'free_text', 'value_free_text': "Test Answer"}
        for answer in answers:
            for field, value in expected_values.items():
                self.assertEqual(answer[field], value, msg="Unable to answer the questionaire. Expected behaviour of %s is not proper." % (field))

    def test_10_questionaire_result_simple_multiple_choice(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
            'page_id': self.page1.id, 'question': 'Q0', 'type': 'simple_choice',
            'labels_ids': [(0, 0, {'value': "Choice0", 'quizz_mark': 0}), (0, 0, {'value': "Choice1", 'quizz_mark': 0})]})
        for i in range(3):
            self.env['questionaire.user_input'].sudo(self.user_public).create({'questionaire_id': self.questionaire1.id, 'user_input_line_ids': [(0, 0, {
                'question_id': question.id,
                'answer_type': 'suggestion',
                'value_suggested': random.choice(question.labels_ids.ids)})]})
        lines = [line.value_suggested.id for line in question.user_input_line_ids]
        answers = [{'text': label.value, 'count': lines.count(label.id), 'answer_id': label.id} for label in question.labels_ids]
        prp_result = self.env['questionaire.questionaire'].prepare_result(question)['answers']
        self.assertItemsEqual(prp_result, answers, msg="Statistics of simple, multiple choice questions are different from expectation")

    def test_11_questionaire_result_matrix(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({
            'page_id': self.page1.id, 'question': 'Q0', 'type': 'matrix', 'matrix_subtype': 'simple',
            'labels_ids': [(0, 0, {'value': "Column0", "quizz_mark": 0}), (0, 0, {'value': "Column1", "quizz_mark": 0})],
            'labels_ids_2': [(0, 0, {'value': "Row0", "quizz_mark": 0}), (0, 0, {'value': "Row1", "quizz_mark": 0})]})
        for i in range(3):
            self.env['questionaire.user_input'].sudo(self.user_public).create({'questionaire_id': self.questionaire1.id, 'user_input_line_ids': [(0, 0, {
                'question_id': question.id, 'answer_type': 'suggestion', 'value_suggested': random.choice(question.labels_ids.ids),
                'value_suggested_row': random.choice(question.labels_ids_2.ids)})]})
        lines = [(line.value_suggested_row.id, line.value_suggested.id) for line in question.user_input_line_ids]
        res = {}
        for i in product(question.labels_ids_2.ids, question.labels_ids.ids):
            res[i] = lines.count((i))
        self.assertEqual(self.env['questionaire.questionaire'].prepare_result(question)['result'], res, msg="Statistics of matrix type questions are different from expectations")

    def test_12_questionaire_result_numeric_box(self):
        question = self.env['questionaire.question'].sudo(self.questionaire_manager).create({'page_id': self.page1.id, 'question': 'Q0', 'type': 'numerical_box'})
        num = [float(n) for n in random.sample(range(1, 100), 3)]
        nsum = sum(num)
        for i in range(3):
            self.env['questionaire.user_input'].sudo(self.user_public).create({'questionaire_id': self.questionaire1.id, 'user_input_line_ids': [(0, 0, {
                'question_id': question.id, 'answer_type': 'number', 'value_number': num[i]})]})
        exresult = {
            'average': round((nsum / len(num)), 2), 'max': round(max(num), 2),
            'min': round(min(num), 2), 'sum': nsum, 'most_common': Counter(num).most_common(5)}
        result = self.env['questionaire.questionaire'].prepare_result(question)
        for key in exresult:
            self.assertEqual(result[key], exresult[key], msg="Statistics of numeric box type questions are different from expectations")

    def test_13_questionaire_actions(self):
        self.env['questionaire.question'].sudo(self.questionaire_manager).create({'page_id': self.page1.id, 'question': 'Q0', 'type': 'numerical_box'})

        actions = {
            'start': {'method': 'public', 'token': '/test', 'text': 'Start'},
            'print': {'method': 'print', 'token': '/test', 'text': 'Print'},
            'result': {'method': 'result', 'token': '', 'text': 'Results of the'},
            'test': {'method': 'public', 'token': '/phantom', 'text': 'Results of the'}}
        for action, val in actions.items():
            result = getattr(self.questionaire1.with_context({'questionaire_token': val['token'][1:]}), 'action_' + action + '_questionaire')()
            url = getattr(self.questionaire1.with_context({'relative_url': True}), val['method'] + '_url') + val['token']
            self.assertEqual(result['url'], url)
