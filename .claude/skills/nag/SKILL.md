---
name: nag
description: Manage Life With Claude feedback (bugs, flaws, wishes). Commands: add, fin, yay, doh.
argument-hint: "[add|fin|yay|doh] [ID or search]"
disable-model-invocation: true
context: fork
model: claude-opus-4-5
---

# /nag

Track issues about Claude Code.

**All paths below are relative to this skill's directory** (`.claude/skills/nag/`).

## Tone

- Concise: as short as possible whilst capturing what matters
- British English throughout
- Positive, friendly, hopeful
- Good humour keeps spirits up
- Titles: short, specific, action-oriented
- Focus on impact, not frustration

## Routing

Parse `$ARGUMENTS`:
- Empty → stats
- `add` or `add <text>` → add workflow
- `fin <target>` → create GitHub issue
- `yay <target>` → mark done
- `doh <target>` → edit

## Scripts

All in `scripts/`. Run Python scripts with `python3`, e.g. `python3 parse-readme.py stats`.
Accept raw questionnaire answers directly (e.g. "🐛 Bug" → normalized internally).

| Script | Usage | Returns |
|--------|-------|---------|
| `parse-readme.py stats` | Get counts | `{"bugs":N,"flaws":N,"wishes":N}` |
| `parse-readme.py search "query"` | Find entries | JSON array |
| `parse-readme.py next-id <category>` | Next ID (accepts "🐛 Bug" or "bug") | e.g. `B001` |
| `add-entry.py '<json>'` | Add entry (accepts raw answers) | Confirms |
| `mark-done.py ID` | Mark done | `TITLE:...` |
| `update-entry.py ID field value` | Edit | Confirms |
| `link-issue.py ID url` | Link GH issue to entry | Updates README |
| `commit.sh "msg" [files]` | Git commit (no push) | — |
| `push.sh` | Git push | — |
| `create-issue.sh ID title body-file` | GH issue | `ISSUE_URL:...` |
| `issues.py get ID` | Get tracked issue URL | URL or exit 1 |
| `issues.py set ID url` | Track issue URL | — |

## Questions

In `questions/`. To ask a question:
1. Read the JSON file with Read tool
2. Parse the `questions` array
3. Call AskUserQuestion tool with the parsed questions
4. Process the response

| File | Use |
|------|-----|
| `add.json` | Category + Priority (after user describes issue) |
| `confirm.json` | Final confirmation |
| `edit-field.json` | Which field to change (/doh) |

## Templates

In `templates/`. To display a template:
1. Read the file with Read tool
2. Replace `{{PLACEHOLDER}}` with actual values
3. Output the result as markdown text (not via a tool)

| File | Placeholders |
|------|-------------|
| `proposal.md` | `{{ID}}`, `{{EMOJI}}`, `{{CATEGORY}}`, `{{PRIORITY}}`, `{{TITLE}}`, `{{DESCRIPTION}}`, `{{GITHUB_ISSUE_BODY}}` (fill from GitHub template for this category) |
| `status.md` | `{{BUGS}}`, `{{FLAWS}}`, `{{WISHES}}` |
| `celebration.md` | `{{ID}}`, `{{TITLE}}` |
| `edit-display.md` | `{{ID}}`, `{{EMOJI}}`, `{{CATEGORY}}`, `{{PRIORITY}}`, `{{TITLE}}`, `{{DESCRIPTION}}` |
| `issue-body.md` | `{{ID}}`, `{{DESCRIPTION}}` |

## Reference

- `reference/detail-files.md` — Load when **creating GitHub issues**. MUST use templates from `templates/github.com_anthropics_claude-code/`.

## IDs & Emojis

| Type | ID prefix | Emoji | Indicates |
|------|-----------|-------|-----------|
| Bug | B | 🐛 | Broken, crash, error, fails |
| Flaw | F | 🤔 | Annoying, awkward, clunky |
| Wish | W | 💫 | Would be nice, want, please add |

Priority: `⭐⭐⭐`=High (blocks work), `⭐⭐`=Medium (notable), `⭐`=Low (nice to have)

## GitHub Templates

Choose template based on **issue content**, not category. All in `templates/github.com_anthropics_claude-code/`:

| Template | Use when |
|----------|----------|
| `bug_report.yml` | Crashes, errors, CLI misbehavior, infrastructure issues, things not working as documented |
| `model_behavior.yml` | Claude (the model) said/did something unexpected in conversation: modified wrong files, ignored instructions, made bad assumptions |
| `feature_request.yml` | New capabilities, enhancements, "it would be nice if..." |

**IMPORTANT**: Follow the YAML structure EXACTLY. Each template has specific fields (dropdowns, checkboxes, textareas). Read the template and fill EVERY field in `body:` according to its type and description.

