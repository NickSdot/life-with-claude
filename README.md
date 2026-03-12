# Life With Claude

Working with Claude Code is rather brilliant. This repository is where I keep constructive feedback to help make it even better — bugs to squash, rough edges to smooth, and wishes for the future.

🐛 Bug · 🤔 Flaw · 💫 Wish

## Open

| Type | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|
| 🐛 | B003 | ⭐⭐ | [--agents flag agents invisible to Claude despite appearing in /agents](#b003) | [#33513](https://github.com/anthropics/claude-code/issues/33513) |
| 🤔 | F001 | ⭐⭐ | [Plan mode compacts context too aggressively near completion](#f001) | [#29371](https://github.com/anthropics/claude-code/issues/29371) |
| 🤔 | F002 | ⭐⭐ | [Compaction doesn't start automatically after Claude exhausts context](#f002) | [#29780](https://github.com/anthropics/claude-code/issues/29780) |
| 🤔 | F003 | ⭐⭐ | [Task references use invisible IDs instead of visible titles](#f003) | [#29800](https://github.com/anthropics/claude-code/issues/29800) |
| 💫 | W001 | ⭐ | [Add turnDurationOverride setting for custom turn duration messages](#w001) | [#30979](https://github.com/anthropics/claude-code/issues/30979) |

### B003
**--agents flag agents invisible to Claude despite appearing in /agents**
Issue: [#33513](https://github.com/anthropics/claude-code/issues/33513)
When I launch Claude Code with --agents to define agents programmatically, Claude cannot find or spawn them when asked. However, the same agents appear correctly in the /agents list under CLI arg agents. No workarounds.
### F001
**Plan mode compacts context too aggressively near completion**
Issue: [#29371](https://github.com/anthropics/claude-code/issues/29371)
Plan mode triggers context compaction at around 166k tokens, even when the agent is about to finish—for example, right after receiving feedback from the plan agent. At that point the bulk of context is already present and finishing the plan should be straightforward. When compaction happens immediately after receiving sub-agent responses, the agent sometimes forgets that feedback entirely and starts the planning process over. Compaction in plan mode should be more context-aware and graceful, considering how close the agent is to completion.
### F002
**Compaction doesn't start automatically after Claude exhausts context**
Issue: [#29780](https://github.com/anthropics/claude-code/issues/29780)
Occasionally, after Claude finishes a longer answer, context sits at 0% but compaction doesn't begin until the next user input—even a simple "yes". If you step away from your desk, you return to find yourself waiting several minutes for compaction that could have already completed in the background.
### F003
**Task references use invisible IDs instead of visible titles**
Issue: [#29800](https://github.com/anthropics/claude-code/issues/29800)
When using the task list (TodoTool), Claude references tasks like "task 8 ... abc". But the task list I see doesn't display any IDs or numbers—just task titles. This makes it hard to understand which task Claude is talking about. Claude should either reference task titles, or the task list should display the IDs Claude uses.
### W001
**Add turnDurationOverride setting for custom turn duration messages**
Issue: [#30979](https://github.com/anthropics/claude-code/issues/30979)
The showTurnDuration setting controls whether the turn duration message appears after responses (e.g., "Cooked for 1m 6s"). Other settings like spinnerTipsEnabled have a companion override setting (spinnerTipsOverride). I'd like to see a turnDurationOverride that lets me customise the turn duration message format. My main use case is including the current date and time (and perhaps the turn start time) alongside the duration, so when I pick up the same session the next day I can see when I left off.

## Done

| Type | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|
| 🐛 | B001 | ⭐⭐⭐ | [Bash tool duplicates output for failed commands](#b001) | [#27621](https://github.com/anthropics/claude-code/issues/27621) |
| 🐛 | B002 | ⭐⭐ | [Unsupported model in agent config silently fails instead of erroring](#b002) | [#32415](https://github.com/anthropics/claude-code/issues/32415) |

### B001
**Bash tool duplicates output for failed commands**
Issue: [#27621](https://github.com/anthropics/claude-code/issues/27621)
When a Bash command exits with a non-zero status code, the tool result displays all output twice—doubling token consumption. Successful commands (exit 0) display correctly. This affects verbose compiler errors, test failures, and any command that fails, potentially adding thousands of unnecessary tokens to context. The duplication appears in the error block and is identical (not interleaved).
### B002
**Unsupported model in agent config silently fails instead of erroring**
Issue: [#32415](https://github.com/anthropics/claude-code/issues/32415)
When I specify a model like `claude-opus-4-5` in agent configuration (frontmatter or `--agents` flag), it silently fails instead of erroring—even though that same model name works with `--model`. Two failure modes: (1) frontmatter agents silently fall back to the main agent's config, burning unexpected tokens; (2) `--agents` flag agents with unsupported models simply don't register, leaving the main agent confused about what agents exist.
