import sqlite3



con = sqlite3.connect("main.db",check_same_thread=False)
cur = con.cursor()


cur.execute("alter table users add column 'LastGrow' ")


con.commit()