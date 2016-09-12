# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from openerp import models, fields, api, exceptions
from datetime import datetime, timedelta
from copy import copy

import logging
_logger = logging.getLogger(__name__)

# Some Selection List.
yesnosel = [('Yes', 'Yes'), ('No', 'No')]
gendersel = [('male','Male'), ('female','Female')]
statussel = [
        ('new', 'New'),
        ('registered', 'Registered'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('checkedin', 'Checked in'),
        ('checkedout', 'Checked out'),
]

class ashram(models.Model):
    _name = 'visitor.ashram'

    name = fields.Char(string='Ashram', required=True)

    _sql_constraints = [
        ('ashram_uniq', 'unique (name)', "Ashram already exists !")
    ]


# Class for the visitor room tag. Eg: AC, Accessibility Etc..
class visitor_room_tags(models.Model):
        _name = 'visitor.room.tags'
        _description = 'Room Attributes like A/C, Accessibility, etc.'
        name = fields.Char('Name', required=True)
        color = fields.Integer('Color Index')
        _sql_constraints = [
               ('name_uniq', 'unique (name)', "Tag name already exists !")
        ]


# Class for the visitor room type Eg: Dorm, Room Etc.
class visitor_room_type(models.Model):
        _name = 'visitor.room.type'
        _description = 'Room Type'
        name = fields.Char('Room Type', required=True)
        _sql_constraints = [
                ('type_uniq', 'unique (name)', "Room Type already exists !")
        ]


# Class for visitor abhyasi information. 
class visitor_abhyasi(models.Model):
        _name = 'visitor.abhyasi'
        _description = 'Abhyasi Detail'
        
        @api.depends('country','overseas')
        def _compute_overseas(self):
            for r in self:
                mystring = r.country
                if (str(mystring).lower().strip() != 'india') == True:
                        r.overseas = "True"
                else:
                        r.overseas = "False"
        
        # Birth year validation.
        @api.constrains('birthyear')
        def _check_birthyear(self):
            for r in self:
                if r.birthyear < 1900:
                    raise exceptions.ValidationError("BirthYear cannot be less than 1900")                
                todayyear = datetime.now().year
                if r.birthyear > todayyear:
                    raise exceptions.ValidationError("BirthYear cannot be greather than %d" % todayyear )                


        @api.depends('birthyear')
        def _compute_age(self):
            for r in self:
                r.age = datetime.now().year - r.birthyear
        

        @api.depends('abhyasi_id', 'center', 'full_name', 'contactnumber')
        def _compute_name(self):
            for r in self:
                r.name = "%s %s %s %s" % (r.abhyasi_id , r.center, r.full_name, r.contactnumber )
        
        name = fields.Char(compute="_compute_name", store=True)
        abhyasi_id =  fields.Char(string='Abhyasi ID', required=True)
        full_name =  fields.Char(string='Full Name', required=True)
        preceptor =  fields.Selection(yesnosel, string='Is Preceptor?', required=True)
        center =  fields.Char('Center', required=True)
        country =  fields.Char('Country', required=True,default='INDIA')
        overseas =  fields.Char(compute="_compute_overseas", string = 'Overseas?')
        contactnumber =  fields.Char('Contact Number')
        birthyear =  fields.Integer(string='Birth Year', required=True)
        gender =  fields.Selection(gendersel, string='Gender', required=True)
        age = fields.Char(compute="_compute_age", string = 'Age')

        _sql_constraints = [
                ('abhyasi_id_uniq', 'unique (name)', "abhyasi_id already exists !")
        ]



# Class for Non Abhyasi Information. 
class visitor_nonabhyasi(models.Model):
        _name = 'visitor.nonabhyasi'
        _description = 'Children or Other Guests' 
        
        # Birth year validation.
        @api.constrains('birthyear')
        def _check_birthyear(self):
            for r in self:
                    if r.birthyear < 1900:
                        raise exceptions.ValidationError("BirthYear cannot be less than 1900")                
                    todayyear = datetime.now().year
                    if r.birthyear > todayyear:
                        raise exceptions.ValidationError("BirthYear cannot be greather than %d" % todayyear )                


        @api.depends('birthyear')
        def _compute_age(self):
            for r in self:
                r.age = datetime.now().year - r.birthyear

        full_name = fields.Char(string='Full Name', required=True)
        birthyear =  fields.Integer(string='Birth Year', required=True)
        gender =  fields.Selection(gendersel, string='Gender', required=True)
        child =  fields.Char(compute="_compute_child", string = 'Child?')
        age = fields.Char(compute="_compute_age", string = 'Age')
        

        @api.depends('birthyear','child')
        def _compute_child(self):
            for r in self:
                todayyear = datetime.now().year
                if (todayyear - r.birthyear <= 15) == True:
                        r.child = "True"
                else:
                        r.child = "False"


# Date-wise Guest Occupancy list -- auto-generated DB
class visitor_datewise(models.Model):
    _name = 'visitor.datewise'
    _description = 'Visitor Date-wise Occupancy List'

    _order = "date asc, state "






    @api.one
    @api.depends('date')
    def _compute_display_name(self):
        self.display_name = "%s" % self.date

    @api.one
    @api.depends('guest_count', 'date', 'stay', 'registrationid')
    def _compute_kitchen(self):
        r = self

        xdate = fields.Datetime.from_string(r.date)

        if r.stay == "arrival":
            arrtime = r.registrationid.checkin_time or r.registrationid.arrival_time
            if arrtime < 10:
                r.breakfast = r.guest_count
            if arrtime < 14:
                r.lunch = r.guest_count
            if arrtime < 21:
                r.dinner = r.guest_count

        elif r.stay == "departure":
            deptime = r.registrationid.checkout_time or r.registrationid.departure_time
            if deptime >= 21:
                r.dinner = r.guest_count
            if deptime >= 14:
                r.lunch = r.guest_count
            if deptime > 10:
                r.breakfast = r.guest_count

        elif r.stay == "fullday":
            r.breakfast = r.guest_count
            r.lunch = r.guest_count
            r.dinner = r.guest_count

        else:
            #control should not come here
            pass




    display_name = fields.Char(compute='_compute_display_name')

    date = fields.Date(string='Date', readonly=True)
    stay = fields.Selection([('arrival','Arrival'), ('fullday','Full Day'), ('departure','Departure')], readonly=True)


    breakfast = fields.Integer(string='Breakfast', store=True, compute="_compute_kitchen", multi="kitchen"  )
    lunch = fields.Integer(string='Lunch', store=True, compute="_compute_kitchen" , multi="kitchen"   )
    dinner = fields.Integer(string='Dinner', store=True, compute="_compute_kitchen" , multi="kitchen"   )

    state = fields.Selection(statussel, related='registrationid.state', store=True )
    registrationid = fields.Many2one(comodel_name='visitor.registration', required=True, ondelete='cascade', readonly=True)

    abhyasi_count = fields.Integer(related='registrationid.abhyasi_count', readonly=True)
    guest_count = fields.Integer(related='registrationid.guest_count', readonly=True)
    children_count = fields.Integer(related='registrationid.children_count', readonly=True)
    abhyasis = fields.Char(related='registrationid.abhyasis', readonly=True)
    children = fields.Char(related='registrationid.children', readonly=True)
    ashram = fields.Char(related='registrationid.ashram.name', store=True, readonly=True)
    roomid = fields.Char(related='registrationid.roomid.name', store=True, readonly=True)



# Visitor Registration Class.
class visitor_registration(models.Model):
        _name = 'visitor.registration'
        _description = 'Visitor Registration'


        # compute the count of abhyasis and non-abhyasis
        @api.depends('visiting_abhyasis', 'visiting_children')
        def _compute_counts(self):
            for r in self:
                r.abhyasi_count = len(r.visiting_abhyasis)
                r.children_count = len(r.visiting_children)
                r.guest_count = r.abhyasi_count + r.children_count

                r.abhyasis = ','.join(r.visiting_abhyasis.mapped('full_name'))
                r.children = ','.join(r.visiting_children.mapped('full_name'))


        @api.depends('batchid', 'record_entry')
        def _compute_name(self):
            for r in self:
                r.name = "%s %s" % (r.batchid, r.record_entry )

        @api.depends('arrival_date', 'departure_date', 'checkout_date', 'checkin_date', 'arrival_time', 'departure_time', 'checkout_time', 'checkin_time')
        def _compute_dates(self):
            for r in self:
                r.todate = r.departure_date
                r.fromdate = r.arrival_date
                r.fromtime = r.arrival_time
                r.totime = r.departure_time
                if r.checkout_date:
                    r.todate = r.checkout_date
                    totime = r.checkout_time
                if r.checkin_date:
                    r.fromdate = r.checkin_date
                    fromtime = r.checkin_time


                r.fromdatetime = fields.Datetime.to_string( fields.Datetime.from_string(r.fromdate) + timedelta(hours=r.fromtime) )
                r.todatetime = fields.Datetime.to_string( fields.Datetime.from_string(r.todate) + timedelta(hours=r.totime) )




        # Update state based on the values of arrival, check-in, check-out, cancellation, etc.
        @api.depends('checkin_date', 'checkout_date', 'cancellation_date', 'arrival_date', 'departure_date')
        def _compute_state(self):
            for r in self:

                if r.cancellation_date:
                    r.state = 'cancelled'
                elif r.checkout_date:
                    r.state = 'checkedout'
                elif r.checkin_date:
                    r.state = 'checkedin'
                elif isinstance(r.id, models.NewId):
                    r.state = 'new'
                else:
                    r.state = 'registered'

                r.active = True


    
        @api.model
        def create(self, vals):


            vals['batchid'] = self.env['ir.sequence'].get('visitor.batch')

            res = super(visitor_registration, self).create(vals)

            for r in res:
              fromdate = fields.Datetime.from_string(r.fromdate)
              todate = fields.Datetime.from_string(r.todate)

              xdate = fromdate
              while xdate <= todate:
                if xdate == fromdate:
                    stay = 'arrival'
                elif xdate == todate:
                    stay = 'departure'
                else:
                    stay = 'fullday'
                r.datewise += r.datewise.new({'date':xdate, 'stay':stay})
                xdate += timedelta(days=1)

            return res
 
        @api.multi
        def write(self, vals):
            res = super(visitor_registration, self).write(vals)

            for r in self:

                fromdate = fields.Datetime.from_string(r.fromdate)
                todate = fields.Datetime.from_string(r.todate)

                r.datewise.unlink()

                # to_add
                xdate = fromdate
                while xdate <= todate:
                    if xdate == fromdate:
                        stay = 'arrival'
                    elif xdate == todate:
                        stay = 'departure'
                    else:
                        stay = 'fullday'

                    r.datewise.create({'date':xdate, 'stay':stay, 'registrationid':r.id})
                    xdate += timedelta(days=1)

            return res

                


        @api.constrains('abhyasi_count')
        def _check_abhyasi_count(self):
            for r in self:
                if r.abhyasi_count < 1:
                    raise exceptions.ValidationError("Please add atleast one visiting abhyasi")

        # Date Validation.
        @api.constrains('arrival_date','departure_date', 'checkin_date', 'checkout_date')
        def _check_dates(self):
            for r in self:
                if r.arrival_date > r.departure_date:
                    raise exceptions.ValidationError("Departure Date should be later than Arrival Date")
                if r.checkin_date is not None and r.checkin_date > r.departure_date:
                    raise exceptions.ValidationError("Departure Date should be later than Checkin Date")


        # Time validation.
        @api.constrains('arrival_time')
        def _check_time(self):
            for r in self:
                if r.arrival_time >=24 or r.arrival_time < 0 :
                    raise exceptions.ValidationError("Please enter TIME in the range of 00:00 to 23:59")

        # Time validation.
        @api.constrains('checkin_time')
        def _checkin_time(self):
            for r in self:
                if r.checkin_time >=24 or r.checkin_time < 0 :
                    raise exceptions.ValidationError("Please enter TIME in the range of 00:00 to 23:59")

        # Time validation.
        @api.constrains('checkout_time')
        def _checkout_time(self):
            for r in self:
                if r.checkout_time >=24 or r.checkout_time < 0 :
                    raise exceptions.ValidationError("Please enter TIME in the range of 00:00 to 23:59")

        # Time validation.
        @api.constrains('departure_time')
        def _departure_time(self):
            for r in self:
                if r.departure_time >=24 or r.departure_time < 0 :
                    raise exceptions.ValidationError("Please enter TIME in the range of 00:00 to 23:59")


        @api.multi
        def retform(self, form_name, view_id):
            return {
                'name':form_name,
                'view_type':'form',
                'view_mode':'form',
                'res_model':'visitor.registration',
                'view_id':view_id,
                'type':'ir.actions.act_window',
                'target':'new',
                'res_id':self.id,
                #'context':context,
            }

        @api.multi
        def button_checkin(self):
            view_id = self.env.ref('maint.visitor_registration_formcheckin').id
            form_name = 'Check-In Form'
            return self.retform(form_name, view_id)


        @api.multi
        def button_checkout(self):
            view_id = self.env.ref('maint.visitor_registration_formcheckout').id
            form_name = 'Check-Out Form'
            return self.retform(form_name, view_id)

        @api.multi
        def button_cancel(self):
            view_id = self.env.ref('maint.visitor_registration_formcancel').id
            form_name = 'Cancellation Form'
            return self.retform(form_name, view_id)

        @api.multi
        def button_uncheckin(self):

            self.checkin_date = None
            self.checkin_time = None
            self.roomid = None


        @api.multi
        def button_uncheckout(self):

            self.checkout_date = None
            self.checkout_time = None

        @api.model
        def scheduler_manage_expiration(self):
            datetime_today = datetime.now()
            ACTIVEDAYS = 7
            EXPIREDAYS = 1

            for r in self.search([('active', '=', True)]):
                edate = fields.Datetime.from_string(r.todate) 

                if edate + timedelta(days=ACTIVEDAYS) < datetime_today:
                    r.active = False

                if edate + timedelta(days=EXPIREDAYS) < datetime_today:
                    if r.state in ['registered']:
                        r.state = "expired"
                    #if r.state in ['checkedin']:
                    #    r.checkout_date = r.departure_date
                    #    r.checkout_time = r.departure_time



        @api.model
        def run_scheduler(self):
            _logger.info('scheduler ran')
            self.scheduler_manage_expiration()
            return True



        active = fields.Boolean(string="Active", default=True)

        state = fields.Selection(statussel, compute='_compute_state', store=True)

        guest_count = fields.Integer(string='Guest Count', compute='_compute_counts', store=True, multi='_counts')
        abhyasi_count = fields.Integer(string='Abhyasi Count', compute='_compute_counts', store=True, multi='_counts')
        children_count = fields.Integer(string='Children in Group', compute='_compute_counts', store=True, multi='_counts')
        abhyasis = fields.Char(string='Abhyasis', compute='_compute_counts', store=True, multi='_counts')
        children = fields.Char(string='Children', compute='_compute_counts', store=True, multi='_counts')

        name = fields.Char(string='Registration Id', compute="_compute_name")
        batchid = fields.Char(string='Batch Id', readonly=True)
        phonenum = fields.Char(string='Phone Number', required=True)
        email = fields.Char(string='Email Id')
        record_entry =  fields.Char(string='Record Entry Date', default=datetime.now().strftime("%Y-%m-%d"), required=True, readonly=True)
        fromdate =  fields.Date(string='From Date', compute="_compute_dates", multi="_dates")
        todate =  fields.Date(string='To Date', compute="_compute_dates", multi="_dates")
        fromtime =  fields.Float(string='From Time', compute="_compute_dates", multi="_dates")
        totime =  fields.Float(string='To Time', compute="_compute_dates", multi="_dates")
        fromdatetime =  fields.Datetime(string='From DateTime', compute="_compute_dates", multi="_dates")
        todatetime =  fields.Datetime(string='To DateTime', compute="_compute_dates", multi="_dates")
        arrival_date =  fields.Date(string='Arrival Date', required=True)
        arrival_time = fields.Float(string='Arrival Time', required=True, default=7.5)
        departure_date =  fields.Date(string='Departure Date',required=True,default=None)
        departure_time = fields.Float(string='Departure Time', required=True, default=16)
        visiting_abhyasis = fields.Many2many(comodel_name='visitor.abhyasi',string='Visiting Abhyasi Details') 
        visiting_children = fields.Many2many(comodel_name='visitor.nonabhyasi',string='Children and Other Guests') 

        checkin_date =  fields.Date(string='Checkin Date', default=None)
        checkin_time = fields.Float(string='Checkin Time', default=None )
        roomid =  fields.Many2one(comodel_name='visitor.rooms', default=None)
        checkout_date =  fields.Date(string='Checkout Date',default=None)
        checkout_time = fields.Float(string='Checkout Time', default=None)
        cancellation_date =  fields.Date('Cancellation Date', default=None)
        datewise = fields.One2many('visitor.datewise', 'registrationid', string='Date-wise Line Items') 
        ashram =  fields.Many2one(comodel_name='visitor.ashram', required=True)
        
        _sql_constraints = [('batchid_uniq', 'unique (batchid)', "ID already exists !")]
        



# Visitor Rooms description.
class visitor_rooms(models.Model):
        _name = 'visitor.rooms'
        _description = 'Visitor Rooms Description'

        ashram =  fields.Many2one(comodel_name='visitor.ashram', required=True)
        name = fields.Char(string='Room Id', required=True)
        capacity = fields.Integer(string="Room Capacity", required=True)
        roomtype =  fields.Many2one(comodel_name='visitor.room.type',required=True )
        tag_ids = fields.Many2many(comodel_name='visitor.room.tags', string ='Tags', copy=False)
        datewise_ids = fields.One2many('visitor.datewise', 'roomid', string='Date-wise Line Items') 
        ynsel = [('Yes', 'Active'), ('No', 'Not Functioning')]
        is_active =  fields.Selection(ynsel, string='Room in Operation?', required=True, default="Yes")
        notes =  fields.Char(string='Additional Notes')
        _sql_constraints = [
                ('roomid_uniq', 'unique (name)', "Room ID already exists !")
        ]
