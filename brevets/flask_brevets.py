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
def display():#jump to display.html with neccessnary data items
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
    db.tododb.drop()#clean db before submit
    open_time=request.form.getlist("open")#get open_time, following 5 step is same
    close_time=request.form.getlist("close")
    km=request.form.getlist("km")
    miles=request.form.getlist("miles")
    location=request.form.getlist('location')
    brevet_dist=request.form.get('distance',type=int)
    counter=0#count # of db been insert
    repeat=False#shows whether input repeat control time
    repeat_check=[]#list to check whether input repeat control time
    in_order=True#shows whether input order is from small ro large
    space_check=False#check whether left space between inputed control time
    have_empty=False#show whether left space between inputed control time
    if(km[0]==""):#the condition first input is empty(not matter whether following input valid)
        message="Cannot submit full empty, and first input also cannot be empty"
        return flask.render_template('error_submit.html',message=message)
    temp_km=float(km[0])#used to compare with above km,so inital as km[0]
    last_dist=0#it hold last valid control distance 
    for i in range(len(km)):
        if(km[i]!=""):#if not empty input
            if location[i]=="":#location is option, so if doesn't input, change to none
                location[i]="None"
            if space_check==True:
            #if one of term is empty(means space_check alreadly change to true),
            #and come to this step means current input isn't empty, existing empty
            #input between to valid input,have_empty change to true, waiting for rise error
                have_empty=True
            if km[i] in repeat_check:
            #repeat_check hold passed valid input, if current input already in the list
            #repeat being true and wait for rise error
                repeat=True
            if float(km[i])<float(temp_km):
            #temp_km hold last valid input, if temP_km bigger than current input,
            #in_order change to False, waiting for rise error
                in_order=False
            if float(km[i])>1.2*float(brevet_dist):
            #every input control km cannot over more than 20% of bre distance
            #if over jump to error_submit.html with below message
                message="Input distance cannot over brevet distance more than 20%"
                return flask.render_template('error_submit.html',message=message)
            last_dist=km[i]#update last control dist
            temp_km=float(km[i])#update temp_km
            repeat_check.append(km[i])#update repeat_check list 
            db.tododb.insert_one({'open':open_time[i],'close':close_time[i],'km':km[i],'miles':miles[i],'location':location[i]})#insert to db
            counter+=1#update counter
        else:#else is empty input, space check change to true
            space_check=True
    if repeat==True:
    #if exist repeat, jump to error with below message
        message="Cannot submit repeat control distances"
        return flask.render_template('error_submit.html',message=message)
    elif in_order==False:
    #if doesn't follow small to big rule, jump to error with below message
        message="Should input control distances from small to large"
        return flask.render_template('error_submit.html',message=message)
    elif have_empty==True:
    #if have empty between two valid control dist, jump to error with below message
        message="Don't left empty between two valid control dist"
        return flask.render_template('error_submit.html',message=message)
    elif float(last_dist)<float(brevet_dist):
    #if last control dist < brevet_dist, jump to error with below message
        message="Last input control distance must over brevet distance"
        return flask.render_template('error_submit.html',message=message)
    return redirect(url_for('index'))

#############

app.debug = DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(PORT))
    app.run(port=PORT, host="0.0.0.0")
