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
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
								autoescape= True)

class Handler(webapp2.RequestHandler):
	def write(self,*a , **kw):
		self.response.out.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)
		
	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class store(db.Model):
	title = db.StringProperty(required=True)
	story = db.TextProperty(required=True)
	name = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

#post-page handler
class PostHandler(Handler):
	def wrote(self, error="", title="", story="", name=""):
		self.render("post-page.html",error = error, title = title, story = story, name = name)
	def get(self):
		self.wrote()

	def post(self):
		title = self.request.get('title')
		story = self.request.get('story')
		name = self.request.get('name')

		if title and story and name:
			if title.isdigit() or name.isdigit():
				self.wrote("please provide name without numbers")
			else:
				a = store(title= title, story = story, name=name)
				a.put()
				X = str(a.key().id()) 
				self.redirect('/display/%s'%X)
		else:
			self.wrote("enter title , name and story")   

#make the user to see whether the post the made is as good as they wanted or is not then it gives them a chance to delete that post...

class User_input(Handler):

	def get(self,id_no):
		input = store.get_by_id(int(id_no))
	
	
		self.render('display.html',arts= input)

	def post(self):
		
		if submit:
			a = store(title= title, story = story, name=name)
			a.put()
			self.redirect('Home.html')
		else:
			self.redirect('post-page.html')

#homepage handler .. fetches data from store table using sql quering
class Homehandler(Handler):
	def get(self):
		arts = db.GqlQuery("SELECT * FROM store "
							"ORDER BY created DESC ")
		self.render("HOME.html",arts = arts)


app = webapp2.WSGIApplication([
	('/post', PostHandler),
	('/display/([0-9]+)', User_input),
	('/',Homehandler)
], debug=True)
