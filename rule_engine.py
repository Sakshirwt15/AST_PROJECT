import json
import re

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
        self.value = value  # Optional value for operand nodes

def create_rule(rule_string):
    # Remove spaces and normalize the rule string
    rule_string = rule_string.replace(" ", "")
    
    # Check for parentheses and balance
    if rule_string.count('(') != rule_string.count(')'):
        raise ValueError(f"Invalid rule string: {rule_string} (unbalanced parentheses)")
    
    # Handle operators precedence
    operators = ["AND", "OR"]
    
    # Iterate over operators to find the main one
    for operator in operators:
        depth = 0
        start = 0
        for i, char in enumerate(rule_string):
            if char == '(':
                depth += 1
            elif char == ')':
                depth -= 1
            elif depth == 0 and rule_string.startswith(operator, i):
                # Split on the operator, considering parentheses
                left_part = rule_string[:i]
                right_part = rule_string[i + len(operator):]
                # Create nodes for the left and right parts
                left_node = create_rule(left_part)
                right_node = create_rule(right_part)
                return Node("operator", left=left_node, right=right_node, value=operator)

    # Handle parentheses
    if rule_string.startswith("(") and rule_string.endswith(")"):
        return create_rule(rule_string[1:-1])  # Recursively parse the inner rule

    # Parse operand using regular expressions
    pattern = re.compile(r"(\w+)\s*([<>]=?|=)\s*(\d+|'[^']+')")
    match = pattern.match(rule_string)
    if match:
        attribute, op, value = match.groups()
        # Clean value if it's a string
        if value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        return Node("operator", left=Node("operand", value=attribute), 
                    right=Node("operand", value=value), value=op)

    raise ValueError("Invalid rule string: {}".format(rule_string))

def combine_rules(rules):
    # This function combines multiple rules into a single AST.
    combined_ast = None
    for rule in rules:
        rule_ast = create_rule(rule)
        if combined_ast is None:
            combined_ast = rule_ast
        else:
            combined_ast = Node("operator", left=combined_ast, right=rule_ast, value="OR")  # Combine with OR for simplicity
    return combined_ast

def evaluate_rule(ast, data):
    # This function evaluates the rule against provided data.
    if ast is None:
        return False
    
    if ast.type == "operand":
        return ast.value  # This should return the attribute name

    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)

        if ast.value == ">":
            return data.get(ast.left.value) > int(ast.right.value)
        elif ast.value == "<":
            return data.get(ast.left.value) < int(ast.right.value)
        elif ast.value == "=":
            return data.get(ast.left.value) == ast.right.value
        elif ast.value == "AND":
            return left_result and right_result
        elif ast.value == "OR":
            return left_result or right_result
    
    return False

# Example usage
if __name__ == "__main__":
    rules = [
        "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing'))",
        "(salary > 50000 OR experience > 5)",
        "(age > 30)"
    ]
    
    combined_ast = combine_rules(rules)
    print("Combined AST:", json.dumps(combined_ast, default=lambda o: o.__dict__, indent=2))

    data = {"age": 35, "department": "Sales", "salary": 60000, "experience": 3}
    result = evaluate_rule(combined_ast, data)
    print("Evaluation Result:", result)  # Expected True or False based on your rules
