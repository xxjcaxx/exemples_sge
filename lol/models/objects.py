# -*- coding: utf-8 -*-

from odoo import models, fields, api

class object(models.Model):
    _name = 'lol.object'
    _description = 'Objects'

    name = fields.Char()
    type = fields.Many2one('lol.object_type', ondelete='restrict')
    character = fields.Many2one('lol.character', ondelete='cascade')
    level = fields.Integer()
    rust = fields.Float()
    characters = fields.Many2many('lol.character')

class object_type(models.Model):
    _name = 'lol.object_type'
    _description = 'Object types'

    name = fields.Char()
    type = fields.Selection([
        ('armor','Armor'),
        ('weapon','Weapon'),
        ('spell','Spell') ])
    character_type = fields.Many2one('lol.character_type')

