# customize.py
NEW_NAME = "aivoicegen"                 # <- your public project/app name
YOUR_NAME = "Harshitha Arroju"          # <- your name
YOUR_REPO_URL = "https://github.com/harshithaarroju01/aivoicegen"  # <- your repo

from pathlib import Path
import re

root = Path(__file__).resolve().parent
pp = root / "pyproject.toml"
consts = root / "aivoicegen" / "constants.py"
version = root / "aivoicegen" / "Swecha"
readme = root / "README.md"
license_f = root / "LICENSE"

# --- helpers
def sub_file(path: Path, subs: list[tuple[str,str]]):
    text = path.read_text(encoding="utf-8", errors="ignore")
    for pat, rep in subs:
        text = re.sub(pat, rep, text, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8")

# --- constants.py: change visible program name + GitHub url
if consts.exists():
    sub_file(consts, [
        (r'^(PROGRAM_NAME\s*=\s*)".*"', rf'\1"{NEW_NAME}"'),
        (r'^(GITHUB_URL\s*=\s*)".*"', rf'\1"{YOUR_REPO_URL}"'),
    ])

# --- pyproject.toml: change project name, urls, script names
if pp.exists():
    sub_file(pp, [
        (r'(?m)^(name\s*=\s*)".*"', rf'\1"{NEW_NAME}"'),
        (r'(?m)^(Homepage\s*=\s*)".*"', rf'\1"{YOUR_REPO_URL}"'),
        (r'(?m)^(Documentation\s*=\s*)".*"', rf'\1"{YOUR_REPO_URL}"'),
        (r'(?m)^(Repository\s*=\s*)".*"', rf'\1"{YOUR_REPO_URL}"'),
        (r'(?m)^(Issues\s*=\s*)".*"', rf'\1"{YOUR_REPO_URL}/issues"'),
        # gui script key: abogen -> NEW_NAME (value still calls abogen.main)
        (r'(?ms)^\[project\.gui-scripts\]\s*\n([^\n]+abogen\s*=\s*"[^\n]+")',
         lambda m: m.group(0).replace("abogen", NEW_NAME, 1)),
        # cli script key: abogen-cli -> NEW_NAME-cli
        (r'(?ms)^\[project\.scripts\]\s*\n([^\n]+abogen-cli\s*=\s*"[^\n]+")',
         lambda m: m.group(0).replace("abogen-cli", f"{NEW_NAME}-cli", 1)),
    ])

# --- VERSION: bump & tag
if version.exists():
    ver_text = version.read_text(encoding="utf-8", errors="ignore").strip()
    if ver_text:
        new_ver = ver_text + "-swecha"
    else:
        new_ver = "1.1.0-swecha"
    version.write_text(new_ver, encoding="utf-8")

# --- README: re-title + add customization note at top
if readme.exists():
    txt = readme.read_text(encoding="utf-8", errors="ignore")
    # Replace first markdown H1 line to use NEW_NAME
    txt = re.sub(r'^#\s*.*$', f"# {NEW_NAME}", txt, count=1, flags=re.MULTILINE)
    banner = (
        f"\n> Customized by **{YOUR_NAME}** during **Swecha AI Internship**.\n"
        f"> Original project under MIT license. See LICENSE.\n\n"
    )
    # Add banner if not present
    if "Customized by" not in txt:
        txt = banner + txt
    readme.write_text(txt, encoding="utf-8")

# --- LICENSE: append modification notice (keep original intact)
mod_line = f"\nAdditional notice: Modifications by {YOUR_NAME}.\n"
with open(license_f, "a", encoding="utf-8") as f:
    f.write(mod_line)

print("✅ Customization complete.")
print(f"- Public name: {NEW_NAME}")
print(f"- Repo URLs set to: {YOUR_REPO_URL}")
