import sys
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def executeSingleInsertOrCreate(query, connStr):
    conn = None
    try:
        conn = psycopg2.connect(connStr)
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn:
            conn.close()

def executeSelect(query, connStr):
    conn = None
    try:
        conn = psycopg2.connect(connStr)
        cur = conn.cursor()
        cur.execute(query)
        return cur.fetchall()
    except Exception as e:
        if conn:
            conn.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn:
            conn.close()

def createDatabase(query, connStr):
    conn = None
    try:
        conn = psycopg2.connect(connStr)
        # not possible to create database in transaction mode
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(query)
    except Exception as e:
        print('Error %s' % e)
        sys.exit(1)
    finally:
        if conn:
            conn.close()

def bulkInsert(query, tuples, connStr):
    conn = None
    try:
        conn = psycopg2.connect(connStr)
        cur = conn.cursor()
        cur.executemany(query, tuples)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()

        print('Error %s' % e)
        sys.exit(1)

    finally:
        if conn:
            conn.close()


