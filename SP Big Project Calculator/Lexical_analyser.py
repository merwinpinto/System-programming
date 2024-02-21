import re

class lexical_analyzer:
    def __init__(self):
        self.tokens = [
            (re.compile(r'\d+\.\d+|\d+'), "NUMBER"),
            (re.compile(r'[a-zA-Z]+'), "VARIABLE"),
            (re.compile(r'[+\-*%/^]'), "OPERATOR"),
            (re.compile(r'\('), "PARENTHESIS"),
            (re.compile(r'\)'), "PARENTHESIS"),
            (re.compile(r'\['), "BRACKET"),
            (re.compile(r'\]'), "BRACKET"),
            (re.compile(r'\{'), "CBRACKET"),
            (re.compile(r'\}'), "CBRACKET")
        ]

    def lexer(self, code):
        tokens = []
        while code:
            if code[0].isspace():
                code = code[1:]
            else:
                matched = False
                for pattern, token_Type in self.tokens:
                    match = pattern.match(code)
                    if match:
                        tokens.append((token_Type, match.group()))
                        code = code[len(match.group()):]
                        matched = True
                        break

                if not matched:
                    raise SyntaxError("Invalid character: " + code[0])
        return tokens

if __name__ == "__main__":
   
    code = input("> > ")
    
    lexeme = lexical_analyzer()
    tokens = lexeme.lexer(code)
    print(tokens)

    tokens_str = ", ".join(map(str, tokens))
    
    # Open a file for writing
    with open("tokens.txt", "w") as file:
        file.write(tokens_str)
    
    print("Tokens have been written to tokens.txt")
            
