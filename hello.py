import os
import random
import urllib2
import flask
from markdown import markdown
from flask import Flask, request, json, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from docutils.core import publish_string
#from pprint import pprint

app = Flask(__name__)
#pprint( os.environ )
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

ROOT_URL = "http://xwl.me/"



    # """ the location of the raw file stored as a string that should be a
    # URI, as well as an associated 'shortUrl' that is used as the location to be served from. """
class rawFile(db.Model):
    __tablename__ = "rawFile"
    remoteUrl = db.Column(db.String(300),unique = True)
    shortUrl = db.Column(db.String(300),primary_key = True)
    def __init__(self, url, shortUrl):
        #super(rawFile, self).__init__()
        self.remoteUrl = url
        self.shortUrl = shortUrl
        
def randomString(): # returns nice 6 character strings
    ourStr = ""
    i = 0
    while i < 15:
        if random.randint(0,1): # If we get a 1, we do letters
            ourChar = chr(random.randint(97,122))
            ourStr += ourChar

        else: # we get a 0, we do a number
            ourChar = str(random.randint(1,9))
            ourStr += ourChar
        i += 1

    return ourStr

# quick function to return the contents of a given url as a string.
def getRemoteRest(url):
    opener = urllib2.build_opener()
    toReturn = opener.open(url).read()

    # Alright, for whatever reason the below is what I had to do to get this
    # to stop throwing unicode errors. It's SUPER hacky, but it works.
    toReturn = toReturn.decode('utf-8')
    toReturn = toReturn.encode('ascii', 'replace')

    return toReturn

@app.route('/')
def hello():

    # Provides us with a super ghetto start page. This is just a string that 
    # will get rendered by a markdown-parser and give us some nice HTMl.
    toReturn = """
Live Markup-Parsing Service
===========================

Give us a live link to the document you're writing, and we'll give you a live link to the parsed version of that document.

---

###Here's a longer explanation:

Let's say you have a file in your Dropbox. It's written in plain-text, but it uses [Markdown](http://daringfireball.net/projects/markdown/) for its markup. You wish you could see what that document looks like if it were actually rendered, and you wish you had a public URL you could send your friends so they could see what your document looks like too.

This is what [xwl.me](http://xwl.me) does. You give it a link to an internet-accessible plain-text document, and xwl.me will give you several links, with each link being your document run through one of several markup language parsers.

Additionally, if you change the document on the web, all you need to do to see the changes in the rendered version is refresh the page! Xwl.me will always show the most up-to-date version of your file.

---

####Here's an example:

> Lets say I have a markdown-formatted document at `http://lelandbatey.com/example.md` . I want to see what my markdown file will look like when it's converted to HTML. To submit my URL to xwl, I'd type in `"http://xwl.me/ar/[MY_URL_GOES_HERE!]"`. 

> For my example document, it'd look like this: `{0}ar/http://lelandbatey.com/example.md`

> When I navigate to `{0}ar/http://lelandbatey.com/example.md` I get served a page that contains just the following:

    
        "parsedMD": "{0}md/f34t26y4pfpt4oa",
        "parsedREST": "{0}rs/f34t26y4pfpt4oa",
        "redirect": "{0}r/f34t26y4pfpt4oa",
        "shortString": "f34t26y4pfpt4oa"
    

> You have your "parsedMD" url which is your doc parsed as **Markdown**, the "parsedREST" which is parsed using the **reStructuredText** parser, and "redirect" which redirects anyone who visits it to your source file.

> You'll notice that each of these URL's is exactly the same, except for the couple of letters in the middle. That's intentional so you can easily access the different operations that can be run on your file.

---

## Get Started!

To get started, just add `http://xwl.me/ar/` in front of any url to a plain text document!

    """

    toReturn = toReturn.format(ROOT_URL)

    return render_template('frontpage.html')
    #return render_template('md.html',content=markdown(toReturn))


@app.route('/list')
def list_all():
    # Gets a list of all the things in the database. Then, builds a string that
    # is of each shortUrl/remoteUrl combination, returning that as output.
    
    toReturn = ""
    fullList = rawFile.query.all()
    # for stuff in fullList:
    #     toReturn += "shortUrl: "+stuff.shortUrl+"  ,  remoteUrl: "+stuff.remoteUrl+"<br><br>\n"
    return render_template('list.html', fullList = fullList)

