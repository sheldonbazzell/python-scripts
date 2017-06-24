import csv
input_file = open('tst.csv', 'rb')
output_file = open('out.csv', 'wb')
reader = csv.reader(input_file)
writer = csv.writer(output_file, delimiter=' ', quotechar='"', quoting=csv.QUOTE_ALL)
with open('out.csv', 'w') as f:
    for row in reader:
        if row[0][0] != '=':
            f.write(','.join(row) + "\n")
        else:
            tmp = []
            for i in xrange(len(row)):
                el = row[i]
                operator = el[len(el)-1]
                nums = map(float, el[1:len(el)-1].strip().split(" "))
                if operator == "+":
                    tmp.append(sum(nums))
                elif operator == "-":
                    tmp.append(reduce(lambda s, x: s - x, nums[1:], nums[0]))
                elif operator == "*":
                    tmp.append(reduce(lambda p, x: p * x, nums[1:], nums[0]))
                elif operator == "/":
                    tmp.append(reduce(lambda q, x: q / x, nums[1:], nums[0]))
            f.write(",".join(map(str,tmp)) + "\n")