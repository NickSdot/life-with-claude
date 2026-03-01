# Life With Claude

Working with Claude Code is rather brilliant. This repository is where I keep constructive feedback to help make it even better — bugs to squash, rough edges to smooth, and wishes for the future.

## 🐛 Bugs
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|
| | B001 | ⭐⭐⭐ | [Bash tool duplicates output for failed commands](#b001) | [#27621](https://github.com/anthropics/claude-code/issues/27621) |

## 🤔 Flaws
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|
| | F001 | ⭐⭐ | [Plan mode compacts context too aggressively near completion](#f001) | [#29371](https://github.com/anthropics/claude-code/issues/29371) |
| | F002 | ⭐⭐ | [Compaction doesn't start automatically after Claude exhausts context](#f002) | |

## 💫 Wishes
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|

---
## Entry Details
### F001
**Plan mode compacts context too aggressively near completion**
Issue: [#29371](https://github.com/anthropics/claude-code/issues/29371)
Plan mode triggers context compaction at around 166k tokens, even when the agent is about to finish—for example, right after receiving feedback from the plan agent. At that point the bulk of context is already present and finishing the plan should be straightforward. When compaction happens immediately after receiving sub-agent responses, the agent sometimes forgets that feedback entirely and starts the planning process over. Compaction in plan mode should be more context-aware and graceful, considering how close the agent is to completion.
### B001
**Bash tool duplicates output for failed commands**
Issue: [#27621](https://github.com/anthropics/claude-code/issues/27621)
When a Bash command exits with a non-zero status code, the tool result displays all output twice—doubling token consumption. Successful commands (exit 0) display correctly. This affects verbose compiler errors, test failures, and any command that fails, potentially adding thousands of unnecessary tokens to context. The duplication appears in the error block and is identical (not interleaved).
### F002
**Compaction doesn't start automatically after Claude exhausts context**
Occasionally, after Claude finishes a longer answer, context sits at 0% but compaction doesn't begin until the next user input—even a simple "yes". If you step away from your desk, you return to find yourself waiting several minutes for compaction that could have already completed in the background.
