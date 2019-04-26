
class Config:
    # The file with the istr to translate
    file_in = "Instr.txt"
    file_out = "Output.txt"

    n_bits = 32


    #\/ Do not touch this! \/
    encd = {}
    decod = {}
    parsed = {}
    #^^^ Do not touch this! ^^^

    #------------------------------ATTENTION-----------------------------
    #------------------------------ATTENTION-----------------------------
    #------------------------------ATTENTION-----------------------------
    # You can use ('ra, rb, rt')   or   ('rs, rt, rd'), but dont mix them


    #To add more instructions, modify this code:
    # use encd['operation'] = 'encode'
    # use 'a', 'b', 't' for register reference, 'x' for bits that dont care and '#' for inmediates
    # dont care's bits will be raplaced by '0'
    # example: encd['beq'] = '011xxxaaaaabbbbb################'
    encd['nop'] = '000xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    encd['add'] = '001xxxaaaaabbbbbtttttxxxxxxxxxxx'
    encd['mov'] = '010xxxxxxxxbbbbb################'
    encd['beq'] = '011xxxaaaaabbbbb################'
    encd['ldr'] = '100xxxaaaaabbbbbxxxxxxxxxxxxxxxx'
    encd['str'] = '101xxxbbbbbaaaaaxxxxxxxxxxxxxxxx'
    # use decod['operation'] = 'assembly language'
    # use 'ra', 'rb', 'rt' for register, '#x' for inmediates
    #               and 'x(ra)' or '#x(ra)' for post/pre increments
    # example: decod['beq'] = 'beq ra, rb, #x'
    # example: decod['ldr'] = 'ldr x(ra), rb' <==> 'ldr #x(ra), rb'
    decod['nop'] = 'nop'
    decod['add'] = 'add ra, rb, rt'
    decod['mov'] = 'mov #x, rb'
    decod['beq'] = 'beq ra, rb, #x'
    decod['ldr'] = 'ldr (ra), rb'
    decod['str'] = 'str ra, (rb)'

    # t-t-th-th-that's all folks!
    for x, y in decod.items():
        y = y.replace('(',',(').replace('(','').replace(')','').replace(' ',',')
        parsed[x] = [x for x in y.upper().split(",") if x is not '']
    for x, y in encd.items():
        #continue
        if y.find('s') is not -1 and y.find('d') is not -1:
            tmp = decod[x]
            decod[x] = tmp.lower().replace('rs','ra').replace('rt','rb').replace('rd','rt')
            encd[x] = y.lower().replace('s','a').replace('t','b').replace('d','t')
        elif y.find('s') is not -1 or y.find('d') is not -1:
            encd.pop(x)
            decod.pop(x)
