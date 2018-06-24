import sys, os

if_total,character = False, '*'
score_file = None
arguments = []

for arg in sys.argv[1:]:
if str(arg) == '--total':
if_total = True
elif str(arg[:11]) == '--character':
character = str(arg[12])
else:
arguments.append(arg)

if not len(arguments):
print("No score file specified.")
sys.exit()

for arg in arguments:
if os.path.isfile( arg):
score_file = arg
else:
print("Invalid path to score file.")
sys.exit()

file = open(score_file, 'r')
score = file.readlines()
n_lines = len(score)
file.close()

channels = []
inner_array = []
for line in score:
line = line.strip()
if line[0] == '|':
inner_array.append(line)
else:
inner_array = []
channels.append(inner_array)
inner_array.append(line)

channels_upd = []
for one_chanel in channels:
inner_array = []
for line in one_chanel:
line = line.replace('*', '1').replace('-', '0')
add = line[1:-1] if line.startswith('|') else line
inner_array.append(line)
channels_upd.append(inner_array)
channels = channels_upd

score_instruments = [line.strip() for line in score if not line.startswith('|')]

for inst in score_instruments:
if not inst.startswith('|') and inst not in os.listdir("instruments"):
print("Unknown source.")
sys.exit()

total_channels = []
for channel in channels:
x_array = []
inst = channel[0]
amplitude = None

with open('instruments/%s' % inst, 'r') as file:
    amplitude = len(file.readlines())

file = open('instruments/%s' % inst, 'r')
coords, values = {}, {}

if amplitude > 0:
    for i in range(amplitude):
        line = file.readline().rstrip()
        symbols = []
        for symbol in enumerate(line):
            symbols.append(symbol)
            for coordinate in symbols:
                if coordinate[1] == ' ':
                    symbols.remove(coordinate)
                elif coordinate[1] == '\t':
                    symbols.remove(coordinate)
            negative = False
            if symbols[0][1] == '-':
                negative = True
            t_array = [int(coordinate[0]) for coordinate in symbols if int(coordinate[0]) > 1]
            x_coord_list = [t - 3 for t in t_array] if negative else [t - 2 for t in t_array]
        y_str_values = {}
        if not negative:
            y_value = int(symbols[0][1])
            y_str_values[y_value] = ' ' + str(y_value)
        else:
            y_value = (int(symbols[1][1]) * -1)
            y_str_values[y_value] = str(y_value)

        for i in x_coord_list:
            values[i] = y_value

    max_value, min_value = max(values.values()), min(values.values())

    for i in range(1, len(channel)):
        count, carray = 0, []
        for z in channel[i]:
            count = (count + 1) if z == '1' else 0
            carray.append(count)
            inner_array = []
            for h in carray:
                item = '0' if not h else '1'
                inner_array.append(item)
            inner_array = ''.join(inner_array)
        channel.append(inner_array)
        channel.remove(channel[1])

    for sub_channel in channel:
        x = -1
        for n in range(len(sub_channel)):
            x = (x + 1) if sub_channel[n] == '1' else -1
            item = x if sub_channel[n] == '1' else 0
            x_array.append((n, item))

    values = list(values.items())
    values_flip = [(_[1], _[0]) for _ in values]

    inner_array = []
    for xl in x_array:
        inner_array.extend([(xl[1],x[1]) for x in values_flip if x[0] == xl[1]])

    rows = []
    for row_number in range(min_value, max_value + 1):
        row = [row_number]
        row.extend([n for n in values_flip if n[0] == row_number])
        rows.append(row)
    rows = rows[::-1]

    coordinates = []
    for coordinate in rows:
        coordinates.extend([(n, coordinate[0]) for n in coordinate[1:]])
    values = sorted(values, key=lambda lba_arg: lba_arg[0])

upd = []
for coordinate in x_array:
    upd.extend([(coordinate[0], x[1]) for x in values if coordinate[1] == x[0]])

xv_dict = {}
for coordinate in upd:
    key = coordinate[0]
    xv_dict[key] = xv_dict.get(key, 0) + coordinate[1]

values_channels = []
for key, value in xv_dict.items():
    values_channels.append((key, value))

for n in range(1, len(values_channels)):
    diff = values_channels[n][1] - values_channels[n - 1][1]
    if diff > 1:
        values_channels.extend([(n, values_channels[n][1] - i) for i in range(1, diff)])
    elif diff < -1:
        values_channels.extend([(n, values_channels[n][1] - i - 1) for i in range(diff, 0)])

my_flip_array = [(_[1], _[0]) for _ in values_channels]
my_flip_array = (sorted(my_flip_array, key=lambda lba_arg: lba_arg[0]))[::-1]

y_values = [coordinate[0] for coordinate in my_flip_array]
x_values = []
for row_number in range(max(y_values, default=0), min(y_values, default=0) - 1, -1):
    x = [row_number]
    x.extend([n[1] for n in my_flip_array if n[0] == row_number])
    x_values.append(x)
x_max = []
for numbers in x_values:
    x_max.extend([_ for _ in numbers])
x_max = max(x_max, default=0)

if not if_total and x_max > 0:
    print("{}:".format(inst))
for number in x_values:
    for x_coord in number[1:]:
        line = [(" " + str(number[0])), ":", "\t"] if number[0] >= 0 else [str(number[0]), ":", "\t"]

    for n in range(x_max + 1):
        item = character if n in number[1:] else " "
        line.append(item)
    if not if_total and x_max > 0:
        print(str(''.join(line)))
total_channels.append(values_channels)
if if_total:
print("if_Total:")
total_channels = []
for channel in total_channels:
for coord in channel:
total_channels.append(coord)
total_values_dict = {}
for coordinate in total_channels:
key = coordinate[0]
total_values_dict[key] = total_values_dict.get(key, 0) + coordinate[1]

total_channels = [(key, value) for key, value in total_values_dict.items()]
for n in range(1, len(total_channels)):
    diff = total_channels[n][1] - total_channels[n - 1][1]
    if diff > 1:
        for i in range(1, diff):
            total_channels.append((n, total_channels[n][1] - i))
    elif diff < -1:
        for i in range(diff, 0):
            total_channels.append((n, total_channels[n][1] - i - 1))

total_vc_flip = [(_[1], _[0]) for _ in total_channels]
total_vc_flip = (sorted(total_vc_flip, key=lambda lba_arg: lba_arg[0]))[::-1]

y_values = [coordinate[0] for coordinate in total_vc_flip]
x_values = []
for row_number in range(max(y_values, default=0), min(y_values, default=0) - 1, -1):
    x = [row_number]
    x.extend([n[1] for n in total_vc_flip if n[0] == row_number])
    x_values.append(x)

for number in x_values:
    line = [str(number[0]), ":", "\t"] if number[0] < 0 else [(" " + str(number[0])), ":", "\t"]
    x_max = [coord[1] for coord in total_vc_flip]
    for n in range(max(x_max, default=0) + 1):
        item = character if n in number[1:] else " "
        line.append(item)
    if max(x_max, default=0) > 0:
        print(str(''.join(line)))
