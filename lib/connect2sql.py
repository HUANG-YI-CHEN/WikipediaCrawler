#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pymssql
import psycopg2

class MSSQL:
    """ [class] """

    def __init__( self, hostname, username, password, database ):
        """ [construct] """
        self.hostname = hostname
        self.username = username
        self.username = username
        self.password = password
        self.database = database
        self.cursor = self.__Connect()

    def __Connect( self ):
        """ [private] Returns class pymssql.connect().coursor(), Get Connection """
        if not self.database :
            raise(NameError,"Not Set Database Info .")
        
        self.connect = pymssql.connect( host = self.hostname, user = self.username, password = self.password, database = self.database, charset="utf8")
        cursor = self.connect.cursor()

        if not cursor:
            raise(NameError,"Connect Database Failed .")
        else:
            return cursor
        
    def ExecQuery( self, sql ):
        """ [public] Returns list, Fetech all select guery  """
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def ExecNonQuery( self, sql ):
        """ [public] No Returns, Excute ( insert, delete, update, stored procedure )  """
        self.cursor.execute(sql)
        self.connect.commit()

    def ExecNonQueryMany( self, sql, args ):
        """ [public] No Returns, Excute ( insert, delete, update, stored procedure )  """
        cursor.executemany(sql,args)
        self.connect.commit()

    def Close( self ):
        """ [public] No Returns, Close database Connect   """
        self.connect.close()

class PGSQL:
    """ [class] """

    def __init__( self, hostname, username, password, database ):
        """ [construct] """
        self.hostname = hostname
        self.username = username
        self.password = password
        self.database = database        
        self.cursor = self.__Connect()

    def __Connect( self ):
        """ [private] Returns class psycopg2.connect.coursor(), Get Connection """
        if not self.database :
            raise(NameError,"Not Set Database Info .")
        
        self.connect = psycopg2.connect("dbname="+ self.database +" user="+ self.username +" host="+ self.hostname +" password="+ self.password)
        cursor = self.connect.cursor()

        if not cursor:
            raise(NameError,"Connect Database Failed .")
        else:
            return cursor

    def ExecQuery( self, sql ):
        """ [public] Returns list, Fetech all select guery  """
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def ExecNonQuery( self, sql ):
        """ [public] No Returns, Excute ( insert, delete, update, stored procedure )  """
        self.cursor.execute(sql)
        self.connect.commit()

    def Close( self ):
        """ [public] No Returns, Close database Connect   """
        self.connect.close()

# def test():
#     sqlserver = MSSQL( hostname='',username='', password='',database='' )
#     sql = ' select top 1 * from object '
#     results = sqlserver.ExecQuery( sql )
#     print (results)
#     sqlserver.Close()

# if __name__ == '__main__':
#     test()