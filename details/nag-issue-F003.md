### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Amodel) for similar behavior reports
- [x] This report does NOT contain sensitive information (API keys, passwords, etc.)

### Type of Behavior Issue

Other unexpected behavior

### What You Asked Claude to Do

Work through a task list using TodoTool.

### What Claude Actually Did

Claude references tasks using internal IDs like "task 8 ... abc" that don't appear anywhere in my visible task list—the UI shows only titles, no IDs or numbers.

### Expected Behavior

Claude should reference tasks by their titles, or the task list UI should display the IDs that Claude uses internally.

### Files Affected

```
N/A - affects conversation output only
```

### Permission Mode

N/A

### Can You Reproduce This?

Yes, every time with the same prompt

### Steps to Reproduce

1. Ask Claude to create several tasks using TodoTool
2. Work through them, with Claude referencing tasks as it proceeds
3. Observe Claude saying things like "task 8" with no way to match it to the visible task list

### Claude Model

Both Sonnet and Opus

### Relevant Conversation

See above.

### Impact

Low - Minor inconvenience

### Claude Code Version

1.0.33

### Platform

Anthropic API

### Additional Context

See above.
