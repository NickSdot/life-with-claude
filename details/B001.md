### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x] I am using the latest version of Claude Code

### What's Wrong?

When a Bash command exits with a non-zero status code, the output displayed in Claude Code's tool result is duplicated (shown twice). Successful commands (exit 0) display output correctly once.

### What Should Happen?

No duplicate output.

### Error Messages/Logs

```
Tool result shows:
Line 1
Line 2

Line 1
Line 2

Expected:
Line 1
Line 2
```

### Steps to Reproduce

1. Open fresh Claude session
2. Run `! echo "Line 1" && echo "Line 2" && exit 1`

**Verification that actual output is not duplicated:**
```sh
(echo "Line 1" && echo "Line 2" && exit 1) 2>&1 | wc -l
#  Returns: 2 (correct)
```

The shell produces 2 lines. The tool result displays 4.

**Comparison: Success vs Failure**

| Command | Exit Code | Output Duplication |
| --- | --- | ---|
| echo "Line 1" && echo "Line 2" | 0 | No (shown once) |
| echo "Line 1" && echo "Line 2" && exit 1 | 1 | Yes (shown twice) |

**Additional Observations:**
- The duplication appears in the `<error>` block of the tool result
- Both stdout and stderr content are duplicated together
- The duplication is identical (not interleaved or reordered)
- Wrapping in a subshell and counting lines confirms the actual output is correct

**Impact on Context Usage:**
The duplicated output consumes approximately 2x the tokens it should. For verbose compiler errors or test failures, this can add thousands of unnecessary tokens to the conversation context.

**Workaround:**
None identified. The duplication happens at the tool result display level, not in the actual command execution.

### Claude Model

Opus

### Is this a regression?

I don't know

### Last Working Version

N/A

### Claude Code Version

2.1.50

### Platform

Anthropic API

### Operating System

macOS

### Terminal/Shell

Terminal.app (macOS)

### Additional Information

Screenshots attached to issue showing the duplicated output in tool results.
