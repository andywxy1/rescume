# Compression-Strategist Agent - REMOVAL NOTICE

## Status: TO BE REMOVED

The `compression-strategist` agent is **obsolete in v2.0.0** and should be removed from the Task tool's agent system.

## Why it's obsolete:

In v1.0, this agent was responsible for:
- Iteratively reducing resume word count to fit one page
- Trimming bullets and compressing content
- Tracking word count reductions
- Deciding what to compress first (Experience vs Skills)

In v2.0, this functionality is completely replaced by:
- **Typst auto-fit templates** that automatically adjust font size
- **Python iterative compilation** that handles page fitting deterministically
- **No word counting** - Typst measures actual rendered content
- **No compression loops** - auto-fit is fast (~50-200ms total)

## Removal Steps:

1. Locate compression-strategist agent definition in Task tool configuration
2. Remove the agent entirely
3. Verify no references remain in:
   - rescume SKILL.md (already cleaned)
   - coverage-tracker SKILL.md (already cleaned)
   - Other agent definitions

## Verification:

After removal:
- [ ] compression-strategist not listed in available subagents
- [ ] No references in any SKILL.md files
- [ ] No references in system prompts
- [ ] Task tool does not offer compression-strategist as an option

## Notes:

This is a configuration change in the Task tool system, not a filesystem change.
The agent definition exists in Claude Code's internal configuration.

Once removed, mark Task #21 as completed.
