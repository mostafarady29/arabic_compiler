#!/usr/bin/env python3
"""
Arabic Programming Language Compiler
Compiles Arabic source code to x86-64 assembly
"""

import sys
import argparse
from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from codegen import CodeGenerator

def compile_file(input_file, output_file):
    """Compile a single Arabic source file to assembly"""
    try:
        # Read source code
        with open(input_file, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Lexical analysis
        print(f"[1/4] Lexical analysis...")
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        
        # Parsing
        print(f"[2/4] Parsing...")
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Semantic analysis
        print(f"[3/4] Semantic analysis...")
        analyzer = SemanticAnalyzer()
        analyzer.analyze(ast)
        
        # Code generation
        print(f"[4/4] Code generation...")
        generator = CodeGenerator()
        assembly = generator.generate(ast)
        assembly += "\n" + generator.add_print_helper()
        
        # Write output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(assembly)
        
        print(f"✓ Compilation successful!")
        print(f"  Output: {output_file}")
        print(f"\nTo assemble and link:")
        print(f"  as {output_file} -o {output_file[:-2]}.o")
        print(f"  ld {output_file[:-2]}.o -o {output_file[:-2]}")
        
        return True
        
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found", file=sys.stderr)
        return False
    except SyntaxError as e:
        print(f"Syntax Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(description='Arabic Programming Language Compiler')
    parser.add_argument('input', help='Input Arabic source file (.ar)')
    parser.add_argument('-o', '--output', help='Output assembly file (.s)', default=None)
    parser.add_argument('--tokens', action='store_true', help='Print tokens')
    parser.add_argument('--ast', action='store_true', help='Print AST')
    
    args = parser.parse_args()
    
    # Determine output filename
    if args.output:
        output_file = args.output
    else:
        output_file = args.input.rsplit('.', 1)[0] + '.s'
    
    # Compile
    success = compile_file(args.input, output_file)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
