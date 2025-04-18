import pymysql

con = None

def connect():
	global con
	con = pymysql.connect(host='localhost', database='appdbproj', user='root', password='', cusorclass=pymysql.cursors.DictCursor) 

# Get birth month function - This checks the input of the month against a dictioonary of months and returns the month number.

                 
    except msql.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        con.close()
        