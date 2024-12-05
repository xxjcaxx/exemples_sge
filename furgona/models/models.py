# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class furgona(models.Model):
     _name = 'furgona.furgona'
     _description = 'furgona.furgona'

     name = fields.Char()
     capacity = fields.Float()
     plate = fields.Char()
     photo = fields.Image(max_width=200)
     historic_paquets = fields.Many2many('furgona.paquet',compute='_get_historic_paquets')

     def _get_historic_paquets(self):
          print(self)
          for f in self:

               f.historic_paquets = (self.env['furgona.travel']
                                     .search([('furgona', '=', f.id)])
                                     .mapped(lambda t: t.paquets).ids)



class paquet(models.Model):
     _name = 'furgona.paquet'
     _description = 'furgona.paquet'

     name = fields.Char(string="Identificator")
     volume = fields.Float()
     viatge_id = fields.Many2one('furgona.travel')

class travel(models.Model):
     _name = 'furgona.travel'
     _description = 'furgona.travel'

     name = fields.Char(string="Identificator")
     driver = fields.Many2one('res.partner')
     furgona = fields.Many2one('furgona.furgona')
     m3 = fields.Float(compute='_get_m3')
     paquets = fields.One2many('furgona.paquet','viatge_id')

     @api.depends('paquets')
     def _get_m3(self):
          for t in self:
               t.m3 = sum(t.paquets.mapped(lambda p: p.volume))

     @api.constrains('paquets','furgona')
     def _check_capacidad(self):
          for t in self:
               if t.m3 > t.furgona.capacity:
                    raise ValidationError("Your record is too old: %s" % t.m3)