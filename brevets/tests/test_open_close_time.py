import arrow
import nose
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log=logging.getLogger(__name__)
import sys
sys.path.append("..")
import acp_times



def test_brevet_distance_200():
    #test case under brevet distance 200.
    time=arrow.now()
    assert acp_times.open_time(0,200,time)==time
    assert acp_times.close_time(0,200,time)==time.shift(hours=1)
    assert acp_times.open_time(20,200,time)==time.shift(minutes=35)
    assert acp_times.close_time(20,200,time)==time.shift(hours=2)
    assert acp_times.open_time(60,200,time)==time.shift(hours=1,minutes=46)
    assert acp_times.close_time(60,200,time)==time.shift(hours=4)
    assert acp_times.open_time(200,200,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(200,200,time)==time.shift(hours=13,minutes=30)
    assert acp_times.open_time(210,200,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(210,200,time)==time.shift(hours=13,minutes=30)

def test_brevet_distance_300():
    #test case under brevet distance 300.
    time=arrow.now()
    assert acp_times.open_time(0,300,time)==time
    assert acp_times.close_time(0,300,time)==time.shift(hours=1)
    assert acp_times.open_time(100,300,time)==time.shift(hours=2,minutes=56)
    assert acp_times.close_time(100,300,time)==time.shift(hours=6,minutes=40)
    assert acp_times.open_time(200,300,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(200,300,time)==time.shift(hours=13,minutes=20)
    assert acp_times.open_time(275,300,time)==time.shift(hours=8,minutes=14)
    assert acp_times.close_time(275,300,time)==time.shift(hours=18,minutes=20)
    assert acp_times.open_time(300,300,time)==time.shift(hours=9)
    assert acp_times.close_time(300,300,time)==time.shift(hours=20)
    assert acp_times.open_time(320,300,time)==time.shift(hours=9)
    assert acp_times.close_time(320,300,time)==time.shift(hours=20)

def test_brevet_distance_400():
    #test case under brevet distance 400.
    time=arrow.now()
    assert acp_times.open_time(0,400,time)==time
    assert acp_times.close_time(0,400,time)==time.shift(hours=1)
    assert acp_times.open_time(200,400,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(200,400,time)==time.shift(hours=13,minutes=20)
    assert acp_times.open_time(300,400,time)==time.shift(hours=9)
    assert acp_times.close_time(300,400,time)==time.shift(hours=20)
    assert acp_times.open_time(346,400,time)==time.shift(hours=10,minutes=27)
    assert acp_times.close_time(346,400,time)==time.shift(hours=23,minutes=4)
    assert acp_times.open_time(400,400,time)==time.shift(hours=12,minutes=8)
    assert acp_times.close_time(400,400,time)==time.shift(days=1,hours=3)
    assert acp_times.open_time(440,400,time)==time.shift(hours=12,minutes=8)
    assert acp_times.close_time(440,400,time)==time.shift(days=1,hours=3)

def test_brevet_distance_600():
    #test case under brevet distance 600.
    time=arrow.now()
    assert acp_times.open_time(0,600,time)==time
    assert acp_times.close_time(0,600,time)==time.shift(hours=1)
    assert acp_times.open_time(200,600,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(200,600,time)==time.shift(hours=13,minutes=20)
    assert acp_times.open_time(300,600,time)==time.shift(hours=9)
    assert acp_times.close_time(300,600,time)==time.shift(hours=20)
    assert acp_times.open_time(400,600,time)==time.shift(hours=12,minutes=8)
    assert acp_times.close_time(400,600,time)==time.shift(days=1,hours=2,minutes=40)
    assert acp_times.open_time(513,600,time)==time.shift(hours=15,minutes=54)
    assert acp_times.close_time(513,600,time)==time.shift(days=1,hours=10,minutes=12)
    assert acp_times.open_time(600,600,time)==time.shift(hours=18,minutes=48)
    assert acp_times.close_time(600,600,time)==time.shift(days=1,hours=16)
    assert acp_times.open_time(700,600,time)==time.shift(hours=18,minutes=48)
    assert acp_times.close_time(700,600,time)==time.shift(days=1,hours=16)

def test_brevet_distance_1000():
    #test case under brevet distance 1000.
    time=arrow.now()
    assert acp_times.open_time(0,1000,time)==time
    assert acp_times.close_time(0,1000,time)==time.shift(hours=1)
    assert acp_times.open_time(200,1000,time)==time.shift(hours=5,minutes=53)
    assert acp_times.close_time(200,1000,time)==time.shift(hours=13,minutes=20)
    assert acp_times.open_time(300,1000,time)==time.shift(hours=9)
    assert acp_times.close_time(300,1000,time)==time.shift(hours=20)
    assert acp_times.open_time(400,1000,time)==time.shift(hours=12,minutes=8)
    assert acp_times.close_time(400,1000,time)==time.shift(days=1,hours=2,minutes=40)
    assert acp_times.open_time(600,1000,time)==time.shift(hours=18,minutes=48)
    assert acp_times.close_time(600,1000,time)==time.shift(days=1,hours=16)
    assert acp_times.open_time(985,1000,time)==time.shift(days=1,hours=8,minutes=33)
    assert acp_times.close_time(985,1000,time)==time.shift(days=3,hours=1,minutes=41)
    assert acp_times.open_time(1000,1000,time)==time.shift(days=1,hours=9,minutes=5)
    assert acp_times.close_time(1000,1000,time)==time.shift(days=3,hours=3)
    assert acp_times.open_time(1005,1000,time)==time.shift(days=1,hours=9,minutes=5)
    assert acp_times.close_time(1005,1000,time)==time.shift(days=3,hours=3)
