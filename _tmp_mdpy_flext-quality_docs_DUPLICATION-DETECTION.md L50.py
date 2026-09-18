# from flext-quality/docs/DUPLICATION-DETECTION.md:50
from flext_quality import FlextDuplicationPlugin
from pathlib import Path

plugin = FlextDuplicationPlugin()

# Check files for duplication
files = [Path("file1.py"), Path("file2.py")]
result = plugin.check(files)

if result.success:
    for dup in result.value.duplicates:
        print(f"{dup.file1} <-> {dup.file2}: {dup.similarity:.1%}")
