#import re
try:
    from config import Config
except ImportError:
    print('[main] ImportError: please download again git repository, config.py missed!')

# Reading the file:
with open(Config.file_in) as f:
    orig = []
    instr = []
    for line in f:
        # for comments: //comments
        if line.startswith('//'):
            continue
        line = line.replace('\n',"").lower()
        if len(line) is 0:
            continue
        orig.append(line)
        line = line.replace(' ',',') #.replace(',,',',')
        instr.append([x for x in line.replace('(',',(').split(",") if x is not ''])

# This func could be called "cheching config.py file"
def run_checks():
    if len(Config.encd) is not len(Config.decod):
        print('[main] Error on config.py:')
        print('\t[config] Lengths dont match (encode, decode)\n\n')
        raise Exception()
    for x, y in Config.encd.items():
        if not isinstance(y,str):
            print('[main] Error on config.py:')
            print("\t[config] \'{0}\' operation must be a string\n\n".format(x))
            raise Exception()
        if len(y) is not Config.n_bits:
            print('[main] Error on config.py:')
            print("\t[config] \'{0}\' operation must have {1} bits\n\n".format(x,Config.n_bits))
            raise Exception()
        if x not in Config.decod:
            print('[main] Error on config.py:')
            print("\t[config] \'{0}\' operation not found on decod\n\n".format(x))
            raise Exception()
        else:
            pass#TODO ra->aaaaa
    for x in Config.decod:
        if x not in Config.encd:
            print('[main] Error on config.py:')
            print("\t[config] \'{0}\' operation not found on encd".format(x))
            raise Exception

# From decimal to binary -> Used to get registers
def  register_to_binary(param, n_bits):
    param = param.replace('(','')
    param = param.replace(')','')
    param = param.replace('r','')
    return "{0:0{bits}b}".format(int(param), bits=n_bits)

# Return a binary number from hex or decimal number
def  inmediate_to_binary(param, n_bits):
    param = param.replace('#','')
    try:
        if param.startswith('0x'):
            return "{0:0{bits}b}".format(int(param, 16), bits=n_bits)
        if (int(param) >= 0):
          return "{0:0{bits}b}".format(int(param), bits=n_bits)
        else:
          return "{0:0{bits}b}".format(int(param) & 0xffff, bits=n_bits)
    except:
        return "{:-^{bits}}".format("ERR", bits=n_bits)

#TODO: More info on exceptions
def to_binary(operation):
    bin = 'Error'
    try:
        list = Config.parsed[operation[0]]
        if len(operation) is not len(list):
            raise TypeError
        bin = Config.encd[operation[0]].upper()
        for i in range(1,len(list)):
            if list[i] == 'RA':
                n_count = bin.count('A')
                bin = bin.replace('A'*n_count,'|' + register_to_binary(operation[i], n_count) + '|')
            elif list[i] == 'RB':
                n_count = bin.count('B')
                bin = bin.replace('B'*n_count,'|' + register_to_binary(operation[i], n_count) + '|')
            elif list[i] == 'RT':
                n_count = bin.count('T')
                bin = bin.replace('T'*n_count,'|' + register_to_binary(operation[i], n_count) + '|')
            elif list[i] == '#X' or list[i] == 'X':
                n_count = bin.count('#')
                bin = bin.replace('#'*n_count,'|' + inmediate_to_binary(operation[i], n_count) + '|')
            else:
                raise TypeError
        if len(bin.replace('|',"")) is not 32:
            raise TypeError
    except TypeError:
        pass
    return bin.replace('||','|')

#TODO: More comments
def to_assembly(binary):
    possible_match = []
    for i in range(1, len(binary)):
        tmp = []
        for x, y in Config.encd.items():
            if y.startswith(binary[:i]):
                tmp.append(x)
        if len(tmp) is 0:
            break
        elif len(tmp) is 1:
            possible_match = tmp
            break
        if len(possible_match) is 0 or len(tmp) < len(possible_match):
            possible_match = tmp
            continue

    if len(possible_match) is 0: # Not found
        return 'CANT MATCH'
    elif len(possible_match) is 1: # YEEEEEEEEEEEEEEEEEEEAAAAAAH BOOOOOOOOY
        ret = Config.decod[possible_match[0]].lower()
        tmp = Config.encd[possible_match[0]]
        try:
            char = ''
            for i in range(Config.n_bits):
                if char == '':
                    char = tmp[:1]
                    tmp = tmp[-len(tmp)+1:]
                    if char[:1] == '1' or char[:1] == '0':
                        char = ''
                        binary = binary[-len(binary)+1:]
                    continue
                # print(char +' || ' + ret)
                if not char.startswith(tmp[:1]):
                    if char[:1] == '#':
                        ret = ret.replace(char[:1], "r{0}".format(int(binary[:len(char)],2)))
                    else:
                        ret = ret.replace('r'+char[:1], "r{0}".format(int(binary[:len(char)],2)))
                    binary = binary[-len(binary)+len(char):]
                    char = tmp[:1]
                else:
                    char = char + tmp[:1]
                tmp = tmp[-len(tmp)+1:]

                if char[:1] == '1' or char[:1] == '0' or char[:1] == 'x':
                    char = ''
                    binary = binary[-len(binary)+1:]

            if len(char) is not 0:
                if char[:1] == '#':
                    ret = ret.replace('x', "{0}".format(int(binary,2)))
                else:
                    ret = ret.replace('r'+char[:1], "r{0}".format(int(binary,2)))
        except:
            return Config.decod[possible_match[0]].lower()
        return ret
    else: # Oof, more than one...
        ret = 'Could be more that 1: '
        for i in possible_match:
            ret = ret + i + ', '
        return ret

