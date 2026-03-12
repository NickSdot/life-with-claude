---
name: nag
description: Manage Life With Claude feedback (bugs, flaws, wishes). Commands: add, fin, yay, doh.
argument-hint: "[add|fin|yay|doh] [ID or search]"
context: fork
agent: general-purpose
model: opus
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

**Command:** $0
**Target:** $1

| Command | Workflow |
|---------|----------|
| (empty) | stats |
| `add` | add |
| `fin` | fin |
| `yay` | yay |
| `doh` | doh |

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
| `issues.py get ID` | Get tracked issue URL | URL or "none" |
| `issues.py set ID url` | Track issue URL or "none" | — |

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

In `templates/`. To use a template:
1. Read the file with Read tool
2. Replace `{{PLACEHOLDER}}` with actual values
3. Output the result as markdown text (not via a tool)

### Display Templates

| File | Placeholders |
|------|-------------|
| `proposal.md` | `{{ID}}`, `{{EMOJI}}`, `{{CATEGORY}}`, `{{PRIORITY}}`, `{{TITLE}}`, `{{DESCRIPTION}}`, `{{GITHUB_ISSUE_BODY}}` |
| `status.md` | `{{BUG}}`, `{{FLAW}}`, `{{WISH}}` |
| `celebration.md` | `{{ID}}`, `{{TITLE}}` |
| `edit-display.md` | `{{ID}}`, `{{EMOJI}}`, `{{CATEGORY}}`, `{{PRIORITY}}`, `{{TITLE}}`, `{{DESCRIPTION}}` |

### GitHub Issue Templates

Use these to build `{{GITHUB_ISSUE_BODY}}`. Read, fill placeholders, preserve structure exactly.

| File | Use when |
|------|----------|
| `github-issue-bug.md` | Crashes, errors, CLI misbehavior, infrastructure issues |
| `github-issue-model.md` | Claude said/did something unexpected: wrong files, ignored instructions, bad assumptions |
| `github-issue-feature.md` | New capabilities, enhancements, "it would be nice if..." |

**CRITICAL**: These templates are structured to match GitHub's issue forms. Do NOT:
- Change checkbox syntax (keep `- [x]` exactly)
- Remove or reorder sections
- Alter heading levels
- Remove links in checkbox labels

For unknown fields, use "Unknown" or "N/A" rather than omitting.

## Reference

- `reference/detail-files.md` — Load when **creating GitHub issues**.
- `templates/github.com_anthropics_claude-code/*.yml` — Original GitHub template definitions (for reference only, use the markdown templates above)

## IDs & Emojis

| Type | ID prefix | Emoji | Indicates |
|------|-----------|-------|-----------|
| Bug | B | 🐛 | Broken, crash, error, fails |
| Flaw | F | 🤔 | Annoying, awkward, clunky |
| Wish | W | 💫 | Would be nice, want, please add |

## GitHub Issue Title Prefixes

Use these exactly as shown (from the GitHub YAML templates):

| Template | Title prefix |
|----------|--------------|
| bug | `[BUG] ` |
| model | `[MODEL] ` |
| feature | `[FEATURE] ` |

Priority: `⭐⭐⭐`=High (blocks work), `⭐⭐`=Medium (notable), `⭐`=Low (nice to have)

## Lookup (for fin/yay/doh)

1. No target? Ask user.
2. Matches `[BFW]\d+`? Direct ID lookup.
3. Otherwise: `parse-readme.py search "query"` → 1 match=use, multiple=ask, none=suggest `/nag`.

---

## Workflow: /nag (stats)

1. `parse-readme.py stats`
2. Read `templates/status.md`, fill counts, display

## Workflow: /nag add [text]

**MANDATORY**: Always show the proposal (via `templates/proposal.md`) and ask for confirmation (via `questions/confirm.json`) before adding an entry. Never skip the review step, even if the user provides complete information upfront.

