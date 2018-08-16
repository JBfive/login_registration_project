from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt

class UserManager(models.Manager):
	def basic_validator(self, postData):
		errors = {}
		if len(postData['first_name']) < 2:
			errors["first_name"] = "Name should be at least 2 character"
		if len(postData['last_name']) < 2:
			errors["last_name"] = "Name should be at least 2 characters"
		if len(postData['email']) < 2:
			errors["email"] = "Incorrect Email format"
		elif not EMAIL_REGEX.match(postData['email']):
			errors["email"] = "Incorrect Email format"
		existing_users = User.objects.filter(email=postData['email'])
		if len(existing_users) > 0:
			errors['email'] = "Email already exists!"
		if len(postData['password']) < 8:
			errors["password"] = "Password must be longer than 8 characters"
		if len(postData['confirm']) < 8:
			errors['confirm'] = "Passwords must match at 8 or more characters"
		pwd=postData['password']
		cpwd=postData['confirm']
		if not cpwd == pwd:
			errors['confirm'] = "Passwords must match"
		print(errors)
		if len(errors):
			result = {'return': errors, 'status': False}
			return result
		else:
			user = User.objects.create(
				first_name=postData['first_name'],
				last_name=postData['last_name'],
				email= postData['email'],
				password= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()))
			print(user)
			result = {'return': user.id, 'status': True}
			return result
	def validate_login(self, postData):
		errors = {}
		user = User.objects.filter(email=postData['email'])
		if bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
			print("password match")
			result = {'return': user[0].id, 'status': True}
			
		else:
			print("failed password")
			errors['login']= "Failed to login"
			if len(errors):
				result = {'return': errors, 'status': False}
		return result		

class User(models.Model):
	first_name= models.CharField(max_length=255)
	last_name= models.CharField(max_length=255)
	email= models.CharField(max_length=255)
	password= models.CharField(max_length=255)
	created_at= models.DateTimeField(auto_now_add = True)
	updated_at= models.DateTimeField(auto_now = True)
	objects = UserManager()
	def __repr__(self):
		return "<User object: {} {} {}>".format(self.first_name, self.last_name, self.email)