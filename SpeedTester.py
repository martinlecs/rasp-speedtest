import globals
import os
import speedtest
import sqlite3


class SQLiteDBConnection:

    def __init__(self, dbpath):
        self._dbpath = dbpath
        self._conn = sqlite3.connect(self._dbpath)
        self._conn.cursor().execute('''CREATE TABLE IF NOT EXISTS results 
            (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp, download, upload, ping, server, ip, isp)''')
        self._conn.commit()

    def insert_row(self, data):
        c = self._conn.cursor()
        c.execute('''INSERT INTO results (timestamp, download, upload, ping, server, ip, isp) 
            VALUES (?,?,?,?,?,?,?)''', data)
        self._conn.commit()

    def dump_table(self):
        c = self._conn.cursor()
        c.execute("SELECT * FROM results")
        return c.fetchall()


class SpeedTester:

    def __init__(self):
        self._db_connection = SQLiteDBConnection(globals.DB_PATH)
        self._st = speedtest.Speedtest()

    def run_speed_test(self):
        """ Runs a speed test on the closest server and saves this information into a SQLite Database """
        self._st.get_best_server()
        self._st.download()
        self._st.upload()
        results = self._st.results.dict()
        data = [results['timestamp'], float(results['download'])/1000000, float(results['upload'])/1000000, results['ping'],
                results['server']['name'], results['client']['ip'], results['client']['isp']]
        self._db_connection.insert_row(data)


if __name__ == "__main__":
    sp = SpeedTester()
    sp.run_speed_test()


