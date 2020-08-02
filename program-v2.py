#!/usr/bin/python3

# Antonio Russoniello
# instagram: @criptorusso
# email: antonioclasesucv@gmail.com
#
# this is an assembler for the hack computer
# 

import sys

variable_memory_count = 16

computation_table = {
            '0':   '1110101010',
            '1':   '1110111111',
            '-1':  '1110111010',
            'D':   '1110001100',
            'A':   '1110110000',
            'M':   '1111110000',
            '!D':  '1110001101',
            '!A':  '1110110001',
            '!M':  '1111110001',            
            '-D':  '1110001111',
            '-A':  '1110110011',
            '-M':  '1111110011',            
            'D+1': '1110011111',
            'A+1': '1110110111',
            'M+1': '1111110111',            
            'D-1': '1110001110',
            'A-1': '1110110010',
            'M-1': '1111110010',            
            'D+A': '1110000010',
            'D+M': '1111000010',            
            'D-A': '1110010011',
            'D-M': '1111010011',            
            'A-D': '1110000111',
            'M-D': '1111000111',            
            'D&A': '1110000000',
            'D&M': '1111000000',           
            'D|A': '1110010101',
            'D|M': '1111010101'            
            }

destination_table = {
            'null': '000',
            'M':    '001',
            'D':    '010',
            'MD':   '011',
            'A':    '100',
            'AM':   '101',
            'AD':   '110',
            'AMD':  '111'
            }
jump_table = {
            'null': '000',
            'JGT':  '001',
            'JEQ':  '010',
            'JGE':  '011',
            'JLT':  '100',
            'JNE':  '101',
            'JLE':  '110',
            'JMP':  '111'
            }     

A_instruct_table = {
            'R0':     '0000000000000000',
            'R1':     '0000000000000001',
            'R2':     '0000000000000010',
            'R3':     '0000000000000011',
            'R4':     '0000000000000100',
            'R5':     '0000000000000101',         
            'R6':     '0000000000000110',
            'R7':     '0000000000000111',
            'R8':     '0000000000001000',
            'R9':     '0000000000001001',
            'R10':    '0000000000001010',
            'R11':    '0000000000001011',      
            'R12':    '0000000000001100',
            'R13':    '0000000000001101',
            'R14':    '0000000000001110',
            'R15':    '0000000000001111',
            'SCREEN': '0100000000000000',               
            'KBD':    '0110000000000000',
            'SP':     '0000000000000000',
            'LCL':    '0000000000000001',            
            'ARG':    '0000000000000010',
            'THAT':   '0000000000000100',      
            'THIS':   '0000000000000011',                             
            }

symbol_table = {}

# debug
#print(computation_table.get('D'))
#print(A_instruct_table.get('R15'))


def first_round_label(asmFile):
    mem_addr = -1
    ff = open(asmFile+'.tmp', 'w')
    with open(asmFile, "r") as f:
        for line in f:
            line_parse = line.strip()
            line_parse = line_parse.replace(" ", "")    
            result = line_parse.find('//')         
            if(int(result >= 1)):
                remove = line_parse[result:]
                #print(remove)
                line_parse = line_parse.replace(remove, "")   
                #print(line_parse)
            if (line.isspace() == False and line_parse[0] != '/' and line_parse[0] != '*'):
                if(line_parse[0] == '('):
                    label = line_parse[1:-1]
                    #print(mem_addr, label)    
                    #symbol_table.has_key(label)
                    symbol_table[label] = mem_addr + 1
                else:
                    mem_addr +=1
                    #print(mem_addr, line.rstrip())
                    ff.write(line_parse +'\n')

        ff.close()
    f.close()
    #print(symbol_table)
    return

