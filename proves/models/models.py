# -*- coding: utf-8 -*-

from odoo import models, fields, api


class proves(models.Model):
    _name = 'proves.proves'
    _description = 'proves.proves'

    name = fields.Char()
    date_start = fields.Datetime()
    date_stop = fields.Datetime()
    sales = fields.Many2many('sale.order')


