#MERWIN PINTO

mnemonics = {
    'START','READ','MOVE','MOVR', 'ADD', 'MUL','LTORG','SUB','BC', 'JUMP', 'DC', 'DS','STOP','END' ,'ORG',
}

statement_type = {
    "START": "AD",
    "READ" : "IS",
    "MOVE": "IS",
    "MOVR": "IS",
    "ADD": "IS",
    "SUB": "IS",
    "MUL": "IS",
    "LTORG":"AD",
    "JUMP": "IS",
    "ORG" : "AD",
    "DC": "DL",
    "DS": "DL",
    "STOP":"AD",
    "END": "AD",
    "AREG": "R",
    "BREG": "R",
    "CREG": "R"
}

val = {
    "START": 1,
    "READ":2,
    "LTORG":2,
    "MOVE": 2,
    "MOVR": 2,
    "ADD": 3,
    "MUL": 4,
    "SUB":5,
    "ORG" : 3,
    "DC": 1,
    "DS": 2,
    "STOP": 4,
    "END": 5,
    "AREG": 1,
    "BREG": 2,
    "CREG": 3,
}

with open("ASM2.txt", 'r') as file:
    read_data = file.read()
    input_lines = read_data.split('\n')

    lc = None
    literal_table = {}
    pool_table = []
    literal_index = 1
    file1 = open("INTERMEDIATE_CODE.txt", "w")
    symbol_index_map = {}  # Dictionary to map symbols to their indices
    symbol_table = {}      # Dictionary to store symbols and their addresses
    symbol_index = 1
    
    for sentence in input_lines:
        formatted_sentence = []
        if lc is not None:
            formatted_sentence.append(f'({lc})')

        if len(sentence) > 0:
            words = sentence.split()
            if lc is None:
                lc = int(words[1])

            else:
                lc += 1  # Increment by 1

            if len(words) > 1:
                symbol = words[0] if words[0] not in mnemonics else None
                if symbol:
                    symbol = symbol.rstrip(':')
                    if symbol not in symbol_index_map:
                        symbol_index_map[symbol] = symbol_index
                        symbol_index += 1
                        symbol_table[symbol] = lc  # Store symbol address

            for word in words:
                if word.endswith(':'):
                    continue  # Skip labels

                if word.startswith('='):
                    word = word.lstrip('=')
                    if word not in literal_table:
                        literal_table[word] = lc
                        pool_table.append(word)
                        lc += 1  # Increment by 1
                        
                    literal_index = list(literal_table.keys()).index(word) + 1
                    formatted_sentence.append(f'(L,{literal_index})')
                else:
                    if word in val:
                        formatted_sentence.append(f'({statement_type[word]},{val[word]})')

                    else:
                        if word.isdigit():
                            formatted_sentence.append(f'(C,{word})')

                        elif word in symbol_table:
                            symbol = word  # Get the symbol
                            index = symbol_index_map[symbol]  # Get the symbol's index
                            formatted_sentence.append(f'(S,{index})')

                        elif word in literal_table:
                            literal_index = list(literal_table.keys()).index(word) + 1
                            formatted_sentence.append(f'(L,{literal_index})')

                        else:
                            formatted_sentence.append(word)

        file1.write(' '.join(formatted_sentence))
        file1.write('\n')

#display section 
    symbol_dict = {}
    file2 = open("SYMBOL.txt",'w')
    file2.write("Symbol Table \n")
    for symbol, address in symbol_table.items():
        symbol_dict[symbol] = address
        file2.write(f"{symbol}\t{address} \n")
    #print(symbol_dict)    

    literal_dict = {}
    file3 = open("LITERAL.txt",'w')
    file3.write("literal Table \n")
    for literal, address in literal_table.items():
        literal_dict[literal] = address
        file3.write(f"{literal}\t{address} \n")
    #print(literal_dict)

    # Generate the Pool Table
    file4 = open("POOL.txt", 'w')
    file4.write("Pool Table\n")
    pool_index = 1
    for literal in pool_table:
        file4.write(f"{pool_index}\n") #\t{literal_table[literal]}\n")
        pool_index += 2
        

    file1.close()
    file2.close()
    file3.close()
    file4.close()