# his name means what he does
def from_binary_to_hexa(num):
    try:
        num = num.replace('X','0')
        num = num.replace('|','')
        res = "0x{0:0{dig}x}".format(int(num,2), dig=Config.n_bits//4)
    except:
        res = 'CANT CONVERT'
    return res

# his name means what he does
def from_hexa_to_binary(num):
    try:
        res = "{0:0{bits}b}".format(int(num,16), bits=Config.n_bits)
    except:
        res = 'CANT CONVERT'
    return res

# Debug mode - - - - -
def testoutput(mtx):
    with open("test.txt", 'w') as f_out:
        for item in mtx:
            f_out.write("%s | " % len(item))
            for subitem in item:
                f_out.write("%s " % subitem)
            f_out.write("\n")

# Done!
def output(ass, mach, unk):
    if (len(ass) + len(mach) + len(unk)) is not len(orig):
        print('[main] Output error:')
        print('\t[output] len(mtx) is not len(orig)')
        return
    with open(Config.file_out, 'w') as f_out:
        f_out.write("##################\n")
        f_out.write("### ASSEMBLY CODE:\n")
        f_out.write("##################\n\n")
        for i in range(len(ass)):
            f_out.write(ass[i][0] + " "*(20-len(ass[i][0]))) #print assembly
            f_out.write("||  " + ass[i][1] + " "*(Config.n_bits+8-len(ass[i][1]))) #print binary
            f_out.write("||  " + ass[i][2]) #print hexa
            f_out.write("\n")
        f_out.write("\n\n\n##################\n")
        f_out.write("#### MACHINE CODE:\n")
        f_out.write("##################\n\n")
        for i in range(len(mach)):
            f_out.write(mach[i][0]+ " "*(Config.n_bits//4+6-len(mach[i][0])) + "||  ") #print hexa
            f_out.write(mach[i][1] + " "*(Config.n_bits+8-len(mach[i][1])) + "||  ") #print binary
            f_out.write(mach[i][2]) #print assembly
            f_out.write("\n")
        f_out.write("\n\n\n##################\n")
        f_out.write("######### UNKNOWN:\n")
        f_out.write("##################\n\n")
        for i in range(len(unk)):
            f_out.write('->  ' + unk[i] + '    ||   <---- WHAT IS THIS????\n')

# TEST test TEST test TEST test TEST :)
def is_machine_lang(orig, parsed):
    try:
        if len(parsed) is not 1:
            raise ValueError
        if orig.startswith('0x'):
            int(orig, 16)
            if len(orig) is not 2+Config.n_bits//4:
                raise ValueError
        else:
            int(orig, 2)
            if len(orig) is not Config.n_bits:
                raise ValueError
    except:
        return False
    return True

# TEST test TEST test TEST test TEST :)
def is_assembly_lang(orig, parsed):
    if parsed[0] not in Config.encd:
        return False
    elif len(parsed) is not len(Config.parsed[parsed[0]]):
        return False
    else:
        return True

# MAIN main MAIN main MAIN main MAIN :D
def main():
    ass_lang = []
    mach_lang =[]
    unknown = []
    for it in range(len(orig)):
        test = []
        if is_assembly_lang(orig[it], instr[it]):
            test.append(orig[it])
            test.append(to_binary(instr[it]))
            test.append(from_binary_to_hexa(test[1]))
            ass_lang.append(test)
        elif is_machine_lang(orig[it], instr[it]):
            if orig[it].startswith('0x'):
                test.append(orig[it])
                test.append(from_hexa_to_binary(orig[it]))
            else:
                test.append(from_binary_to_hexa(orig[it]))
                test.append(orig[it])
            test.append(to_assembly(test[1]))
            mach_lang.append(test)
        else:
            unknown.append(orig[it])

    output(ass_lang, mach_lang, unknown)
    print("Done. :)\n")


if __name__ == '__main__':
    print('\n')
    run_checks()
    main()
