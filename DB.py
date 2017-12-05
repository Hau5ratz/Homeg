import sqlite3
import os
import time
from geopy.geocoders import Nominatim
import sys


class DB():
    def __init__(self, owner, db):
        self.db = db
        self.owner = owner

    def __enter__(self):
        if os.path.exists(self.db):
            self.owner.conn = sqlite3.connect(self.db)
            self.owner.c = self.owner.conn.cursor()
        else:
            print('database does not exist')
            exit()

    def __exit__(self, type, value, traceback):
        self.owner.conn.commit()
        self.owner.conn.close()

class DBM():
    def __init__(self, db):
        self.db = db
        with DB(self, self.db):
            self.knownids = self._IDknown()
            self.t = self._namet()
            self.bin1 = dict()
            self.bin2 = dict()
            self.geo = Nominatim()
            self.gon = True
            if 'NO' not in self.CUNknown:
                x = ['NO', 'No information']
                self._update('country', x)
                self.CUNknown.append('NO')

    def columns(self, table):
        '''
        Gives the column names of a give table
        '''
        insert = '''
                PRAGMA
                table_info(%s)
                ''' % table
        self.c.execute(insert)
        return [x[1] for x in self.c]

    def update(self, dc):
        '''
        I'm actually going to do this iota by iota of conversation
        SO i should probably have two running versions of update
        3 versions of update
        a scribe
        a meta
        a session ledger
        '''

                insert = [int(key),
                          value["Description"],
                          value["Basic Skills"],
                          value["Pref Skills"],
                          value["Title"]]

                self._update(self.t[-5], insert)
            self.knownids = self._IDknown()

    def _update(self, tname, values, e=False):
        '''
                Get's a dictionary in the format:

                {key:dick}
                dick = {columnn:columnv}
        '''
        try:
            columns = self.columns(tname)

            ######################
            # Sanatize:
            values = [v.replace("'", "") if isinstance(
                v, str) else v for v in values]
            values = [v if isinstance(v, int) else "'" +
                      v + "'" for v in values]
            #####################
            insert = '''INSERT INTO %s '''
            col = '(%s' + (', %s' * (len(columns) - 1)) + ')'
            val = ' VALUES (%s' + (', %s' * (len(values) - 1)) + ')'
            inject = insert % tname
            inject += col % tuple(columns)
            inject += val % tuple(values)
            self.c.execute(inject)
        except sqlite3.IntegrityError as ex:
            print(ex)
            print('dump:')
            print(tname)
            print(values)
            print(self.t)
            print(self.knownids)
            print(values[0])
            print(values[0] in self.COMknown)
            raise Exception
            exit()

    def pull(self, tname, values, e=False):
        with DB(self, self.db):
            columns = self.columns(tname)

            ######################
            # Sanatize:
            values = [v.replace("'", "") if isinstance(
                v, str) else v for v in values]
            values = [v if isinstance(v, int) else "'" +
                      v + "'" for v in values]
            #####################
            insert = '''SELECT FROM %s '''
            col = '(%s' + (', %s' * (len(columns) - 1)) + ')'
            val = ' VALUES (%s' + (', %s' * (len(values) - 1)) + ')'
            inject = insert % tname
            inject += col % tuple(columns)
            inject += val % tuple(values)
            self.c.execute(inject)


    # Sanatizers

    # Data pullers
    
    # Just keeping some of these as examples

    def _IDknown(self):
        insert = '''
                SELECT ID
                FROM active_jobs
                '''
        self.c.execute(insert)
        return [x[0] for x in self.c]

    def _COknown(self):
        insert = '''
                SELECT comp_ID, name
                FROM companies
                '''
        self.c.execute(insert)
        return {x[1]: x[0] for x in self.c}

    def _namet(self):
        insert = '''
                SELECT name
                FROM sqlite_master
                WHERE type="table"
                '''
        self.c.execute(insert)
        return [x[0] for x in self.c]

    def _catlearn(self):
        insert = '''
                SELECT cat_id, name
                FROM categories
                '''
        self.c.execute(insert)
        return {x[1]: x[0] for x in self.c}

    # Extranious

    def _exit(self):
        self.conn.close()
        sys.exit(0)
