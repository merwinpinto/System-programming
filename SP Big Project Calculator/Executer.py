Tokens = [('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '5'), ('OPERATOR', '*'), ('NUMBER', '2'), ('OPERATOR', '+'), ('NUMBER', '2')]

print(Tokens)

class Node:
    def __init__(self, Type, value):
        self.Type = Type
        self.value = value
        self.left = None
        self.right = None


def parse_expression(tokens):
    operators = {
        '+', 
        '-', 
        '*', 
        '/'
        }

    precedence = {
            '+': 1,
            '-': 1,
            '*': 2,
            '/': 2
            }

    def is_higher_precedence(op1, op2):
        return precedence[op1] >= precedence[op2]

    def create_binary_node(operator_stack, value_stack):
        right = value_stack.pop()
        left = value_stack.pop()
        operator = operator_stack.pop()
        node = Node('OPERATOR', operator)
        node.left = left
        node.right = right
        value_stack.append(node)

    operator_stack = []
    value_stack = []

    for token_Type, token_value in tokens:
        if token_Type == 'NUMBER':
            value_stack.append(Node('NUMBER', token_value))
        elif token_Type == 'OPERATOR':
            while (
                operator_stack and
                operator_stack[-1] in operators and
                is_higher_precedence(operator_stack[-1], token_value)
            ):
                create_binary_node(operator_stack, value_stack)
            operator_stack.append(token_value)

        elif token_Type == 'PARENTHESIS':
            if token_value == '(':
                operator_stack.append(token_value)

            else:
                while operator_stack and operator_stack[-1] != '(':
                    create_binary_node(operator_stack, value_stack)
                operator_stack.pop()

    while operator_stack:
        create_binary_node(operator_stack, value_stack)

    return value_stack[0]


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


# Parse the Tokens
parsed_tree = parse_expression(Tokens)
result = Execute(parsed_tree)
print("Result >>  ",result)

