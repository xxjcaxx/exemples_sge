# -*- coding: utf-8 -*-

from odoo import models, fields, api
import math

class player(models.Model):
     _name = 'roma.player'
     _description = 'Players of Roma Aeterna Game'

     name = fields.Char(required=True)
     citicens = fields.One2many('roma.citicen','player')

class city(models.Model):
    _name = 'roma.city'
    _description = 'Cities'

    name = fields.Char(required=True)
    level = fields.Selection([('1','Villa'),('2','Oppidum'),('3','Urbs')], required=True, default='1')
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

    metal = fields.Float(default=1000)
    gold = fields.Float(default=100)
    food = fields.Float(default=10000)

    buildings = fields.One2many('roma.building','city')
    units = fields.One2many('roma.unit','city')

class citicen(models.Model):
    _name = 'roma.citicen'
    _description = 'Important Citicen'

    name = fields.Char(required=True)
    player = fields.Many2one('roma.player', required=True)
    hierarchy = fields.Selection([('1','Equites'),('2','Patricius'),('3','Magister'),('4','Potestas'),('5','Consul'),('6','Dictator')],required=True)
    # Sols pot haver un cónsul o un Dictador. Sols hi ha dictador en situació de guerra. Sols hi ha un potestas, que tria als magister
    # A partir de magister pots tindre legios
    # A partir de potestas pots controlar el senat
    # A partir de consul pots tindre dictador i més d'una legio
    # Tindre dictador millora molt el rendiment en batalles però es perd en lealtat, salut i producció
    city = fields.Many2one('roma.city',required=True)

class building_type(models.Model):
    _name = 'roma.building_type'
    _description = 'Type of buildings'

    name = fields.Char()
    food_production = fields.Float()
    soldiers_production = fields.Float()
    gold_production = fields.Float()
    metal_production = fields.Float()
    icon = fields.Image(max_width=200, max_height=200)

class building(models.Model):
    _name = 'roma.building'
    _description = 'Buildings of the cities'

    name = fields.Char(compute='_get_name')
    type = fields.Many2one('roma.building_type',required=True)
    city = fields.Many2one('roma.city',required=True)
    level = fields.Integer(default=1)
    food_production = fields.Float(compute='_get_productions')
    soldiers_production = fields.Float(compute='_get_productions')
    gold_production = fields.Float(compute='_get_productions')
    metal_production = fields.Float(compute='_get_productions')

    @api.depends('type','level')
    def _get_productions(self):
        for b in self:
            b.food_production = b.type.food_production+ b.type.food_production * math.log(b.level)
            b.soldiers_production =  b.type.soldiers_production+b.type.soldiers_production * math.log(b.level)
            b.gold_production =  b.type.gold_production+b.type.gold_production * math.log(b.level)
            b.metal_production = b.type.metal_production+b.type.metal_production * math.log(b.level)

    @api.depends('type','city')
    def _get_name(self):
        for b in self:
            b.name = 'undefined'
            if b.type and b.city:
                b.name = b.type.name +" "+ b.city.name +" "+ str(b.id)

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
    total_soldiers = fields.Integer(compute='_get_total_soldiers')

    @api.depends('legionaries','equites','units')
    def _get_total_soldiers(self):
        print(self)
        for unit in self:
            total = unit.legionaries + unit.equites
            for subunit in unit.units:
                total = total + subunit.total_soldiers
        unit.total_soldiers = total

