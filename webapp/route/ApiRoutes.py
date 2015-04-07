from flask import Blueprint, current_app, Response, request, render_template, redirect, escape
from texttemplatematcher import fuzzymatcher, difflibmatcher
from utils.AppConfig import config

apiroutes = Blueprint('apiroutes', __name__)

class ApiRoutesConst(object):
    INDEX        = '/'
    HEALTH_CHECK = '/api/health_check'

@apiroutes.route(ApiRoutesConst.INDEX)
def index():
    return render_template("index.html", previnput={"template":"input a {{object}} and this will {{action}}.",
                                                    "inputtext":"input a string and this will match variables in the template."})

@apiroutes.route(ApiRoutesConst.HEALTH_CHECK)
def health_check():
    return 'Api is alive'

@apiroutes.route("/match_template", methods=["GET", "POST"])
def match_template():
    if request.method == "GET":
        return redirect(ApiRoutesConst.INDEX)
    text            = request.form.get("inputtext", "") #For textarea only
    template        = request.form.get("template", "")  #For textarea only
    escapedtext     = str(escape(text))     #Prevent XSS
    escapedtemplate = str(escape(template)) #Prevent XSS

    match_functions = [
        {"function":"Fuzzy (Levenshtein)",
         "result": fuzzymatcher.mark(escapedtext, fuzzymatcher.template_match(escapedtext, escapedtemplate).vars, prefix='<mark>', suffix='</mark>')}
        , {"function":"Simple Sequence Matcher (Diff)",
           "result": difflibmatcher.mark(escapedtext, difflibmatcher.template_match(escapedtext, escapedtemplate), prefix='<mark>', suffix='</mark>')}
                       ]
    return render_template("index.html", previnput={"template":template, "inputtext":text}, match_functions=match_functions)
