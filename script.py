import csv
import sys

def parse_input(input_file):
    """Parses file, returns cell values list and dict for cell references."""
    alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    cells, result = {}, []
    for i in xrange(len(input_file)):
        row, tmp = input_file[i], []
        for j in xrange(len(row)):
            val, key, math = row[j], alph[j], None
            if val and val[0] == "=":
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
            tmp.append(val)
            # add cell value to lookup table
            cells.setdefault(key, []).append(val)
        result.append(tmp)
    return [result, cells]


def user_input(prompt=None):
    """If user runs script without a valid csv file, this function
    implements raw_input, but doesn't write prompt to stdout.
    """
    if prompt:
        sys.stderr.write(str(prompt))
    return raw_input()


def main():
    f = sys.argv[1]
    if f[len(f)-3:] != 'csv':
        f = user_input("Please enter valid csv file: ")
    input_file = open(f, 'rb')
    L = list(csv.reader(input_file))
    out = parse_input(L)
    out_list, out_lookup = out[0], out[1]
    for line in out_list:
        for j in xrange(len(line)):
            if line[j] == "Invalid operator":
                continue
            elif type(line[j]) is str and len(line[j]) > 1 and line[j][0] in out_lookup:
                col, row = line[j][0], int(line[j][1]) - 1
                line[j] = out_lookup[col][row]
        print ",".join(map(str,line))
    input_file.close()


if __name__ == "__main__":
    main()