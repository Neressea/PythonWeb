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
import os
import webapp2
import jinja2

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.write(*a, **kw)

    def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def render_page(self):
		articles = Article.all().order("-created")
		self.render("front.html", articles=articles)

	def get(self):
		self.render_page()

class PostPage(Handler):
	def render_page(self, subject="", content="", error=""):
		self.render("post.html", subject=subject, content=content, error=error)

	def get(self):
		self.render("post.html")

	def post(self):
		subject = self.request.get("subject")
		content = self.request.get("content")

		if subject and content:
			art = Article(content = content, subject=subject)
			art.put()
			self.redirect('/'+str(art.key().id()))
		else:
			error = "we need both subject and a content"
			self.render_page(subject, content, error)

class PermaPage(Handler):
	def get(self, id):
		key = db.Key.from_path('Article', int(id))
		article = db.get(key)

		if not article:
			self.error(404)
			return

		self.render("unique.html", article=article)

class Article(db.Model):
	content = db.TextProperty(required = True)
	subject = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

app = webapp2.WSGIApplication([('/', MainPage), ('/newpost', PostPage), (r'/(\d+)', PermaPage)], debug=True)
