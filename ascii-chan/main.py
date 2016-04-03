#!/usr/bin/env python
# encoding=utf8  
import sys  

reload(sys)  
sys.setdefaultencoding('utf8')

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
import re
import sys
import webapp2
import jinja2
import time
import urllib2
from xml.dom import minidom

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

#Pour recuperer les coordonnees
def get_coords(ip):
	url = "http://ip-api.com/xml/" + ip
	content = None
	try:
		content = urllib2.urlopen(url).read()
	except Exception:
		return None#Il n'y a pas de coordonnees, on envoie des données aléatoires

	if content:
		p = minidom.parseString(content)
    	location = p.getElementsByTagName("query")[0]
    	if location.getElementsByTagName("lat"):
	        lat = location.getElementsByTagName("lat")
	        lon = location.getElementsByTagName("lon")
	        return db.GeoPt(lat[0].firstChild.data, lon[0].firstChild.data)

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"

def gmaps_image(points):
    url = GMAPS_URL
    for p in points:
        url+="&markers=%d,%d" % (p.lat, p.lon)
    return url

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
    	self.response.write(*a, **kw)

    def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

    def render(self, template, **kw):
    	self.write(self.render_str(template, **kw))

class MainPage(Handler):
	def render_page(self, title="", art="", error=""):
		arts = Art.all().order("-created")
		arts = list(arts)

		points= filter(None, (a.coords for a in arts))
		img_url = None
		if points:
			img_url = gmaps_image(points)

		self.render("front.html", arts=arts, title=title, art=art, error=error, img_url=img_url)

	def get(self):
		self.render_page()

	def post(self):
		title = self.request.get("title")
		art = self.request.get("art")

		if title and art:

			art = Art(art = art, title=title)
			coords = get_coords(self.request.remote_addr)
			if coords:
				art.coords = coords

			art.put()
			time.sleep(0.1)
			self.redirect('/')
		else:
			error = "we need both title and a art"
			self.render_page(title, art, error)

class Art(db.Model):
	art = db.TextProperty(required = True)
	title = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)
	coords = db.GeoPtProperty()

app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