def second_round_label(asmFile):
    #mem_addr = -1
    ff = open(asmFile+'.obj', 'w')    
    global variable_memory_count
    with open(asmFile+'.tmp', "r") as f:
         for line in f:
            #mem_addr +=1
            if(line[0] == '@' and line[1:-1].isdigit() == False):
                label = line[1:].rstrip()
                #print(label, symbol_table.get(label))
                if(symbol_table.get(label) is not None):
                    ff.write(str(symbol_table.get(label)) + '\n')
                    pass
                else:            
                    #print(label)
                    #print(mem_addr, label)  
                    #is not a number and not in the table then add next R 
                    #print(symbol_table.get(line[1:-1]))
                    if(line[1:-1].isdigit() == False and symbol_table.get(line[1:-1]) == None):
                        #print('bingo')
                        if(A_instruct_table.get(label) == None):
                            symbol_table[label] = variable_memory_count
                            ff.write(str(variable_memory_count) + '\n')
                            variable_memory_count +=1                            
                        else:
                            ff.write(str((line[1:-1])) + '\n')
            elif(line[0] == '@' and line[1:-1].isdigit() == True):
                ff.write(line[1:])
            elif(line[0] != '(' and line[:-1] !=')'):
                ff.write(line)
    print(symbol_table)
    ff.close
    f.close()
    return

def is_a_symbol(pline):
    label = symbol_table.get(pline)
    bin_code = str("{0:b}".format(int(label)))
    bin_code = bin_code.rjust(16, '0')
    return bin_code

def is_a_num_mem(pline):
    bin_code = str("{0:b}".format(int(pline)))
    bin_code = bin_code.rjust(16, '0')
    return bin_code

def comp_without_jmp(pline):
    computation = pline.split('=')
    dest = computation[0]
    comp = computation[1]
    jump_code = jump_table.get('null')    
    comp_code = computation_table.get(comp)
    dest_code = destination_table.get(dest)
    return comp_code, dest_code, jump_code
           
def not_comp_with_jmp(pline):
    computation = pline.split(';')
    comp = computation[0]
    jump = computation[1]            
    comp_code = computation_table.get(comp)
    dest_code = destination_table.get('null')
    jump_code = jump_table.get(jump)
    return comp_code, dest_code, jump_code

def not_comp_with_jmp_comma(pline):
    computation = pline.split(',')
    comp = computation[0]
    jump = computation[1]            
    comp_code = computation_table.get(comp)
    dest_code = destination_table.get('null')
    jump_code = jump_table.get(jump)
    return comp_code, dest_code, jump_code

##########################################
def third_round_computation(asmFile):
    f = open(asmFile+'.obj', 'r')
    ff = open(asmFile+'.bin', 'w')
    fff = open(asmFile+'.hack', 'w')
    for line in f:
        parse_line = line[:-1]
        parse_line = parse_line.rstrip()
        print(parse_line)
        if(parse_line in A_instruct_table.keys()):
            var_to_bin = A_instruct_table.get(parse_line)
            ff.write(str(var_to_bin) + '\n')
            fff.write(str(var_to_bin) + '\n')            
        elif(parse_line in symbol_table.keys()):
            var_to_bin = is_a_symbol(parse_line)
            ff.write(str(var_to_bin) + '\n')
            fff.write(str(var_to_bin) + '\n')            

        elif(parse_line.isdigit() == True):
            var_to_bin = is_a_num_mem(parse_line)
            ff.write(str(var_to_bin) + '\n')
            fff.write(str(var_to_bin) + '\n')            

        elif('=' in line and ';' not in line):
            c_code, d_code, j_code = comp_without_jmp(parse_line)
            ff.write(parse_line + ' ' + str(c_code) + str(d_code) + str(j_code) + '\n')   
            fff.write(str(c_code) + str(d_code) + str(j_code) + '\n')                      

        elif('=' not in line and ';' in line):
            c_code, d_code, j_code = not_comp_with_jmp(parse_line)
            ff.write(parse_line + ' ' + str(c_code) + str(d_code) + str(j_code) + '\n')    
            fff.write(str(c_code) + str(d_code) + str(j_code) + '\n')                

        elif('=' not in line and ',' in line):
            c_code, d_code, j_code = not_comp_with_jmp_comma(parse_line)
            ff.write(parse_line + ' ' + str(c_code) + str(d_code) + str(j_code) + '\n')  
            fff.write(str(c_code) + str(d_code) + str(j_code) + '\n')                 
    f.close()
    ff.close()
    fff.close()
    return


fileName = str(sys.argv[1]) 
first_round_label(fileName)
second_round_label(fileName)
third_round_computation(fileName)