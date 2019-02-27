"""sqlalchemy models"""
# pylint: disable=too-few-public-methods,abstract-method

from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy_json import NestedMutableJson
from sner.server.extensions import db


class Profile(db.Model):
	"""holds settings/arguments for type of scan/scanner. eg. host discovery, fast portmap, version scan, ..."""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	module = db.Column(db.String(100), nullable=False)
	params = db.Column(db.Text())
	tasks = relationship('Task', back_populates='profile')
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

	def __str__(self):
		return '<Profile: %s>' % self.name


class Task(db.Model):
	"""profile assignment for specific targets"""

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(1000))
	profile_id = db.Column(db.Integer(), db.ForeignKey('profile.id'), nullable=False)
	profile = relationship('Profile', back_populates='tasks')
	targets = db.Column(NestedMutableJson(), nullable=False)
	group_size = db.Column(db.Integer(), nullable=False)
	scheduled_targets = relationship('ScheduledTarget', back_populates='task', cascade='delete,delete-orphan')
	jobs = relationship('Job', back_populates='task', cascade='delete,delete-orphan')
	priority = db.Column(db.Integer(), nullable=False)
	created = db.Column(db.DateTime(), default=datetime.utcnow)
	modified = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

	def __repr__(self):
		return '<Task: %s>' % self.name
	def __str__(self):
		return '<Task: %s>' % self.name


class ScheduledTarget(db.Model):
	"""scheduled item"""

	id = db.Column(db.Integer, primary_key=True)
	target = db.Column(db.Text(), nullable=False)
	task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)
	task = relationship('Task', back_populates='scheduled_targets')


class Job(db.Model):
	"""assigned job"""

	id = db.Column(db.String(100), primary_key=True)
	assignment = db.Column(db.Text())
	result = db.Column(db.LargeBinary)
	task_id = db.Column(db.Integer(), db.ForeignKey('task.id'), nullable=False)
	task = relationship('Task', back_populates='jobs')
	targets = db.Column(NestedMutableJson(), nullable=False)
	time_start = db.Column(db.DateTime(), default=datetime.utcnow)
	time_end = db.Column(db.DateTime())