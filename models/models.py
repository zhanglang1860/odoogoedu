# -*- coding: utf-8 -*-
import random

from odoo.exceptions import UserError, ValidationError
from datetime import timedelta
from odoo import models, fields, api, exceptions, _

class Course(models.Model):
    _name = 'odoogoedu.course'
    _description = "课程记录"

    name = fields.Char(string="课程名", required=True)
    description = fields.Text(string="课程描述")
    responsible_id = fields.Many2one('res.users',
        ondelete='set null', string="负责人", index=True)
    session_ids = fields.One2many(
    'odoogoedu.session', 'course_id', string="课时")

    _sql_constraints = [
        ('name_description_check',
         'CHECK(name != description)',
         "课程名与课程描述不能相同"),

        ('name_unique',
         'UNIQUE(name)',
         "课程名不能重复"),

    ]


    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', u"%{}的副本".format(self.name))])
        if not copied_count:
            new_name = u"{}的副本".format(self.name)
        else:
            new_name = u"{} ({})的副本".format(self.name, copied_count)

        default['name'] = new_name
        return super(Course, self).copy(default)

class Session(models.Model):
    _name = 'odoogoedu.session'
    _description = "课时"

    name = fields.Char(required=True)
    start_date = fields.Date(default=fields.Date.today)
    duration = fields.Float(digits=(6, 2), help="时长（天）")
    seats = fields.Integer(string="座位数")
    instructor_id = fields.Many2one('res.partner', string="Instructor",
                                    domain=['|', ('instructor', '=', True), ('category_id.name', 'ilike', "Teacher")])
    course_id = fields.Many2one('odoogoedu.course',
        ondelete='cascade', string="课程", required=True)
    attendee_ids = fields.Many2many('res.partner', string="学生")
    taken_seats = fields.Float(string="Taken seats", compute='_taken_seats')

    active = fields.Boolean(default=True)
    color = fields.Integer()

    def get_user(self):
        print('get_user')
        print(self)
        print(self.env)
        print(self.env.cr)
        print(self.env.uid)
        print(self.env.context )
        print(self.env.ref)
        print(self.env['res.users'])

        return self.env.uid
    user_id = fields.Many2one('res.users', default=get_user)

    @api.constrains('instructor_id', 'attendee_ids')
    def _check_instructor_not_in_attendees(self):
        print("_check_instructor_not_in_attendees")
        for r in self:
            if r.instructor_id and r.instructor_id in r.attendee_ids:
                raise ValidationError(_("A session's instructor can't be an attendee"))

    @api.onchange('seats', 'attendee_ids')
    def _verify_valid_seats(self):
        print("_verify_valid_seats")
        print(self)
        self.ensure_one()

        self.seats = str(random.randint(1, 1e6))
        self.test_name = str(random.randint(1, 1e6))
        #self.duration = str(random.randint(1, 1e6))
        if self.seats < 0:
            #raise UserError('不生效')
            return {
                'warning': {
                    'title': _("Incorrect 'seats' value"),
                    'message': _("The number of available seats may not be negative"),
                },
            }
        if self.seats < len(self.attendee_ids):
            return {
                'warning': {
                    'title': _("Too many attendees"),
                    'message': _("Increase seats or remove excess attendees"),
                },
            }
    @api.depends('seats', 'attendee_ids')
    def _taken_seats(self):
        for r in self:
            if not r.seats:
                r.taken_seats = 0.0
            else:
                r.taken_seats = 100.0 * len(r.attendee_ids) / r.seats

    test_name = fields.Char(compute='_compute_name')

    @api.depends('seats')
    def _compute_name(self):
        print('_compute_name')

        print(self) #odoogoedu.session(1, 2)
       # print(self.test_name)  #odoogoedu.session(1, 2).test_name  #ValueError: Expected singleton: odoogoedu.session(1, 2)
        for record in self:
            print(record) #odoogoedu.session(1, )
            print(record.test_name)
            record.test_name = str(random.randint(1, 1e6))
            #record.duration = str(random.randint(1, 1e6))
            print(record.test_name)
        #raise UserError('不生效')
    end_date = fields.Date(string="End Date", store=True,
        compute='_get_end_date', inverse='_set_end_date')
    end_date_display = fields.Date(string="End Date display",
        compute='_get_end_date',store=True)


    @api.depends('start_date', 'duration')
    def _get_end_date(self):
        for r in self:
            if not (r.start_date and r.duration):
                r.end_date = r.start_date
                continue
            # Add duration to start_date, but: Monday + 5 days = Saturday, so
            # subtract one second to get on Friday instead
            start = r.start_date
            duration = timedelta(days=r.duration, seconds=-1)
            r.end_date = start + duration
            r.end_date_display = r.end_date + timedelta(days=1)

    def _set_end_date(self):
        for r in self:
            if not (r.start_date and r.end_date):
                continue
            # Compute the difference between dates, but: Friday - Monday = 4 days,
            # so add one day to get 5 days instead
            start_date = r.start_date
            end_date = r.end_date
            r.duration = (end_date - start_date).days+1
            r.end_date_display = r.end_date + timedelta(days=1)
    attendees_count = fields.Integer(
        string="Attendees count", compute='_get_attendees_count', store=True)

    @api.depends('attendee_ids')
    def _get_attendees_count(self):
        for r in self:
            r.attendees_count = len(r.attendee_ids)
class CourseExtension(models.Model):
    _inherit = 'odoogoedu.course'
    note = fields.Char(default="Extended")
    def call(self):
        return self.check("model Course")
    def check(self, s):
        return "This is {} record {}".format(s, self.name)


class Course2(models.Model):
    _name = 'odoogoedu.course2'
    _inherit = 'odoogoedu.course'
    def call(self):
        return self.check("model Course2")


class Child0(models.Model):
    _name = 'delegation.child0'
    field_0 = fields.Integer()


class Child1(models.Model):
    _name = 'delegation.child1'
    field_1 = fields.Integer()


class Delegating(models.Model):
    _name = 'delegation.parent'
    _inherits = {
      'delegation.child0': 'child0_id',
      'delegation.child1': 'child1_id',
    }
    child0_id = fields.Many2one('delegation.child0', required=True, ondelete='cascade')
    child1_id = fields.Many2one('delegation.child1', required=True, ondelete='cascade')



