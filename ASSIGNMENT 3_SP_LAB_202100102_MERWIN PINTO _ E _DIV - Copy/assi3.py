lines_list=[]
with open('IntermediateCode.txt','r')as file:
    for line in file:
        words = line.strip().split()  
        lines_list.append(words)       
for line in lines_list:
    print(line)
print()
symbolTable=[]

with open('SymbolTable.txt','r')as file:
    for line in file:
        words = line.strip().split()  
        symbolTable.append(words)       
        
for line in symbolTable:
    print(line)

print()
litTable=[]
with open('LiteralTable.txt','r') as file:
    for line in file:
        literal=line.strip().split()
        litTable.append(literal)

for literal in litTable:
    print(literal)


with open('MachineCode.txt','w') as myfile:
    for line in lines_list:
        if line[0]=='AD':
            print()
            myfile.write('\n')

        elif line[0]=='DL':
            print(line[1]+'\t0\t'+line[3])
            myfile.write(line[1]+'\t0\t'+line[3]+'\n')

        elif line[0]=='IS':
            if len(line)==3:
                index=int(line[2][1:])
                print(line[1]+'\t0\t'+symbolTable[index-1][1])
                myfile.write(line[1]+'\t0\t'+symbolTable[index-1][1]+'\n')

            else:
                if line[2].startswith('R') and line[3].startswith('R'):
                    print(line[1]+'\t'+line[2][1:]+line[3][1:])
                    myfile.write(line[1]+'\t'+line[2][1:]+'\t'+line[3][1:]+'\n')

                elif line[2].startswith('R') and line[3].startswith('S'):
                    index=int(line[3][1:])
                    print(line[1]+'\t'+line[2][1:]+'\t'+symbolTable[index-1][1])
                    myfile.write(line[1]+'\t'+line[2][1:]+'\t'+symbolTable[index-1][1]+'\n')

                elif line[2].startswith('R') and line[3].startswith('L'):
                    index=int(line[3][1:])
                    print(line[1]+'\t'+line[2][1:]+'\t'+litTable[index-1][1])
                    myfile.write(line[1]+'\t'+line[2][1:]+'\t'+litTable[index-1][1]+'\n')

                elif line[2].startswith('S') and line[3].startswith('R'):
                    index=int(line[2][1:])
                    print(line[1]+'\t'+symbolTable[index-1][1]+'\t'+line[3][1:])
                    myfile.write(line[1]+'\t'+symbolTable[index-1][1]+'\t'+line[3][1:]+'\n')




                    
                

                    
                


        
