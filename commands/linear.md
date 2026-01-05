---
description: Manage Linear tickets - create, update, query, and review issues without MCP dependency
argument-hint: [operation and details]
allowed-tools: Skill(manage-linear)
---

<objective>
Delegate Linear operations to the manage-linear skill: $ARGUMENTS

This routes to specialized skill for creating tickets (feature/bug/task), querying issues, updating properties, and reviewing tickets with implementation plans.
</objective>

<process>
1. Use Skill tool to invoke manage-linear skill
2. Pass user's request: $ARGUMENTS
3. Let skill handle workflow with secure API wrapper
</process>

<success_criteria>
- Skill successfully invoked
- Arguments passed correctly to skill
- Linear operations executed without exposing credentials
</success_criteria>
