# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from openerp import models, fields, api
from datetime import datetime


class visitor_room_tags(models.Model):
	_name = 'visitor.room.tags'
	_description = 'Room Attributes like A/C, Accessibility, etc.'
	name = fields.Char('Name', required=True)
	color = fields.Integer('Color Index')
	_sql_constraints = [
			('name_uniq', 'unique (name)', "Tag name already exists !")
	]


class visitor_room_type(models.Model):
	_name = 'visitor.room.type'
	_description = 'Room Type'
	name = fields.Char('Room Type', required=True)
	_sql_constraints = [
		('type_uniq', 'unique (name)', "Room Type already exists !")
	]


yesnosel = [('Yes', 'Yes'), ('No', 'No')]
gendersel = [('male','Male'), ('female','Female')]
timesel = [('latenight','7PM-11PM'), ('evening','3PM-7PM'), ('afternoon', '11AM-3PM'),   ('morning', '6AM-10AM'),   ('early morning', '12AM-6AM') ]


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
		#self.overseas = ((self.country.lower().strip()) != 'india')

	abhyasi_id =  fields.Char(string='Abhyasi ID', required=True)
	full_name =  fields.Char(string='Full Name', required=True)
	preceptor =  fields.Selection(selection = yesnosel, string='Is Preceptor?', required=True)
	center =  fields.Char('Center', required=True)
	country =  fields.Char('Country', required=True,default='INDIA')
	overseas =  fields.Char(compute="_compute_overseas", string = 'Overseas?')
	#overseas =  fields.Char('Overseas?')
	contactnumber =  fields.Char('Contact Number')
	birthyear =  fields.Integer('Birth Year', required=True)
	gender =  fields.Selection(selection=gendersel, string='Gender', required=True)

	_sql_constraints = [
		('abhyasi_id_uniq', 'unique (abhyasi_id)', "abhyasi_id already exists !")
	]


@api.one
@api.constrains('birthyear')
def _check_birthyear(self):
	if self.birthyear < 1900:
		raise ValidationError("BirthYear cannot be less than 1900")
	todayyear = datetime.now().year
	if self.birthyear > todayyear:
		raise ValidationError("BirthYear cannot be greather than %d" % todayyear )


class visitor_nonabhyasi(models.Model):
	_name = 'visitor.nonabhyasi'
	_description = 'Children or People without Abhyasi ID' 

	full_name = fields.Char(string='Full Name', required=True)
	birthyear = fields.Integer(string='Birth Year', required=True, default=0)
	gender =  fields.Selection(string='Gender', selection=gendersel, required=True)
	child =  fields.Char(compute="_compute_child", string = 'Child?')
	#child =  fields.Char(string = 'Child?')
	
	@api.depends('birthyear','child')
	def _compute_child(self):
		#for rec in self:
		todayyear = datetime.now().year
		if (todayyear - self.birthyear <= 15) == True:
			self.child = "True"
		else:
			self.child = "False"


	@api.one
	@api.constrains('birthyear')
	def _check_birthyear(self):
		if self.birthyear < 1900:
			raise ValidationError("BirthYear cannot be less than 1900")
		todayyear = datetime.now().year
		if self.birthyear > todayyear:
			raise ValidationError("BirthYear cannot be greather than %d" % todayyear )


class visitor_registration(models.Model):
	_name = 'visitor.registration'
	_description = 'Visitor Registrations'
	batchid =  fields.Char('Batch Id', default=datetime.now().strftime("%Y%m%d%H%M%S"), required=True, readonly=True)
	record_entry =  fields.Char(string='Record Entry Date', default=datetime.now().strftime("%Y-%m-%d"), readonly=True)
	arrival_date =  fields.Date(string='Arrival Date', required=True)
	arrival_time =  fields.Selection(selection=timesel, string='Arrival Time', required=True)
	departure_date =  fields.Date(string='Departure Date',required=True)
	departure_time =  fields.Selection(selection=timesel, string='Departure Time', required=True)
	spot_registration = fields.Selection(string='Spot Registeration?', selection=yesnosel, required=True)
	cancelled = fields.Selection(string='Cancelled?', selection=yesnosel, default='No' )
	cancelation_date =  fields.Date('Cancelation Date')
	_sql_constraints = [('batchid_uniq', 'unique (batchid)', "ID already exists !")]



class visitor_rooms(models.Model):
	_name = 'visitor.rooms'
	_description = 'Visitor Rooms Description'
	roomid =  fields.Char(string='Room Id', required=True)
	roomtype =  fields.Many2one(comodel_name='visitor.room.type',      required=True )
	ac =  fields.Selection(yesnosel,string='Air-Conditioned?', required=True)
	tag_ids = fields.Many2many(comodel_name='visitor.room.tags', string ='Tags', copy=False)
	#active =  fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Room in Operation?', required=True)
	notes =  fields.Text('Room Description')
	_sql_constraints = [
		('roomid_uniq', 'unique (roomid)', "Room ID already exists !")
	]