## Lookup (for fin/yay/doh)

1. No target? Ask user.
2. Matches `[BFW]\d+`? Direct ID lookup.
3. Otherwise: `parse-readme.py search "query"` → 1 match=use, multiple=ask, none=suggest `/nag`.

---

## Workflow: /nag (stats)

1. `parse-readme.py stats`
2. Read `templates/status.md`, fill counts, display

## Workflow: /nag add [text]

**If text provided** (e.g. `/nag add the context window keeps compacting`):
- Transform user's raw thoughts into a polished entry:
  - **Category**: Infer from keywords (broken/crash → bug, annoying/awkward → flaw, want/wish → wish)
  - **Priority**: Infer from severity/frequency mentioned
  - **Title**: 5-10 words, action-oriented, MUST include key context (e.g., "plan mode" if that's the context). Don't over-generalise—preserve the specific scenario.
  - **Description**: Capture the full nuance. Include: what happens, when/where it happens, why it's problematic, what would be better. Don't strip detail that helps understand the issue.

**If no text** (just `/nag add`):
1. Output: "What's the issue?" (wait for user to type description)
2. User submits description
3. Immediately call AskUserQuestion with `questions/add.json` (category + priority)
4. Transform user's description into title + polished description (same rules as text-provided case)

Then:
1. `python3 parse-readme.py next-id <category>` → get ID (e.g. "B001")
2. Choose the best GitHub template based on issue content (see "GitHub Templates" table). Fill EVERY field from the YAML `body:` section:
   - `type: dropdown` → pick the most appropriate option
   - `type: checkbox` → mark as checked [x] or unchecked [ ]
   - `type: textarea` → write content matching the placeholder guidance
   - `type: input` → provide value (use "Unknown" if not available)
   Format the filled template as markdown. This becomes `{{GITHUB_ISSUE_BODY}}`
3. Read `templates/proposal.md`, fill all placeholders including `{{GITHUB_ISSUE_BODY}}`, output as markdown
4. Read `questions/confirm.json`, call AskUserQuestion:
   - "Lovely" → continue to step 5
   - "Hang on" → ask what to change, update values, go back to step 3
   - "No" → output "Alright, discarded." and stop
5. `python3 add-entry.py '{"id":"...","category":"...","priority":"...","title":"...","description":"..."}'`
6. `commit.sh "➕ {ID}: {title}" README.md`
7. Remind user: "Committed locally. Run `/nag fin {ID}` when ready to push and file with Anthropic."

If user wants extended details during edit: load `reference/detail-files.md`, collect content, write to `details/{ID}.md`, include in commit.

## Workflow: /nag fin <target>

Load `reference/detail-files.md`.

1. Lookup entry
2. `python3 issues.py get {ID}` → if URL returned, report it and stop
3. `push.sh` → push any pending commits first
4. `python3 parse-readme.py search "{ID}"` → get entry details as JSON
5. Check if `details/{ID}.md` exists (Read tool)
6. Choose the best GitHub template based on issue content (see "GitHub Templates" table)
7. Build issue body following template's YAML structure
8. Write body to `$TMPDIR/nag-issue-{ID}.md` (Write tool)
9. `create-issue.sh "{ID}" "{title}" "$TMPDIR/nag-issue-{ID}.md"` → parse `ISSUE_URL:` from output
10. `python3 link-issue.py {ID} {url}` → updates README with issue link
11. `python3 issues.py set {ID} {url}`
12. `commit.sh "📤 {ID}: Created issue" README.md .claude/skills/nag/issues.json`
13. `push.sh`
14. Output the issue URL

## Workflow: /nag yay <target>

1. Lookup entry
2. `mark-done.py {ID}` → get title
3. `commit.sh "✅ {ID}: {title}"`
4. Celebrate via `templates/celebration.md`
5. Remind user: "Committed locally. Run `/nag fin {ID}` to push."

## Workflow: /nag doh <target>

1. Lookup entry
2. `parse-readme.py search "{ID}"` → get current state as JSON
3. Display current state via `templates/edit-display.md` (fill + output)
4. `issues.py get {ID}` → if URL returned, mention "Also tracked as issue: {url}"
5. Ask via `questions/edit-field.json` → user picks field (title/priority/description/category)
6. Ask user: "What should the new {field} be?" (free text via AskUserQuestion with 2 placeholder options)
7. `update-entry.py {ID} {field} "{new_value}"`
8. `commit.sh "📝 {ID}: Updated {field}"`
9. If issue URL exists → `gh issue edit {url} --title` or `--body` to sync
10. Remind user: "Committed locally. Run `/nag fin {ID}` to push."
