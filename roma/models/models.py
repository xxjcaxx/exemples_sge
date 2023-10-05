# -*- coding: utf-8 -*-

from odoo import models, fields, api


class player(models.Model):
     _name = 'roma.player'
     _description = 'Players of Roma Aeterna Game'

     name = fields.Char()


class city(models.Model):
    _name = 'roma.city'
    _description = 'Cities'

    name = fields.Char()
    level = fields.Selection([('1','Villa'),('2','Oppidum'),('3','Urbs')])
    player = fields.Many2one('roma.player')
    forum_level = fields.Integer()
    # Desbloca la capacitat de tindre magisters, consul o dictador
    thermae_level = fields.Integer()
    theater_level = fields.Integer()
    circus_level = fields.Integer()
    temple_level = fields.Integer()
    # Els deus ajuden a la lealtat i en la resta de coses

    health = fields.Float()
    loyalty = fields.Float()
    gods = fields.Integer()

    metal = fields.Float()
    gold = fields.Float()
    food = fields.Float()

    buildings = fields.One2many('roma.building','city')
    units = fields.One2many('roma.unit','city')

class citicen(models.Model):
    _name = 'roma.citicen'
    _description = 'Important Citicen'

    name = fields.Char()
    hierarchy = fields.Selection([('1','Equites'),('2','Patricius'),('3','Magister'),('4','Potestas'),('5','Consul'),('6','Dictator')])
    # Sols pot haver un cónsul o un Dictador. Sols hi ha dictador en situació de guerra. Sols hi ha un potestas, que tria als magister
    # A partir de magister pots tindre legios
    # A partir de potestas pots controlar el senat
    # A partir de consul pots tindre dictador i més d'una legio
    # Tindre dictador millora molt el rendiment en batalles però es perd en lealtat, salut i producció
    city = fields.Many2one('roma.city')

class building_type(models.Model):
    _name = 'roma.building_type'
    _description = 'Type of buildings'

    name = fields.Char()
    food_production = fields.Float()
    soldiers_production = fields.Float()
    gold_production = fields.Float()
    metal_production = fields.Float()

class building(models.Model):
    _name = 'roma.building'
    _description = 'Buildings of the cities'

    name = fields.Char()
    type = fields.Many2one('roma.building_type')
    city = fields.Many2one('roma.city')
    level = fields.Integer()


class unit(models.Model):
    _name = 'roma.unit'
    _description = 'Group of soldiers'

    name = fields.Char()
    city = fields.Many2one('roma.city')
    type = fields.Selection([('1','Saeculum'),('2','Cohortis'),('3','Legio')])
    #  1 Centuria 80 soldats
    # 2 Cohortis 6 centuries
    # 3 Legio 10 cohortes
    legionaries = fields.Integer()
    equites = fields.Integer()
    parent_unit = fields.Many2one('roma.unit')
    units = fields.One2many('roma.unit','parent_unit')
    training = fields.Float(default=1)


