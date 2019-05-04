# -*- coding: utf-8 -*-

from odoo import models, fields, api

class GhuAdvisor(models.Model):
    _name = 'ghu.advisor'
    _description = "Advisor"
    _order = "nomination DESC, nationality ASC, lastname ASC"
    _inherit = ['website.published.mixin']
    _inherits = {"res.partner": "partner_id"}

    is_cafeteria = fields.Boolean(
        string=u'Is cafeteria?',
    )
    
    advisor_id = fields.Char('Advisor ID', size=12)

    nomination = fields.Char('Nomination', size=128)

    academic_degree = fields.Char('Academic Degree', size=128)

    skype = fields.Char('Skype', size=128)

    nationality = fields.Many2one(
        string=u'Nationality',
        comodel_name='res.country'
    )
        
    native_language = fields.Many2one(
        string=u'Native Language',
        comodel_name='res.lang'
    )

    foreign_languages = fields.Many2many(
        string=u'Teaching Languages',
        comodel_name='ghu.lang',
        relation='advisor_lang_rel',
        column1='advisor_id',
        column2='lang_id'
    )
    
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'), ('o', 'Other')],
        string='Gender',
        required=True)
        
    birth_date = fields.Date(
        string=u'Birthday',
        default=fields.Date.context_today
    )

    vita = fields.Binary('Vita')

    degree = fields.Binary(
        string='Degree'
    )
    
    agreement = fields.Binary(
        string=u'Agreement',
    )

    programs = fields.Many2many(
        string=u'Programs',
        comodel_name='ghu.program',
        relation='advisor_program_rel',
        column1='advisor_id',
        column2='program_id',
    )

    @api.multi
    def all_languages(self):
        res = set()
        for advisor in self:
            res.update(advisor.foreign_languages)
        
        return sorted(res, key=lambda lang: lang.name.lower() if lang.name else "")

    @api.multi
    def all_countries(self):
        res = set()
        for advisor in self:
            res.add(advisor.nationality)
        
        return sorted(res, key=lambda nationality: nationality.name.lower() if nationality.name else "")

    @api.multi
    def all_programs(self):
        res = set()
        for advisor in self:
            res.update(advisor.programs)

        return sorted(res, key=lambda program: program.name.lower() if program.name else "")


class GhuLang(models.Model):
    _name = 'ghu.lang'
    _rec_name = 'name'
    _description = "Language"

    name = fields.Char('Name', size=128)