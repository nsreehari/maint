# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time
import datetime
from dateutil.relativedelta import relativedelta

import openerp
from openerp import tools
from openerp.exceptions import UserError
from openerp.osv import fields, osv
from openerp.tools.translate import _


class visitor_rooms_tag(osv.Model):
    _name = 'visitor.rooms.tag'
    _columns = {
        'name': fields.char('Name', required=True),
        'color': fields.integer('Color Index'),
    }
    _sql_constraints = [
            ('name_uniq', 'unique (name)', "Tag name already exists !"),
    ]


class visitor_abhyasi(osv.Model):
	_name = 'visitor.abhyasi'
	_columns = {
		'abhyasi_id': fields.char('Abhyasi ID', required=True),
		'full_name': fields.char('Full Name', required=True),
		'preceptor': fields.char('Preceptor Name', required=True),
		#'overseas': fields.char('Overseas (Y/N)', required=True),					#	Drop Down
		'overseas': fields.selection([('yes','Yes'), ('no','No')],'overseas', required=True),
		'center': fields.char('Center', required=True),		
		'country': fields.char('Country', required=True),		
		'contactnumber': fields.char('Abhyasi ID', required=True),					#	Int
		'birthyear': fields.char('Birth Year', required=True),						#	Date
		'gender': fields.char('Gender (M/F)', required=True),						#	Drop Down
		'identificationdoc': fields.char('Identification Doc', required=True),
	}
	
	_sql_constraints = [
		('abhyasi_id_uniq', 'unique (abhyasi_id)', "abhyasi_id already exists !"),
	]

	
class visitor_nonabhyasi(osv.Model):	
	_name = 'visitor.nonabhyasi'	
	_columns = {	
		'full_name': fields.char('Full Name', required=True),	
		'birthyear': fields.char('Birth Year', required=True),						#	Date	
		'gender': fields.char('Gender (M/F)', required=True),						#	Drop Down
		'child': fields.char('Identification Doc', required=True),	
	}	
	

#class visitor_reg_non_abhyasi(osv.Model):	
#	_name = 'visitor.reg.non.abhyasi'		
#	_columns = {	
#		'id': fields.char('ID', required=True),		
#		'person_id': fields.char('Person ID', required=True),		
#		'regestration_bach_id': fields.char('Regestration Batch ID', required=True),	
#	}		
#	
#	_sql_constraints = [
#		('id_uniq', 'unique (id)', "ID already exists !"),
#		('person_id_uniq', 'unique (person_id)', "person_id already exists !"),
#	]
	
	
#class visitor_reg_abhyasi(osv.Model):	
#	_name = 'visitor.reg.abhyasi'			
#	_columns = {		
#		'id': fields.char('ID', required=True),		
#		'person_id': fields.char('Person ID', required=True),			
#		'regestration_bach_id': fields.char('Regestration Batch ID', required=True),		
#	}			
#		
#	_sql_constraints = [	
#		('id_uniq', 'unique (id)', "ID already exists !"),	
#		('person_id_uniq', 'unique (person_id)', "person_id already exists !"),	
#	]	
	
class visitor_registration(osv.Model):	
	_name = 'visitor.registration'				
	_columns = {			
		'batchid': fields.char('Batch Id', required=True),			
		'record_entry': fields.date('Record Entry Date', required=True),
		'arrival_date': fields.date('Arrival Date', required=True),
		'arrival_time': fields.char('Arrival Time', required=True),					#	Time			
		'departure_date': fields.date('Departure Date', required=True),
		'departure_time': fields.char('Departure Time', required=True),					#	Time			
		'spot_registeration': fields.char('Spot Registeration', required=True),
		'Canceled': fields.char('Canceled (Y/N)', required=True),
		'cancelation_date': fields.date('Cancelation Date', required=True),
	}				
			
	_sql_constraints = [		
		('batchid_uniq', 'unique (batchid)', "ID already exists !"),		
	]

class visitor_checkins(osv.Model):	
	_name = 'visitor.checkins'				
	_columns = {			
		'checkinid': fields.char('Checkin Id', required=True),		
		'entry_date': fields.date('Entry Date', required=True),
		'arrival_date': fields.date('Arrival Date', required=True),
		'arrival_time': fields.char('Arrival Time', required=True),					#	Time			
		'departure_date': fields.date('Departure Date', required=True),
		'departure_time': fields.char('Departure Time', required=True),					#	Time			
		'regestration_id': fields.char('Registration ID', required=True),
		'person_id': fields.char('Person ID', required=True),	
		'accomodation_alloted': fields.char('Accomodation Alloted', required=True),
		'documents': fields.char('Documents Attached (Y/N)', required=True),
	}				
	
	
class visitor_rooms(osv.Model):	
	_name = 'visitor.rooms'					
	_columns = {				
		'roomid': fields.char('Room Id', required=True),				
		'room_type': fields.char('Room type', required=True),	
		'a/c': fields.char('A/C', required=True),	
		#'attached_bathroom': fields.char('Attached Bathroom', required=True),					#	Time				
		#'accessibility': fields.char('Accessibility', required=True),	
		#'family_priority': fields.char('Family Priority', required=True),					#	Time				
		#'familyinfantpriority': fields.char('Family Infant Priority', required=True),	
		'elderly': fields.char('Elderly', required=True),	
		'active': fields.char('Active', required=True),	
		'tag_ids' :fields.many2many('visitor.rooms.tag', 'abhyasi_visitor_room_tag_rel', 'visitor_room_tag_id','tag_id', 'Tags', copy=False),
		#'tag_ids' :fields.many2many('visitor.rooms.tag', 'abhyasi_visitor_room_tag_rel', 'visitor_room_tag_id','tag_id', copy=False),
}					
				
	_sql_constraints = [			
		('roomid_uniq', 'unique (roomid)', "Room ID already exists !"),			
	]		