from MLNewsArticle import finalDict
import mysql.connector
import json

# Connect to MySQL server
cnxn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password!",
  database="NewsExtractDb"
)


# Create a cursor object
cursor = cnxn.cursor()

# Sample data in string format
lst = finalDict


# Insert data into database
sql = "INSERT INTO dataset (title, summary, link, topic) VALUES (%s, %s, %s, %s)"
params = [(item['title'], item['summary'], item['link'], ', '.join(item['topic'])) for item in lst]
cursor.executemany(sql, params)
cnxn.commit()



'''
cursor.execute("SELECT @@version;") 
row = cursor.fetchone() 
while row: 
    print(row[0])
    row = cursor.fetchone()


# Do the insert
cursor.executemany("""INSERT INTO dataset(id, title, summary, link, topic) VALUES (1, 'add some title', 'add some summary', 'add some link', 'add some topic')""",theNewList)
#commit the transaction
cnxn.commit()




lst = []
for x in theNewList[]

print(columns)

#sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("dbo.Dataset", columns, placeholders)
# valid in Python 3
#cursor.execute(sql, list(theNewList.values()))



# Do the insert
cursor.execute("insert into Dataset (id, title, summary, link, topic) VALUES ('1', 'add some title', 'add some summary', 'add some link', 'add some topic')")
#commit the transaction
cnxn.commit()






sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("dbo.Dataset", columns, placeholders)
# valid in Python 3
cursor.execute(sql, list(theNewList.values()))
'''
