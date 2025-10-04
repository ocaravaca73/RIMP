---
name: Telemetry Test Issue
about: Test issue for validating telemetry label mappings in project-sync workflow
title: '[TEST] Telemetry: '
labels: ['area:telemetry']
assignees: ''
---

## Test Issue for Telemetry Workflow

This is a test issue to validate that the `project-sync.yml` workflow correctly maps telemetry labels to Project fields.

### Expected Behavior

When labels are added to this issue, the workflow should:
1. Add the issue to the "RIMP – Product & Delivery" project
2. Map labels to appropriate Project V2 fields

### Test Checklist

Add labels to test different scenarios:

- [ ] `type:feature` - Should set Type = Feature
- [ ] `type:spike` - Should set Type = Spike  
- [ ] `type:task` - Should set Type = Task
- [ ] `type:bug` - Should set Type = Bug
- [ ] `type:chore` - Should set Type = Chore

Area (Telemetry):
- [ ] `area:telemetry` - Should set Area = Telemetry ⭐

Priority:
- [ ] `prio:P0` - Should set Priority = P0
- [ ] `prio:P1` - Should set Priority = P1
- [ ] `prio:P2` - Should set Priority = P2
- [ ] `prio:P3` - Should set Priority = P3

Sprint:
- [ ] `sprint:current` - Should set Sprint to current iteration

Estimate:
- [ ] `estimate:1` - Should set Estimate = 1
- [ ] `estimate:3` - Should set Estimate = 3
- [ ] `estimate:5` - Should set Estimate = 5
- [ ] `estimate:8` - Should set Estimate = 8

### Validation Steps

1. Add labels to this issue
2. Check GitHub Actions runs (Actions tab)
3. Verify workflow completes successfully
4. Check the Project board
5. Verify fields are set correctly

### Common Test Combinations

**Telemetry Feature:**
```
type:feature, area:telemetry, prio:P1, estimate:5
```

**Telemetry Bug (Urgent):**
```
type:bug, area:telemetry, prio:P0, sprint:current
```

**Telemetry Spike:**
```
type:spike, area:telemetry, estimate:3
```

---
*This issue can be closed after testing is complete.*
