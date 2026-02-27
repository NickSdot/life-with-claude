# Life With Claude

Working with Claude Code is rather brilliant. This repository is where I keep constructive feedback to help make it even better — bugs to squash, rough edges to smooth, and wishes for the future.

## 🐛 Bugs
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|

## 🤔 Flaws
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|
| | F001 | ⭐⭐ | [Plan mode compacts context too aggressively near completion](#f001) | [#29371](https://github.com/anthropics/claude-code/issues/29371) |

## 💫 Wishes
| Done | ID | ⭐ | Title | Issue |
|------|----|----|-------|-------|

---
## Entry Details
### F001
**Plan mode compacts context too aggressively near completion**
Issue: [#29371](https://github.com/anthropics/claude-code/issues/29371)
Plan mode triggers context compaction at around 166k tokens, even when the agent is about to finish—for example, right after receiving feedback from the plan agent. At that point the bulk of context is already present and finishing the plan should be straightforward. When compaction happens immediately after receiving sub-agent responses, the agent sometimes forgets that feedback entirely and starts the planning process over. Compaction in plan mode should be more context-aware and graceful, considering how close the agent is to completion.
