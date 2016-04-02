#!/usr/bin/env python
# coding=<utf-8>
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2
import hmac
import hashlib
import random
import string

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

####### Fonctions de hashages #######  

#To hash cookies
SECRET = 'imsosecret'
def hash_str(s):
    return hmac.new(SECRET, s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split('|')[0]
    if h == make_secure_val(val):
        return val

#To hash passwords
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))

def make_pw_hash(name, pw, salt=make_salt()):
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s,%s' % (h, salt)

def valid_pw(name, pw, h):
    salt = h.split(',')[1]
    print(salt)
    return h == make_pw_hash(name, pw, salt)



class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.write(*a, **kw)

    def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def get(self):
		cookie = self.request.cookies.get('user_id')
		if cookie:
			secure_val = check_secure_val(cookie)
			if secure_val is None:
				self.redirect("/signup")
			else:
				id = int(secure_val)
				username = User.get_by_id(id).username	
				self.render("front.html", username=username)
		else:
			self.render("front.html")

#Classe pour la creation d un utilisateur
class CreateUser(Handler):
	def render_page(self, username="", password="", error=""):
		self.render("create_user.html", username=username, password=password, error=error)

	def get(self):
		self.render("create_user.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")

		if username and password and verify:

			#On verifie si le pass est identique a la verif
			if password != verify:
				error = "password and verification are'nt identical"
				self.render_page(username, password, error)
			else:
				#On verifie si l'utilisateur existe deja
				verif_user = db.GqlQuery("SELECT * FROM User WHERE username = :1", username)
				verif_user.run()
				if verif_user.count() != 0:
					error = "Ce nom d'utilisateur existe deja !"
					self.render_page(username, password, error)
				else:
					hashpass = make_pw_hash(username, password)
					usr = User(password = hashpass, username=username)
					usr.put()
					#On ajoute le cookie
					string_id = str(usr.key().id())
					secure_val = make_secure_val(string_id)
					self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % secure_val)
					self.redirect('/')
		else:
			error = "we need both username, a password and a verification of the password"
			self.render_page(username, password, error)

class Login(Handler):
	def render_page(self, username="", password="", error=""):
		self.render("login.html", username=username, password=password, error=error)

	def get(self):
		self.render("login.html")

	def post(self):
		username = self.request.get("username")
		password = self.request.get("password")

		if username and password:
			verif_user = db.GqlQuery("SELECT * FROM User WHERE username = :1", username)
			user = verif_user.get()
			if user is None:
				error="Probleme de login"
				self.render_page(username, password, error)
			else:
				if valid_pw(user.username, password, user.password):
					string_id = str(user.key().id())
					secure_val = make_secure_val(string_id)
					self.response.headers.add_header('Set-Cookie', 'user_id=%s; Path=/' % secure_val)
					self.redirect('/')
				else:
					error="Probleme de login"
					self.render_page(username, password, error)
		else:
			error = "un des champs n'est pas renseigne"
			self.render_page(username, password, error)

class Logout(Handler):
	def get(self):
		cookie = self.request.cookies.get('user_id')
		if cookie:
			self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')
		self.redirect("/signup")

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.EmailProperty(required = False)

app = webapp2.WSGIApplication([('/', MainPage), ('/signup', CreateUser), ('/login', Login), ('/logout', Logout)], debug=True)
