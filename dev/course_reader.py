__author__ = "mas2tg"

import psycopg2
import csv

def load_course_database(db_name, csv_filename):
    #conn = psycopg2.connect("dbname=course1 user=postgres password=password")
    conn = psycopg2.connect(database=db_name, user="postgres", password="wombat")
    cur = conn.cursor()

    #Create new table
    cur.execute("DROP TABLE IF EXISTS coursedata;")
    cur.execute("CREATE TABLE coursedata (deptID text, courseNum int, semester int, meetingType text, seatsTaken int, seatsOffered int, instructor text);")

    #Read from csv and load into db
    with open(csv_filename, 'rU') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
             cur.execute("INSERT INTO coursedata (deptid, coursenum, semester, meetingtype, seatstaken, seatsoffered, instructor) VALUES (%s,%s,%s,%s,%s,%s,%s);", row)

    #Save and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
        load_course_database("course1", "seas-courses-5years.csv")
