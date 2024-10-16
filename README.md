# tablefile package for python for reading a data file with multiple columns separated by space or any other character

Install command: 
---------------
`pip install tablefile`


Use example:
------------
```
from tablefile import *
f1=file("C:/Folder/SubFolder/data-file-name.txt","\t") # Last argument specifies the column separator (here tab). 
#    or
f1=file("C:/Folder/SubFolder/data-file-name.txt") #If separator is a blank-space (" ") one need not specify separator.

lines=f1.read("l/c") # or simply 'f1.read()', by default This will read all the lines and store in 'lines' as list array
cols=f1.read("c/l")# Will read all the columns and store in 'cols' as list array
average=f1.read("av") # Calculates and stores column-wise average values in a list
sum=f1.read("sm") # Calculates and stores column-wise sum values in a list
std=f1.read("sd") # Calculates and stores column-wise standard deviation for a population in a list
stds=f1.read("sds") # Calculates and stores column-wise standard deviation for a sample in a list
min=f1.read("mn") # Calculates and stores column-wise minimum values in a list
max=f1.read("mx") # Calculates and stores column-wise maximum values in a list
print(lines[i][j]) # Prints column j element of line number i  (e.g. for 1st line i=0 and for 1st column j=0)
print(cols[i][j]) # Prints column i element of line number j  
print("Average=",average,"Sum=",sum,"Sigma_population=",std,"Sigma_sample=",stds,"Maximum=",max,"Minimum=",min)

# In the below operations the argument can be any 'list'
List_converted=convert(cols[0],'(x**2+sin(x))/2') # converts elements of a list by following any pre-defined expression
Value_sum=sm(cols[0]) # Summation of numeric elements. 
Value_av=av(cols[0]) # Average of numeric elements. 
Value_sd=sd(cols[0]) # Standard deviation of numeric elements. 
Value_sd_sample=sds(cols[0]) # Standard deviation of numeric elements. 
Value_mx=mx(cols[0]) # Maximum of numeric elements. 
Value_mn=mn(cols[0]) # Minimum of numeric elements. 
print(List_converted,Value_sum,Value_av,Value_sd,Value_sd_sample,Value_mx,Value_mn)

# **In all above cases Strings will be neglected during the calculation**
```

For details please follow the link https://www.researchsquare.com/article/rs-1004075/v2
