"""
Code Generator for Arabic Programming Language
Generates x86-64 assembly code (Intel syntax) for Linux
"""

from ast_nodes import *

class CodeGenerator:
    def __init__(self):
        self.output = []
        self.label_counter = 0
        self.string_counter = 0
        self.data_section = []
        self.current_function = None
        self.local_vars = {}  # Maps variable name to stack offset
        self.stack_offset = 0
    
    def new_label(self, prefix="L"):
        """Generate a unique label"""
        label = f"{prefix}{self.label_counter}"
        self.label_counter += 1
        return label
    
    def emit(self, code):
        """Emit assembly code"""
        self.output.append(code)
    
    def generate(self, program):
        """Generate assembly for entire program"""
        # Enable Intel syntax for GNU assembler
        self.emit(".intel_syntax noprefix")
        self.emit("")
        
        # Generate data section
        self.emit(".section .data")
        self.emit("fmt_int: .asciz \"%d\\n\"")
        
        # Generate code section
        self.emit(".section .text")
        self.emit(".global _start")
        
        # Generate each function
        for func in program.functions:
            self.generate_function(func)
        
        # Generate _start entry point that calls رئيسية (main)
        self.emit("")
        self.emit("_start:")
        self.emit("    call رئيسية")
        self.emit("    mov rdi, rax")
        self.emit("    mov rax, 60")
        self.emit("    syscall")
        
        return "\n".join(self.output)
    
    def generate_function(self, func):
        """Generate code for a function"""
        self.current_function = func
        self.local_vars = {}
        self.stack_offset = 0
        
        self.emit("")
        self.emit(f"{func.name}:")
        self.emit("    push rbp")
        self.emit("    mov rbp, rsp")
        
        # Reserve space for local variables (we'll fix this later)
        # For now, reserve 256 bytes
        self.emit("    sub rsp, 256")
        
        # Store parameters on stack
        param_registers = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']
        for i, param in enumerate(func.params):
            if i < len(param_registers):
                offset = self.allocate_local(param)
                self.emit(f"    mov [rbp{offset}], {param_registers[i]}")
        
        # Generate function body
        self.generate_block(func.body)
        
        # Function epilogue (in case no return statement)
        self.emit("    mov rsp, rbp")
        self.emit("    pop rbp")
        self.emit("    ret")
    
    def allocate_local(self, name):
        """Allocate space for a local variable on stack"""
        self.stack_offset -= 8
        self.local_vars[name] = self.stack_offset
        return self.stack_offset
    
    def get_var_location(self, name):
        """Get stack location of variable"""
        if name in self.local_vars:
            return f"[rbp{self.local_vars[name]}]"
        else:
            raise NameError(f"Variable '{name}' not found")
    
    def generate_block(self, block):
        """Generate code for a block"""
        for stmt in block.statements:
            self.generate_statement(stmt)
    
    def generate_statement(self, stmt):
        """Generate code for a statement"""
        if isinstance(stmt, VarDecl):
            # Allocate space and evaluate initial value
            offset = self.allocate_local(stmt.name)
            self.generate_expression(stmt.value)
            self.emit(f"    mov [rbp{offset}], rax")
        
        elif isinstance(stmt, Assignment):
            self.generate_expression(stmt.value)
            location = self.get_var_location(stmt.name)
            self.emit(f"    mov {location}, rax")
        
        elif isinstance(stmt, IfStatement):
            else_label = self.new_label("else")
            end_label = self.new_label("endif")
            
            # Evaluate condition
            self.generate_expression(stmt.condition)
            self.emit("    cmp rax, 0")
            self.emit(f"    je {else_label}")
            
            # Then block
            self.generate_block(stmt.then_block)
            self.emit(f"    jmp {end_label}")
            
            # Else block
            self.emit(f"{else_label}:")
            if stmt.else_block:
                self.generate_block(stmt.else_block)
            
            self.emit(f"{end_label}:")
        
        elif isinstance(stmt, WhileStatement):
            start_label = self.new_label("while_start")
            end_label = self.new_label("while_end")
            
            self.emit(f"{start_label}:")
            self.generate_expression(stmt.condition)
            self.emit("    cmp rax, 0")
            self.emit(f"    je {end_label}")
            
            self.generate_block(stmt.body)
            self.emit(f"    jmp {start_label}")
            
            self.emit(f"{end_label}:")
        
        elif isinstance(stmt, ReturnStatement):
            self.generate_expression(stmt.value)
            self.emit("    mov rsp, rbp")
            self.emit("    pop rbp")
            self.emit("    ret")
        
        elif isinstance(stmt, PrintStatement):
            # Evaluate expression and print using syscall
            self.generate_expression(stmt.value)
            self.generate_print_int()
        
        elif isinstance(stmt, FunctionCall):
            self.generate_function_call(stmt)
    
    def generate_expression(self, expr):
        """Generate code for expression, result in rax"""
        if isinstance(expr, Number):
            self.emit(f"    mov rax, {expr.value}")
        
        elif isinstance(expr, Identifier):
            location = self.get_var_location(expr.name)
            self.emit(f"    mov rax, {location}")
        
        elif isinstance(expr, BinaryOp):
            # Evaluate right side first, push to stack
            self.generate_expression(expr.right)
            self.emit("    push rax")
            
            # Evaluate left side
            self.generate_expression(expr.left)
            
            # Pop right side to rbx
            self.emit("    pop rbx")
            
            # Perform operation
            if expr.op == '+':
                self.emit("    add rax, rbx")
            elif expr.op == '-':
                self.emit("    sub rax, rbx")
            elif expr.op == '*':
                self.emit("    imul rax, rbx")
            elif expr.op == '/':
                self.emit("    cqo")
                self.emit("    idiv rbx")
            elif expr.op == '==':
                self.emit("    cmp rax, rbx")
                self.emit("    sete al")
                self.emit("    movzx rax, al")
            elif expr.op == '!=':
                self.emit("    cmp rax, rbx")
                self.emit("    setne al")
                self.emit("    movzx rax, al")
            elif expr.op == '>':
                self.emit("    cmp rax, rbx")
                self.emit("    setg al")
                self.emit("    movzx rax, al")
            elif expr.op == '<':
                self.emit("    cmp rax, rbx")
                self.emit("    setl al")
                self.emit("    movzx rax, al")
            elif expr.op == '>=':
                self.emit("    cmp rax, rbx")
                self.emit("    setge al")
                self.emit("    movzx rax, al")
            elif expr.op == '<=':
                self.emit("    cmp rax, rbx")
                self.emit("    setle al")
                self.emit("    movzx rax, al")
        
        elif isinstance(expr, UnaryOp):
            self.generate_expression(expr.value)
            if expr.op == '-':
                self.emit("    neg rax")
        
        elif isinstance(expr, FunctionCall):
            self.generate_function_call(expr)
    
    def generate_function_call(self, call):
        """Generate function call"""
        # Evaluate arguments and pass in registers
        param_registers = ['rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9']
        
        # Evaluate arguments in reverse order and push to stack
        for arg in reversed(call.args):
            self.generate_expression(arg)
            self.emit("    push rax")
        
        # Pop arguments into registers
        for i in range(len(call.args)):
            if i < len(param_registers):
                self.emit(f"    pop {param_registers[i]}")
        
        # Call function
        self.emit(f"    call {call.name}")
    
    def generate_print_int(self):
        """Generate code to print integer in rax"""
        # Convert integer to string and print
        # For simplicity, we'll use a simple digit-by-digit conversion
        
        self.emit("    # Print integer in rax")
        self.emit("    mov rdi, rax")
        self.emit("    call print_number")
    
    def add_print_helper(self):
        """Add helper function to print numbers"""
        helper = """
print_number:
    push rbp
    mov rbp, rsp
    sub rsp, 32
    
    mov rax, rdi
    mov rcx, 10
    lea rsi, [rbp-32]
    mov BYTE PTR [rsi], 10
    inc rsi
    
    test rax, rax
    jns .convert_digits
    neg rax
    push rax
    mov rax, 45
    mov BYTE PTR [rsi], al
    inc rsi
    pop rax
    
.convert_digits:
    test rax, rax
    jnz .digit_loop
    mov BYTE PTR [rsi], 48
    inc rsi
    jmp .print_loop
    
.digit_loop:
    test rax, rax
    jz .print_loop
    xor rdx, rdx
    div rcx
    add dl, 48
    mov BYTE PTR [rsi], dl
    inc rsi
    jmp .digit_loop
    
.print_loop:
    dec rsi
    cmp BYTE PTR [rsi], 10
    je .end_print
    
    mov rax, 1
    mov rdi, 1
    mov rdx, 1
    syscall
    jmp .print_loop
    
.end_print:
    mov rsp, rbp
    pop rbp
    ret
"""
        return helper
