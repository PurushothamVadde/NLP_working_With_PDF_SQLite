## Text Analytics project 0  "Norman Database for incidents"

In this project we downloaded the INCIDENTS pdf data from normanpd website and stored the pdf data into database and performed the text search operations. \
The projects have below files: 
## 1.main.py 

The main.py accept the url as input argument, the project0.py is imported into main.py file and execute the below functions by function calling through main.py. 
1. data = project0.fetchincidents(url)
2. incidents = project0.extractincidents(data)
3. db = project0.createdb()
4. project0.populatedb(db, incidents)
5. project0.status(db)

## 2. project0.py
The project file contains the below functions

### **fetchincidents(url)**

This function takes argument as url and using urllib we will read the data from url and the data read is in the form of bytes. The bytes data is stored into the temp_file which is created using the tempfile package, and the function returns the address of the temp_file.

### **extractincidents(temp_file)**

The address of the temp_file is passed as argument to the **extractincidents(temp_file)**, by using the PdfFileReader method in PyPDF2 package the bytes data is read and stored in pdfReader, from the pdfReader the data is extracted  and stored in the page using **extractText()**. The extracted data has five columns values of a incidents table. The extracted data is in form of string and each word is separated with ‘ \n’ and the replaced the ‘ \n’ with blank and stored in pagedata. After replacing the blank the pagedata is splitted into list by using 
> re.split(r"\s+(?=\d+/\d+/\d+\s)", pagedata)

After splitting the list with date we got each list contains the 5 column values separated by \n.

- **Handling the missing values in the list:**

After splitting the data using date regular expression, we have two issue in the list
- **Missing values in incident:**
The incident column has some missing values to handle that we checked the length if each list and added the null value if length of list is less than 5, after adding the null value in the 5th column the 4th and 5th columns are swapped so that the null value is inserted into the incident column

>if (len(pagedata)<5): \
            pagedata.append('null') \
            pagedata[3], pagedata[4] = pagedata[4], pagedata[3]

- **length of list is greater than 5:**
We have few lists where the length of the list has greater than the 5 so we add two conditions if the length is >5 we are removing last value and if length is >6 we are removing two values in the list.

> if (len(pagedata)>6): \
            pagedata.pop() \
            pagedata.pop() \
  if (len(pagedata)>5): \
            pagedata.pop() 
            
After handling the issues, the lists are appended and formed a list with sub lists where each sub list has 5 values of 5 columns from the pdf, we read using URL and the function extractincidents returns the list.

### **createdb()**

The db norman.db is created using the package sqlite3, by **sqlite3.connect ()** creates a db file and using execute function we can execute queries, a table is created in database norman.db using the below query

> **CREATE TABLE IF NOT EXISTS incidents
                (incident_time TEXT,
                incident_number TEXT,
                incident_location TEXT,
                nature TEXT, 
                incident_ori TEXT)**;
                
### **populatedb(db, incidents)**

The list from extractincidents and  db name from created is passed as input parameters to **populated()**, 
In this function we connect to **norman.db** which we created in **created()** and the iterate to each list which we got form the extract incidents and insert each list into the table using below query.

> db.execute(" INSERT INTO  incidents VALUES (?,?,?,?,?);", (incidents[i]))

### **status(db)**
In this function we connect to the norman.db again by taking the input argument as db name and we get each incident and not of times incident occurred using below query.

> db.execute("""SELECT nature ||'|'|| count(*) FROM incidents GROUP BY nature """)

The | is used to separate the incident type and count of incident.


## 3.test_project0.py

The test_project0.py file contains the unit testcases to test each method is working are not which we designed in the project0.py file, in this file we written the below 5 testcases to test each method. we import the project0 file to test access the functions in project.py.

### **test_fetchincidents():**
In this test case we test the fetchincidents method by passing the  URL  to **fetchincidents( )** method and we use the arrest statement test the is returning some value are not, if it returns some value the test case will pass.

      > assert project0.fetchincidents(url) is not None

### **test_extractincidents():**

In this test case we test the extactincidents, the function returns the list where each list has length of 5, we test the function by iterating through each list and check length is >1 or not.

      > temp_file = project0.fetchincidents(url)
      result = project0.extractincidents(temp_file)
      for i in result:
            assert len(i) > 1

### **test_createdb():**

In this testcase we would test the **createdb()**, the createdb method would return the db name if it executed successfully, the assert statement checks the return name is norman.db or not.
  
     > assert project0.createdb() == 'norman.db'

### **test_populatedb( ):**

In this method we test the **populated()** method, to test the method we get the incidents list form extractincidents, dbname  from createdb and pass as the input arguments to the populate db, after  running the populated method we connect to db using sqlite3 and fetch the values and we will check the length of each row should be equal to 5, if the length of each row is equal to 5 then the test case will pass else the test case will  fail. 

      > db.execute('select * from incidents;' )
      result = db.fetchall()
      for i in result:
         assert len(i) == 5

## **test_status( ):**

In this method we test the **status()** by executing all the methods the status () method will return the string of incidents and number of incidents to test this we will iterate to each string and check the length of the string is >0. If the function is not returning the any values the testcase will fail.

     > result = db.fetchall()
       for i in result:
         assert len(i) > 0






