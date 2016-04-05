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
import webapp2
import cgi
import codecs

class RotHandler(webapp2.RequestHandler):
    def get(self):
        self.form()

    def form(self, val=""):
    	self.response.write("<html><header><title>Super ROT 13 !</title></header><body><a href=\"/\" id=\"retour\">Revenir au menu des problèmes</a><form action=\"/rot13\" method=\"post\">ROT 13<br><textarea name=\"text\">%s</textarea><br><input type=\"submit\" value=\"OK !\"><form></body></html>" % val)

    def post(self):
		text = self.request.get("text")
		text = codecs.encode(text, 'rot_13')
		self.form(cgi.escape(text, quote = True))
