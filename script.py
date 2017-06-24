import csv
input_file = open('tst.csv', 'rb')
reader = csv.reader(input_file)
L = list(reader)
alph = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
vals = {} # cell value lookup table
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
                nums = map(float, val[1:len(val)-1].strip().split(" "))
                if operator == "+":
                    val = sum(nums)
                elif operator == "-":
                    val = reduce(lambda s, x: s - x, nums[1:], nums[0])
                elif operator == "*":
                    val = reduce(lambda p, x: p * x, nums[1:], nums[0])
                elif operator == "/":
                    val = reduce(lambda q, x: q / x, nums[1:], nums[0])
            # didnt work, so try adding this cell's value from dictionary 'vals'
            except ValueError:
                try:
                    val = vals[val[1:]]
                except KeyError:
                    val = 'undefined'
        # this catches cases that didn't go inside initial if
        # i.e. given a value to directly copy over
        tmp.append(val)
        vals[key] = val
    print ",".join(map(str,tmp))