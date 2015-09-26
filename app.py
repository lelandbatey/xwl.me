from __future__ import print_function
from flask import Flask, request, json, render_template, redirect, make_response
from docutils.core import publish_string
from markdown import markdown
from lib import make_pdf, rand_string
from db import MdModel
import jsonpickle
import requests
import json
import os
from os.path import dirname, realpath, join


# TODO: Move functionality to app from hello.py
APP = Flask(__name__)

APP.config.update(dict(
	DATABASE=join(dirname(realpath(__file__)), "remote_md_database.sqlite3")
))


ROOT_URL = "http://xwl.me/"

def jdump(in_data):
    """Creates prettified json representation of passed in object."""
    return json.dumps(in_data, sort_keys=True, indent=4, separators=(',', ': '))

def make_json_response(in_data):
    """Format an object as a json response"""
    if not isinstance(in_data, basestring):
        in_data = jsonpickle.encode(in_data)
    response = make_response(in_data)
    response.headers["Content-type"] = "application/json"
    return response

def get_model():
    """Returns an instance of the model"""
    model = MdModel(APP.config['DATABASE'])
    return model


class AutoQuery(object):
    """Eases database calls via automatic cleanup"""
    def __getattr__(self, name):
        def db_func(*args, **kwargs):
            database = get_model()
            db_method = getattr(database, name)
            return_value = db_method(*args, **kwargs)
            database.session.close()
            return return_value
        return db_func

@APP.route('/favicon.ico')
def handle_favicon():
    """Otherwise causes crashes"""
    return ""

@APP.route('/')
def home():
    """Render the frontpage"""
    return render_template('frontpage.html')

@APP.route('/md2pdf/')
def mdpdfPage():
    return render_template('md2pdf.html')

@APP.route('/list')
def list_all():
    entries = AutoQuery().get_all()
    return render_template('list.html', fullList=entries)

@APP.route('/api/md2pdf/', methods=['POST'])
def build_pdf():
    """Given the form variables 'mdHolder' and 'template', returns a
    pandoc-rendered pdf of that markdown."""
# submitForm
#   - template : "default/tablet/none"
#   - body : "<base 64 encoded body goes here>"
# Example as if running on localhost:
# http://localhost:5000/api/md2pdf/?template=tablet&body=IyBUZXN0IG9mIGEgc29tZXRoaW5n

    body = request.form['mdHolder']
    template = request.form['template']
    if not body:
        return "No text to convert"
    if not template:
        template = 'default'

    response = make_response(make_pdf(body, template))
    response.headers['Content-type'] = "application/pdf"

    return response


@APP.route('/rs/<in_short_url>')
def render_restructuredtext(in_short_url):
    entry = AutoQuery().get_by_shortkey(in_short_url)
    rs = requests.get(entry.remote_url).text
    content = publish_string(rs, writer_name='html')
    try:
        return render_template('md.html', content=content)
    except:
        return "nothing found\n"

@APP.route('/md/<in_short_url>')
def render_markdown(in_short_url):
    entry = AutoQuery().get_by_shortkey(in_short_url)
    md = requests.get(entry.remote_url).text
    content = markdown(md)
    try:
        return render_template('md.html', content=content)
    except:
        return "no file for this URL"

@APP.route('/r/<in_short_url>')
def redirect_from_shorturl(in_short_url):
    entry = AutoQuery().get_by_shortkey(in_short_url)
    try:
        return redirect(entry.remote_url, code=302)
    except:
        return "not a valid reference\n"

# By tacking a URL onto the end of this, that URL gets added to the database
# with a randomly generated shortUrl.
@APP.route('/ar/<path:in_url>')
def add_remote_url(in_url):
    rand_short_key = rand_string()

    # Prevent submission of urls from this site
    if ROOT_URL in in_url:
        return 'invalid URL'

    # Ghetto fix for auto-decoding of url by flask
    in_url = requests.utils.quote(in_url)
    in_url = in_url.replace("%3A",":")

    # Pre-query for existing entry for the given remote_url
    existing_entry = AutoQuery().get_by_remote_url(in_url)
    print(existing_entry)

    if existing_entry:
        rand_short_key = existing_entry.short_key
    else:
        AutoQuery().add_entry(rand_short_key, in_url)

    url_fmt = lambda middle: "{}{}{}".format(ROOT_URL, middle, rand_short_key)
    to_return = {
        "shortString" : rand_short_key,
        "parsedMD" : url_fmt("md/"),
        "parsedREST" : url_fmt("rs/"),
        "redirect" : url_fmt('r/')
    }
    to_return = jdump(to_return)

    # Set plaintext content type so browsers render text correctly
    response = make_response(to_return)
    response.headers["Content-type"] = "text/plain"
    return response

# Gonna be a catch-all route for this domain
@APP.route('/<path:in_url>')
def prettyPage(in_url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0'
    }

    def iteratorLen(someVal):
        i = 0
        for x in someVal:
            i += 1
        return i

    if 'http' not in in_url:
        in_url = 'http://'+in_url

    r = requests.get(in_url, headers=headers)
    soup = bs4.BeautifulSoup(r.text)

    most_children = None
    child_count = 0

    # Removes un-necessary things from the data we get
    [s.extract() for s in soup(['script','option','head'])]

    # Sets 'most_children' to the tag that has the most children. This is
    # because the main body is generally one div filled with lots of <p> tags
    # and the like.
    for x in soup.descendants:
        if hasattr(x, "children"): # This pretty much just checks if it's a 'tag'
            tempCount = iteratorLen(x.children)
            if tempCount >= child_count:
                child_count = tempCount
                most_children = x
    # Some sites are awesome and wrap the entire article in an "article" tag.
    # On sites like that, we just use the contents of the first "article" tag
    # we find.
    if soup.findAll('article'):
        most_children = soup.findAll('article')[0]
    return render_template('md.html', content=most_children.prettify())



if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    APP.debug = True
    APP.run(host='0.0.0.0', port=port)


