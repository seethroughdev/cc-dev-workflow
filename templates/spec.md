# Technical Specification Template

> **Note**: This template is for understanding problems and exploring solutions, not for writing code. Include enough technical detail to guide implementation, but details don't need to be exact. The goal is to think through the approach before coding.

## Summary

<Brief overview of what this specification describes and the problem it solves>

## Solution

<High-level description of the proposed solution and approach - focus on "what" and "why", not detailed "how">

## Technical Implementation

### [Component/Module Name]

**Location**: `path/to/file.mjs:line-range`

**Changes**:

1. <First change description>
   - <Implementation detail>
2. <Second change description>
   - <Implementation detail>

### [Storage/State Pattern] (if applicable)

**Pattern**: <Pattern name and why it was chosen>

- Key format: `pattern_key_${variable}`
- Value: `{ field1, field2, timestamp }`
- Functions: `saveData(args)`, `loadData(args)`

### [Integration Points] (if applicable)

**Priority Logic**:

1. <Primary behavior - e.g., URL params take precedence>
2. <Fallback behavior - e.g., localStorage if no URL param>
3. <Default behavior - e.g., system default>

**Validation**: <What needs to be validated>

## Testing

**Test Environment**: <URL or location for testing>

**Test Cases**:

- [ ] <Test case 1>
- [ ] <Test case 2>
- [ ] <Edge case 1>
- [ ] <Edge case 2>

## Impact

- [ ] No breaking changes
- [ ] Minimal performance impact
- [ ] Backward compatible
- [ ] Security/privacy considerations: <details if applicable>

## Resources

- <Related documentation>
- <Reference implementations>

---

## Example: Persistent View Memory

### Summary

Add persistent view memory so users automatically return to their last visited view when navigating to an entity grid, improving workflow continuity.

### Solution

Store the last active viewId in localStorage per entity. When loading a grid without a viewId in query parameters, automatically activate the last viewed view for that entity.

### Technical Implementation

#### localStorage Storage

**Location**: `js/components/viewgrid/local-storage.mjs:98`

**Changes**:

1. Add storage functions following existing `viewgrid_unsaved_*` pattern
   - `saveLastViewId(entity, viewId)` - Store last view with timestamp
   - `loadLastViewId(entity)` - Retrieve last view for entity

#### Store Integration

**Location**: `js/components/viewgrid/store.mjs`

**Changes**:

1. Add effect to track activeViewId changes (line 52)
   - Watch activeViewId signal changes
   - Call `saveLastViewId()` when changed and store initialized
   - Mirrors existing pattern for syncing viewId to query params (lines 47-51)

2. Update `fetchViews` to use lastViewId (lines 966-976)
   - Check if URL activeViewId is valid, use it and update localStorage
   - Fall back to localStorage if no URL viewId
   - Fall back to first view if localStorage empty or invalid
   - Validate viewId exists in current views array

#### Priority Logic

**URL vs localStorage Responsibility**:

1. **URL has viewId**: Use it (source of truth), then update localStorage
2. **URL has NO viewId**: Fall back to localStorage
3. **No valid viewId found**: Use first view

**Validation**: Ensure any viewId (from URL or localStorage) exists in the views array

### Testing

**Test Environment**: `http://localhost:3000/albert.html#uiviewgrid`

**Test Cases**:

- [ ] Navigate to Tasks grid, select view, return - shows last selected view
- [ ] Navigate to Inventory grid, select different view - shows Inventory's last view
- [ ] Direct URL with viewId param - uses URL param (not localStorage)
- [ ] Direct URL with different viewId than localStorage - uses URL, updates storage
- [ ] Invalid viewId in URL - falls back to localStorage, then first view
- [ ] Clear localStorage - falls back to first view
- [ ] Share URL with viewId - recipient sees correct view

### Impact

- [x] No breaking changes
- [x] Minimal performance impact (localStorage read on init, write on view change)
- [x] Backward compatible - gracefully falls back to existing behavior
- [x] Preserves shareable URL functionality
- [x] Improves workflow efficiency for repeated view access

### Resources

- Existing pattern: `viewgrid_unsaved_*` in `local-storage.mjs`
- Related: Query param sync effect in `store.mjs:47-51`

---

## Usage Guidelines

**When to Use This Template:**

- Complex features requiring detailed technical planning
- Features with multiple integration points or priority logic
- Storage/state pattern changes affecting multiple components
- Features requiring specific testing scenarios
- When you need to think through an approach before writing code

**When to Use Other Templates:**

- Simple bug fixes: Use [ticket-bug.md](ticket-bug.md)
- User-facing features: Use [ticket-feature.md](ticket-feature.md)
- Pull requests: Use [pr-new.md](pr-new.md)
- Implementation plans: Use [plan-summary.md](plan-summary.md)

**Philosophy:**

- This is a planning document, not a code solution
- Include enough detail to guide implementation without being prescriptive
- Explore potential solutions and trade-offs
- Think through integration points and edge cases
- Details can be approximate - the goal is to reduce unknowns before coding

**Structure Tips:**

- Focus on "what" and "why", light on detailed "how"
- File paths and line numbers help orient but don't need to be exact
- Document priority/fallback logic and integration patterns
- Use checkboxes for testing and impact items
- Identify unknowns or areas needing investigation
