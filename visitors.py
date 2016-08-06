# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from openerp import models, fields, api
from datetime import datetime


#	Birth year validation.
@api.one
@api.constrains('arrival_date','departure_date')
def _check_dates(self):
	if self.arrival_date > self.departure_date:
		raise ValidationError("Please give the Arrival date first.")


#	Date Validation.
@api.one
@api.constrains('birthyear')
def _check_birthyear(self):
	if self.birthyear < 1900:
		raise ValidationError("BirthYear cannot be less than 1900")		
	todayyear = datetime.now().year
	if self.birthyear > todayyear:
		raise ValidationError("BirthYear cannot be greather than %d" % todayyear )		


#	Some Selection List.
yesnosel = [('Yes', 'Yes'), ('No', 'No')]
gendersel = [('male','Male'), ('female','Female')]
timesel = [('latenight','7PM-11PM'), ('evening','3PM-7PM'), ('afternoon', '11AM-3PM'),   ('morning', '6AM-10AM'),   ('early morning', '12AM-6AM') ]


#	Class for the visitor room tag. Eg: AC, Accessibility Etc..
class visitor_room_tags(models.Model):
	_name = 'visitor.room.tags'
	_description = 'Room Attributes like A/C, Accessibility, etc.'
	name = fields.Char('Name', required=True)
	color = fields.Integer('Color Index')
	_sql_constraints = [
			('name_uniq', 'unique (name)', "Tag name already exists !")
	]


#	Class for the visitor room type Eg: Dorm, Room Etc.
class visitor_room_type(models.Model):
	_name = 'visitor.room.type'
	_description = 'Room Type'
	name = fields.Char('Room Type', required=True)
	_sql_constraints = [
		('type_uniq', 'unique (name)', "Room Type already exists !")
	]


#	Class for visitor abhyasi information. 
class visitor_abhyasi(models.Model):
	_name = 'visitor.abhyasi'
	_inherit = 'mail.thread'
	_description = 'Abhyasi Detail'
	
	@api.depends('country','overseas')
	def _compute_overseas(self):
		mystring = self.country
		if (str(mystring).lower().strip() != 'india') == True:
			self.overseas = "True"
		else:
			self.overseas = "False"
	
	@api.one
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

	_constraints = [
		(_check_birthyear, "Invalid Birth Year", ['birthyear']),
	]


#	Class for Non Abhyasi Information. 
class visitor_nonabhyasi(models.Model):
	_name = 'visitor.nonabhyasi'
	_description = 'Children or People without Abhyasi ID' 
	
	@api.one
	@api.depends('birthyear')
	def _compute_age(self):
		self.age = datetime.now().year - self.birthyear

	full_name = fields.Char(string='Full Name', required=True)
	birthyear =  fields.Integer(string='Birth Year', required=True)
	gender =  fields.Selection(gendersel, string='Gender', required=True)
	child =  fields.Char(compute="_compute_child", string = 'Child?')
	age = fields.Char(compute="_compute_age", string = 'Age')
	
	_constraints = [
		(_check_birthyear, "Invalid Birth Year", ['birthyear']),
	]

	@api.depends('birthyear','child')
	def _compute_child(self):
		todayyear = datetime.now().year
		if (todayyear - self.birthyear <= 15) == True:
			self.child = "True"
		else:
			self.child = "False"


#	Visitor Registration Class.
class visitor_registration(models.Model):
	_name = 'visitor.registration'
	_description = 'Visitor Registrations'
	batchid = fields.Char(string='Batch Id', default=lambda self: self._compute_batchid(), required=True)
	record_entry =  fields.Char(string='Record Entry Date', default=datetime.now().strftime("%Y-%m-%d"), required=True, readonly=True)
	arrival_date =  fields.Date(string='Arrival Date', required=True, default=None)
	arrival_time =  fields.Selection(timesel, string='Arrival Time', required=True)
	departure_date =  fields.Date(string='Departure Date',required=True,default=None)
	departure_time =  fields.Selection(timesel, string='Departure Time', required=True)
	spot_registration = fields.Selection(yesnosel, string='Spot Registeration?', required=True)
	cancelled = fields.Selection(yesnosel, string='Cancelled?', default='No' )
	cancelation_date =  fields.Date('Cancelation Date')

	@api.model
	def _compute_batchid(self):
		return str(datetime.now().strftime("%Y%m%d%H%M%S%f")) 
	
	_sql_constraints = [('batchid_uniq', 'unique (batchid)', "ID already exists !")]
	
	_constraints = [
		(_check_dates, "Arrival date should be less than or equal to depaure date", ['arrival_date','departure_date']),
	]


#	Visitor Rooms description.
class visitor_rooms(models.Model):
	_name = 'visitor.rooms'
	_description = 'Visitor Rooms Description'
	roomid =  fields.Char(string='Room Id', required=True)
	roomtype =  fields.Many2one(comodel_name='visitor.room.type',required=True )
	ac =  fields.Selection(yesnosel,string='Air-Conditioned?', required=True)
	tag_ids = fields.Many2many(comodel_name='visitor.room.tags', string ='Tags', copy=False)
	is_active =  fields.Selection(yesnosel, string='Room in Operation?', required=True)
	notes =  fields.Text('Room Description')
	_sql_constraints = [
		('roomid_uniq', 'unique (roomid)', "Room ID already exists !")
	]