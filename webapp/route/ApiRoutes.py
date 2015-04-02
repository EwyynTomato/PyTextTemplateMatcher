from flask import Blueprint, current_app, Response, request, render_template
from texttemplatematcher import fuzzymatcher
from utils.AppConfig import config

apiroutes = Blueprint('apiroutes', __name__)

class ApiRoutesConst(object):
    INDEX        = '/'
    HEALTH_CHECK = '/api/health_check'

@apiroutes.route(ApiRoutesConst.INDEX)
def index():
    return render_template("index.html")

@apiroutes.route(ApiRoutesConst.HEALTH_CHECK)
def health_check():
    return 'Api is alive'

@apiroutes.route("/dude")
def dude():
    text = "input a string and this will match variables in the template."
    template = "input a {{object}} and this will {{action}}."
    result =  fuzzymatcher.fuzzy_template_match(text, template)
    return repr(result)