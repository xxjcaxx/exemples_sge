# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class student(models.Model):
     _name = 'school.student'
     _description = 'The Students'

     name = fields.Char()
     birth_date = fields.Date()
     photo = fields.Image(max_width=200, max_height=200)
     topics = fields.Many2many('school.topic')
     passed_topics = fields.Many2many(comodel_name='school.topic',
                                      relation='passed_topics_students',
                                      column1='student_id',
                                      column2='topic_id')
     qualifications = fields.One2many('school.qualification', 'student')

class topic(models.Model):
    _name = 'school.topic'
    _description = 'The Topics'

    name = fields.Char()
    course = fields.Selection([('1','First'),('2','Second')])
    teacher = fields.Many2one('school.teacher')
    teacher_phone = fields.Char(related='teacher.phone')
    students = fields.Many2many('school.student')
    passed_students = fields.Many2many(comodel_name='school.student',
                                      relation='passed_topics_students',
                                      column1='topic_id',
                                      column2='student_id')
    qualifications = fields.One2many('school.qualification','topic')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Custom Warning Message'),
    ]
class teacher(models.Model):
    _name = 'school.teacher'
    _description = 'The Teachers'

    name = fields.Char()
    phone = fields.Char()
    topics = fields.One2many('school.topic','teacher')

class qualification(models.Model):
    _name = 'school.qualification'
    _description = 'Student Qualifications'

    student = fields.Many2one('school.student')
    topic = fields.Many2one('school.topic')
    qualification = fields.Float()
    passes = fields.Boolean(compute='_get_passes')

    def _get_date(self):
        return fields.datetime.now()

    date = fields.Datetime(default = _get_date)

    @api.depends('qualification')
    def _get_passes(self):
        for q in self:
            print(q,self)
            if q.qualification >= 5:
                q.passes = True
            else:
                q.passes = False

    @api.constrains('qualification')
    def _check_qualification(self):
        for q in self:
            if q.qualification > 10:
                raise ValidationError("The qualification is too high: %s" % q.qualification)
            if q.qualification < 0:
                raise ValidationError("The qualification is too low: %s" % q.qualification)

