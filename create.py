import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect("database.db")
    curr = conn.cursor()
    curr.execute("CREATE TABLE users(user text, password text)")#, pk text)")
    conn.commit()
    conn.close()

    print "Done"
