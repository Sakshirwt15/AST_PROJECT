import tkinter as tk
from tkinter import messagebox, scrolledtext
import json

class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type  # "operator" or "operand"
        self.left = left  # Reference to left child
        self.right = right  # Reference to right child
        self.value = value  # Optional value for operand nodes

def create_rule(rule_string):
    # Example implementation for creating a rule
    # This would include parsing the rule_string to create an AST
    return Node("operand", value=rule_string)  # Placeholder implementation

def combine_rules(rules):
    # Combine rules into a single AST
    return Node("operator", left=create_rule(rules[0]), right=create_rule(rules[1]), value="OR")  # Placeholder

def evaluate_rule(ast, data):
    # Example evaluation logic
    if ast.type == "operand":
        # Check the rules; this needs a proper parser implementation
        return data.get("age", 0) > 30  # Placeholder evaluation
    elif ast.type == "operator":
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)
        return left_result or right_result if ast.value == "OR" else left_result and right_result
    return False

class RuleEngineApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Rule Engine")
        self.root.geometry("600x500")
        self.root.configure(bg="#f4f4f4")
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Rule Engine", font=("Arial", 24), bg="#f4f4f4")
        title_label.pack(pady=10)

        self.rule_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=5, font=("Arial", 12))
        self.rule_input.insert(tk.END, "Enter your rule here...")
        self.rule_input.pack(pady=10, padx=10, fill=tk.X)

        create_rule_btn = tk.Button(self.root, text="Create Rule", command=self.create_rule, bg="#007BFF", fg="white", font=("Arial", 14), height=2)
        create_rule_btn.pack(pady=5)

        self.data_input = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=5, font=("Arial", 12))
        self.data_input.insert(tk.END, 'Enter data as JSON e.g. {"age": 35, "department": "Sales"}')
        self.data_input.pack(pady=10, padx=10, fill=tk.X)

        evaluate_btn = tk.Button(self.root, text="Evaluate Rule", command=self.evaluate_rule, bg="#28A745", fg="white", font=("Arial", 14), height=2)
        evaluate_btn.pack(pady=5)

        self.output = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=10, font=("Arial", 12))
        self.output.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    def create_rule(self):
        rule_string = self.rule_input.get("1.0", tk.END).strip()
        if rule_string:
            ast = create_rule(rule_string)
            self.output.insert(tk.END, f"Created AST: {ast.value}\n")
        else:
            messagebox.showwarning("Warning", "Please enter a valid rule.")

    def evaluate_rule(self):
        data_string = self.data_input.get("1.0", tk.END).strip()
        try:
            data = json.loads(data_string)
            ast = create_rule(self.rule_input.get("1.0", tk.END).strip())
            result = evaluate_rule(ast, data)
            self.output.insert(tk.END, f"Evaluation Result: {result}\n")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON data.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RuleEngineApp(root)
    root.mainloop()
