# RIMP

## Project Management

This repository includes tools and documentation for managing issues in GitHub Projects.

### Adding Issues to Projects

Due to GitHub Projects V2 API authentication requirements, issues must be added to projects using one of these methods:

1. **Manual (Recommended)**: Use the GitHub web interface
   - See [ADD_ISSUE_TO_PROJECT.md](./ADD_ISSUE_TO_PROJECT.md) for step-by-step instructions

2. **Automated**: Use the provided script with proper credentials
   - Run: `GITHUB_TOKEN=your_token ./add_issue_to_project.sh`
   - Requires fine-grained PAT with `project` permissions

### Documentation

- [ADD_ISSUE_TO_PROJECT.md](./ADD_ISSUE_TO_PROJECT.md) - Complete guide for adding issues to projects
- [GITHUB_PROJECTS_LIMITATION.md](./GITHUB_PROJECTS_LIMITATION.md) - Technical details about API limitations
- [add_issue_to_project.sh](./add_issue_to_project.sh) - Automation script for users with proper credentials
