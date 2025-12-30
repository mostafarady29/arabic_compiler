#!/bin/bash
# سكريبت تشغيل سريع للبرامج العربية
# Quick run script for Arabic programs

if [ $# -eq 0 ]; then
    echo "الاستخدام: ./run.sh <ملف_البرنامج.ar>"
    echo "Usage: ./run.sh <program_file.ar>"
    exit 1
fi

PROGRAM=$1
BASENAME=$(basename "$PROGRAM" .ar)

echo "🔨 جاري الترجمة... Compiling..."
python3 compiler.py "$PROGRAM" -o "${BASENAME}.s" || exit 1

echo "🔧 جاري التجميع... Assembling..."
as "${BASENAME}.s" -o "${BASENAME}.o" || exit 1

echo "🔗 جاري الربط... Linking..."
ld "${BASENAME}.o" -o "${BASENAME}" || exit 1

echo "▶️  تشغيل البرنامج... Running..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./"${BASENAME}"
EXIT_CODE=$?
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ انتهى البرنامج برمز الخروج: $EXIT_CODE"
echo "   Program exited with code: $EXIT_CODE"

# تنظيف الملفات المؤقتة
echo ""
echo "🧹 تنظيف الملفات المؤقتة..."
rm -f "${BASENAME}.s" "${BASENAME}.o"
echo "✓ تم!"
