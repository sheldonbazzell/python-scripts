import csv, sys
def user_input(prompt=None):
    """if user runs script w/out valid csv file, this function
    prevents the prompt from being written to stdout
    """
    if prompt:
        sys.stderr.write(str(prompt))
    return raw_input()

def parse_input(input_file):
    """iterates input file and returns list to be printed and
    lookup table used for cell references
    """
    alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cells, result = {}, []
    for i in xrange(len(input_file)):
        row, tmp = L[i], []
        for j in xrange(len(row)):
            val, key = row[j], alph[j] + str(i+1)
            if val[0] == "=":
                # try to convert character at index 1 to float to determine
                # if input is mathematical operation or cell reference
                try:
                    math = float(val[1])
                except ValueError:
                    val = val[1:]
                if math:
                    operator = val[len(val)-1]
                    nums = map(float, val[1:len(val)-1].strip().split(" "))
                    if operator == "+":
                        val = sum(nums)
                    elif operator == "-":
                        val = reduce(lambda s, x: s - x, nums[1:], nums[0])
                    elif operator == "*":
                        val = reduce(lambda p, x: p * x, nums[1:], nums[0])
                    elif operator == "/":
                        val = reduce(lambda q, x: q / x, nums[1:], nums[0])
                    else:
                        val = "Invalid operator"
                    try:
                        a = float(val)
                        b = int(val)
                        if a == b:
                            val = int(val)
                        else:
                            val = float(val)
                    except ValueError:
                        pass
                    math = None
            tmp.append(val)
            # add cell value to lookup table
            cells[key] = val
        result.append(tmp)
    return [result, cells]

def main():
    """passes input file to invocation of parse_input, iterates
    parse_input's return value to print spreadsheet cells to stdout
    """
    f = sys.argv[1]
    if f[len(f)-3:] != 'csv':
        f = user_input("Please enter valid csv file: ")
    input_file = open(f, 'rb')
    L = list(csv.reader(input_file))
    out = parse_input(L)
    out_list, out_lookup = out[0], out[1]
    for line in out_list:
        for j in xrange(len(line)):
            if line[j] in out_lookup:
                line[j] = out_lookup[line[j]]
        print ",".join(map(str,line))
    input_file.close()
main()
