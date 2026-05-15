import os
from pathlib import Path

ROOT = Path('.')

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>{title}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            line-height: 1.6;
        }}

        h1 {{
            border-bottom: 2px solid #ccc;
            padding-bottom: 10px;
        }}

        ul {{
            list-style-type: none;
            padding-left: 0;
        }}

        li {{
            margin: 8px 0;
        }}

        a {{
            text-decoration: none;
            color: #0366d6;
        }}

        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <ul>
        {links}
    </ul>
</body>
</html>
"""

EXCLUDED = {
    '.git',
    '.github',
    '__pycache__'
}

for current_dir, dirs, files in os.walk(ROOT):
    dirs[:] = [d for d in dirs if d not in EXCLUDED]

    current_path = Path(current_dir)

    links = []

    # Add parent link
    if current_path != ROOT:
        links.append('<li><a href="../index.html">⬅ Back</a></li>')

    # Add subfolders
    for d in sorted(dirs):
        links.append(f'<li>📁 <a href="{d}/index.html">{d}</a></li>')

    # Add files
    for f in sorted(files):
        if f == 'index.html':
            continue

        file_path = current_path / f

        # Only include readable docs/files
        allowed = (
            f.endswith('.html') or
            f.endswith('.md') or
            f.endswith('.txt') or
            f.endswith('.pdf') or
            f.endswith('.json')
        )

        if allowed:
            links.append(f'<li>📄 <a href="{f}">{f}</a></li>')

    title = current_path.name if current_path.name else 'Documentation Home'

    html = HTML_TEMPLATE.format(
        title=title,
        links='\n'.join(links)
    )

    output_file = current_path / 'index.html'

    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(html)

    print(f'Generated: {output_file}')

print('\nDone generating all index pages.')