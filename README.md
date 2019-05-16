# Encoder MIPS-processor

[![Python Version](https://img.shields.io/badge/Python-3.5%2B-blue.svg)](https://www.python.org)

Encoder based on 32-bit \(5-stage\) pipelined MIPS processor
> Assembly code \<\-\> Machine code

## Getting Started
How to :)

### Prerequisites
- [Python](https://www.python.org)! \([v3.5+](https://www.python.org/downloads/)\)
- *of course download this repo and star it*
> t-t-th-th-that's all folks!


## Encode\/decode!
First, must add/edit all operations to encode\/decode

### Modifying [config.py](config.py)
You can use editors like Atom or Notepad++ to modify this file
#### - Input\/Output file
This must be a raw text file \(.txt, .in, .out, without extension, ...\). Please dont use word files\(like .doc, .docx, ...\)
#### - Bits?
Yeah, you can modify the number of bits that the instructions must have
#### - Adding new operations
For each operation, you must write his encoded form \(Binary form\) and his decoded form \(Assembly form\)
 Example:
 ```python
 #encd['operation'] = 'encode'
 encd['add'] = '001xxxaaaaabbbbbtttttxxxxxxxxxxx'
 decod['add'] = 'add ra, rb, rt'

 encd['mov'] = '010xxxxxxxxbbbbb################'
 decod['mov'] = 'mov #x, rb'
 ```
There are 2 ways to type the registers. Either ('ra,rb,rt'), either ('rs,rd,rd').

:warning: All the bits that have the same meaning must be type together: ~~abaab~~ -> aaabb \|\| bbaaa

More info on [config.py](config.py)

### Let's machine work
1. Create your input file and type on it your assembly\/machine code:
  Example:
  ```
  ;Comment!
  add r1,r2,r3
  beq r1,r1,#3 ;OMG HOW THIS WORKS
  00100010001110110010010001111011
  01101110101001110100100000001100;M;O;R;E COMMENTS!
  ```
2. Execute the program:
   - You can open a terminal on path and type `python inst-translate.py` \(You can see err msg\)
   - Or press double-clic on `inst-translate.py`
3. DONE!, check output file and enjoy :)

## License
Check it!: [LICENSE](License.md)