#            __                          _       __           __
#       ____/ /__  ____  ________  _____(_)___ _/ /____  ____/ /
#      / __  / _ \/ __ \/ ___/ _ \/ ___/ / __ `/ __/ _ \/ __  / 
#     / /_/ /  __/ /_/ / /  /  __/ /__/ / /_/ / /_/  __/ /_/ /  
#     \__,_/\___/ .___/_/   \___/\___/_/\__,_/\__/\___/\__,_/   
#              /_/                                              
@app.route('/add', methods = ['POST'])
def addUrl():

    # If there is a JSON request and if they've specified a remote URL, then we 
    # create a new entry in the database with a randomly generated accessible url
    # that is 15 characters long.
    if request.json:
        if request.json["remoteUrl"]:
            thisFile = rawFile(request.json["remoteUrl"],randomString())
            db.session.add(thisFile)
            db.session.commit()
            return '{"value":"It seems to have worked!\n"}'
        else:
            print request.data
            return '{"value" : "no key named remoteUrl. request data:'+request.data+'"}\n'
    else:
        print request.data
        return '{"value" : "request not json. request data:'+request.data+'"}\n'


@app.route('/rs/<shortenedUrl>')
def renderText(shortenedUrl):
    
    toReturn = ""
    remoteUrl = rawFile.query.filter_by(shortUrl=shortenedUrl).first()
    
    try:
        return render_template('md.html',\
            content=publish_string( \
                getRemoteRest(remoteUrl.remoteUrl),\
                writer_name='html'))
    except:
        toReturn = "nothing found\n"
    
    return toReturn

@app.route('/md/<shortenedUrl>')
def renderMarkDown(shortenedUrl):
    remoteUrl = rawFile.query.filter_by(shortUrl=shortenedUrl).first()
    print remoteUrl.remoteUrl
    try:
        return render_template('md.html',\
        content=markdown(getRemoteRest(remoteUrl.remoteUrl)))


    except:
        return "no file for this URL"

# Method for redirection
@app.route('/r/<shortenedUrl>')
def redirect(shortenedUrl):
    remoteUrl = rawFile.query.filter_by(shortUrl=shortenedUrl).first()

    try:
        return flask.redirect(remoteUrl.remoteUrl,code=302)
    except:
        return "not a valid reference\n"

# By tacking a URL onto the end of this, that URL gets added to the database 
# with a randomly generated shortUrl.
@app.route('/ar/<path:remoteDocUrl>')
def addRemoteUrl(remoteDocUrl):

    if ROOT_URL in remoteDocUrl:
        return 'invalid URL' # if they try to submit a link to the site itself,
                             # then they're gonna have a bad time :)
    # This is a pretty ghetto fix for the problem of certain characters (like spaces) not getting escaped, then breaking stuff when we try to get the data at that url.
    remoteDocUrl = urllib2.quote(remoteDocUrl)
    remoteDocUrl = remoteDocUrl.replace("%3A",":")

    randShortUrl = randomString()
    
    # Pre-emptivley queries the database to see if this remoteUrl has been
    # submitted already. This with be of type "none" if nothings' been submitted
    givenLongUrl = rawFile.query.filter_by(remoteUrl = remoteDocUrl).first()


    try:
        if givenLongUrl.shortUrl: # If there's already a database entry for this remoteUrl
            randShortUrl = givenLongUrl.shortUrl

    except AttributeError: # If this remoteUrl is not in the database already, 
                           # then generate an entry.
        thisFile = rawFile(remoteDocUrl,randShortUrl)
        db.session.add(thisFile)
        db.session.commit()

    # We want a valid JSON object so we create a dict.
    returnDict = {
    "shortString" : randShortUrl,
    "parsedMD" : ROOT_URL+"md/"+randShortUrl,
    "parsedREST" : ROOT_URL+"rs/"+randShortUrl,
    "redirect" : ROOT_URL+"r/"+randShortUrl }

    # The extra options are there to make the output prettier :)
    toReturn = json.dumps(returnDict,sort_keys=True,indent=4, separators=(',', ': '))

    # By default the "content-type" of stuff that gets returned is set to 
    # "text/html", and because of that most web browsers won't render it with 
    # raw formatting like tabs and line returns. However, by setting it to
    # "text/plain" the browser treats it like a plaintext file and formatting
    # is rendered correctly!
    response = flask.make_response(toReturn)
    response.headers["Content-type"] = "text/plain"


    return response


if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    #app.debug = True
    app.run(host='0.0.0.0', port=port)
