Tokens = [('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '5'), ('OPERATOR', '*'), ('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '2')]


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

if __name__ == "__main__":
    print("Tokens:")
    print(Tokens)
    
    parsed_tree = parse_expression(Tokens)
    
    print("Parsed Tree:")
    print_ast(parsed_tree, 0)
