#!/usr/bin/python
# -*- coding: utf-8 -*-

# DOCS @ http://mysql-python.sourceforge.net/MySQLdb.html#mysqldb
import MySQLdb
import gc

class MyPigFarm:
    # ------------ INITialize database ------------------

    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'Snemeis15'
        self.name = 'documents'
        self.use_unicode = True
        self.charset = 'utf8'


class MyPig:
    # --------------- INITialize table  ------------------

    def __init__(self, database, table):
        
        self.db = database
        self.table = table
        self.columns = self.get_columns()

    def get_columns(self):
        c, conn = self.open()
        
        columns = []
        c.execute('DESCRIBE %s' % self.table)
        fields_info = c.fetchall()

        for i in range(0,len(fields_info)):
            columns.append(fields_info[i][0])

        self.close(c, conn)
        return columns

    # ------------- OPEN, CLOSE connection -------------

    def open(self):
        conn = MySQLdb.connect(host = self.db.host,
                               user = self.db.user,
                               passwd= self.db.passwd,
                               db = self.db.name,
                               use_unicode=self.db.use_unicode, 
                               charset=self.db.charset)  
        c = conn.cursor()
        return c, conn

    def close(self, c, conn):
        conn.commit()
        c.close()
        conn.close()
        gc.collect()

    # ------------- GENERAL SQL-QUERY methods ---------------

    def select(self, column_indexes, ID='', orderby=''):
        c, conn = self.open()

        selected = []
        column_string = ''

        if column_indexes == '*':
            column_string = column_indexes
        else:
            for index in column_indexes:

                true_index = int(index)
                selected.append(self.columns[true_index])

            column_string = ", ".join(selected)
        
        sql = "SELECT %s FROM %s" % (column_string, self.table)
        where = " WHERE ID='%s'" % ID
        order = " ORDER BY %s" % orderby

        if ID != '':
            sql += where
            c.execute(sql)
            select_result = c.fetchone()
        elif orderby != '':
            sql += order
            c.execute(sql)
            select_result = c.fetchall()
        else:
            c.execute(sql)
            select_result = c.fetchall()

        self.close(c, conn)
        return select_result

    def rowupdate(self, columns, values, rowid):
    	c, conn = self.open()

        zipped_string = ''
        modvalue = ''

        for column, value in zip(columns, values):

            if value == 'CURRENT_TIMESTAMP()':
                zipped_string += column + '=' + value + ', '
            else:
                zipped_string += column + '=\'' + value + '\', '
        zipped_string = zipped_string[0:-2]

        sql = ("UPDATE %s SET " % self.table) + zipped_string + (" WHERE ID=%s" % rowid)
        c.execute(sql)

        self.close(c, conn)
        return 'success'

    def opprett_dokument(self, ny_bestilling):
        c, conn = self.open()

        c.execute("INSERT INTO main"
                  "(Tittel, Emne, Forfatter, Opprettet) "
                  "VALUES ('%s', '%s', '%s', "
                  "CURRENT_TIMESTAMP())"
                   % (ny_bestilling['tittel'],
                  ny_bestilling['emne'],
                  ny_bestilling['forfatter']))

        self.close(c, conn)
        return 'success'