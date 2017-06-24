# in order to optimize the program, i attempted to use a generator function
# the problem with this approach was that i couldn't account for the forward
# pointing values, as they were yet to be uncovered in the generator object
# thus, i reverted back using a list and a lookup table
# despite being slower, it does successfully parse a csv of 1 million rows

import csv, sys
# in case user runs script w/out valid csv file
# using this function (as opposed to simple raw_input())
# to prevent prompt from being written to stdout
def user_input(prompt=None):
    if prompt:
        sys.stderr.write(str(prompt))
    return raw_input()

f = sys.argv[1]
# if the file extension isn't 'csv', ask for new file name
if f[len(f)-3:] != 'csv':
    f = user_input("Please enter valid csv file: ")

input_file = open(f, 'rb')
L = list(csv.reader(input_file))

alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
vals = {} # cell value lookup table
lookups = [] # to be referenced after vals is fully populated
result = [] # to be printed to stdout

# def parse_input(L):
for i in xrange(len(L)):
    row = L[i]
    tmp = []
    for j in xrange(len(row)):
        val = row[j]
        key = alph[j] + str(i+1)
        if val[0] == '=':
            # try to convert element at index 1 to int
            try:
                int(val[1])
                # it worked, so we're doing a mathematical operation
                operator = val[len(val)-1]
                # parse this element of the csv row
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
                    val = " Not a valid operator"
            # didnt work, so its a cell reference (e.g. C2), add key
            # to 'lookups' list, will use this list after lookup table
            # is complete to account for the cases of forward pointing
            # cell references (e.g. setting cell A1 to D4)
            except ValueError:
                val = val[1:]
        try:
            val = float(val)
        except ValueError:
            pass
        tmp.append(val)
        # add cell value to lookup table
        vals[key] = val
    result.append(tmp)
        # yield tmp
# result = parse_input(L)
for line in result:
    for j in xrange(len(line)):
        if line[j] in vals:
            line[j] = vals[line[j]]
    print ",".join(map(str,line))
input_file.close()