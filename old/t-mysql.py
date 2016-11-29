import MySQLdb
import MySQLdb.cursors

conn1 = conn = MySQLdb.connect(
    host = '127.0.0.1',
    user = 'root',
    passwd = 'root',
    db = 'test',
    charset='utf8',
    cursorclass= MySQLdb.cursors.SSDictCursor)

sql = 'select * from users limit 10';
try:
        cur = conn1.cursor()
        cur.execute(sql)
        results = cur.fetchall()
except MySQLdb.Error, e:
        print e
	conn1.rollback()

for result in results:
	print result['user_id'], result['user_name'], result['email']