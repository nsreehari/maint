# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from openerp import models, fields, api, exceptions
from datetime import datetime


# Some Selection List.
yesnosel = [('Yes', 'Yes'), ('No', 'No')]
gendersel = [('male','Male'), ('female','Female')]


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
		mystring = self.country
		if (str(mystring).lower().strip() != 'india') == True:
			self.overseas = "True"
		else:
			self.overseas = "False"
	
        # Birth year validation.
        @api.constrains('birthyear')
        def _check_birthyear(self):
	    if self.birthyear < 1900:
                raise exceptions.ValidationError("BirthYear cannot be less than 1900")		
	    todayyear = datetime.now().year
	    if self.birthyear > todayyear:
		raise exceptions.ValidationError("BirthYear cannot be greather than %d" % todayyear )		


	@api.depends('birthyear')
	def _compute_age(self):
		self.age = datetime.now().year - self.birthyear
	
	
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
		('abhyasi_id_uniq', 'unique (abhyasi_id)', "abhyasi_id already exists !")
	]



# Class for Non Abhyasi Information. 
class visitor_nonabhyasi(models.Model):
	_name = 'visitor.nonabhyasi'
	_description = 'Children or Other Guests' 
	
        # Birth year validation.
        @api.constrains('birthyear')
        def _check_birthyear(self):
	    if self.birthyear < 1900:
                raise exceptions.ValidationError("BirthYear cannot be less than 1900")		
	    todayyear = datetime.now().year
	    if self.birthyear > todayyear:
		raise exceptions.ValidationError("BirthYear cannot be greather than %d" % todayyear )		


	@api.depends('birthyear')
	def _compute_age(self):
		self.age = datetime.now().year - self.birthyear

	full_name = fields.Char(string='Full Name', required=True)
	birthyear =  fields.Integer(string='Birth Year', required=True)
	gender =  fields.Selection(gendersel, string='Gender', required=True)
	child =  fields.Char(compute="_compute_child", string = 'Child?')
	age = fields.Char(compute="_compute_age", string = 'Age')
	

	@api.depends('birthyear','child')
	def _compute_child(self):
		todayyear = datetime.now().year
		if (todayyear - self.birthyear <= 15) == True:
			self.child = "True"
		else:
			self.child = "False"


# Visitor Registration Class.
class visitor_registration(models.Model):
	_name = 'visitor.registration'
	_description = 'Visitor Registrations'

        # Update status based on the values of arrival, check-in, check-out, cancellation, etc.
        @api.depends('arrival_date', 'checkin_date', 'checkout_date', 'cancellation_date')
        def _compute_state(self):
            for r in self:
                if isinstance(r.id, models.NewId):
                    r.status = 'new'
                    return

                if r.cancellation_date:
                    r.status = 'cancelled'
                elif r.checkout_date:
                    r.status = 'checkedout'
                elif r.checkin_date:
                    r.status = 'checkedin'
                else:
                    r.status = 'registered'

        # Date Validation.
        @api.constrains('arrival_date','departure_date', 'checkin_date', 'checkout_date')
        def _check_dates(self):
            for r in self:
	        if r.arrival_date > r.departure_date:
	    	    raise ValidationError("Departure Date should be later than Arrival Date")
                if r.checkin_date is not None and r.checkin_date > r.departure_date:
	    	    raise ValidationError("Departure Date should be later than Checkin Date")


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
        def button_checkin(self):
            view_id = self.env.ref('maint.visitor_registration_formcheckin').id
            form_name = 'Check-In Form'
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
        def button_checkout(self):
            view_id = self.env.ref('maint.visitor_registration_formcheckout').id
            form_name = 'Check-Out Form'
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
        def button_cancel(self):
            view_id = self.env.ref('maint.visitor_registration_formcancel').id
            form_name = 'Cancellation Form'
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
        def button_uncheckin(self):

            self.checkin_date = None
            self.checkin_time = None
            self.roomid = None


        @api.multi
        def button_uncheckout(self):

            self.checkout_date = None
            self.checkout_time = None


	status = fields.Selection([
                        ('new', 'Draft'),
			('registered', 'Registered'),
			('checkedin', 'Checked in'),
			('checkedout', 'Checked out'),
			('cancelled', 'Cancelled'),
			], compute='_compute_state', store=True)

	batchid = fields.Char(string='Batch Id', default=lambda self: self._compute_batchid(), required=True)
	record_entry =  fields.Char(string='Record Entry Date', default=datetime.now().strftime("%Y-%m-%d"), required=True, readonly=True)
	arrival_date =  fields.Date(string='Arrival Date', required=True)
        arrival_time = fields.Float(string='Arrival Time', required=True, default=-1)
	departure_date =  fields.Date(string='Departure Date',required=True,default=None)
        departure_time = fields.Float(string='Departure Time', required=True, default=-1)
	abhyasi_visitor = fields.Many2many(comodel_name='visitor.abhyasi',string='Visiting Abhyasi Details') 
	abhyasi_non_visitor = fields.Many2many(comodel_name='visitor.nonabhyasi',string='Children and Other Guests') 

	checkin_date =  fields.Date(string='Checkin Date', default=None)
        checkin_time = fields.Float(string='Checkin Time', default=None )
	roomid =  fields.Many2one(comodel_name='visitor.rooms', default=None)
	checkout_date =  fields.Date(string='Checkout Date',default=None)
        checkout_time = fields.Float(string='Checkout Time', default=None)
	cancellation_date =  fields.Date('Cancellation Date', default=None)
	
	@api.model
	def _compute_batchid(self):
		return str(datetime.now().strftime("%Y%m%d%H%M%S%f")) 
	
	_sql_constraints = [('batchid_uniq', 'unique (batchid)', "ID already exists !")]
	



# Visitor Rooms description.
class visitor_rooms(models.Model):
	_name = 'visitor.rooms'
	_description = 'Visitor Rooms Description'
	name = fields.Char(string='Room Id', required=True)
	roomtype =  fields.Many2one(comodel_name='visitor.room.type',required=True )
	ac =  fields.Selection(yesnosel,string='Air-Conditioned?', required=True)
	tag_ids = fields.Many2many(comodel_name='visitor.room.tags', string ='Tags', copy=False)
	is_active =  fields.Selection(yesnosel, string='Room in Operation?', required=True)
	notes =  fields.Text('Room Description')
	_sql_constraints = [
		('roomid_uniq', 'unique (name)', "Room ID already exists !")
	]
