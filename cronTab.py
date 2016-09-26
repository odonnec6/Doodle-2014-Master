#!/usr/bin/env python

import sqlite3 as lite
import sys
import datetime

con = None

try:
    con = lite.connect('doodle/db.sqlite3')

    now = datetime.datetime.now()
    oldest = now - datetime.timedelta(days=30)
    query_string = "select id from poll_poll where time_created < '" + str(oldest) + "';"
    polls = con.execute(query_string)
    for poll in polls:
        poll_id = poll[0]
        query_string = "select id from poll_time where poll_id_id = '" + str(poll_id) + "';"
        times = con.execute(query_string)
        for time in times:
            time_id = time[0]
            query_string = "select id, option_id from poll_option_time_id where time_id = '" + str(time_id) + "';"
            options = con.execute(query_string)
            for option in options:
                m2m_id = option[0]
                option_id = option[1]
                query_string = "delete from poll_option where id = '" + str(option_id) + "';"
                print query_string
                con.execute(query_string)
                con.commit()
                query_string = "delete from poll_option_time_id where id = '" + str(m2m_id) + "';"
                print query_string
                con.execute(query_string)
                con.commit()
            query_string = "delete from poll_time where id = '" + str(time_id) + "';"
            print query_string
            con.execute(query_string)
            con.commit()
        query_string = "delete from poll_poll where id = '" + str(poll_id) + "';"
        print query_string
        times = con.execute(query_string)
        con.commit()
except lite.Error, e:
    print "Error %s:" % e.args[0]
    sys.exit(1)
finally:
    if con:
        con.close()
