"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request,Flask,redirect,url_for,render_template
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import configparser
import config
import os
import logging
from pymongo import MongoClient

###
# Globals
###
app = flask.Flask(__name__)
config = configparser.ConfigParser()
if os.path.isfile("./credentials.ini"):
    config.read("./credentials.ini")
else:
    config.read("./app.ini")
global PORT
PORT=config["DEFAULT"]["PORT"]
global DEBUG
DEBUG=config["DEFAULT"]["DEBUG"]
client= MongoClient('mongodb://'+os.environ['MONGODB_HOSTNAME'],27017)
db=client.tododb
###
# Pages
###

@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')

@app.route("/display")
def display():
    return flask.render_template("display_brevets.html",items=list(db.tododb.find()))

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

@app.route("/_submit",methods=['POST'])
def submit():
    db.tododb.drop()
    open_time=request.form.getlist("open")
    close_time=request.form.getlist("close")
    km=request.form.getlist("km")
    miles=request.form.getlist("miles")
    location=request.form.getlist('location')
    for i in range(len(open_time)):
        if(open_time[i]!=""):
            if (location[i]==""):
                location[i]="None"
            db.tododb.insert_one({'open':open_time[i],'close':close_time[i],'km':km[i],'miles':miles[i],'location':location[i]}) 
    if 
    return redirect(url_for('index'))

#############

app.debug = DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(PORT))
    app.run(port=PORT, host="0.0.0.0")
