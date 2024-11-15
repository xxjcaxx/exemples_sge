# -*- coding: utf-8 -*-

from odoo import models, fields, api


class game(models.Model):
    _name = 'lol.game'
    _description = 'games'

    name = fields.Char()
    init_date = fields.Datetime()
    end_date = fields.Datetime()
    duration = fields.Integer()
