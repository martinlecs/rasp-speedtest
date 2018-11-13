from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from server import st
import sqlite3


class SQLiteDBConnection:

    def __init__(self, dbpath):
        self._dbpath = dbpath
        self._conn = None

    def __enter__(self):
        self._conn = sqlite3.connect(self._dbpath)
        self._conn.cursor().execute('''CREATE TABLE IF NOT EXISTS results 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp, download, upload, ping, server, ip, isp)''')
        self._conn.commit()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._conn.close()

    def insert_row(self, data):
        self._conn.cursor().execute('''INSERT INTO results (timestamp, download, upload, ping, server, ip, isp) 
            VALUES (?,?,?,?,?,?,?)''', data)
        self._conn.commit()

    def dump_table(self):
        c = self._conn.cursor()
        c.execute("SELECT * FROM results")
        return c.fetchall()

with SQLiteDBConnection('/Users/martinle/Projects/rasp-speedtest/store.db') as spd_test:
    st.get_best_server()
    st.download()
    st.upload()
    results = [st.results.dict()['timestamp'], st.results.dict()['download'], st.results.dict()['upload'],
               st.results.dict()['ping'], st.results.dict()['server']['name'], st.results.dict()['client']['ip'],
               st.results.dict()['client']['isp']]
    spd_test.insert_row(results)
    spd_test.dump_table()

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=run_speed_test, trigger="interval", minutes=15)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())


