import pymysql

con = None

def connect():
	global con
	con = pymysql.connect(host='localhost', database='appdbproj', user='root', password='', cusorclass=pymysql.cursors.DictCursor) 
