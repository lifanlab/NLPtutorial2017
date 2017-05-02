import sys
print("Hello World")

my_int = 4
my_float = 2.5
my_string = "hello"

print("string: %s\tfloat: %f\t int: %d" % (my_string, my_float, my_int))

my_variable = 4
if my_variable == 4:
    print("my variable is not 4")
else:
    print("my_variable is not 4")

for i in range(1, my_variable):
    print("i == %d" %(i))

from collections import defaultdict
my_dict = defaultdict(lambda: 0)
my_dict["eric"] = 33
print(my_dict["eric"])
print(my_dict["fred"])

for foo, bar in sorted(my_dict.items()):
  print("%s --> %r" % (foo,bar))


my_file = open(sys.argv[1], "r")
for line in my_file:
  line = line.strip()
  if len(line) != 0:
    print(line)
