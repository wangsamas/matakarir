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

_logger = logging.getLogger(__name__)


class WebsiteQuestionaire(http.Controller):
    # HELPER METHODS #

    def _check_bad_cases(self, vacancy, questionaire, token=None):
        # In case of bad questionaire, redirect to questionaires list
        if not questionaire.sudo().exists():
            return werkzeug.utils.redirect("/questionaire/")

        # In case of auth required, block public user
        if questionaire.auth_required and request.env.user == request.website.user_id:
            return request.render("hr_apply.auth_required", {'questionaire': questionaire, 'vacancy':vacancy, 'token': token})

        # In case of non open questionaires
        if questionaire.stage_id.closed:
            return request.render("questionaire.notopen")

        # If there is no pages
        if not questionaire.page_ids:
            return request.render("questionaire.nopages", {'questionaire': questionaire})

        # Everything seems to be ok
        return None

    def _check_deadline(self, user_input):
        '''Prevent opening of the questionaire if the deadline has turned out

        ! This will NOT disallow access to users who have already partially filled the questionaire !'''
        deadline = user_input.deadline
        if deadline:
            dt_deadline = fields.Datetime.from_string(deadline)
            dt_now = datetime.now()
            if dt_now > dt_deadline:  # questionaire is not open anymore
                return request.render("questionaire.notopen")
        return None

    ## ROUTES HANDLERS ##

    # Questionaire start
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/start/<model("questionaire.questionaire"):questionaire>',
                 '/apply/vacancy/<model("hr.job"):vacancy>/questionaire/start/<model("questionaire.questionaire"):questionaire>/<string:token>'],
                type='http', auth='public', website=True)
    def start_questionaire(self, vacancy, questionaire, token=None, **post):
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        OldUserInput = request.env['questionaire.user_input'].search([
            ('questionaire_id', '=',  questionaire.id), 
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        UserInput = request.env['questionaire.user_input']

        # Test mode
        if token and token == "phantom":
            _logger.info("[questionaire] Phantom mode")
            user_input = UserInput.create({'questionaire_id': questionaire.id, 'test_entry': True})
            data = {'questionaire': questionaire, 'vacancy':vacancy, 'page': None, 'token': user_input.token}
            return request.redirect('/apply/vacancy/%s/questionaire/fill/%s/%s' % (vacancy.id, questionaire.id, user_input.token))
#            return request.render('hr_apply.questionaire_init', data)

        # END Test mode

        # Controls if the questionaire can be displayed
        errpage = self._check_bad_cases(vacancy, questionaire, token=token)
        if errpage:
            return errpage

        # Manual questionaireing
        if not token:
            vals = {'questionaire_id': questionaire.id}
            if request.website.user_id != request.env.user:
                vals['partner_id'] = request.env.user.partner_id.id
            user_input = UserInput.create(vals)
        else:
            user_input = UserInput.sudo().search([('token', '=', token)], limit=1)
            if not user_input:
                return request.render("website.403")

        # Do not open expired questionaire
        errpage = self._check_deadline(user_input)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # Intro page
            data = {'questionaire': questionaire, 'vacancy':vacancy, 'page': None, 'token': user_input.token, 'old_user_input_id': OldUserInput}
            return request.render('hr_apply.questionaire_init', data)
        else:
            return request.redirect('/apply/vacancy/%s/questionaire/fill/%s/%s' % (vacancy.id, questionaire.id, user_input.token))

    # Questionaire displaying
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/fill/<model("questionaire.questionaire"):questionaire>/<string:token>',
                 '/apply/vacancy/<model("hr.job"):vacancy>/questionaire/fill/<model("questionaire.questionaire"):questionaire>/<string:token>/<string:prev>'],
                type='http', auth='public', website=True)
    def fill_questionaire(self, vacancy, questionaire, token, prev=None, **post):
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        OldUserInput = request.env['questionaire.user_input'].search([
            ('questionaire_id', '=',  questionaire.id), 
            ('partner_id', '=', request.env.user.partner_id.id)
        ])
        for Old in OldUserInput:
            if Old.token != token:
                Old.sudo().unlink()

        '''Display and validates a questionaire'''
        Questionaire = request.env['questionaire.questionaire']
        UserInput = request.env['questionaire.user_input']

        # Controls if the questionaire can be displayed
        errpage = self._check_bad_cases(vacancy, questionaire)
        if errpage:
            return errpage

        # Load the user_input
        user_input = UserInput.sudo().search([('token', '=', token)], limit=1)
        if not user_input:  # Invalid token
            return request.render("website.403")

        # Do not display expired questionaire (even if some pages have already been
        # displayed -- There's a time for everything!)
        errpage = self._check_deadline(user_input)
        if errpage:
            return errpage

        # Select the right page
        if user_input.state == 'new':  # First page
            page, page_nr, last = Questionaire.next_page(user_input, 0, go_back=False)
            data = {'questionaire': questionaire, 'vacancy':vacancy, 'page': page, 'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            return request.render('hr_apply.questionaire', data)
        elif user_input.state == 'done':  # Display success message
            return request.redirect('/apply/vacancy/%s' % (vacancy.id))
#            return request.render('questionaire.sfinished', {'questionaire': questionaire,
#                                                             'token': token,
#                                                             'quest': questionaire,
#                                                             'partner': user_input.partner_id,
#                                                             'user_input': user_input})
        elif user_input.state == 'skip':
            flag = (True if prev and prev == 'prev' else False)
            page, page_nr, last = Questionaire.next_page(user_input, user_input.last_displayed_page_id.id, go_back=flag)

            #special case if you click "previous" from the last page, then leave the questionaire, then reopen it from the URL, avoid crash
            if not page:
                page, page_nr, last = Questionaire.next_page(user_input, user_input.last_displayed_page_id.id, go_back=True)

            data = {'questionaire': questionaire, 'vacancy':vacancy, 'page': page, 'page_nr': page_nr, 'token': user_input.token}
            if last:
                data.update({'last': True})
            return request.render('hr_apply.questionaire', data)
        else:
            return request.render("website.403")

    # AJAX prefilling of a questionaire
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/prefill/<model("questionaire.questionaire"):questionaire>/<string:token>',
                 '/apply/vacancy/<model("hr.job"):vacancy>/questionaire/prefill/<model("questionaire.questionaire"):questionaire>/<string:token>/<model("questionaire.page"):page>'],
                type='http', auth='public', website=True)
    def prefill(self, vacancy, questionaire, token, page=None, **post):
        vacancy = request.env['hr.job'].sudo().search([("id","=",vacancy.id)])
        UserInputLine = request.env['questionaire.user_input_line']
        ret = {}

        # Fetch previous answers
        if page:
            previous_answers = UserInputLine.sudo().search([('user_input_id.token', '=', token), ('page_id', '=', page.id)])
        else:
            previous_answers = UserInputLine.sudo().search([('user_input_id.token', '=', token)])

        # Return non empty answers in a JSON compatible format
        for answer in previous_answers:
            if not answer.skipped:
                answer_tag = '%s_%s_%s' % (answer.questionaire_id.id, answer.page_id.id, answer.question_id.id)
                answer_value = None
                if answer.answer_type == 'free_text':
                    answer_value = answer.value_free_text
                elif answer.answer_type == 'text' and answer.question_id.type == 'textbox':
                    answer_value = answer.value_text
                elif answer.answer_type == 'text' and answer.question_id.type != 'textbox':
                    # here come comment answers for matrices, simple choice and multiple choice
                    answer_tag = "%s_%s" % (answer_tag, 'comment')
                    answer_value = answer.value_text
                elif answer.answer_type == 'number':
                    answer_value = str(answer.value_number)
                elif answer.answer_type == 'date':
                    answer_value = answer.value_date
                elif answer.answer_type == 'suggestion' and not answer.value_suggested_row:
                    answer_value = answer.value_suggested.id
                elif answer.answer_type == 'suggestion' and answer.value_suggested_row:
                    answer_tag = "%s_%s" % (answer_tag, answer.value_suggested_row.id)
                    answer_value = answer.value_suggested.id
                if answer_value:
                    ret.setdefault(answer_tag, []).append(answer_value)
                else:
                    _logger.warning("[questionaire] No answer has been found for question %s marked as non skipped" % answer_tag)
        return json.dumps(ret)

    # AJAX scores loading for quiz correction mode
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/scores/<model("questionaire.questionaire"):questionaire>/<string:token>'],
                type='http', auth='public', website=True)
    def get_scores(self, questionaire, token, page=None, **post):
        ret = {}

        # Fetch answers
        previous_answers = request.env['questionaire.user_input_line'].sudo().search([('user_input_id.token', '=', token)])

        # Compute score for each question
        for answer in previous_answers:
            tmp_score = ret.get(answer.question_id.id, 0.0)
            ret.update({answer.question_id.id: tmp_score + answer.quizz_mark})
        return json.dumps(ret)

    # AJAX submission of a page
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/submit/<model("questionaire.questionaire"):questionaire>'], type='http', methods=['POST'], auth='public', website=True)
    def submit(self, vacancy, questionaire, **post):
        _logger.debug('Incoming data: %s', post)
        page_id = int(post['page_id'])
        questions = request.env['questionaire.question'].search([('page_id', '=', page_id)])

        # Answer validation
        errors = {}
        for question in questions:
            answer_tag = "%s_%s_%s" % (questionaire.id, page_id, question.id)
            errors.update(question.validate_question(post, answer_tag))

        ret = {}
        if len(errors):
            # Return errors messages to webpage
            ret['errors'] = errors
        else:
            # Store answers into database
            try:
                user_input = request.env['questionaire.user_input'].sudo().search([('token', '=', post['token'])], limit=1)
            except KeyError:  # Invalid token
                return request.render("website.403")
            user_id = request.env.user.id if user_input.type != 'link' else SUPERUSER_ID

            for question in questions:
                answer_tag = "%s_%s_%s" % (questionaire.id, page_id, question.id)
                request.env['questionaire.user_input_line'].sudo(user=user_id).save_lines(user_input.id, question, post, answer_tag)

            if post['classification_method_id']:
                classifications = request.env['questionaire.classification'].search([('classification_method_id', '=', int(post['classification_method_id']))])
                for classification in classifications:
                    user_classification_ids = request.env['questionaire.user_classification'].search([
                        ('user_input_id', '=', user_input.id),
                        ('page_id', '=', page_id),
                        ('classification_id', '=', classification.id)
                    ])
                    if not user_classification_ids:
                        user_classification_ids = request.env['questionaire.user_classification'].create({
                            'user_input_id': user_input.id,
                            'page_id': page_id,
                            'classification_id': classification.id,
                        })
                    classification_score_ids = request.env['questionaire.classification_score'].search([
                        ('classification_id', '=', classification.id),
                        ('questionaire_id', '=', questionaire.id),
                        ('partner_id', '=', request.env.user.partner_id.id)
                    ])
                    if not classification_score_ids:
                        classification_score_ids = request.env['questionaire.classification_score'].create({
                            'classification_id': classification.id,
                            'questionaire_id': questionaire.id,
                            'partner_id': request.env.user.partner_id.id,
                        })
                    classification_score_ids._compute_score()                    
        
            go_back = post['button_submit'] == 'previous'
            next_page, _, last = request.env['questionaire.questionaire'].next_page(user_input, page_id, go_back=go_back)
            vals = {'last_displayed_page_id': page_id}
            if next_page is None and not go_back:
                vals.update({'state': 'done'})
            else:
                vals.update({'state': 'skip'})
            user_input.sudo(user=user_id).write(vals)
            ret['redirect'] = '/apply/vacancy/%s/questionaire/fill/%s/%s' % (vacancy.id, questionaire.id, post['token'])
            if go_back:
                ret['redirect'] += '/prev'            
        
        return json.dumps(ret)

    # Printing routes
    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/print/<model("questionaire.questionaire"):questionaire>',
                 '/apply/vacancy/<model("hr.job"):vacancy>/questionaire/print/<model("questionaire.questionaire"):questionaire>/<string:token>'],
                type='http', auth='public', website=True)
    def print_questionaire(self, vacancy, questionaire, token=None, **post):
        '''Display an questionaire in printable view; if <token> is set, it will
        grab the answers of the user_input_id that has <token>.'''
        
        return request.render('hr_apply.questionaire_print',
                                      {'questionaire': questionaire,
                                       'vacancy':vacancy,
                                       'token': token,
                                       'page_nr': 0,
                                       'quizz_correction': True if questionaire.quizz_mode and token else False})

    @http.route(['/apply/vacancy/<model("hr.job"):vacancy>/questionaire/results/<model("questionaire.questionaire"):questionaire>'],
                type='http', auth='user', website=True)
    def questionaire_reporting(self, vacancy, questionaire, token=None, **post):
        '''Display questionaire Results & Statistics for given questionaire.'''
        result_template = 'questionaire.result'
        current_filters = []
        filter_display_data = []
        filter_finish = False

        if not questionaire.user_input_ids or not [input_id.id for input_id in questionaire.user_input_ids if input_id.state != 'new']:
            result_template = 'questionaire.no_result'
        if 'finished' in post:
            post.pop('finished')
            filter_finish = True
        if post or filter_finish:
            filter_data = self.get_filter_data(post)
            current_filters = questionaire.filter_input_ids(filter_data, filter_finish)
            filter_display_data = questionaire.get_filter_display_data(filter_data)
        return request.render(result_template,
                                      {'questionaire': questionaire,
                                       'vacancy': vacancy,
                                       'questionaire_dict': self.prepare_result_dict(questionaire, current_filters),
                                       'page_range': self.page_range,
                                       'current_filters': current_filters,
                                       'filter_display_data': filter_display_data,
                                       'filter_finish': filter_finish
                                       })
        # Quick retroengineering of what is injected into the template for now:
        # (TODO: flatten and simplify this)
        #
        #     questionaire: a browse record of the questionaire
        #     questionaire_dict: very messy dict containing all the info to display answers
        #         {'page_ids': [
        #
        #             ...
        #
        #                 {'page': browse record of the page,
        #                  'question_ids': [
        #
        #                     ...
        #
        #                     {'graph_data': data to be displayed on the graph
        #                      'input_summary': number of answered, skipped...
        #                      'prepare_result': {
        #                                         answers displayed in the tables
        #                                         }
        #                      'question': browse record of the question_ids
        #                     }
        #
        #                     ...
        #
        #                     ]
        #                 }
        #
        #             ...
        #
        #             ]
        #         }
        #
        #     page_range: pager helper function
        #     current_filters: a list of ids
        #     filter_display_data: [{'labels': ['a', 'b'], question_text} ...  ]
        #     filter_finish: boolean => only finished questionaires or not
        #

    def prepare_result_dict(self, questionaire, current_filters=None):
        """Returns dictionary having values for rendering template"""
        current_filters = current_filters if current_filters else []
        Questionaire = request.env['questionaire.questionaire']
        result = {'page_ids': []}
        for page in questionaire.page_ids:
            page_dict = {'page': page, 'question_ids': []}
            for question in page.question_ids:
                question_dict = {
                    'question': question,
                    'input_summary': Questionaire.get_input_summary(question, current_filters),
                    'prepare_result': Questionaire.prepare_result(question, current_filters),
                    'graph_data': self.get_graph_data(question, current_filters),
                }

                page_dict['question_ids'].append(question_dict)
            result['page_ids'].append(page_dict)
        return result

    def get_filter_data(self, post):
        """Returns data used for filtering the result"""
        filters = []
        for ids in post:
            #if user add some random data in query URI, ignore it
            try:
                row_id, answer_id = ids.split(',')
                filters.append({'row_id': int(row_id), 'answer_id': int(answer_id)})
            except:
                return filters
        return filters

    def page_range(self, total_record, limit):
        '''Returns number of pages required for pagination'''
        total = ceil(total_record / float(limit))
        return range(1, int(total + 1))

    def get_graph_data(self, question, current_filters=None):
        '''Returns formatted data required by graph library on basis of filter'''
        # TODO refactor this terrible method and merge it with prepare_result_dict
        current_filters = current_filters if current_filters else []
        Questionaire = request.env['questionaire.questionaire']
        result = []
        if question.type == 'multiple_choice':
            result.append({'key': ustr(question.question),
                           'values': Questionaire.prepare_result(question, current_filters)['answers']
                           })
        if question.type == 'simple_choice':
            result = Questionaire.prepare_result(question, current_filters)['answers']
        if question.type == 'matrix':
            data = Questionaire.prepare_result(question, current_filters)
            for answer in data['answers']:
                values = []
                for row in data['rows']:
                    values.append({'text': data['rows'].get(row), 'count': data['result'].get((row, answer))})
                result.append({'key': data['answers'].get(answer), 'values': values})
        return json.dumps(result)
