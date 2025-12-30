"""
Lexer for Arabic Programming Language
Tokenizes Arabic source code into meaningful tokens
"""

import re
from enum import Enum, auto

class TokenType(Enum):
    # Keywords
    VAR = auto()        # متغير
    IF = auto()         # اذا
    ELSE = auto()       # والا
    WHILE = auto()      # بينما
    FOR = auto()        # لكل
    FUNCTION = auto()   # دالة
    RETURN = auto()     # ارجع
    PRINT = auto()      # اطبع
    
    # Identifiers and literals
    IDENTIFIER = auto()
    NUMBER = auto()
    
    # Operators
    PLUS = auto()       # +
    MINUS = auto()      # -
    MULTIPLY = auto()   # *
    DIVIDE = auto()     # /
    ASSIGN = auto()     # =
    EQ = auto()         # ==
    NE = auto()         # !=
    GT = auto()         # >
    LT = auto()         # <
    GE = auto()         # >=
    LE = auto()         # <=
    
    # Delimiters
    LPAREN = auto()     # (
    RPAREN = auto()     # )
    LBRACE = auto()     # {
    RBRACE = auto()     # }
    SEMICOLON = auto()  # ;
    COMMA = auto()      # ,
    
    # Special
    EOF = auto()
    NEWLINE = auto()

class Token:
    def __init__(self, type, value, line, column):
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"

class Lexer:
    # Arabic keywords mapping
    KEYWORDS = {
        'متغير': TokenType.VAR,
        'اذا': TokenType.IF,
        'والا': TokenType.ELSE,
        'بينما': TokenType.WHILE,
        'لكل': TokenType.FOR,
        'دالة': TokenType.FUNCTION,
        'ارجع': TokenType.RETURN,
        'اطبع': TokenType.PRINT,
    }
    
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens = []
    
    def error(self, msg):
        raise SyntaxError(f"Lexer error at {self.line}:{self.column}: {msg}")
    
    def current_char(self):
        if self.pos >= len(self.source):
            return None
        return self.source[self.pos]
    
    def peek_char(self, offset=1):
        pos = self.pos + offset
        if pos >= len(self.source):
            return None
        return self.source[pos]
    
    def advance(self):
        if self.pos < len(self.source):
            if self.source[self.pos] == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
            self.pos += 1
    
    def skip_whitespace(self):
        while self.current_char() and self.current_char() in ' \t\r\n':
            self.advance()
    
    def skip_comment(self):
        # Skip single-line comments starting with //
        if self.current_char() == '/' and self.peek_char() == '/':
            while self.current_char() and self.current_char() != '\n':
                self.advance()
    
    def read_number(self):
        start_col = self.column
        num = ''
        while self.current_char() and self.current_char().isdigit():
            num += self.current_char()
            self.advance()
        return Token(TokenType.NUMBER, num, self.line, start_col)
    
    def read_identifier(self):
        start_col = self.column
        ident = ''
        
        # Arabic characters and underscores
        while self.current_char() and (self.current_char().isalnum() or 
                                       self.current_char() == '_' or
                                       self.is_arabic_char(self.current_char())):
            ident += self.current_char()
            self.advance()
        
        # Check if it's a keyword
        token_type = self.KEYWORDS.get(ident, TokenType.IDENTIFIER)
        return Token(token_type, ident, self.line, start_col)
    
    def is_arabic_char(self, char):
        """Check if character is in Arabic Unicode range (excluding punctuation)"""
        if not char:
            return False
        code = ord(char)
        # Exclude Arabic punctuation marks like ؛ (U+061B) and ، (U+060C)
        if code in [0x060C, 0x061B, 0x061F]:  # Arabic comma, semicolon, question mark
            return False
        return (0x0600 <= code <= 0x06FF) or (0x0750 <= code <= 0x077F)
    
    def tokenize(self):
        while self.pos < len(self.source):
            self.skip_whitespace()
            
            if self.pos >= len(self.source):
                break
            
            # Skip comments
            if self.current_char() == '/' and self.peek_char() == '/':
                self.skip_comment()
                continue
            
            char = self.current_char()
            col = self.column
            
            # Numbers
            if char.isdigit():
                self.tokens.append(self.read_number())
            
            # Identifiers and keywords (including Arabic)
            elif char.isalpha() or char == '_' or self.is_arabic_char(char):
                self.tokens.append(self.read_identifier())
            
            # Operators and delimiters
            elif char == '+':
                self.tokens.append(Token(TokenType.PLUS, '+', self.line, col))
                self.advance()
            elif char == '-':
                self.tokens.append(Token(TokenType.MINUS, '-', self.line, col))
                self.advance()
            elif char == '*':
                self.tokens.append(Token(TokenType.MULTIPLY, '*', self.line, col))
                self.advance()
            elif char == '/':
                self.tokens.append(Token(TokenType.DIVIDE, '/', self.line, col))
                self.advance()
            elif char == '=':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.EQ, '==', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.ASSIGN, '=', self.line, col))
                    self.advance()
            elif char == '!':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.NE, '!=', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.error(f"Unexpected character '!'")
            elif char == '>':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.GE, '>=', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.GT, '>', self.line, col))
                    self.advance()
            elif char == '<':
                if self.peek_char() == '=':
                    self.tokens.append(Token(TokenType.LE, '<=', self.line, col))
                    self.advance()
                    self.advance()
                else:
                    self.tokens.append(Token(TokenType.LT, '<', self.line, col))
                    self.advance()
            elif char == '(':
                self.tokens.append(Token(TokenType.LPAREN, '(', self.line, col))
                self.advance()
            elif char == ')':
                self.tokens.append(Token(TokenType.RPAREN, ')', self.line, col))
                self.advance()
            elif char == '{':
                self.tokens.append(Token(TokenType.LBRACE, '{', self.line, col))
                self.advance()
            elif char == '}':
                self.tokens.append(Token(TokenType.RBRACE, '}', self.line, col))
                self.advance()
            elif char == ';' or char == '؛':  # Support both ASCII and Arabic semicolon
                self.tokens.append(Token(TokenType.SEMICOLON, ';', self.line, col))
                self.advance()
            elif char == ',' or char == '،':  # Support both ASCII and Arabic comma
                self.tokens.append(Token(TokenType.COMMA, ',', self.line, col))
                self.advance()
            else:
                self.error(f"Unexpected character '{char}'")
        
        # Add EOF token
        self.tokens.append(Token(TokenType.EOF, None, self.line, self.column))
        return self.tokens
