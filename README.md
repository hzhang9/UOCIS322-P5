# UOCIS322 - Project 5 #
Brevet time calculator with AJAX and MongoDB!

## Overview

Store control times from Project 4 in a MongoDB database.

## Recall Project 4

### Overview

Reimplement the RUSA ACP controle time calculator with Flask and AJAX.

#### ACP controle times

Controls are points where a rider must obtain proof of passage, and control[e] times are the minimum and maximum times by which the rider must arrive at the location. In other words, essentially replacing the calculator here [https://rusa.org/octime_acp.html](https://rusa.org/octime_acp.html).   

### Time algorithm description

#### Open time

For open time, there's not randonneuring events, all of output time follow the rule:
control distance(referred to as cd then) equals 0, time=0; 0<cd<=200, time=cd/34; 200<cd<=400,because in distances 0-200, moving speed is 15 km/h, so time= 200/34 + (cd-200)/32; and for range in 400-600, 600-1000, maximun speed respectively are 30 and 28, by the same piecewise calculation, can get open time.
And if control dist over brevet distance less than or equals 20%(over more than 20% will be illegal), the open time of control distance will just equals open time of brevet distance, such as open_time(200,200,t)==open_time(210,200,t)==open_time(240,200,t).

#### Close time

Close time will be more complex, when cd==0, time will be 1 hour rather than 0, and in range 0<cd<=60, time= 1+cd/20; following part is similar to above open time,the minimum speed in range 60-600,600-1000,respectively are 15 and 11.428. By the same method, can get close time. Also, same with open time,  if control dist over brevet distance less than or equals 20%(over more than 20%  will be illegal), the close time of control distance will just equals close time of brevet distance.
And the reason close time is more complex is close time exist some special distance, which are 200km, 300km, 400km, 600km and 1000km, those also are possible value of brevet distance, if control distance equals one of above num, in some cases, time will be a fixed value, which respectively are 13.5h, 20h, 27h, 40h and 75h.
And the "some cases" are:
1. if control distance== brevet_distance, time will be the fixed number, such as close_time(200,200,t), the change to time will be 13.5 hours rather than 200/15=13.333 hours.
2. if control distance is 200km or 400km, and less than brevet distance, the time should be calculate as normal rather than fixed number(and also should consider case 1),else if control distance is 300km, 600km or 1000km, time should be above fixed number, such as close_time(200,600,t)=200/15=13.333!=13.5, or close_time(300,600,t)=20!=300/15, and so on.

#### Return

Above description shows the maximun and minimun time cost, so after get time offset in hour format, finally separate the fraction into minutes, and shift arrow to expected open time and close time, that's what needed to return.

## Diffence with Project4

In this project,  will add the following:

1. Add two buttons `Submit` and `Display` in the ACP calculator page.

2. Upon clicking the `Submit` button, the control times should be inserted into a MongoDB database.

3. Upon clicking the `Display` button, the entries from the database should be displayed in a new page.


## Identifying Information

Author: Haoran Zhang, hzhang9@uoregon.edu
