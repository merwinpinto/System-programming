#MERWIN PINTO _ ROLL NO 1 _DIV E
def Symbol_table_generation(sentences_array, mnemonics):
    symbol_table = {}
    lc = None  # Initialize location counter

    for sentence in sentences_array:
        if len(sentence) > 0:  # Checks address
            if lc is None:
                lc = int(sentence[1])

            elif sentence[0].upper() == "ORG":
                lc = int(sentence[1]) if len(sentence) > 1 else None

            else:
                lc += 2  # Increment lc by 2 for each instruction

            if len(sentence) > 1:  # Checks symbols and labels
                symbol = sentence[0] if sentence[0] not in mnemonics else None
                if symbol:
                    symbol = symbol.rstrip(':')
                    symbol_table[symbol] = lc

    file2 = open("SYMBOL.txt",'w')
    file2.write("Symbol Table \n")
    for symbol, address in symbol_table.items():
        file2.write(f"{symbol}\t{address} \n")
    
    return symbol_table

def IC_generation(symbol_table):
    print("\nINTERMEDIATE CODE\n")

    file3 = open("INTERMEDIATE_CODE.txt", "w")
    for sentence in sentences_array:
        formatted_sentence = []
        for word in sentence:
            if word.endswith(':'):
                continue  # Skip labels
            if word in opcode:
                formatted_sentence.append(f'({statement_type[word]},{opcode[word]})')
            else:
                if word.isdigit():
                    formatted_sentence.append(f'(C,{word})')  # If constant then put in C,number form
                elif word in symbol_table:
                    symbol_index = list(symbol_table.keys()).index(word) + 1
                    formatted_sentence.append(f'(S,{symbol_index})')  # Replace symbol with its index
                else:
                    formatted_sentence.append(word.replace(',', '').replace(':', ''))

        print(' '.join(formatted_sentence))
        file3.write(' '.join(formatted_sentence))
        file3.write('\n')

file = open('ASM.txt', 'r')
read_data = file.read()
input_lines = read_data.split('\n')

sentences_array = []
for line in input_lines:
    words = line.split()
    sentences_array.append(words)

mnemonics = {
    'START', 'MOV', 'ADD', 'MUL', 'JUMP', 'DC', 'DS', 'END' ,'ORG'
}

statement_type = {
    "START": "AD",
    "MOV": "IS",
    "ADD": "IS",
    "MUL": "IS",
    "JUMP": "IS",
    "ORG" : "AD",
    "DC": "DL",
    "DS": "DL",
    "END": "AD",
    "AREG": "R",
    "BREG": "R",
    "CREG": "R",
}

opcode = {
    "START": 1,
    "MOV": 1,
    "ADD": 2,
    "MUL": 3,
    "JUMP": 4,
    "ORG" : 2,
    "DC": 1,
    "DS": 2,
    "END": 3,
    "AREG": 1,
    "BREG": 2,
    "CREG": 3,
}

symbol_table = Symbol_table_generation(sentences_array, mnemonics)
IC_generation(symbol_table)
