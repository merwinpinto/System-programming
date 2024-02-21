import re
default = re.compile(r'&(\w+)(=)?(\w+)?')
endline = "\n"
tab = "\t"

class macroPass1:
    def __init__(self):
        self.MNT = {} 
        self.MDT = [] 
        self.MDTPointer = 1
        self.KPDT_ARRAY = [] 
        self.KPDT_pointer = 1 
        self.PNTAB = {} 
        self.inputFile = open("input.txt",mode="r")
        self.ICpointer = 0
        self.ICFile = open('IC.txt',mode='w')
        self.MDTFile = open('MDT.txt',mode='w')
        self.MNTFile = open('MNT.txt',mode='w')
        self.KPDT_ARRAYFile = open('KPDT.txt',mode='w')
        self.PNTABFile = open('PNT.txt',mode='w')
    
    
    def covertToTuple(self,param,current_macro):
        id = self.PNTAB[current_macro].index(param) + 1
        return "(P," + str(id) + ")"

    def parseFile(self):
        lines = self.inputFile.readlines()
        inMacroDefinition = False
        currentMacroName = None
        for line in lines:
            line = line.strip('\n')
            line = line.split('\t')
            part_1 = line[0]
            if part_1 == "START":
                break
            self.ICpointer += 1 
            part_2 = []
            if len(line) > 1:
                part_2 = line[1].split(', ')
            
            if part_1 == "MACRO":
                inMacroDefinition = True
                continue
            elif inMacroDefinition == True:
                self.PNTAB[part_1] = []
                currentMacroName = part_1
                PP_C = 0
                KPDT_C = 0
                for param in part_2:
                    find = default.search(param)
                    self.PNTAB[part_1].append(find.groups()[0])
                    if find.group(2) == None:
                        PP_C += 1
                    else:
                        KPDT_C += 1
                        
                        if find.group(3) == None:
                            self.KPDT_ARRAY.append((find.group(1),"----"))
                        else:
                            self.KPDT_ARRAY.append((find.group(1),find.group(3)))
                inMacroDefinition = False
                if KPDT_C == 0:
                    self.MNT[part_1] = [PP_C,KPDT_C,self.MDTPointer,0]
                else:
                    self.MNT[part_1] = [PP_C,KPDT_C,self.MDTPointer,self.KPDT_pointer]
                self.KPDT_pointer += KPDT_C
            elif part_1 == "MEND":
                self.MDT.append([])
                self.MDT[-1].append("MEND")
                self.MDTPointer += 1
                currentMacroName = None
            else:
                self.MDT.append([])
                self.MDT[-1].append(part_1)
                for param in part_2:
                    find = default.search(param)
                    if find != None:
                        self.MDT[-1].append(self.covertToTuple(find.group(1),currentMacroName))
                    else:
                        self.MDT[-1].append(param)

                self.MDTPointer += 1
        #Write the Intermediate Code file
        while self.ICpointer < len(lines):
            line = lines[self.ICpointer]
            self.ICFile.write(line)
            self.ICpointer += 1
        self.ICFile.close()
        self.inputFile.close()
    
    def writeKPDT_ARRAY(self):
        print("\nKeyword Parameter Default Table:")
        counter = 1
        for value in self.KPDT_ARRAY:
            line = value[0] + tab + value[1] + endline
            self.KPDT_ARRAYFile.write(line)
            print(counter,line,end="",sep="\t")
            counter += 1
        self.KPDT_ARRAYFile.close()

    def writeMNT(self):
        line = "Name" + tab + "PP" + tab + "KP" + tab + "MDTP" + tab + "KPDTP" + endline
        print("\nMacro Name Table:")
        print(line,end="")
        self.MNTFile.write(line)
        for key,value in self.MNT.items():
            line = key
            for ele in value:
                line += tab + str(ele)
            line += endline
            print(line,end="")
            self.MNTFile.write(line)
        self.MNTFile.close()
    
    def writePNTAB(self):
        print("\nParameter Name Table:")
        for key,value in self.PNTAB.items():
            line = key
            for param in value:
                line += tab + param
            line += endline
            print(line,end="")
            self.PNTABFile.write(line)
        self.PNTABFile.close()
    
    def writeMDT(self):
        print("\nMacro Definition Table:")
        counter = 1
        for value in self.MDT:
            line = ""
            for item in value:
                line += item + tab
            line += endline
            print(counter,line,end="",sep="\t")
            self.MDTFile.write(line)
            counter += 1
        self.MDTFile.close()
pass1 = macroPass1()  
pass1.parseFile()
pass1.writeMNT()
pass1.writePNTAB()
pass1.writeMDT()
pass1.writeKPDT_ARRAY()