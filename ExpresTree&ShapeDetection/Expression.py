# Nicolas Urrea
# nu22c
# 05/29/2025
# The program in this file is the individual work of Nicolas Urrea

class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def is_operator(self):
        return self.value in ['+', '-', '*', '/', 'u-']

def generate_expression_tree(tokens):
    stack = []
    for token in tokens:
        if token in ['+', '-', '*', '/']:
            if len(stack) < 2:
                raise ValueError("Not enough operands for binary operator.")
            # pop last two for binary  
            right = stack.pop()
            left = stack.pop()
            node = Node(token)
            node.left = left
            node.right = right
            stack.append(node)
        elif token == 'u-':
            if len(stack) < 1:
                #pop one for unary
                raise ValueError("Not enough operands for unary operator.")
            operand = stack.pop()
            node = Node('u-')
            node.right = operand
            stack.append(node)
        else:
            #if num/variable, create node
            stack.append(Node(token))
    if len(stack) != 1:
        raise ValueError("Invalid postfix expression.")
    return stack[0]

def generate_infix_expression(node):
    if node is None:
        return ""

    if not node.is_operator():
        return str(node.value)

    if node.value == 'u-':
        return f"( -{generate_infix_expression(node.right)} )"

    left_expr = generate_infix_expression(node.left)
    right_expr = generate_infix_expression(node.right)
    return f"( {left_expr} {node.value} {right_expr} )"

def evaluate_expression(node, variables):
    if node is None:
        raise ValueError("Invalid expression tree: node is missing.")

    if not node.is_operator():
        try:
            return float(node.value)
        except ValueError:
            #check if its a variable and get its value
            if node.value in variables:
                return float(variables[node.value])
            else:
                raise ValueError(f"Undefined variable: {node.value}")

    if node.value == 'u-':
        right_val = evaluate_expression(node.right, variables)
        return -right_val

    left_val = evaluate_expression(node.left, variables)
    right_val = evaluate_expression(node.right, variables)

    if node.value == '+':
        return left_val + right_val
    elif node.value == '-':
        return left_val - right_val
    elif node.value == '*':
        return left_val * right_val
    elif node.value == '/':
        return left_val / right_val
    else:
        raise ValueError(f"Unknown operator: {node.value}")

def main():
    try:
        postfix = input("Enter the postfix expression: ").split()
        tree_root = generate_expression_tree(postfix)

        infix = generate_infix_expression(tree_root)
        print("The infix expression is", infix)

        variables = {}
        for token in postfix:
            if token.isalpha() and token not in variables:
                val = input(f"Enter the values of\n{token}: ")
                variables[token] = float(val)

        result = evaluate_expression(tree_root, variables)
        print(f"The result is {result}")

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()