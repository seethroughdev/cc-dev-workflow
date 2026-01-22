# PR Description Template

Use this structure for all PR descriptions.

```markdown
## Summary

<!-- One-liner: what changed and why it matters -->

## Problem

<!-- Brief explanation of what was wrong -->

- **Issue 1**: <description>
- **Issue 2**: <description>

## Solution

**Root Cause**: <underlying cause(s)>

**Fix Approach**:
1. <fix description>
2. <fix description>

## Changes

### `path/to/file1.ts`
- <key change>
- <key change>

### `path/to/file2.ts`
- <key change>

## Testing

- [ ] Functionality tested in affected components
- [ ] Verified visual styling changes across screen sizes
- [ ] Confirmed no regressions via existing tests
- [ ] Added/updated tests as needed

## Impact

- [x] No breaking changes
- [ ] Requires migration or config changes
- [ ] Affects API, performance, or user behavior

## Review Notes

<!-- Highlight architectural shifts, simplifications, or risk areas -->

- **Area 1**: <what changed and why>
- **Area 2**: <implications>
```

## Section Guidelines

**Summary**: Single sentence. Focus on user/developer impact, not implementation details.

**Problem**: List concrete issues being fixed. Include ticket reference if available.

**Solution**: Explain root cause first, then enumerate fixes. Keep brief.

**Changes**: Group by file. Only list significant changes, not every line modified.

**Testing**: Check off what was verified. Add specific test scenarios if complex.

**Impact**: Be honest about breaking changes or migration needs.

**Review Notes**: Call out non-obvious decisions, performance considerations, or areas needing careful review.
