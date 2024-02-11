import sqlite3 

connection=sqlite3.connect("patient.db")

# cursor 
cursor = connection.cursor() 

# table 
table_info = """
Create table PATIENT(NAME VARCHAR(25),AGE INT,ILLNESS VARCHAR(25),BMI FLOAT,ERSTATUS VARCHAR(25)); 
"""

cursor.execute(table_info)
cursor.execute('''Insert Into PATIENT values('Edgar',67,'Diabetes',29.0,'Positive')''')
cursor.execute('''Insert Into PATIENT values('Fiona',79,'Diabetes',22.2,'Negative')''')
cursor.execute('''Insert Into PATIENT values('Alexandria',55,'Flu',27.8,'Positive')''')
cursor.execute('''Insert Into PATIENT values('Gina',28,'Allergies',19.6,'Negative')''')
cursor.execute('''Insert Into PATIENT values('Hans',60,'Diabetes',28.1,'Positive')''')
cursor.execute('''Insert Into PATIENT values('Ian',43,'Allegeries',19.7,'Negative')''')
cursor.execute('''Insert Into PATIENT values('Elon',71,'Diabetes',28.3,'Negative')''')

# insert records 
cursor.execute("")

# display records 
print("The inserted records are")

data=cursor.execute('''Select * from PATIENT''')

for row in data: 
    print(row)

connection.commit()
connection.close() 