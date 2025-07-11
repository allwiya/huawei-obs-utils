#!/usr/bin/env python3
"""
Script to update copyright headers in all Python files

Copyright 2025 CCVASS - Lima, Peru

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: contact@ccvass.com
"""

import glob
import os

COPYRIGHT_HEADER = """
Copyright 2025 CCVASS - Lima, Peru

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: contact@ccvass.com
"""


def update_python_file(filepath):
    """Update copyright header in a Python file"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.split("\n")

    # Find the end of the existing docstring
    in_docstring = False
    docstring_end = 0

    for i, line in enumerate(lines):
        if line.strip().startswith('"""') or line.strip().startswith("'''"):
            if not in_docstring:
                in_docstring = True
            else:
                docstring_end = i
                break
        elif in_docstring and (line.strip().endswith('"""') or line.strip().endswith("'''")):
            docstring_end = i
            break

    # Check if copyright already exists
    has_copyright = any("Copyright 2025 CCVASS" in line for line in lines[:20])

    if not has_copyright and docstring_end > 0:
        # Insert copyright after docstring
        new_lines = lines[: docstring_end + 1]
        new_lines.append(COPYRIGHT_HEADER)
        new_lines.extend(lines[docstring_end + 1 :])

        new_content = "\n".join(new_lines)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

        print(f"✅ Updated: {filepath}")
    else:
        print(f"⏭️  Skipped: {filepath} (already has copyright or no docstring)")


def main():
    """Main function to update all Python files"""
    print("🔄 Updating copyright headers in Python files...")

    # Find all Python files
    python_files = []
    for pattern in ["*.py", "tests/*.py"]:
        python_files.extend(glob.glob(pattern))

    # Update each file
    for filepath in python_files:
        if os.path.isfile(filepath):
            update_python_file(filepath)

    print(f"\n✅ Processed {len(python_files)} Python files")
    print("🎉 Copyright header update completed!")


if __name__ == "__main__":
    main()
