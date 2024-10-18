# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
     _name = 'lol.player'
     _description = 'Players'

     name = fields.Char()
     characters = fields.One2many('lol.character','player')