"""
Semantic Analyzer for Arabic Programming Language
Performs type checking and symbol table management
"""

from ast_nodes import *

class SymbolTable:
    """Manages variable and function scopes"""
    def __init__(self, parent=None):
        self.symbols = {}
        self.parent = parent
    
    def define(self, name, type='int'):
        """Define a variable in current scope"""
        if name in self.symbols:
            raise NameError(f"Variable '{name}' already defined in this scope")
        self.symbols[name] = type
    
    def lookup(self, name):
        """Look up a variable in current or parent scopes"""
        if name in self.symbols:
            return self.symbols[name]
        elif self.parent:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Variable '{name}' not defined")
    
    def exists(self, name):
        """Check if variable exists in any scope"""
        if name in self.symbols:
            return True
        elif self.parent:
            return self.parent.exists(name)
        return False

class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.functions = {}  # Store function definitions
    
    def error(self, msg):
        raise SemanticError(msg)
    
    def analyze(self, program):
        """Analyze the entire program"""
        # First pass: collect function definitions
        for func in program.functions:
            if func.name in self.functions:
                self.error(f"Function '{func.name}' already defined")
            self.functions[func.name] = func
        
        # Second pass: analyze each function
        for func in program.functions:
            self.analyze_function(func)
    
    def analyze_function(self, func):
        """Analyze a function"""
        # Create new scope for function
        self.current_scope = SymbolTable(self.global_scope)
        
        # Add parameters to scope
        for param in func.params:
            self.current_scope.define(param)
        
        # Analyze function body
        self.analyze_block(func.body)
        
        # Return to global scope
        self.current_scope = self.global_scope
    
    def analyze_block(self, block):
        """Analyze a block of statements"""
        for stmt in block.statements:
            self.analyze_statement(stmt)
    
    def analyze_statement(self, stmt):
        """Analyze a statement"""
        if isinstance(stmt, VarDecl):
            self.analyze_expression(stmt.value)
            self.current_scope.define(stmt.name)
        
        elif isinstance(stmt, Assignment):
            if not self.current_scope.exists(stmt.name):
                self.error(f"Variable '{stmt.name}' not defined")
            self.analyze_expression(stmt.value)
        
        elif isinstance(stmt, IfStatement):
            self.analyze_expression(stmt.condition)
            self.analyze_block(stmt.then_block)
            if stmt.else_block:
                self.analyze_block(stmt.else_block)
        
        elif isinstance(stmt, WhileStatement):
            self.analyze_expression(stmt.condition)
            self.analyze_block(stmt.body)
        
        elif isinstance(stmt, ReturnStatement):
            self.analyze_expression(stmt.value)
        
        elif isinstance(stmt, PrintStatement):
            self.analyze_expression(stmt.value)
        
        elif isinstance(stmt, FunctionCall):
            if stmt.name not in self.functions:
                self.error(f"Function '{stmt.name}' not defined")
            for arg in stmt.args:
                self.analyze_expression(arg)
    
    def analyze_expression(self, expr):
        """Analyze an expression"""
        if isinstance(expr, Number):
            pass  # Literals are always valid
        
        elif isinstance(expr, Identifier):
            if not self.current_scope.exists(expr.name):
                self.error(f"Variable '{expr.name}' not defined")
        
        elif isinstance(expr, BinaryOp):
            self.analyze_expression(expr.left)
            self.analyze_expression(expr.right)
        
        elif isinstance(expr, UnaryOp):
            self.analyze_expression(expr.value)
        
        elif isinstance(expr, FunctionCall):
            if expr.name not in self.functions:
                self.error(f"Function '{expr.name}' not defined")
            for arg in expr.args:
                self.analyze_expression(arg)

class SemanticError(Exception):
    pass
