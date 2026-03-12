### Preflight Checklist

- [x] I have searched [existing issues](https://github.com/anthropics/claude-code/issues?q=is%3Aissue%20state%3Aopen%20label%3Abug) and this hasn't been reported yet
- [x] This is a single bug report (please file separate reports for different bugs)
- [x] I am using the latest version of Claude Code

### What's Wrong?

When I launch Claude Code with `--agents` to define agents programmatically (e.g. `claude --agents '{"makahoni": {"description": "Agent makahoni boss", "prompt": "Tell me what model you are, then STOP", "model": "opus"}}'`), Claude cannot find or spawn them when asked. It responds saying the agent doesn't exist, despite the agent being registered and visible in the `/agents` list under "CLI arg agents".

### What Should Happen?

Claude should be able to find and spawn agents defined via `--agents`, just as it can with project agents or built-in agents.

### Error Messages/Logs

```
Full session transcript:

➜ claude --agents '{
  "makahoni": {
    "description": "Agent makahoni boss",
    "prompt": "Tell me what model you are, then STOP",
    "model": "opus"
  }
}'

❯ Spawn the makahoni agent and tell me what it tells you

∴ Thinking…

  The user is asking me to "spawn the makahoni agent." There's no agent called "makahoni" in any of the available tools or agent configurations.
  Let me check if there's a file referencing this.

⏺ There's no agent called "makahoni" — it doesn't exist in the project's agent definitions or available tools. The agents I can see are:
  - ...

  Did you mean one of these, or is "makahoni" something else entirely?

❯ /agents

  Agents
  13 agents

    CLI arg agents
    makahoni · opus
```

### Steps to Reproduce

1. Run `claude --agents '{"makahoni": {"description": "Agent makahoni boss", "prompt": "Tell me what model you are, then STOP", "model": "opus"}}'`
2. Ask Claude to "Spawn the makahoni agent and tell me what it tells you"
3. Claude responds that the agent doesn't exist
4. Run `/agents` — the agent appears under "CLI arg agents"

### Claude Model

Opus

### Is this a regression?

I don't know

### Last Working Version

N/A

### Claude Code Version

2.1.74

### Platform

Anthropic API

### Operating System

macOS

### Terminal/Shell

N/A

### Additional Information

No workarounds known. The agent is correctly registered (visible in `/agents`) but not accessible to Claude for spawning.
