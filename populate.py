import json
import random
import string
import psycopg2
import random
import datetime
from datetime import timedelta

import math

first_names = ['Alice', 'Bob', 'Charlie', 'David', 'Emily', 'Frank', 'Gina', 'Hannah', 'Isaac', 'Julia', 'Kevin', 'Lily', 'Mike', 'Nancy', 'Olivia', 'Peter', 'Qiana', 'Rachel', 'Sarah', 'Tom', 'Ursula', 'Vicky', 'Wendy', 'Xander', 'Yvonne', 'Zach']

last_names = ['Adams', 'Brown', 'Clark', 'Davis', 'Edwards', 'Foster', 'Gomez', 'Harris', 'Ivanov', 'Johnson', 'Kim', 'Lopez', 'Martin', 'Nguyen', 'Olsen', 'Parker', 'Quinn', 'Rivera', 'Smith', 'Taylor', 'Upton', 'Vargas', 'Walker', 'Xu', 'Young', 'Zhang']


conn = psycopg2.connect(database="new", user="nvkhoan", password="asdf", host="localhost", port="5432")

def populate_cabinet_table(conn, r,c):
    """Populate the Cabinet table with random data.

    Args:
        conn: A psycopg2 database connection object.
        num_rows: The number of rows to insert into the table.
    """
    cur = conn.cursor()
    cur.execute("DELETE FROM cabinet")
    list_userid = random.sample(range(1, 50), 15)
    this_date=datetime.datetime.now().date()
    for y in range(r):
        for x in range(c):
            coord = json.dumps({'x': x, 'y': y})
            id = y * c + x + 1
            aval = random.choice([True, False])
            if aval==False and len(list_userid)!=0:
                open=False
                start = datetime.time(
                    random.randint(7, 21),
                    random.randint(0, 59),
                    random.randint(0, 59)
                )
                start = datetime.datetime.combine(this_date,start)
                userid=list_userid.pop(0)
            else:
                aval=True
                open = False
                start = None
                userid = None 
            cur.execute("INSERT INTO Cabinet (ID, coord, avail, open, start, userid) VALUES (%s, %s, %s, %s, %s, %s)", (id, coord, aval, open, start, userid))
    conn.commit()
def populate_customer_table(conn, num):
    cur = conn.cursor()
    cur.execute("DELETE FROM customer")
    for id in range (1,num+1):
        fn=random.choice(first_names)
        ln=random.choice(last_names)
        name=fn+" "+ln
        email=fn.lower()+"."+ln.lower()+str(id)+"@example.com"
        password="somerandomnumber"
        photo=str(id)+".png"
        cur.execute("INSERT INTO customer (id,name,email,password,photo) VALUES (%s,%s,%s,%s,%s)",(id,name,email,password,photo))
    conn.commit()
# populate_customer_table(conn,50)
def populate(conn,num_rentals):
    cur = conn.cursor()
    cur.execute("DELETE FROM cabinet_locker_rentals")
    cabinetIDs = [i for i in range(1,61)]
    customerIDs = [i for i in range (1,51)]
    paymentMethods = ['credit', 'cash', 'banking','ewallet']
    for i in range (0,num_rentals):
        cabinetID = random.choice(cabinetIDs)
        customerID = random.choice(customerIDs)
        rentdate = datetime.datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        duration = timedelta(hours=random.randint(1,5),minutes=random.randint(0,59))
        paymentMethod = random.choice(paymentMethods)
        hours = duration.total_seconds() // 3600  # get the total hours in the duration
        if duration.total_seconds() % 3600 > 0:  # check if there are any remaining minutes
            hours = math.ceil(hours)  # round up to the next hour if there are remaining minutes
        fee = 15000 * hours  # calculate the fee based on the rounded-up duration
        cur.execute("INSERT INTO Cabinet_Locker_Rentals (ID, cabinetID, CustomerID, rentdate, duration, paymentMethod, fee) VALUES (%s, %s, %s, %s, %s, %s, %s)", (i+1, cabinetID, customerID, rentdate, duration, paymentMethod, fee))
    conn.commit()
    cur.close()
    conn.close()
populate_customer_table(conn,50)
populate_cabinet_table(conn,3,20)
populate (conn,20)