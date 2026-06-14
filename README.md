# tablefile Package Tutorial (v0.1.2)

`tablefile` is a python package for reading, processing, and modifying tabular data files (separated by tabs, spaces, or any other delimiter) easily for analytical applications.

## Installation
```bash
pip install tablefile
```

---

## What's New in v0.1.2 (Changelog from v0.0.5)

1. **New `readlines()` and `readcols()` APIs**:
   - Replaced legacy cryptic parameter calls like `f1.read('c/l')` and `f1.read('l/c')` with dedicated, readable methods `f1.readcols()` and `f1.readlines()`.
2. **Line-Wise (Row-Wise) Statistics**:
   - `readlines(*operator)` now accepts statistical operators (`"av"`, `"sd"`, `"sm"`, `"mx"`, `"mn"`, etc.) and performs calculations row-wise (line-by-line) instead of column-wise.
3. **Robust Missing-Column Handling (Padding)**:
   - If columns are missing or the file has uneven lines, the package pads them with `"?"` to avoid indexing exceptions, allowing mathematical calculations to proceed while letting users know some columns are missing.
4. **Enhanced Separator Detection & Auto-splitting**:
   - When no separator is specified (e.g. `file("data.txt")`), the package defaults to whitespace splitting (any combination of spaces and tabs). Even if a data separator is not explicitly given, the module is still expected to auto-detect the pattern and give correct results.
5. **Direct File Modifying API**:
   - Added `f1.write(lineNo, ColNo, value)` to replace any element in the file on disk, preserving comments, blank lines, and file delimiters (auto-detected).
6. **Strict Type Preservation**:
   - Elements are parsed preserving their exact types (`int`, `float`, and `str`). For example, integers in the file remain `int` when loaded, instead of being cast to `float` as in `v0.0.5`.
7. **Clean Exception Handling**:
   - Added exception handling. Common errors (missing file, out-of-bounds row/column index, invalid operator name) print clear explanations and exit normally with code `0` instead of throwing a Python traceback stack.

---

## Quick Start Tutorial

### 1. Opening a File
To open a file, import the package and instantiate a `file` object. 

```python
from tablefile import *

# Open a file separated by tabs:
f1 = file("data.txt", "\t")

# Open a file without specifying a separator (even if the data separator is not given, the module is expected to give correct results):
f1 = file("data.txt")
```

### 2. Reading Data
You can read data row-wise (lines) or column-wise.

```python
# Read lines (rows):
# Output is a list of lists representing each data line
lines = f1.readlines()
print(lines[0])     # Prints the first data row: e.g., [1.5, 2, 'abc']

# Read columns:
# Output is a list of lists representing each data column
cols = f1.readcols()
print(cols[0])      # Prints the first column: e.g., [1.5, 3.0, 5.0]

# Backward Compatibility:
# Calling read() without arguments behaves exactly as f1.readlines().
# Calling read("c/l") behaves exactly as f1.readcols().
lines = f1.read()
cols = f1.read("c/l")
```

### 3. Calculating Statistics
You can perform column-wise or line-wise statistical operations. The calculation ignores any strings, empty fields, or missing column values (`"?"`).

**Column-Wise Statistics (using `readcols()` or `read()`):**
```python
averages = f1.readcols("av")     # Column-wise averages
sums = f1.readcols("sm")         # Column-wise sums
stdev_pop = f1.readcols("sd")    # Column-wise population standard deviation
stdev_sam = f1.readcols("sds")   # Column-wise sample standard deviation
maximums = f1.readcols("mx")     # Column-wise maximum values
minimums = f1.readcols("mn")     # Column-wise minimum values

# Backward Compatibility syntax is also supported:
averages = f1.read("av")
```

**Line-Wise (Row-Wise) Statistics (using `readlines()`):**
```python
line_averages = f1.readlines("av")  # Average value for each row
line_sums = f1.readlines("sm")      # Sum value for each row
line_std = f1.readlines("sd")       # Population standard deviation for each row
line_max = f1.readlines("mx")       # Maximum value for each row
line_min = f1.readlines("mn")       # Minimum value for each row
```

### 4. Modifying Data
To replace or insert a value in the file on disk:

```python
# write(lineNo, ColNo, value)
# Example: replace the element at 0-indexed row 2, column 5 with "new_val":
f1.write(2, 5, "new_val")
```
*Note: If `ColNo` exceeds the current columns in that line, the package automatically pads the columns with `"?"` and writes the value, preserving the rest of the file layout (including comments and empty lines).*

---

## Operator Reference Sheet

| Operator | Alias | Description |
| :--- | :--- | :--- |
| `"av"` | `"average"` | Calculates numeric average |
| `"sm"` | `"sum"` | Calculates numeric summation |
| `"sd"` | `"sigma"` | Calculates population standard deviation |
| `"sds"` | `"sigma_sample"` | Calculates sample standard deviation |
| `"mx"` | `"maximum"` | Finds the maximum numeric value |
| `"mn"` | `"minumum"` | Finds the minimum numeric value |
| `"c/l"` | `"col/line"` | Columns format (list of columns) |
| `"l/c"` | `"line/col"` | Lines format (list of lines) |

---

## Detailed Method Reference

### `readlines(*operator)`
- **Arguments**: Optional string operator (`"av"`, `"sm"`, `"sd"`, `"sds"`, `"mx"`, `"mn"`, `"l/c"`, `"c/l"`).
- **Return Type**: `List` (List of lists representing rows, or list of line-wise values if statistics operator is used).
- **Behavior**: Auto-pads missing columns with `"?"`. Preserves numeric/string types.

### `readcols(*operator)`
- **Arguments**: Optional string operator (`"av"`, `"sm"`, `"sd"`, `"sds"`, `"mx"`, `"mn"`, `"l/c"`, `"c/l"`).
- **Return Type**: `List` (List of lists representing columns, or list of column-wise values if statistics operator is used).
- **Behavior**: Transposes rows to columns. Auto-pads missing columns with `"?"`.

### `write(lineNo, ColNo, value)`
- **Arguments**: 
  - `lineNo` (`int`): 0-indexed data line number (ignores comment and empty lines). Supports negative indexes (e.g. `-1` for last line).
  - `ColNo` (`int`): 0-indexed column index. Supports negative indexes.
  - `value` (`Any`): The value to write. The type of the value is preserved exactly when written and read back.
- **Return Type**: `None`
- **Behavior**: Modifies the file on disk. Auto-pads columns with `"?"` if writing out of bounds.

---

## General Helpers (One-Dimensional Lists)
In addition to the file methods, standard functions are exported to compute metrics on any 1D list:

```python
# Convert all numeric elements following a string expression
List_converted = convert(cols[0], '(x**2+sin(x))/2')

# Operations:
Value_sum = sm(cols[0])        # Summation
Value_av = av(cols[0])          # Average
Value_sd = sd(cols[0])          # Population StDev
Value_sd_sample = sds(cols[0])  # Sample StDev
Value_mx = mx(cols[0])          # Maximum
Value_mn = mn(cols[0])          # Minimum
```
*(All standard functions ignore string values during the calculation.)*
