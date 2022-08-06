import sys
import matplotlib.pyplot as plt

complete_input = sys.stdin.read()
f = (complete_input.split("\n"))

# lines = [line.rstrip() for line in f]
lines = []
for line in f:
    if line != "":
        lines.append(line.rstrip())

OPcode = {"10000": ("add", "A"),
          "10001": ("sub", "A"),
          "10110": ("mul", "A"),
          "11010": ("xor", "A"),
          "11011": ("or", "A"),
          "11100": ("and", "A"),
          "11000": ("rs", "B"),
          "11001": ("ls", "B"),
          "10010": ("mov", "B"),
          "10011": ("mov", "C"),
          "10111": ("div", "C"),
          "11101": ("not", "C"),
          "11110": ("cmp", "C"),
          "10100": ("ld", "D"),
          "10101": ("st", "D"),
          "11111": ("jmp", "E"),
          "01101": ("jgt", "E"),
          "01111": ("je", "E"),
          "01100": ("jlt", "E"),
          "01010": ("hlt", "F"),
          }

registers = {"000": ["R0", 0],
             "001": ["R1", 0],
             "010": ["R2", 0],
             "011": ["R3", 0],
             "100": ["R4", 0],
             "101": ["R5", 0],
             "110": ["R6", 0],
             "111": ["FLAGS", [0, 0, 0, 0]]  # V / L / G / E
             }

mem = ["0000000000000000"] * 256
# print(lines)
# print(mem)
for i in range(len(lines)):
    mem[i] = lines[i]


# print(registers)
# print(mem , len(mem))

def binaryToDecimal(n):
    return int(n, 2)


def a_type(inst):
    flagreset()
    if OPcode[inst[0:5]][0] == "add":

        if registers[inst[7:10]][1] + registers[inst[10:13]][1] > 65535:

            registers[inst[13:]][1] = overflowtobin(registers[inst[7:10]][1] + registers[inst[10:13]][1])
            registers["111"][1][0] = 1

        else:

            registers[inst[13:]][1] = registers[inst[7:10]][1] + registers[inst[10:13]][1]
    elif OPcode[inst[0:5]][0] == "sub":
        if registers[inst[7:10]][1] - registers[inst[13:]][1] < 0:
            registers[inst[13:]][1] = 0
            registers["111"][1][0] = 1
        else:
            registers[inst[13:]][1] = registers[inst[7:10]][1] - registers[inst[10:13]][1]
    elif OPcode[inst[0:5]][0] == "mul":

        if registers[inst[7:10]][1] * registers[inst[10:13]][1] > 65535:
            registers[inst[13:]][1] = overflowtobin(registers[inst[10:13]][1] + registers[inst[7:10]][1])
            registers["111"][1][0] = 1

        else:
            registers[inst[13:]][1] = registers[inst[7:10]][1] * registers[inst[13:]][1]

    elif OPcode[inst[0:5]][0] == "or":
        registers[inst[13:]][1] = registers[inst[7:10]][1] | registers[inst[10:13]][1]

    elif OPcode[inst[0:5]][0] == "and":
        registers[inst[13:]][1] = registers[inst[7:10]][1] & registers[inst[10:13]][1]

    elif OPcode[inst[0:5]][0] == "xor":
        registers[inst[13:]][1] = registers[inst[7:10]][1] & registers[inst[10:13]][1]


def b_type(inst):
    flagreset()

    if OPcode[inst[0:5]][0] == "mov":
        registers[inst[5:8]][1] = binaryToDecimal(inst[8:])

    elif OPcode[inst[0:5]][0] == "rs":
        registers[inst[5:8]][1] = registers[inst[5:8]][1] >> binaryToDecimal(inst[8:])

    elif OPcode[instruction[0:5]][0] == "ls":
        registers[inst[5:8]][1] = registers[inst[5:8]][1] << binaryToDecimal(inst[8:])


