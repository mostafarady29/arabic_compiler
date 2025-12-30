"""
Parser for Arabic Programming Language
Builds an Abstract Syntax Tree from tokens
"""

from lexer import TokenType, Token
from ast_nodes import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    
    def error(self, msg):
        token = self.current_token()
        raise SyntaxError(f"Parser error at {token.line}:{token.column}: {msg}")
    
    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return self.tokens[-1]  # EOF
    
    def peek_token(self, offset=1):
        pos = self.pos + offset
        if pos < len(self.tokens):
            return self.tokens[pos]
        return self.tokens[-1]  # EOF
    
    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
    
    def expect(self, token_type):
        """Consume a token of the expected type or raise error"""
        token = self.current_token()
        if token.type != token_type:
            self.error(f"Expected {token_type}, got {token.type}")
        self.advance()
        return token
    
    def parse(self):
        """Parse the entire program"""
        functions = []
        while self.current_token().type != TokenType.EOF:
            functions.append(self.parse_function())
        return Program(functions)
    
    def parse_function(self):
        """Parse function definition: دالة name(params) { body }"""
        self.expect(TokenType.FUNCTION)
        
        name_token = self.expect(TokenType.IDENTIFIER)
        name = name_token.value
        
        self.expect(TokenType.LPAREN)
        params = []
        
        # Parse parameters
        if self.current_token().type != TokenType.RPAREN:
            params.append(self.expect(TokenType.IDENTIFIER).value)
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                params.append(self.expect(TokenType.IDENTIFIER).value)
        
        self.expect(TokenType.RPAREN)
        
        body = self.parse_block()
        
        return Function(name, params, body)
    
    def parse_block(self):
        """Parse block: { statements }"""
        self.expect(TokenType.LBRACE)
        statements = []
        
        while self.current_token().type != TokenType.RBRACE:
            statements.append(self.parse_statement())
        
        self.expect(TokenType.RBRACE)
        return Block(statements)
    
    def parse_statement(self):
        """Parse a statement"""
        token = self.current_token()
        
        if token.type == TokenType.VAR:
            return self.parse_var_decl()
        elif token.type == TokenType.IF:
            return self.parse_if_statement()
        elif token.type == TokenType.WHILE:
            return self.parse_while_statement()
        elif token.type == TokenType.RETURN:
            return self.parse_return_statement()
        elif token.type == TokenType.PRINT:
            return self.parse_print_statement()
        elif token.type == TokenType.IDENTIFIER:
            # Could be assignment or function call
            if self.peek_token().type == TokenType.ASSIGN:
                return self.parse_assignment()
            elif self.peek_token().type == TokenType.LPAREN:
                stmt = self.parse_function_call()
                self.expect(TokenType.SEMICOLON)
                return stmt
            else:
                self.error(f"Unexpected identifier")
        else:
            self.error(f"Unexpected token {token.type}")
    
    def parse_var_decl(self):
        """Parse variable declaration: متغير x = expr;"""
        self.expect(TokenType.VAR)
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return VarDecl(name, value)
    
    def parse_assignment(self):
        """Parse assignment: x = expr;"""
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.ASSIGN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return Assignment(name, value)
    
    def parse_if_statement(self):
        """Parse if statement: اذا (condition) { ... } والا { ... }"""
        self.expect(TokenType.IF)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        
        then_block = self.parse_block()
        
        else_block = None
        if self.current_token().type == TokenType.ELSE:
            self.advance()
            else_block = self.parse_block()
        
        return IfStatement(condition, then_block, else_block)
    
    def parse_while_statement(self):
        """Parse while loop: بينما (condition) { ... }"""
        self.expect(TokenType.WHILE)
        self.expect(TokenType.LPAREN)
        condition = self.parse_expression()
        self.expect(TokenType.RPAREN)
        body = self.parse_block()
        return WhileStatement(condition, body)
    
    def parse_return_statement(self):
        """Parse return: ارجع expr;"""
        self.expect(TokenType.RETURN)
        value = self.parse_expression()
        self.expect(TokenType.SEMICOLON)
        return ReturnStatement(value)
    
    def parse_print_statement(self):
        """Parse print: اطبع(expr);"""
        self.expect(TokenType.PRINT)
        self.expect(TokenType.LPAREN)
        value = self.parse_expression()
        self.expect(TokenType.RPAREN)
        self.expect(TokenType.SEMICOLON)
        return PrintStatement(value)
    
    def parse_expression(self):
        """Parse expression with operator precedence"""
        return self.parse_comparison()
    
    def parse_comparison(self):
        """Parse comparison operators: ==, !=, >, <, >=, <="""
        left = self.parse_additive()
        
        while self.current_token().type in [TokenType.EQ, TokenType.NE, 
                                            TokenType.GT, TokenType.LT,
                                            TokenType.GE, TokenType.LE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_additive()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_additive(self):
        """Parse addition and subtraction"""
        left = self.parse_multiplicative()
        
        while self.current_token().type in [TokenType.PLUS, TokenType.MINUS]:
            op = self.current_token().value
            self.advance()
            right = self.parse_multiplicative()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_multiplicative(self):
        """Parse multiplication and division"""
        left = self.parse_unary()
        
        while self.current_token().type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            op = self.current_token().value
            self.advance()
            right = self.parse_unary()
            left = BinaryOp(left, op, right)
        
        return left
    
    def parse_unary(self):
        """Parse unary operators"""
        if self.current_token().type == TokenType.MINUS:
            op = self.current_token().value
            self.advance()
            return UnaryOp(op, self.parse_unary())
        
        return self.parse_primary()
    
    def parse_primary(self):
        """Parse primary expressions: numbers, identifiers, function calls, parentheses"""
        token = self.current_token()
        
        if token.type == TokenType.NUMBER:
            self.advance()
            return Number(token.value)
        
        elif token.type == TokenType.IDENTIFIER:
            # Check if it's a function call
            if self.peek_token().type == TokenType.LPAREN:
                return self.parse_function_call()
            else:
                self.advance()
                return Identifier(token.value)
        
        elif token.type == TokenType.LPAREN:
            self.advance()
            expr = self.parse_expression()
            self.expect(TokenType.RPAREN)
            return expr
        
        else:
            self.error(f"Unexpected token in expression: {token.type}")
    
    def parse_function_call(self):
        """Parse function call: name(args)"""
        name = self.expect(TokenType.IDENTIFIER).value
        self.expect(TokenType.LPAREN)
        
        args = []
        if self.current_token().type != TokenType.RPAREN:
            args.append(self.parse_expression())
            while self.current_token().type == TokenType.COMMA:
                self.advance()
                args.append(self.parse_expression())
        
        self.expect(TokenType.RPAREN)
        return FunctionCall(name, args)
