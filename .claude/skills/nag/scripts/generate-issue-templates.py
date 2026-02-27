#!/usr/bin/env python3
"""Generate markdown fill-in templates from GitHub issue YAML templates.

Converts YAML form definitions to markdown templates with {{PLACEHOLDERS}}.
Preserves structure strictly: checkboxes stay checkboxes, links stay links.

No external dependencies - parses YAML manually since structure is predictable.
"""

import re
import sys
from pathlib import Path

# Add script directory to path for bootstrap
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap import GH_TEMPLATES_DIR, TEMPLATES_DIR


# Map YAML template filenames to output markdown filenames
TEMPLATE_MAP = {
    "bug_report.yml": "github-issue-bug.md",
    "feature_request.yml": "github-issue-feature.md",
    "model_behavior.yml": "github-issue-model.md",
}


def parse_yaml_template(yaml_path: Path) -> list[dict]:
    """Parse GitHub issue YAML template into structured items.

    Simple parser for the specific YAML structure used by GitHub issue templates.
    Handles: type, id, attributes.label, attributes.options, attributes.render
    """
    content = yaml_path.read_text()
    items = []
    current_item = None
    current_options = []
    in_options = False
    indent_stack = []

    for line in content.split('\n'):
        stripped = line.strip()

        # New body item
        if re.match(r'^- type:\s*(\w+)', stripped):
            if current_item:
                if current_options:
                    current_item['options'] = current_options
                items.append(current_item)
            match = re.match(r'^- type:\s*(\w+)', stripped)
            current_item = {'type': match.group(1)}
            current_options = []
            in_options = False

        elif current_item:
            # Item ID
            if match := re.match(r'^id:\s*(.+)', stripped):
                current_item['id'] = match.group(1).strip()

            # Label
            elif match := re.match(r'^label:\s*(.+)', stripped):
                current_item['label'] = match.group(1).strip()

            # Render (for code blocks)
            elif match := re.match(r'^render:\s*(.+)', stripped):
                current_item['render'] = match.group(1).strip()

            # Options start
            elif stripped == 'options:':
                in_options = True

            # Option label (checkbox item with label: prefix)
            elif in_options and (match := re.match(r'^- label:\s*(.+)', stripped)):
                current_options.append(match.group(1).strip())

            # Plain option (dropdown item, just "- value")
            elif in_options and (match := re.match(r'^- ([^:].*)$', stripped)):
                # Only if it's not a nested key like "- label:"
                value = match.group(1).strip().strip('"').strip("'")
                if value:
                    current_options.append(value)

    # Don't forget last item
    if current_item:
        if current_options:
            current_item['options'] = current_options
        items.append(current_item)

    return items


def yaml_to_markdown(yaml_path: Path) -> str:
    """Convert a GitHub issue YAML template to markdown with placeholders."""
    items = parse_yaml_template(yaml_path)
    sections = []

    for item in items:
        item_type = item.get('type')
        item_id = item.get('id', '').upper().replace('-', '_')
        label = item.get('label', '')

        if item_type == 'markdown':
            # Skip intro markdown - it's just instructions
            continue

        elif item_type == 'checkboxes':
            sections.append(f"### {label}\n")
            for opt_label in item.get('options', []):
                # Keep checkbox syntax exactly, preserve any markdown links
                sections.append(f"- [x] {opt_label}")
            sections.append("")  # blank line after

        elif item_type == 'textarea':
            placeholder_id = f"{{{{{item_id}}}}}"
            sections.append(f"### {label}\n")
            # Only use code block for non-markdown render types (shell, etc.)
            render_type = item.get('render')
            if render_type and render_type != 'markdown':
                sections.append(f"```\n{placeholder_id}\n```\n")
            else:
                sections.append(f"{placeholder_id}\n")

        elif item_type == 'dropdown':
            placeholder_id = f"{{{{{item_id}}}}}"
            options = item.get('options', [])
            sections.append(f"### {label}\n")
            sections.append(f"{placeholder_id}")
            if options:
                # Include options as HTML comment (hidden when rendered)
                opts_str = " | ".join(options)
                sections.append(f"<!-- Options: {opts_str} -->\n")
            else:
                sections.append("\n")

        elif item_type == 'input':
            placeholder_id = f"{{{{{item_id}}}}}"
            sections.append(f"### {label}\n")
            sections.append(f"{placeholder_id}\n")

    return "\n".join(sections).strip() + "\n"


def generate_all():
    """Generate all markdown templates from YAML sources."""
    gh_templates_dir = Path(GH_TEMPLATES_DIR)
    templates_dir = Path(TEMPLATES_DIR)

    if not gh_templates_dir.exists():
        print(f"GitHub templates directory not found: {gh_templates_dir}")
        sys.exit(1)

    generated = []
    for yaml_name, md_name in TEMPLATE_MAP.items():
        yaml_path = gh_templates_dir / yaml_name
        md_path = templates_dir / md_name

        if not yaml_path.exists():
            print(f"Warning: {yaml_path} not found, skipping")
            continue

        markdown = yaml_to_markdown(yaml_path)
        md_path.write_text(markdown)
        generated.append(md_name)
        print(f"Generated: {md_name}")

    return generated


if __name__ == "__main__":
    generate_all()
