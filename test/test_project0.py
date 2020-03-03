import project0
import sqlite3

url = "http://normanpd.normanok.gov/filebrowser_download/657/2020-02-27%20Daily%20Incident%20Summary.pdf"


def test_fetchincidents():
      assert project0.fetchincidents(url) is not None


def test_extractincidents():
      temp_file = project0.fetchincidents(url)
      result = project0.extractincidents(temp_file)
      for i in result:
            assert len(i) >1

def test_createdb():
      assert project0.createdb() == 'norman.db'


def test_populatedb( ):
      temp_file = project0.fetchincidents(url)
      incidents = project0.extractincidents(temp_file)
      db = project0.createdb()
      project0.populatedb(db, incidents)
      database = sqlite3.connect(db)
      db = database.cursor()
      db.execute('select * from incidents;' )
      result = db.fetchall()
      for i in result:
         assert len(i) == 5


def test_status( ):
      temp_file = project0.fetchincidents(url)
      incidents = project0.extractincidents(temp_file)
      db = project0.createdb()
      project0.populatedb(db, incidents)
      result = project0.status(db)
      for i in result:
         assert len(i) > 0



