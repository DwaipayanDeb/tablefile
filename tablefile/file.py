
#v0.1.1
from math import *
class file:

    def __init__(self,filename,*separator):   # * symbol before separator makes it optional variable for user while creating the object (also it allows more than one sparator values)
        self.filename=filename
        self.separator=separator
        if len(self.separator) != 0 and self.separator[0] is not None:
            self._validate_separator(self.filename, self.separator[0])
        try:
            f=open(self.filename,"r+")
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found. Please check the path.")
            import sys
            sys.exit(0)
        except Exception as e:
            print(f"Error opening file '{self.filename}': {e}")
            import sys
            sys.exit(0)
        lineno=0
        for lns in f.readlines():
            if not lns[0:1]=="#" and not lns[0:1]=="\n":
                lineno+=1
        self.lines=lineno #len(f.readlines())
       # print(len(self.lines))
        f.close()
        
    def _validate_separator(self, filename, sep):
        """Validate that the provided separator splits the first line into multiple fields."""
        try:
            with open(filename, 'r') as fh:
                for line in fh:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    parts = line.split(sep)
                    if len(parts) <= 1:
                        raise ValueError(
                            f"The separator '{sep}' does not appear to split the input file '{filename}'. "
                            "Please provide the correct delimiter for the file format."
                        )
                    break
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: {filename}")
        except UnicodeDecodeError:
            raise ValueError(f"Unable to read file '{filename}'. Please ensure it is a text file.")

    def _parse_val(self, s):
        try:
            stripped = s.strip()
            if '.' in stripped:
                return float(stripped)
            else:
                return int(stripped)
        except ValueError:
            return s

    def _validate_op(self, operator):
        valid_ops = (
            "l/c", "line/col",
            "c/l", "col/line",
            "av", "average",
            "sm", "sum",
            "sd", "sigma",
            "sds", "sigma_sample",
            "mx", "maximum",
            "mn", "minumum"
        )
        if len(operator) > 0:
            op = operator[0]
            if op not in valid_ops:
                print(f"Error: Invalid operator '{op}'. Valid operators are: {', '.join(valid_ops)}")
                import sys
                sys.exit(0)

    def readlines(self, *operator):
        self._validate_op(operator)
        colArgs = []
        with open(self.filename, "r") as f:
            lines = f.readlines()
        if len(self.separator) != 0:
            sep = self.separator[0]
        else:
            sep = None
        
        raw_lines = []
        max_cols = 0
        for ln in lines:
            if not ln[0:1] == "#" and not ln[0:1] == "\n":
                a = ln.split(sep)
                for i in range(len(a)):
                    a[i] = self._parse_val(a[i])
                raw_lines.append(a)
                if len(a) > max_cols:
                    max_cols = len(a)
                    
        for a in raw_lines:
            while len(a) < max_cols:
                a.append("?")
            colArgs.append(a)
            
        if len(operator) == 0:
            return colArgs
            
        op = operator[0]
        if op in ("l/c", "line/col"):
            return colArgs
            
        opRow = []
        [opRow.append([]) for ax in range(len(colArgs))]
        
        if op in ("av", "average"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    opRow[i] = sum(row_nums) / len(row_nums)
                except:
                    opRow[i] = "Error"
        elif op in ("sm", "sum"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    opRow[i] = sum(row_nums)
                except:
                    opRow[i] = "Error"
        elif op in ("sd", "sigma"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    mean = sum(row_nums) / len(row_nums)
                except:
                    opRow[i] = "Error"
                    continue
                temp_list = []
                for val in row_nums:
                    try:
                        temp_list.append((val - mean) ** 2)
                    except:
                        pass
                try:
                    opRow[i] = (sum(temp_list) / len(temp_list)) ** 0.5
                except:
                    opRow[i] = "Error"
        elif op in ("sds", "sigma_sample"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    mean = sum(row_nums) / len(row_nums)
                except:
                    opRow[i] = "Error"
                    continue
                temp_list = []
                for val in row_nums:
                    try:
                        temp_list.append((val - mean) ** 2)
                    except:
                        pass
                try:
                    opRow[i] = (sum(temp_list) / (len(temp_list) - 1)) ** 0.5
                except:
                    opRow[i] = "Error"
        elif op in ("mx", "maximum"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    opRow[i] = max(row_nums)
                except:
                    opRow[i] = "Error"
        elif op in ("mn", "minumum"):
            for i in range(len(opRow)):
                row_nums = [val for val in colArgs[i] if not type(val) == str]
                try:
                    opRow[i] = min(row_nums)
                except:
                    opRow[i] = "Error"
        elif op in ("c/l", "col/line"):
            return self.readcols()
            
        return opRow

    def readcols(self, *operator):
        self._validate_op(operator)
        colArgs = self.readlines()
        if len(colArgs) == 0:
            return []
            
        op = operator[0] if len(operator) > 0 else "c/l"
        
        if op in ("l/c", "line/col"):
            return colArgs
            
        opCol = []
        [opCol.append([]) for ax in range(len(colArgs[0]))]
        
        if op in ("av", "average"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    opCol[i] = sum(opCol[i]) / len(opCol[i])
                except:
                    opCol[i] = "Error"
        elif op in ("sm", "sum"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    opCol[i] = sum(opCol[i])
                except:
                    opCol[i] = "Error"
        elif op in ("sd", "sigma"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    mean = sum(opCol[i]) / len(opCol[i])
                except:
                    opCol[i] = "Error"
                    continue
                
                opCol[i] = []
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        try:
                            opCol[i].append((colArgs[j][i] - mean) ** 2)
                        except:
                            pass
                try:
                    opCol[i] = (sum(opCol[i]) / len(opCol[i])) ** 0.5
                except:
                    opCol[i] = "Error"
        elif op in ("sds", "sigma_sample"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    mean = sum(opCol[i]) / len(opCol[i])
                except:
                    opCol[i] = "Error"
                    continue
                
                opCol[i] = []
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        try:
                            opCol[i].append((colArgs[j][i] - mean) ** 2)
                        except:
                            pass
                try:
                    opCol[i] = (sum(opCol[i]) / (len(opCol[i]) - 1)) ** 0.5
                except:
                    opCol[i] = "Error"
        elif op in ("mx", "maximum"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    opCol[i] = max(opCol[i])
                except:
                    opCol[i] = "Error"
        elif op in ("mn", "minumum"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    if not type(colArgs[j][i]) == str:
                        opCol[i].append(colArgs[j][i])
                try:
                    opCol[i] = min(opCol[i])
                except:
                    opCol[i] = "Error"
        elif op in ("c/l", "col/line"):
            for i in range(len(opCol)):
                for j in range(len(colArgs)):
                    opCol[i].append(colArgs[j][i])
                    
        return opCol

    def read(self, *operator):
        if len(operator) == 0:
            return self.readlines()
        return self.readcols(*operator)

    def write(self, lineNo, ColNo, value):
        with open(self.filename, "r") as f:
            lines = f.readlines()
        
        if len(self.separator) != 0:
            sep = self.separator[0]
        else:
            # Dynamically detect if tab is used in the file
            sep = None
            for ln in lines:
                if "\t" in ln:
                    sep = "\t"
                    break
            if sep is None:
                sep = " "
            
        data_line_indices = []
        for idx, ln in enumerate(lines):
            if not ln[0:1] == "#" and not ln[0:1] == "\n":
                data_line_indices.append(idx)
                
        try:
            target_idx = data_line_indices[lineNo]
        except IndexError:
            print(f"Error: lineNo '{lineNo}' is out of range. The file has {len(data_line_indices)} data lines (0 to {len(data_line_indices)-1}).")
            import sys
            sys.exit(0)
            
        ln = lines[target_idx]
        ln_clean = ln.rstrip('\r\n')
        line_ending = ln[len(ln_clean):]
        
        parts = ln_clean.split(sep)
        
        if ColNo < 0:
            ColNo = len(parts) + ColNo
            if ColNo < 0:
                print(f"Error: ColNo '{ColNo}' is out of range for this line which has {len(parts)} columns.")
                import sys
                sys.exit(0)
                
        while len(parts) <= ColNo:
            parts.append("?")
            
        parts[ColNo] = str(value)
        lines[target_idx] = sep.join(parts) + line_ending
        
        with open(self.filename, "w") as f:
            f.writelines(lines)

            
def convert(List,expression):
    a=[] 
    for itm in List:
        if isinstance(itm,list):
            print('Convert error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('Convert error: Not a list input. Correct input- convert(list,experssion). Example- convert([4,7,"abc",20],"(x**2+1)/5")')
        return   
    for item in List:
        if type(item)!=str:
            x=item
            try:
                a.append(eval(expression))
            except:
                print('Convert error: Could not complete operation')
        else:
            a.append(item) 
    return a
def sd(List):
    for itm in List:
        if isinstance(itm,list):
            print('sd error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sd error: Not a list input.')
        return
    sum=0
    ssum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    try:
        avg=sum/Num
        for item in List:
            if not isinstance(item,str):
                ssum=ssum+(item-avg)**2

        return (sqrt(ssum/Num))
    except ZeroDivisionError:
        print("sd error: No numeric elements in the input list to compute standard deviation.")
        import sys
        sys.exit(0)
def sds(List):
    for itm in List:
        if isinstance(itm,list):
            print('sd error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sd error: Not a list input.')
        return
    sum=0
    ssum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    try:
        avg=sum/Num
        for item in List:
            if not isinstance(item,str):
                ssum=ssum+(item-avg)**2

        return (sqrt(ssum/(Num-1)))
    except ZeroDivisionError:
        print("sds error: Not enough numeric elements to compute sample standard deviation (needs at least 2).")
        import sys
        sys.exit(0)

def av(List):
    for itm in List:
        if isinstance(itm,list):
            print('av error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('av error: Not a list input.')
        return
    sum=0
    Num=0
    for item in List:
        if not isinstance(item,str):
            sum=sum+item
            Num+=1
    try:
        avg=sum/Num
        return avg
    except ZeroDivisionError:
        print("av error: No numeric elements in the input list to compute average.")
        import sys
        sys.exit(0)
def mx(List):
    for itm in List:
        if isinstance(itm,list):
            print('mx error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('mx error: Not a list input.')
        return
    maxval=-10000000000
    for item in List:
        if not isinstance(item,str):
            if item>maxval:
                maxval=item
    return maxval
def mn(List):
    for itm in List:
        if isinstance(itm,list):
            print('mn error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('mn error: Not a list input.')
        return
    minval=10000000000
    for item in List:
        if not isinstance(item,str):
            if item<minval:
                minval=item
    return minval

def sm(List):
    for itm in List:
        if isinstance(itm,list):
            print('sm error: Input list must be one dimensional.')
            return
    if not isinstance(List,list):
        print('sm error: Not a list input.')
        return
    sumval=0
    for item in List:
        if not isinstance(item,str):
            sumval=sumval+item
    return sumval
    """def lines:
        f=open(self.filename,"r+")
        lines=f.readlines()
        return"""  
    