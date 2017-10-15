import sqlite3 as lite
import scraper


class PhoneDataLayer(object):
    def __init__(self, db='numbers.db'):
        con = None
        try:
            con = lite.connect(db)
            with con:
                cur = con.cursor()
                cur.execute("DROP TABLE IF EXISTS Numbers")
                cur.execute(
                    "CREATE TABLE Numbers(number TEXT primary key not null, count INT, comment TEXT, date TEXT)")
        except lite.Error, e:
            raise e
        finally:
            if con:
                con.close()

    def insert_entries(self, entries):
        con = lite.connect('numbers.db')
        with con:
            cur = con.cursor()
            for entry in entries:
                cur.execute('INSERT OR REPLACE INTO Numbers(number, count, comment, date) VALUES (?, ?, ?, CURRENT_TIMESTAMP);', [
                            entry.phone_number, entry.report_count, entry.comment])
        con.close()

    def get_db_entries(self):
        con = lite.connect('numbers.db')
        rows = None
        with con:
            cur = con.cursor()
            cur.execute('SELECT * FROM Numbers ORDER BY date')
            rows = cur.fetchall()

        entries = []
        for row in rows:
            entries[len(entries):] = [
                scraper.PhoneNumberEntry(row[0], row[1], row[2])]

        con.close()
        return entries

    def get_entries(self, count=None, area_code=None):
        parser = scraper.Parser(
            scraper.ValidUAOpener().open(scraper.PHONE_SITE).read())
        entries = parser.parse()
        self.insert_entries(entries)
        return_entries = self.get_db_entries()

        if count is None or count < 1:
            count = 60

        if area_code is not None:
            return_entries = [
                entry for entry in return_entries if entry.area_code == area_code]

        if count <= len(return_entries):
            return_entries = return_entries[:count]

        return return_entries
