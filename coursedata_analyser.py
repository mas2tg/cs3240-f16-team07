__author__ = "mas2tg"

import psycopg2

def instructor_numbers(dept_id):
    #connect to db
    conn = psycopg2.connect(database="course1", user="postgres", password="wombat")
    cur = conn.cursor()

    #Get numbers

    cur.execute("SELECT deptId, seatstaken, instructor FROM coursedata WHERE deptId=%s;",(dept_id,))

    dict = {}
    for row in cur:
        if row[2] not in dict:
            dict[row[2]] = int(row[1])
        else:
            dict[row[2]] += int(row[1])
    
    #Save and close
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    instructor_numbers('STS')
    
