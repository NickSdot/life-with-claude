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

Parse $ARGUMENTS:
- (no arguments) → stats
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
| `issues.py get ID` | Get tracked issue data | URL, template name, or JSON object |
| `issues.py set ID url` | Track issue URL | — |
| `issues.py set ID template body-file` | Track template + approved body | — |

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
| `status.md` | `{{BUGS}}`, `{{FLAWS}}`, `{{WISHES}}` |
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

**If text provided** (e.g. `/nag add the context window keeps compacting`):
- Transform user's raw thoughts into a polished entry:
  - **Category**: Infer from keywords (broken/crash → bug, annoying/awkward → flaw, want/wish → wish)
  - **Priority**: Infer from severity/frequency mentioned
  - **Title**: 5-10 words, action-oriented, MUST include key context (e.g., "plan mode" if that's the context). Don't over-generalise—preserve the specific scenario.
  - **Description**: Capture the full nuance. Include: what happens, when/where it happens, why it's problematic, what would be better. Don't strip detail that helps understand the issue.

**If no text** (just `/nag add`):
1. Output: "What's the issue?" (wait for user to type description)
2. User submits description
3. Immediately call AskUserQuestion with `questions/add.json` (category + priority + template)
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
5. `python3 add-entry.py '{"id":"...","category":"...","priority":"...","title":"...","description":"..."}'`
6. Write the approved `{{GITHUB_ISSUE_BODY}}` to `.claude/tmp/nag-body-{ID}.md`
7. `python3 issues.py set {ID} {template} .claude/tmp/nag-body-{ID}.md` → store template + approved body
8. `commit.sh "➕ {ID}: {title}" README.md .claude/skills/nag/issues.json`
9. **If template is "none":** "Committed locally. This entry won't create a GitHub issue."
   **Otherwise:** "Committed locally. Run `/nag fin {ID}` when ready to push and file with Anthropic."

If user wants extended details during edit: load `reference/detail-files.md`, collect content, write to `details/{ID}.md`, include in commit.

## Workflow: /nag fin <target>

Load `reference/detail-files.md`.

1. Lookup entry
2. `python3 issues.py get {ID}` → check stored value:
   - If `"none"` → output "No GitHub issue configured for this entry." and stop
   - If starts with `http` → output "Issue already exists: {url}" and stop
   - If JSON object with `template` and `body` → use stored body (skip steps 4-7)
   - If template name (`bug`, `model`, `feature`) → continue with that template
   - If not found (exit 1) → ask which template to use
3. `push.sh` → push any pending commits first
4. `python3 parse-readme.py search "{ID}"` → get entry details as JSON
5. Check if `details/{ID}.md` exists (Read tool)
6. Read the template file based on stored value:
   - `bug` → `templates/github-issue-bug.md`
   - `model` → `templates/github-issue-model.md`
   - `feature` → `templates/github-issue-feature.md`
7. Fill all `{{PLACEHOLDERS}}` in the template
8. Write issue body to `.claude/tmp/nag-issue-{ID}.md`:
   - If stored value has `body` field → use that directly
   - Otherwise → use filled template from step 7
9. Build title with prefix: `[BUG] `, `[MODEL] `, or `[FEATURE] ` + entry title
10. `create-issue.sh "{template}" "{title}" ".claude/tmp/nag-issue-{ID}.md"` → parse `ISSUE_URL:` from output
11. `python3 link-issue.py {ID} {url}` → updates README with issue link
12. `python3 issues.py set {ID} {url}` → replace stored data with actual URL
13. `commit.sh "📤 {ID}: Created issue" README.md .claude/skills/nag/issues.json`
14. `push.sh`
15. Output the issue URL

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
