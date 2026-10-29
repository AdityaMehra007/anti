import os
import sys

path = os.path.join("blackbird", "blackbird.py")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

target1 = 'lines = getLinesFromFile("assets/text/splash.txt")'
replacement1 = 'splash_path = os.path.join(config.ASSETS_DIRECTORY, "text", "splash.txt"); lines = getLinesFromFile(splash_path) if isFile(splash_path) else getLinesFromFile("assets/text/splash.txt")'

target2 = 'config.console = Console()'
replacement2 = '''if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    config.console = Console()'''

text = text.replace(target1, replacement1)
text = text.replace(target2, replacement2, 1)

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("blackbird.py successfully patched for Windows UTF-8 and cross-directory paths.")
