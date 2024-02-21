import re

# LEXICAL ANALYSER
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


# PARSER
class Node:
    def __init__(self, Type, value):
        self.Type = Type
        self.value = value
        self.left = None
        self.right = None

def parse_expression(tokens):
    operators = {'+', '-', '*', '/', '%', '^'}

    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '%': 2,
        '^': 3,
    }

    def is_higher_precedence(op1, op2):
        return precedence[op1] >= precedence[op2]

    def create_binary_node(op_stack, value_stack):
        right = value_stack.pop()
        left = value_stack.pop()
        operator = op_stack.pop()
        node = Node('OPERATOR', operator)
        node.left = left
        node.right = right
        value_stack.append(node)

    op_stack = []
    value_stack = []

    for token_Type, token_value in tokens:
        if token_Type == 'NUMBER' or token_Type == 'VARIABLE':
            value_stack.append(Node(token_Type, token_value))

        elif token_Type == 'OPERATOR':
            while ( op_stack and op_stack[-1] in operators and is_higher_precedence(op_stack[-1], token_value)):
                create_binary_node(op_stack, value_stack)
            op_stack.append(token_value)

        elif token_Type in ('PARENTHESIS', 'BRACKET'):
            if token_value in '({[':
                op_stack.append(token_value)
            elif token_value in ')}]':
                while op_stack and op_stack[-1] not in '({[':
                    create_binary_node(op_stack, value_stack)
                if op_stack and op_stack[-1] in '({[':
                    op_stack.pop()
                else:
                    raise SyntaxError(f"Unmatched closing bracket: {token_value}")

    while op_stack:
        create_binary_node(op_stack, value_stack)

    return value_stack[0]

def print_ast(node, indent=0):
    if node is not None:
        print(" " * indent + f"{node.Type}: {node.value}")
        print_ast(node.left, indent + 2)
        print_ast(node.right, indent + 2)


# EXECUTER
variable_values = {}

def Execute(node):
    if node.Type == 'NUMBER':
        return float(node.value)

    elif node.Type == 'VARIABLE':
        variable_name = node.value
        if variable_name not in variable_values:
            value = input(f"Enter the value for variable '{variable_name}': ")
            variable_values[variable_name] = float(value)
        return variable_values[variable_name]

    elif node.Type == 'OPERATOR':
        left = Execute(node.left)
        right = Execute(node.right)

        if node.value == '+':
            return left + right

        elif node.value == '-':
            return left - right

        elif node.value == '*':
            return left * right

        elif node.value == '/':
            if right == 0:
                raise ZeroDivisionError("Division by zero")
            return left / right

        elif node.value == '%':
            return left % right

        elif node.value == '^':
            return left ** right

# Main loop
if __name__ == "__main__":
    print("\n\n\t\t------------------ PYTHON EXPRESSION CALCULATOR INTERPRETER ------------------\n\nuse numericals or variables in your expression\n\nType 'exit' to quit\n\n")

    lexeme = lexical_analyzer()

    while True:
        code = input("> > ")
        if code.lower() == 'exit':
            break

        try:
            Tokens = lexeme.lexer(code)
            print("TOKENS GENERATED : ", Tokens)

            parse_tree = parse_expression(Tokens)

            print("PARSE TREE GENERATED : ")
            print_ast(parse_tree, 0)

            result = Execute(parse_tree)
            print("RESULT ", result)
            print("\n\n")

        except SyntaxError as e:
            print("Syntax Error:", e)

        except ValueError as e:
            print("Value Error:", e)

        variable_values = {}
