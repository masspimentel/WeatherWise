import sqlite3

#function used to create tables in db

def weatherDB(db):
    conn = sqlite3.connect('weatherProj\WeatherApp.db')

    cur = conn.cursor()

    cur.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY NOT NULL,
                    username TEXT NOT NULL,
                    salt_password TEXT NOT NULL,
                    hashed_password TEXT NOT NULL,
                    FOREIGN KEY(user_id) REFERENCES userPref(id) ON DELETE CASCADE

                )
    ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS userPref (
                    id INTEGER PRIMARY KEY NOT NULL,
                    phone_num TEXT,
                    city TEXT,
                    country_code TEXT,
                    user_id INTEGER,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    weatherDB('weatherProj\WeatherApp.db')