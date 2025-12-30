"""
AST Node Classes for Arabic Programming Language Compiler
Defines the structure of the Abstract Syntax Tree
"""

class ASTNode:
    """Base class for all AST nodes"""
    pass

class Program(ASTNode):
    """Root node containing all functions"""
    def __init__(self, functions):
        self.functions = functions
    
    def __repr__(self):
        return f"Program({self.functions})"

class Function(ASTNode):
    """Function definition node"""
    def __init__(self, name, params, body):
        self.name = name
        self.params = params  # List of parameter names
        self.body = body  # Block node
    
    def __repr__(self):
        return f"Function({self.name}, {self.params}, {self.body})"

class Block(ASTNode):
    """Block of statements"""
    def __init__(self, statements):
        self.statements = statements
    
    def __repr__(self):
        return f"Block({self.statements})"

class VarDecl(ASTNode):
    """Variable declaration: متغير x = 5;"""
    def __init__(self, name, value):
        self.name = name
        self.value = value  # Expression node
    
    def __repr__(self):
        return f"VarDecl({self.name}, {self.value})"

class Assignment(ASTNode):
    """Variable assignment: x = 10;"""
    def __init__(self, name, value):
        self.name = name
        self.value = value  # Expression node
    
    def __repr__(self):
        return f"Assignment({self.name}, {self.value})"

class IfStatement(ASTNode):
    """If statement with optional else"""
    def __init__(self, condition, then_block, else_block=None):
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block
    
    def __repr__(self):
        return f"IfStatement({self.condition}, {self.then_block}, {self.else_block})"

class WhileStatement(ASTNode):
    """While loop"""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
    
    def __repr__(self):
        return f"WhileStatement({self.condition}, {self.body})"

class ReturnStatement(ASTNode):
    """Return statement"""
    def __init__(self, value):
        self.value = value  # Expression node
    
    def __repr__(self):
        return f"ReturnStatement({self.value})"

class PrintStatement(ASTNode):
    """Print statement: اطبع(x);"""
    def __init__(self, value):
        self.value = value  # Expression node
    
    def __repr__(self):
        return f"PrintStatement({self.value})"

class BinaryOp(ASTNode):
    """Binary operation: left op right"""
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # '+', '-', '*', '/', '==', '!=', '>', '<', '>=', '<='
        self.right = right
    
    def __repr__(self):
        return f"BinaryOp({self.left}, {self.op}, {self.right})"

class UnaryOp(ASTNode):
    """Unary operation: op value"""
    def __init__(self, op, value):
        self.op = op  # '-', '!'
        self.value = value
    
    def __repr__(self):
        return f"UnaryOp({self.op}, {self.value})"

class Number(ASTNode):
    """Numeric literal"""
    def __init__(self, value):
        self.value = int(value)
    
    def __repr__(self):
        return f"Number({self.value})"

class Identifier(ASTNode):
    """Variable or function reference"""
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f"Identifier({self.name})"

class FunctionCall(ASTNode):
    """Function call"""
    def __init__(self, name, args):
        self.name = name
        self.args = args  # List of expression nodes
    
    def __repr__(self):
        return f"FunctionCall({self.name}, {self.args})"
