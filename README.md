



# RIMP
Real-time insights for motorsports platforms
## Project Management

This repository includes tools and documentation for managing issues in GitHub Projects.

> **The only source of truth for scheduling and project management is ** [Azure DevOps Boards – RIMP](<URL_A_TU_BOARD>)
>
> GitHub is only used for coding/PRs/CI. All the works ( epics/US/tasks**código/PRs/tasks/bugs/etc  lives in **ADO Boards**.


### Testing the Workflow

The repository includes comprehensive testing tools for the label-to-project-field mapping workflow:

1. **Automated Tests**: `node test-label-mappings.js`
   - Validates all label mapping logic
   - Tests 19 different scenarios including telemetry labels
   - No API access required

2. **Label Validation**: `./validate-labels.sh label1 label2 ...`
   - Quickly validates label format before applying to issues
   - Shows expected field mappings
   - Example: `./validate-labels.sh type:feature area:telemetry prio:P1`

3. **Complete Documentation**: See [TESTING_WORKFLOW.md](./TESTING_WORKFLOW.md)
   - Detailed testing guide
   - Manual testing procedures
   - Troubleshooting tips

### Adding Issues to Projects

Due to GitHub Projects V2 API authentication requirements, issues must be added to projects using one of these methods:

1. **Manual (Recommended)**: Use the GitHub web interface
   - See [ADD_ISSUE_TO_PROJECT.md](./ADD_ISSUE_TO_PROJECT.md) for step-by-step instructions

2. **Automated**: Use the provided script with proper credentials
   - Run: `GITHUB_TOKEN=your_token ./add_issue_to_project.sh`
   - Requires fine-grained PAT with `project` permissions

### Documentation

- [TESTING_WORKFLOW.md](./TESTING_WORKFLOW.md) - Complete testing guide for the workflow
- [ADD_ISSUE_TO_PROJECT.md](./ADD_ISSUE_TO_PROJECT.md) - Complete guide for adding issues to projects
- [GITHUB_PROJECTS_LIMITATION.md](./GITHUB_PROJECTS_LIMITATION.md) - Technical details about API limitations
- [add_issue_to_project.sh](./add_issue_to_project.sh) - Automation script for users with proper credentials

### Testing Tools

- **test-label-mappings.js** - Automated test suite for label mappings (19 test cases)
- **validate-labels.sh** - Quick validation tool for label formats
- **.github/ISSUE_TEMPLATE/telemetry-test.md** - Issue template for manual testing
