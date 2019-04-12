import re

file = "Instr.txt"

with open(file) as f:
    orig = []
    instr = []
    for line in f:
        line = line.replace('\n',"")
        orig.append(line)
        instr.append([x for x in line.replace(' ',',').split(",")])

def  register_to_binary(param):
    param = param.replace('(','')
    param = param.replace(')','')
    param = param.replace('r','')
    return "{0:05b}".format(int(param))

def  parameter_to_binary(param):
    param = param.replace('#','')
    return "{0:016b}".format(int(param))

def to_binary(list):
    char = ''
    try:
        if list[0] == 'nop':
            char = '000|000|00000|00000|00000|00000000000'
        elif list[0] == 'add':
            char = '001|XXX|'
            if len(list) is not 4:
                raise TypeError
            char = char + register_to_binary(list[1]) + '|' + register_to_binary(list[2]) + '|' + register_to_binary(list[3]) + '|XXXXXXXXXXX'
        elif list[0] == 'mov':
            char = '010|XXX|XXXXX|'
            if len(list) is not 3:
                raise TypeError
            char = char + register_to_binary(list[2]) + '|' + parameter_to_binary(list[1])
        elif list[0] == 'beq':
            char = '011|XXX|'
            if len(list) is not 4:
                raise TypeError
            char = char + register_to_binary(list[1]) + '|' + register_to_binary(list[2]) + '|' + parameter_to_binary(list[3])
        elif list[0] == 'ldr':
            char = '100|XXX|'
            if len(list) is not 3:
                raise TypeError
            char = char + register_to_binary(list[1]) + '|' + register_to_binary(list[2]) + '|XXXXX|XXXXXXXXXXX'
        elif list[0] == 'str':
            char = '101|XXX|'
            if len(list) is not 3:
                raise TypeError
            char = char + register_to_binary(list[2]) + '|' + register_to_binary(list[1]) + '|XXXXX|XXXXXXXXXXX'
        if len(char.replace('|',"")) is not 32:
            raise TypeError
    except TypeError:
        char = "Error"

    return char

def to_hexa(num):
    if num == 'Error':
        return 'Error'
    num = num.replace('X','0')
    num = num.replace('|','')
    return hex(int(num,2))

def testoutput(mtx):
    with open("output_test.txt", 'w') as f_out:
        for item in mtx:
            f_out.write("%s | " % len(item))
            for subitem in item:
                f_out.write("%s " % subitem)
            f_out.write("\n")

def output(mtx):
    if len(mtx) is not len(orig):
        print('Error')
        return
    with open("output_test.txt", 'w') as f_out:
        for i in range(len(mtx)):
            f_out.write("|" + orig[i] + " "*(20-len(orig[i])) + mtx[i][1] + " "*(45-len(mtx[i][1])) + mtx[i][2])
            f_out.write("\n")


def main():
    tab = []
    for ins in instr:
        test = []
        test.append(ins)
        test.append(to_binary(ins))
        test.append(to_hexa(test[1]))
        tab.append(test)
    output(tab)



if __name__ == '__main__':
    main()
