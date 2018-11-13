from abc import abstractmethod, ABC
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from server import st
import sqlite3



class DatabaseManager(ABC):

    def __init__(self, database):
        self._conn = sqlite3.connect(database)
        self._cursor = self._conn.cursor()

    @abstractmethod
    def insert_row(self, data):
        pass


class SpeedTester(DatabaseManager):

    def __init__(self, database):
        super().__init__(database)
        try:
            self._cursor.execute('''CREATE TABLE results (timestamp, download, upload, ping, server, ip, isp)''')
            self._conn.commit()
        except:
            pass
        finally:
            self._conn.close()

    def insert_row(self, data):
        self._cursor.execute('INSERT INTO results VALUES (?,?,?,?,?,?,?)', data)


spd_test = SpeedTester('store.db')


def run_speed_test():
    st.get_best_server()
    st.download()
    st.upload()

    results = {
        'timestamp': st.results.dict()['timestamp'],
        'download': st.results.dict()['download'],
        'upload': st.results.dict()['upload'],
        'ping': st.results.dict()['ping'],
        'server': st.results.dict()['server']['name'],
        'ip': st.results.dict()['client']['ip'],
        'isp': st.results.dict()['client']['isp']
    }

    spd_test.insert_row(results)

# scheduler = BackgroundScheduler()
# scheduler.add_job(func=run_speed_test, trigger="interval", minutes=15)
# scheduler.start()
#
# # Shut down the scheduler when exiting the app
# atexit.register(lambda: scheduler.shutdown())

if __name__ == "__main__":
    run_speed_test()
