"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import configparser
import config
import os
import logging

###
# Globals
###
app = flask.Flask(__name__)
config = configparser.ConfigParser()
if os.path.isfile("./credentials.ini"):
    print("break1")
    config.read("./credentials.ini")
else:
    print("break2")
    config.read("./app.ini")
global PORT
PORT=config["DEFAULT"]["PORT"]
global DEBUG
DEBUG=config["DEFAULT"]["DEBUG"]
###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))
    dist=request.args.get('dist',type=int)#get brevet_dist
    bd=request.args.get('bd',type=str)#get begin date
    arrow_bd=arrow.get(bd,"YYYY-MM-DDTHH:mm")#change date to be arrow
    #call open_time and close_time, then change return value(is arrow) from
    #those two function to be "YYYY-MM-DDTHH:mm" format
    open_time = acp_times.open_time(km, dist,arrow_bd).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, dist,arrow_bd).format('YYYY-MM-DDTHH:mm')
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)#pass on to calc.html
#############

app.debug = DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(PORT))
    app.run(port=PORT, host="0.0.0.0")
