### Preflight Checklist

- [x] I have searched [existing requests](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20label%3Aenhancement) and this feature hasn't been requested yet
- [x] This is a single feature request (not multiple features)

### Problem Statement

The `showTurnDuration` setting controls whether a turn duration message appears after responses (e.g., "Cooked for 1m 6s"), but there's no way to customise its format. Other settings like `spinnerTipsEnabled` have a companion override setting (`spinnerTipsOverride`), yet `showTurnDuration` has no equivalent. I'd like to include the current date/time alongside the duration so that when I return to a session later, I can see when I last interacted.

### Proposed Solution

Add a `turnDurationOverride` setting (similar to `spinnerTipsOverride`) that accepts a custom format string for the turn duration message. It should support placeholders such as:
- `{duration}` — the turn duration (e.g., "1m 6s")
- `{time}` — current time when the turn completed
- `{date}` — current date
- `{startTime}` — when the turn started

Example: setting `turnDurationOverride` to `"Cooked for {duration} (finished at {time} on {date})"` would produce something like "Cooked for 1m 6s (finished at 14:32 on 2026-03-05)".

### Alternative Solutions

- Logging turn timestamps to a file or the conversation history (less visible, harder to glance at)
- A separate "last active" indicator in the UI (solves part of the problem but doesn't integrate with the existing turn duration message)

### Priority

Low - Nice to have
<!-- Options: Critical - Blocking my work | High - Significant impact on productivity | Medium - Would be very helpful | Low - Nice to have -->

### Feature Category

Configuration and settings
<!-- Options: CLI commands and flags | Interactive mode (TUI) | File operations | API and model interactions | MCP server integration | Performance and speed | Configuration and settings | Developer tools/SDK | Documentation | Other -->

### Use Case Example

I often work in long-running Claude Code sessions across multiple days. When I return to a session, I scroll up to see where I left off. Currently the turn duration message only shows "Cooked for 1m 6s" with no timestamp. With a `turnDurationOverride`, I could configure it to show "Cooked for 1m 6s (finished at 17:45 on 2026-03-04)" — immediately telling me when that turn happened.

### Additional Context

The pattern already exists in the codebase: `spinnerTipsEnabled` has `spinnerTipsOverride`. This would follow the same convention for `showTurnDuration`.
