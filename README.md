# مترجم اللغة العربية البرمجية
# Arabic Programming Language Compiler

A compiler written in Python that translates Arabic programming language source code into x86-64 assembly code.

## اللغة العربية البرمجية (Arabic Programming Language)

### الكلمات المفتاحية (Keywords)

- `متغير` (mutaghayyir) - variable declaration
- `اذا` (idha) - if
- `والا` (wa-illa) - else
- `بينما` (baynama) - while
- `دالة` (dallah) - function
- `ارجع` (irjiʿ) - return
- `اطبع` (itbaʿ) - print

### مثال (Example)

```arabic
دالة رئيسية() {
    متغير س = 10؛
    متغير ص = 20؛
    متغير مجموع = س + ص؛
    اطبع(مجموع)؛
    ارجع 0؛
}
```

## الميزات (Features)

- ✅ Variables and assignments
- ✅ Arithmetic operations (+, -, *, /)
- ✅ Comparison operators (==, !=, >, <, >=, <=)
- ✅ Conditional statements (if/else)
- ✅ While loops
- ✅ Functions with parameters
- ✅ Recursion
- ✅ Print statement for output
- ✅ Full UTF-8 Unicode support

## التثبيت (Installation)

No installation required! Just Python 3.6+ and standard Linux tools (`as`, `ld`).

```bash
# Clone or download the compiler
cd arabic_compiler
```

## الاستخدام (Usage)

### 1. Write your Arabic program

Create a `.ar` file:

```arabic
// hello.ar
دالة رئيسية() {
    متغير رقم = 42؛
    اطبع(رقم)؛
    ارجع 0؛
}
```

### 2. Compile to assembly

```bash
python3 compiler.py examples/hello.ar -o hello.s
```

### 3. Assemble and link

```bash
as hello.s -o hello.o
ld hello.o -o hello
```

### 4. Run!

```bash
./hello
# Output: 42
```

## أمثلة (Examples)

### Example 1: Basic Arithmetic

```arabic
دالة رئيسية() {
    متغير س = 15؛
    متغير ص = 7؛
    متغير نتيجة = س + ص * 2؛
    اطبع(نتيجة)؛  // Output: 29
    ارجع 0؛
}
```

### Example 2: Factorial (Recursion)

```arabic
دالة مضروب(ع) {
    اذا (ع <= 1) {
        ارجع 1؛
    } والا {
        متغير نتيجة = ع * مضروب(ع - 1)؛
        ارجع نتيجة؛
    }
}

دالة رئيسية() {
    متغير نتيجة = مضروب(5)؛
    اطبع(نتيجة)؛  // Output: 120
    ارجع 0؛
}
```

### Example 3: Fibonacci Sequence

```arabic
دالة رئيسية() {
    متغير ا = 0؛
    متغير ب = 1؛
    متغير عداد = 0؛
    
    بينما (عداد < 10) {
        اطبع(ا)؛
        متغير مؤقت = ا + ب؛
        ا = ب؛
        ب = مؤقت؛
        عداد = عداد + 1؛
    }
    
    ارجع 0؛
}
```

## بنية المترجم (Compiler Architecture)

The compiler consists of four main phases:

1. **Lexer** (`lexer.py`) - Tokenizes Arabic source code
2. **Parser** (`parser.py`) - Builds Abstract Syntax Tree (AST)
3. **Semantic Analyzer** (`semantic.py`) - Validates variable usage and types
4. **Code Generator** (`codegen.py`) - Generates x86-64 assembly code

## القواعد النحوية (Syntax Rules)

### Variable Declaration
```arabic
متغير اسم = قيمة؛
```

### Assignment
```arabic
اسم = قيمة_جديدة؛
```

### If Statement
```arabic
اذا (شرط) {
    // code
} والا {
    // code
}
```

### While Loop
```arabic
بينما (شرط) {
    // code
}
```

### Function Definition
```arabic
دالة الاسم(معامل1، معامل2) {
    // code
    ارجع قيمة؛
}
```

### Print Statement
```arabic
اطبع(تعبير)؛
```

### Comments
```arabic
// تعليق سطر واحد
```

## المتطلبات (Requirements)

- Python 3.6 or higher
- GNU Assembler (`as`) for x86-64
- GNU Linker (`ld`)
- Linux operating system

## الملفات (Files)

```
arabic_compiler/
├── compiler.py      # Main compiler driver
├── lexer.py         # Lexical analyzer
├── parser.py        # Parser
├── ast_nodes.py     # AST node definitions
├── semantic.py      # Semantic analyzer
├── codegen.py       # Code generator
├── README.md        # Documentation
└── examples/        # Example programs
    ├── hello.ar
    ├── factorial.ar
    ├── fibonacci.ar
    └── comprehensive.ar
```

## القيود (Limitations)

Current version supports:
- Integer arithmetic only (no strings or floats)
- No arrays or data structures
- Limited to x86-64 Linux
- No standard library (only print function)

## المساهمة (Contributing)

Feel free to extend the compiler with:
- String support
- Arrays and data structures
- More control flow (for loops, switch)
- Standard library functions
- Optimization passes

## الترخيص (License)

Free to use and modify for educational purposes.

---

**صُنع بـ ❤️ لمجتمع المبرمجين العرب**  
**Made with ❤️ for the Arab programming community**
