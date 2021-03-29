# tablefile
A python package for reading tabular data and analysis
# tablefile is a python package for reading a data file with multiple columns separated by space or any other character

Install command: 
---------------
`pip install tablefile`


Use example:
------------
```
from tablefile import file
f1=file("C:/Folder/SubFolder/data-file-name.txt","\t") # Last argument here specifies the column separator (here tab). 
#    or
f1=file("C:/Folder/SubFolder/data-file-name.txt") #If separator is blank or space (" ") one need not specify separator.
lines=[] # An empty list to store lines from the file
cols=[]  # An empty list to store columns from the file 
average=[] # An empty list to store average of column values
sum=[] # An empty list to store summation of column values
sd=[] # An empty list to store standard deviation of column values
max=[] # An empty list to store maximum number among column values
min=[] # An empty list to store minimum number among column values
 
f1.read(lines,"l/c") # or just 'f1.read(lines)'. This will read all the lines and store in 'lines' as list array
f1.read(cols,"c/l")# Will read all the columns and store in 'cols' as list array
f1.read(average,"av")
f1.read(sum,"sm")
f1.read(sd,"sd")
f1.read(max,"mx")
f1.read(min,"mn")
print(lines[i][j]) # Prints column j element of line number i  (e.g. for 1st line i=0 and for 1st column j=0)
print(cols[i][j]) # Prints column i element of line number j  
print("Average=",average,"Sum=",sum,"Sigma=",sd,"Maximum=",max,"Minimum=",min)
```

For details please follow the link https://www.respt.in/p/python-package-tablefile.html
