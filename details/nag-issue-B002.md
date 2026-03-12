### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x] I am using the latest version of Claude Code

### What's Wrong?

When I specify a model in agent configuration, certain model names are silently rejected—even if those same names work with the `--model` CLI flag. There are two failure modes:

**Failure mode 1: Silent fallback (frontmatter agents)**

With the main agent running Opus 4.6 + high effort, I created a subagent with this frontmatter:

```yaml
---
name: player
description: The player agent is used to debug an agent bug
model: claude-opus-4-5
---
Answer only on which exact model version you run, then STOP.
```

The agent spawns, but uses the main agent's config (Opus 4.6 with high effort) instead of the specified model. No warning, no error—just unexpected token burn.

**Failure mode 2: Agent doesn't register (--agents flag)**

When passing agents via CLI:

```bash
claude --agents '{
  "player": {
    "description": "Agent educator",
    "prompt": "Tell me what model you are, then STOP",
    "model": "claude-opus-4-5"
  }
}'
```

The agent simply doesn't exist. Asking to "spawn a player agent" results in:

> What do you mean by "player agent"? Could you give me more context on what it should do?

No error about invalid model, no error about failed registration—the agent is silently dropped.

### What Should Happen?

If a model name is invalid or unsupported for agents, Claude Code should error immediately with a clear message, e.g.:

> Error: Model 'claude-opus-4-5' is not supported for agents. Supported models: claude-sonnet-4-6, claude-opus-4-6, ...

Or better: support the same models for agents that work with `--model`.

### Error Messages/Logs

```
None—that's the problem. Both failures are completely silent.
```

### Steps to Reproduce

1. Run `claude --model claude-opus-4-5` (works fine)
2. Create an agent with `model: claude-opus-4-5` in frontmatter, or via `--agents` JSON
3. Observe: no error, but the model is ignored or the agent doesn't register

### Claude Model

Opus

### Is this a regression?

I don't know

### Last Working Version

N/A

### Claude Code Version

Latest

### Platform

Anthropic API

### Operating System

macOS

### Terminal/Shell

Other

### Additional Information

The core inconsistency: `claude --model claude-opus-4-5` works, but `model: claude-opus-4-5` in agent config doesn't. The same model name should either work everywhere or error everywhere.
