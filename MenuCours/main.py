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
import os
import webapp2

from handlers.MainHandler import * 
from handlers.BlogHandler import * 
from handlers.Rot13Handler import * 
from handlers.AsciiChanHandler import * 

class MainPage(Handler):
	def get(self):
		self.render("front.html")

app = webapp2.WSGIApplication([('/', MainPage),
	('/blog/?', BlogPage),
	('/blog/.json/?', BlogJSON),
	('/blog/newpost/?', PostPage),
	('/blog/(\d+)/?', PermaPage),
	(r'/blog/(\d+)\.json/?', PermaJSON),
	(r'/blog/login/?', Login),
	(r'/blog/signup/?', CreateUser),
	(r'/blog/logout/?', Logout),
	('/blog/flush/?', Flush),
	('/asciichan/?', AsciiPage),
	('/rot13/?', RotHandler)],
	debug=True)