def c_type(inst):

    if OPcode[inst[0:5]][0] == "div":
        flagreset()
        print("gg")
        registers["000"][1] = registers[inst[10:13]][1] // registers[inst[13:]][1]

        registers["001"][1] = registers[inst[10:13]][1] % registers[inst[13:]][1]

    elif OPcode[inst[0:5]][0] == "not":

        # r1 = !r2
        # r2 = !r1 need

        flagreset()
        temp = dectobin(registers[inst[10:13]][1])
        temp2 = ""
        for i in temp:
            if i == '0':
                temp2 += '1'
            else:
                temp2 += '0'
        registers[inst[13:]][1] = binaryToDecimal(temp2)


    elif OPcode[inst[0:5]][0] == "cmp":

        if registers[inst[10:13]][1] > registers[inst[13:]][1]:
            registers["111"][1][2] = 1
        elif registers[inst[10:13]][1] < registers[inst[13:]][1]:
            registers["111"][1][1] = 1
        elif registers[inst[10:13]][1] == registers[inst[13:]][1]:
            registers["111"][1][3] = 1

    elif OPcode[inst[0:5]][0] == "mov":

        if inst[13:] == "111":
            registers[inst[10:13]][1] = 8 * registers["111"][1][0] + 4 * registers["111"][1][1] + 2 *registers["111"][1][2] + registers["111"][1][3]
            flagreset()
        elif inst[10:13] == "111":
            registers[inst[13:]][1] = 8 * registers["111"][1][0] + 4 * registers["111"][1][1] + 2 *registers["111"][1][2] + registers["111"][1][3]
        else:
            flagreset()
            registers[inst[13:]][1] = registers[inst[10:13]][1]


def d_type(inst):
    flagreset()
    if OPcode[inst[0:5]][0] == "st":
        mem[binaryToDecimal(inst[8:])] = dectobin(registers[inst[5:8]][1])

    elif OPcode[inst[0:5]][0] == "ld":
        registers[inst[5:8]][1] = binaryToDecimal(mem[binaryToDecimal(inst[8:])])


def e_type(inst):
    global PC
    if OPcode[inst[0:5]][0] == "jmp":
        PC = binaryToDecimal(inst[8:]) - 1

    elif OPcode[inst[0:5]][0] == "jlt" and registers["111"][1][1] == 1:
        PC = binaryToDecimal(inst[8:]) - 1

    elif OPcode[inst[0:5]][0] == "jgt" and registers["111"][1][2] == 1:
        PC = binaryToDecimal(inst[8:]) - 1

    elif OPcode[inst[0:5]][0] == "je" and registers["111"][1][3] == 1:
        PC = binaryToDecimal(inst[8:]) - 1

    flagreset()


def execute(inst):
    if OPcode[inst[0:5]][1] == "A":
        a_type(inst)
    elif OPcode[inst[0:5]][1] == "B":
        b_type(inst)
    elif OPcode[inst[0:5]][1] == "C":
        c_type(inst)
    elif OPcode[inst[0:5]][1] == "D":
        d_type(inst)
    elif OPcode[inst[0:5]][1] == "E":
        e_type(inst)


PC = 0


def printreg():
    print(dectobin(registers["000"][1]), dectobin(registers["001"][1]), dectobin(registers["010"][1]),
          dectobin(registers["011"][1]), dectobin(registers["100"][1]), dectobin(registers["101"][1]),
          dectobin(registers["110"][1]), dectobin(
            8 * registers["111"][1][0] + 4 * registers["111"][1][1] + 2 * registers["111"][1][2] + registers["111"][1][3]))


def overflowtobin(value):

    return binaryToDecimal((bin(value)[2:])[-16:])


def dectobin(value):
    return "0" * (16 - len(bin(value)[2:])) + bin(value)[2:]


def flagreset():
    registers["111"][1] = [0, 0, 0, 0]



y=[]

while mem[PC][0:5] != "01010":
    # print(PC)
    instruction = mem[PC]
    y.append(PC)
    print("0" * (8 - len(bin(PC)[2:])) + bin(PC)[2:], end=" ")
    execute(instruction)

    printreg()
    PC += 1


flagreset()
print("0" * (8 - len(bin(PC)[2:])) + bin(PC)[2:], end=" ")
printreg()

for i in mem:
    print(i)



#bonus
y.append(PC)
x = []
for i in range(len(y)):
    x.append(i+1)
plt.scatter(x, y)
plt.xlabel('Cycle Number')
plt.ylabel('Memory Address ')
plt.title('Question Three')
plt.show()
