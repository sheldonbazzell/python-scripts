import csv
import sys
import os.path

def parse_input(input_file):
    """Parses file, returns cell values list and dict for cell references."""
    cells, result, lookups = {}, [], []
    operators = {"+":add, "-":subtract, "*":multiply, "/":divide}
    for i in xrange(len(input_file)):
        row, tmp = input_file[i], []
        for j in xrange(len(row)):
            val, key = row[j], chr(j + 97)
            math, ref_to_cell = None, None
            if val and val[0] == "=":
                # try to convert character at index 1 to float to determine
                # if input is mathematical operation or cell reference
                try:
                    math = float(val[1])
                except ValueError:
                    ref_to_cell = val[1:]
                except IndexError:
                    # passed "=" without cell reference
                    val = "missing RPN calculation or cell reference"
                if math:
                    operator = val[len(val)-1]
                    nums = map(float, val[1:len(val)-1].strip().split(" "))
                    if operator in operators:
                        fn = operators[operator]
                        val = fn(nums)
                    else:
                        val = "Invalid operator"
                    if not isinstance(val, ZeroDivisionError):
                        a, b = int(val), float(val)
                        val = int(val) if a == b else float(val)
                elif ref_to_cell:
                    val = ref_to_cell
                    col_to_idx = ord(val[0].lower()) - 97
                    row_to_idx = int(val[1]) - 1
                    location = ((i, j), (row_to_idx, col_to_idx))
                    lookups.append(location)
            tmp.append(val)
        result.append(tmp)
    return [result, lookups]


def calc_references(refs, out_list):
    """Calculate cell references and return updated list."""
    for cell in refs:
        orig, ref = cell[0], cell[1]
        orig_row, orig_col = orig[0], orig[1]
        ref_row, ref_col = ref[0], ref[1]
        out_list[orig_row][orig_col] = out_list[ref_row][ref_col]
    return out_list


# mathematical operations
def add(nums):
    return sum(nums)

def subtract(nums):
    return reduce(lambda s, x: s - x, nums[1:], nums[0])

def multiply(nums):
    return reduce(lambda p, x: p * x, nums[1:], nums[0])

def divide(nums):
    try:
        return reduce(lambda q, x: q / x, nums[1:], nums[0])
    except ZeroDivisionError as e:
        return e


def valid_file(f):
    """Validate that input file exists and is a csv."""
    if f[len(f)-3:] != 'csv':
        f = user_input("Please enter valid csv file: ")
    while not os.path.isfile(f):
        f = user_input("Please enter valid csv file: ")
    return f


def user_input(prompt=None):
    """Prompt user for new file without writing prompt to stdout."""
    if prompt:
        sys.stderr.write(str(prompt))
    return raw_input()


def main():
    f = valid_file(sys.argv[1])
    input_file = open(f, 'rb')
    L = list(csv.reader(input_file))
    out = parse_input(L)
    out_list, out_lookups = out[0], out[1]
    if out_lookups:
        out_list = calc_references(out_lookups, out_list)
    for line in out_list:
        print ",".join(map(str,line))
    input_file.close()


if __name__ == "__main__":
    main()