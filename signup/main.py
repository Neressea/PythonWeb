#!/usr/bin/env python
#
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
import webapp2
import cgi
import re

class MainHandler(webapp2.RequestHandler):

	def get(self):
		self.form()

	def form(self, user="", email="", err_user="", err_password="", err_verify="",err_email=""):
		form = """<html><header><title>Form test</title></header>
			   <body><form action=\"/signup\" method=\"post\">Sign Up !<br>
			   <br><label>Utilisateur: <input name=\"username\" type=\"text\" value=\"%(username)s\"></label> <span style=\"color: red\">%(err_user)s</span>
			   <br><label>Mot de passe: <input name=\"password\" type=\"password\"></label> <span style=\"color: red\">%(err_password)s</span>
			   <br><label>Verification: <input name=\"verify\" type=\"password\"></label> <span style=\"color: red\">%(err_verify)s</span>
			   <br><label>Email: <input name=\"email\" type=\"email\" value=\"%(email)s\"></label> <span style=\"color: red\">%(err_email)s</span>
			   <br><input type=\"submit\" value=\"OK !\"><form></body></html>"""
		form = form % {"username": user, "email": email, "err_user": err_user, "err_password": err_password, "err_verify": err_verify, "err_email": err_email}
		self.response.write(form)

	def post(self):
		USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
		PASS_RE = re.compile(r"^.{3,20}$")
		MAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")

		err_user=""
		err_password=""
		err_verify=""
		err_email=""

		if not USER_RE.match(username):
			err_user="Nom d'utilisateur invalide"

		if not PASS_RE.match(password):
			err_password = "Mot de passe invalide"

		if verify != password:
			err_verify = "Mots de passe differents"

		if email != "":
			if not MAIL_RE.match(email):
				err_email = "Mail invalide"

		if err_user != "" or err_password != "" or err_verify != "" or err_email != "":
			self.form(username, email, err_user, err_password, err_verify, err_email)
		else:
			self.redirect("/welcome?username=%s" % username)

class Connected(webapp2.RequestHandler):
	def get(self):
		name = self.request.get("username")
		self.response.write("<html><header><title>Form test</title></header><body>"
			+"<h1>Welcome, %s !</h1></body></html>" % name)


app = webapp2.WSGIApplication([
    ('/signup', MainHandler),
    ('/welcome', Connected)
], debug=True)
