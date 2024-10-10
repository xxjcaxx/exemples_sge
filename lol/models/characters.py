# -*- coding: utf-8 -*-

from odoo import models, fields, api


class character(models.Model):
     _name = 'lol.character'
     _description = 'Character'

     name = fields.Char()