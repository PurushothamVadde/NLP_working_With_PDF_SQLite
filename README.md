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

- Handling the missing values in the list:

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
            pagedata.pop() \
            
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


