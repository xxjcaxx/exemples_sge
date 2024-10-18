# -*- coding: utf-8 -*-

from odoo import models, fields, api


class character(models.Model):
     _name = 'lol.character'
     _description = 'Character'

     name = fields.Char()
     type = fields.Many2one('lol.character_type',  ondelete='restrict')
     image = fields.Image(related='type.image', store=False)
     player = fields.Many2one('lol.player',  ondelete='cascade')
     armor = fields.Many2one('lol.object', domain="[('type.type','=','armor')]")
     level = fields.Integer()
     objects = fields.Many2many('lol.object', domain="[('type.character_type','=',type)]")
     objects_qty = fields.Integer(compute='_get_objects_qty')
     inventory = fields.Many2many(comodel_name='lol.object', # El model en el que es relaciona
                            relation='inventory_objects_characters', # (opcional) el nom del la taula en mig
                            column1='character_id', # (opcional) el nom en la taula en mig de la columna d'aquest model
                            column2='object_id')  # (opcional) el nom de la columna de l'altre model.

     @api.depends('objects')
     def  _get_objects_qty(self):
         for character in self:
           #  print(self, character, character.objects)
             character.objects_qty = len(character.objects)


class character_type(models.Model):
    _name = 'lol.character_type'
    _description = 'Character types'

    name = fields.Char()
    image = fields.Image(max_width=200, max_height=200)


