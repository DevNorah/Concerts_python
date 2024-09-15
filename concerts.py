import sqlite3

# connect to the database
conn = sqlite3.connect('my_concerts.db')
cursor = conn.cursor()

# create bands table
cursor.execute('''CREATE TABLE IF NOT EXISTS bands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    hometown TEXT NOT NULL
)''')

# venues table
cursor.execute('''CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    city TEXT NOT NULL
    
)''')

# concerts table
cursor.execute('''CREATE TABLE IF NOT EXISTS concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER,
    venue_id INTEGER,
    date TEXT,
    FOREIGN KEY (band_id) REFERENCES bands(id),
    FOREIGN KEY (venue_id) REFERENCES venues(id)
)''')

# commit changes
conn.commit()
conn.close()

def seed_database():
    conn = sqlite3.connect('my_concerts.db')
    cursor = conn.cursor()

    # insert bands
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Sauti_sol', 'Nairobi')")
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Elani', 'Nairobi')")
    cursor.execute("INSERT INTO bands (name, hometown) VALUES ('Wakadinali', 'Mombasa')")

    # insert venues
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Quiver', 'Nairobi')")
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Megacity', 'Kisumu')")
    cursor.execute("INSERT INTO venues (title, city) VALUES ('Tunnel', 'Mombasa')")

    # insert concerts
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 1, '2025-12-01')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (2, 2, '2022-02-14')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (1, 3, '2025-04-23')")
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (3, 1, '2025-12-25')")

    conn.commit()
    conn.close()


# object relationship methods
class Concert:
    def __init__(self,concert_id,  band_id, venue_id, date):
        self.id = concert_id  
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date

    @classmethod
    def band(cls, concert_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT bands.id, bands.name, bands.hometown 
                FROM concerts 
                JOIN bands ON concerts.band_id = bands.id 
                WHERE concerts.id = ?
            ''', (concert_id,))
        band = cursor.fetchone()
        return band
    
    @classmethod
    def venue(cls, concert_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
                SELECT venues.id, venues.title, venues.city
                FROM concerts
                JOIN venues ON concerts.venue_id = venues.id
                WHERE concerts.id = ?
            ''', (concert_id,))
        venue = cursor.fetchone()
        return venue
    
    def hometown_show(self):
          conn = sqlite3.connect('my_concerts.db')
          cursor = conn.cursor()
          cursor.execute('''
            SELECT bands.hometown, venues.city
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.id = ?
        ''', (self.id,))
          band_hometown, venue_city = cursor.fetchone()
          return band_hometown == venue_city
    
    def introduction(self):
           conn = sqlite3.connect('my_concerts.db')
           cursor = conn.cursor()
           cursor.execute('''
            SELECT bands.name, bands.hometown, venues.city
            FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.id = ?
        ''', (self.id,))
           band_name, band_hometown, venue_city = cursor.fetchone()
           return f"Hello {venue_city}!!!!! We are {band_name} and we're from {band_hometown}"

        

# band methods
class Band:
    @classmethod
    def concerts(cls, band_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts 
            WHERE band_id = ?
        ''', (band_id,))
        return cursor.fetchall()

    @classmethod
    def venues(cls, band_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT venues.* 
            FROM concerts
            JOIN venues ON concerts.venue_id = venues.id
            WHERE concerts.band_id = ?
        ''', (band_id,))
        return cursor.fetchall()

    @classmethod
    def play_in_venue(cls, band_id, venue_id, date):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO concerts (band_id, venue_id, date) 
            VALUES (?, ?, ?)
        ''', (band_id, venue_id, date))
        conn.commit()

    @classmethod
    def all_introductions(cls, band_id):
           conn = sqlite3.connect('my_concerts.db')
           cursor = conn.cursor()
           cursor.execute('''
            SELECT concerts.id FROM concerts
            WHERE concerts.band_id = ?
        ''', (band_id,))
           concert_ids = cursor.fetchall()
           introductions = []
           for concert_id in concert_ids:
                concert = Concert(concert_id[0], band_id, None, None)  # Create concert object
                introductions.append(concert.introduction())
           return introductions

    @classmethod
    def most_performances(cls):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, COUNT(concerts.id) AS performance_count
            FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            GROUP BY bands.id
            ORDER BY performance_count DESC
            LIMIT 1
        ''')
        return cursor.fetchone()


# venue methods
class Venue:
    @classmethod
    def concerts(cls, venue_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM concerts WHERE venue_id = ?', (venue_id,))
        return cursor.fetchall()

    @classmethod
    def bands(cls, venue_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT bands.* FROM concerts
            JOIN bands ON concerts.band_id = bands.id
            WHERE concerts.venue_id = ?
        ''', (venue_id,))
        return cursor.fetchall()

    @classmethod
    def concert_on(cls, venue_id, date):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts 
            WHERE venue_id = ? AND date = ?
        ''', (venue_id, date))
        return cursor.fetchone()

    @classmethod
    def most_frequent_band(cls, venue_id):
        conn = sqlite3.connect('my_concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT bands.name, COUNT(concerts.id) AS performance_count
            FROM bands
            JOIN concerts ON bands.id = concerts.band_id
            WHERE concerts.venue_id = ?
            GROUP BY bands.id
            ORDER BY performance_count DESC
            LIMIT 1
        ''', (venue_id,))
        results = cursor.fetchone()
        conn.close()
        return results

# Main script
if __name__ == "__main__":
    seed_database()