**If text provided** (e.g. `/nag add the context window keeps compacting`):
1. Transform user's raw thoughts into a polished entry:
   - **Category**: Infer from keywords (broken/crash → bug, annoying/awkward → flaw, want/wish → wish)
   - **Priority**: Infer from severity/frequency mentioned
   - **Title**: 5-10 words, action-oriented, MUST include key context (e.g., "plan mode" if that's the context). Don't over-generalise—preserve the specific scenario.
   - **Description**: Capture the full nuance. Include: what happens, when/where it happens, why it's problematic, what would be better. Don't strip detail that helps understand the issue.
2. Call AskUserQuestion with `questions/add.json` to confirm/adjust category, priority, and select template

**If no text** (just `/nag add`):
1. Output: "What's the issue?" (wait for user to type description)
2. User submits description
3. Call AskUserQuestion with `questions/add.json` (category + priority + template)
4. Transform user's description into title + polished description (same rules as text-provided case)

**Template mapping** (from questionnaire answer):
- "🐛 Bug report" → `bug` (uses `github-issue-bug.md`)
- "🤖 Model behaviour" → `model` (uses `github-issue-model.md`)
- "✨ Feature request" → `feature` (uses `github-issue-feature.md`)
- "📝 None" → `none` (no GitHub issue)

Then:
1. `python3 parse-readme.py next-id <category>` → get ID (e.g. "B001")
2. **If template is NOT "none":**
   - Read the chosen template (e.g. `templates/github-issue-bug.md`), fill all `{{PLACEHOLDERS}}`. This becomes `{{GITHUB_ISSUE_BODY}}`
   - Read `templates/proposal.md`, fill all placeholders, output as markdown
3. **If template IS "none":**
   - Skip GitHub preview. Show only: ID, category, priority, title, description
4. Read `questions/confirm.json`, call AskUserQuestion:
   - "Lovely" → continue to step 5
   - "Hang on" → ask what to change, update values, go back to step 2
   - "No" → output "Alright, discarded." and stop
5. **If template is NOT "none":** create the GitHub issue now:
   - Write the approved `{{GITHUB_ISSUE_BODY}}` to `details/{ID}.md`
   - `create-issue.sh "{template}" "{entry_title}" "details/{ID}.md"` → parse `ISSUE_URL:` from output
6. `python3 add-entry.py '{"id":"...","category":"...","priority":"...","title":"...","description":"..."}'`
7. **If issue was created:** `python3 link-issue.py {ID} {url}` → adds issue link to README entry
8. `python3 issues.py set {ID} {url_or_"none"}` → track URL or "none"
9. `commit.sh "➕ {ID}: {title}" README.md details/issues.json details/`
10. `push.sh`
11. **If template is "none":** "Done. This entry won't create a GitHub issue."
    **Otherwise:** Output the issue URL.

If user wants extended details during edit: load `reference/detail-files.md`, collect content, write to `details/{ID}.md`, include in commit.

## Workflow: /nag fin <target>

Creates a GitHub issue for entries that were added without one (template "none" or failed creation).

1. Lookup entry
2. `python3 issues.py get {ID}` → check stored value:
   - If starts with `http` → output "Issue already exists: {url}" and stop
   - If `"none"` or not found → continue
3. Ask which template to use (AskUserQuestion with template options from `questions/add.json`, template question only)
4. `python3 parse-readme.py search "{ID}"` → get entry details as JSON
5. Read the chosen template file, fill all `{{PLACEHOLDERS}}`
6. Write issue body to `details/{ID}.md`
7. `create-issue.sh "{template}" "{entry_title}" "details/{ID}.md"` → parse `ISSUE_URL:`
8. `python3 link-issue.py {ID} {url}` → updates README with issue link
9. `python3 issues.py set {ID} {url}` → replace stored data with URL
10. `commit.sh "📤 {ID}: Created issue" README.md details/issues.json details/`
11. `push.sh`
12. Output the issue URL

## Workflow: /nag yay <target>

1. Lookup entry
2. `mark-done.py {ID}` → get title
3. `python3 issues.py get {ID}` → if URL returned, close it: `gh issue close {url}`
4. `commit.sh "✅ {ID}: {title}"`
5. `push.sh`
6. Celebrate via `templates/celebration.md`

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
10. `push.sh`
