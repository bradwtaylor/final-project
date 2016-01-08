import os

import jinja2

import webapp2
import cgi
from datetime import datetime
from pytz import timezone
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

template_dir = os.path.join(os.path.dirname (__file__), 'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape= True)

#setting default values for global variables

# comments are handled by code used in the Wallbook tutorial used in the Udacity course Intro to Programming Stage 4.8 lesson "Create a working datastore"

HOME_GUESTBOOK_NAME = 'home_guestbook'
stage_guestbook_name = "default"
error = 'Enter comment here'



class Handler(webapp2.RequestHandler):
    def write(self, *a,**kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template,**kw))

# MainPage handler generates the home page and home page comments

class MainPage(Handler):
    def get(self):
        global error
        user = users.get_current_user()
 
        guestbook_name = self.request.get('guestbook_name',
                                          HOME_GUESTBOOK_NAME)
     
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
       
        url, url_linktext = url_link_sub(users.create_logout_url(self.request.uri + '#comments'),users.create_login_url(self.request.uri + '#comments'))

        sign_query_params = urllib.urlencode({'guestbook_name':
                                             guestbook_name})
        self.render("/stages/home.html", guestbook_name=guestbook_name, sign_query_params=sign_query_params, url=url, url_linktext=url_linktext, error=error)
        
        greetings_query = Greeting.query(
            ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        greetings = greetings_query.fetch()
        self.response.write('%s' % get_comments_sub(user, greetings))
        error = 'Enter comment here'
        

# stages is the handler for generating the pages with the individual stage content and the corresponding comments

class stages(Handler):
    def get(self):
        global error
        user = users.get_current_user()
        stagenum = self.request.get('stage')
        stagenum = stagenum and int(stagenum)
        stage_guestbook_name = self.request.get('guestbook_name')

        greetings_query = Greeting.query(
            ancestor=stage_guestbook_key(stage_guestbook_name)).order(-Greeting.date)
       
        url, url_linktext = url_link_sub(users.create_logout_url(self.request.uri + '#comments'),users.create_login_url(self.request.uri + '#comments'))

        # Write the submission form and the footer of the page
        sign_query_params = urllib.urlencode({'guestbook_name':
                                              stage_guestbook_name})

        self.render("stages/stage.html", stage=stagenum, guestbook_name=stage_guestbook_name, sign_query_params=sign_query_params, url=url, 
            url_linktext=url_linktext, error=error)
        greetings = greetings_query.fetch()
        self.response.write('%s' % get_comments_sub(user, greetings))
        error = 'Enter comment here'
        

#url_link_sub checks if the current user is logged in or logged out in order to generate a "login" or "logout" link below the comments box
def url_link_sub(logout_url,login_url):
    user = users.get_current_user()

    if user:
            url = logout_url
            url_linktext = ('Logged in as: %s Click here to log out' % user)
    else:
            url = login_url
            url_linktext = 'Login'
    return (url, url_linktext)

# get_comments_sub downloads the appropriate comment guestbook and formats the comments to be added at the bottom of the page
def get_comments_sub(user, greetings):
        comments = ''

        for greeting in greetings:
            date = greeting.date
            dateutc = date.replace(tzinfo=timezone('US/Central'))
            localdate = dateutc.astimezone(timezone('US/Central'))

            if greeting.author:
                author = greeting.author.email
                if user and user.user_id() == greeting.author.identity:
                    author += ' (You)'
                comments = comments + ('<b>%s</b> wrote:' % author)
            else:
                comments = comments + ('An anonymous person wrote:')
            
            comments = comments + ('<blockquote>%s<br>Date/Time: %s </blockquote><hr>' % 
                (cgi.escape(greeting.content),localdate.strftime("%d-%b-%Y %I:%M:%S %p %Z")))

        return comments


# returns the key for the home page guestbook
def guestbook_key(guestbook_name=HOME_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

# returns the key for the appropriate stage guestbook
def stage_guestbook_key(guestbook_name=stage_guestbook_name):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Stage_Guestbook', guestbook_name)



class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)


# handler for posting comments on the home page to the datastore
class Guestbook(webapp2.RequestHandler):
    def post(self):
        global error
        guestbook_name = self.request.get('guestbook_name',
                                          HOME_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        
        if greeting.content.strip():
                greeting.put()
                error = 'Enter comment here'
        else:
            error = 'Please provide a comment before hitting Submit!'      
            
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))

# handler for posting comments on the stage pages to the datastore
class Stage_Guestbook(webapp2.RequestHandler):
    def post(self):
        global error
        stagenum = self.request.get('stage')

        stage_guestbook_name = self.request.get('guestbook_name')

        greeting = Greeting(parent=stage_guestbook_key(stage_guestbook_name))

        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        if greeting.content.strip():
                greeting.put()
                error = 'Enter comment here'
        else:
            error = 'Please provide a comment before hitting Submit!'      
            
        query_params = {'guestbook_name': stage_guestbook_name}
        self.redirect('/stage.html?' + urllib.urlencode(query_params) + '&stage=' + str(stagenum))

class resume(Handler):
    def get(self):
        self.render("resume/index.html")

  
app = webapp2.WSGIApplication ([('/', MainPage),('/stage.html', stages), ('/sign', Guestbook), ('/signstage', Stage_Guestbook),
    ('/resume', resume)], debug=True)
