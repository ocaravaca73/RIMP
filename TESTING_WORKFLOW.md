# Testing the Project Sync Workflow

This document explains how to test the label-to-project-field mapping workflow defined in `.github/workflows/project-sync.yml`.

## Overview

The `project-sync.yml` workflow automatically:
1. Adds issues and pull requests to the GitHub Project
2. Maps labels to Project V2 fields
3. Updates the item with appropriate field values

## Label Mappings

### Type Labels → Type Field
- `type:feature` → Feature
- `type:spike` → Spike
- `type:task` → Task
- `type:bug` → Bug
- `type:chore` → Chore

### Area Labels → Area Field
- `area:app` → App
- `area:backend` → Backend
- `area:realtime` → Realtime
- `area:telemetry` → Telemetry ⭐
- `area:data` → Data
- `area:ux` → UX
- `area:ops` → Ops

### Priority Labels → Priority Field
- `prio:P0` → P0 (Highest)
- `prio:P1` → P1
- `prio:P2` → P2
- `prio:P3` → P3 (Lowest)

### Sprint Label → Sprint Field
- `sprint:current` → Sets to current sprint based on today's date

### Estimate Labels → Estimate Field
- `estimate:N` → N (where N is a number, e.g., `estimate:5` → 5 points)

## Running Tests

### Automated Tests

Run the label mapping validation tests:

```bash
node test-label-mappings.js
```

This script validates all label mapping logic without requiring API access. It tests:
- ✅ All type labels (feature, spike, task, bug, chore)
- ✅ All area labels (app, backend, realtime, **telemetry**, data, ux, ops)
- ✅ Priority labels (P0-P3)
- ✅ Sprint labels (sprint:current)
- ✅ Estimate labels (estimate:N)
- ✅ Edge cases (no labels, invalid formats, multiple labels)

### Manual Testing with Issues

To test the workflow end-to-end with real GitHub Projects:

#### Prerequisites
1. A fine-grained Personal Access Token with:
   - `project` read/write permissions
   - Access to the repository and project
2. Store the token as `COPILOT_MCP_GITHUB_PROJECT_TOKEN` in the `copilot` environment

#### Test Case 1: Telemetry Feature
1. Create a test issue
2. Add labels: `type:feature`, `area:telemetry`, `prio:P1`, `estimate:5`
3. The workflow should:
   - Add the issue to the project
   - Set Type = Feature
   - Set Area = Telemetry
   - Set Priority = P1
   - Set Estimate = 5

#### Test Case 2: Telemetry Bug (Current Sprint)
1. Create a test issue
2. Add labels: `type:bug`, `area:telemetry`, `prio:P0`, `sprint:current`
3. The workflow should:
   - Add the issue to the project
   - Set Type = Bug
   - Set Area = Telemetry
   - Set Priority = P0
   - Set Sprint = Current sprint iteration

#### Test Case 3: Telemetry Spike
1. Create a test issue
2. Add labels: `type:spike`, `area:telemetry`, `estimate:3`
3. The workflow should:
   - Add the issue to the project
   - Set Type = Spike
   - Set Area = Telemetry
   - Set Estimate = 3

## Workflow Triggers

The workflow runs on:
- `workflow_dispatch` - Manual trigger from Actions tab
- `issues` events: `opened`, `edited`, `labeled`, `unlabeled`
- `pull_request` events: `opened`, `edited`, `labeled`, `unlabeled`

## Manual Triggering

To manually test the workflow:

1. Go to the repository's Actions tab
2. Select "Sync labels with Project fields" workflow
3. Click "Run workflow"
4. Select the branch
5. Click "Run workflow"

The workflow will process the most recent issue/PR event.

## Troubleshooting

### Error: "Personal Access Tokens are not supported for this endpoint"

**Cause:** Using a Classic PAT instead of a fine-grained token

**Solution:**
1. Create a fine-grained Personal Access Token
2. Grant `project` read/write permissions
3. Update the `COPILOT_MCP_GITHUB_PROJECT_TOKEN` secret

### Error: "Project not found"

**Cause:** Project name doesn't match or user doesn't have access

**Solution:**
1. Verify project name: "RIMP – Product & Delivery"
2. Check token has access to the project
3. Verify `PROJECT_OWNER` is set correctly

### Labels not updating fields

**Cause:** Field names in the project don't match expectations

**Solution:**
1. Check project has these fields:
   - Type (Single Select)
   - Priority (Single Select)
   - Area (Single Select)
   - Sprint (2w) (Iteration)
   - Estimate (pts) (Number)
2. Verify option names match exactly (case-sensitive)

## Testing Checklist

When testing the workflow, verify:

- [ ] Issues with telemetry labels are added to project
- [ ] Type field is set correctly from `type:*` labels
- [ ] Area field is set to "Telemetry" from `area:telemetry` label
- [ ] Priority field is set correctly from `prio:P*` labels
- [ ] Sprint field is set when `sprint:current` label is present
- [ ] Estimate field is set correctly from `estimate:N` labels
- [ ] Pull requests are also processed
- [ ] Editing labels triggers update
- [ ] Unlabeling triggers update
- [ ] Invalid label formats are ignored gracefully
- [ ] Multiple labels of same category (first wins)

## Example Test Scenarios

### Scenario 1: Telemetry Bootstrap (Minimal)
```
Labels: type:spike, area:telemetry
Expected: Type=Spike, Area=Telemetry
```

### Scenario 2: Telemetry Feature (Complete)
```
Labels: type:feature, area:telemetry, prio:P1, estimate:5, sprint:current
Expected: Type=Feature, Area=Telemetry, Priority=P1, Estimate=5, Sprint=Current
```

### Scenario 3: Telemetry Bug (Urgent)
```
Labels: type:bug, area:telemetry, prio:P0
Expected: Type=Bug, Area=Telemetry, Priority=P0
```

## Validation Script Output

The test script provides clear feedback:

```
🧪 Testing Label Mappings for project-sync.yml

======================================================================
✅ Test 1: Telemetry feature with priority and estimate
✅ Test 2: Telemetry bug in current sprint
✅ Test 3: Telemetry spike without priority
...
======================================================================

📊 Test Results: 19 passed, 0 failed out of 19 tests

✅ All tests passed!
```

## References

- [GitHub Projects V2 API Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
- [GitHub Actions workflow syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub GraphQL API](https://docs.github.com/en/graphql)
