### Preflight Checklist

- [x] I have searched [existing requests](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20label%3Aenhancement) and this feature hasn't been requested yet
- [x] This is a single feature request (not multiple features)

### Problem Statement

Occasionally, after Claude finishes a longer task, the context indicator shows 0% but compaction doesn't begin automatically. The system waits idle until the user submits their next message—even something as brief as "yes"—before starting compaction.

If you step away from your desk expecting to continue later, you return to find context still at 0% and nothing happening. Your next keystroke then triggers a multi-minute wait for compaction to complete.

### Proposed Solution

When Claude finishes an answer that exhausts context (0% remaining), compaction should trigger automatically in the background rather than waiting for the next user input. This way, users returning to their session find compaction already done or in progress.

### Alternative Solutions

None

### Priority

Medium - Would be very helpful

### Feature Category

Performance and speed

### Use Case Example

1. Claude completes a longer multi-step task
2. Context reaches 0% as Claude finishes its final answer
3. User steps away for a break
4. Ten minutes later, user returns expecting to continue
5. Typing any input now triggers a 3-minute compaction wait
6. **Expected**: Compaction should have started automatically, completing during the user's break

### Additional Context

This appears to be an edge case—compaction usually triggers near 0% as expected. The issue occurs specifically when context hits 0% exactly as Claude finishes speaking.
