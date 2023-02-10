import pyodbc as po
from MLNewsArticle import finalDict


# Connection variables
server = '127.0.0.1'
database = 'NewsExtractDb'
username = 'sa'
password = 'MyPass@word'

# Connection string
cnxn = po.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
        server+';DATABASE='+database+';UID='+username+';PWD=' + password)
cursor = cnxn.cursor()


#thenewList = finalDict

lst = [{'title':'this a title', 'summary': 'this a summary', 'link': 'this a link', 'topic': "this a topic, this a topic2, this a topic3"}, 
       {'title':'this a title2', 'summary': 'this a summary2', 'link': 'this a link2', 'topic': "this a topic, this a topic2, this a topic3"}, 
       {'title':'this a title3', 'summary': 'this a summary3', 'link': 'this a link3', 'topic': "this a topic, this a topic2, this a topic3"}]

newList = [*[list(idx.values()) for idx in lst]]

print(newList)


cursor.executemany("""
INSERT INTO dbo.Dataset (title, summary, link, [topic]) 
VALUES (?,?,?,?)""",newList)
cnxn.commit()

'''
cursor.execute("""
DELETE FROM dbo.Dataset""")
cnxn.commit()
'''

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
