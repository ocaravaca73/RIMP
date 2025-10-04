# GitHub Projects API Limitation

## Issue
Unable to add issue #16 to GitHub Project "RIMP – Product & Delivery" via API due to authentication limitations.

## Problem
The GitHub Projects V2 API returns error: "Personal Access Tokens are not supported for this endpoint"

## Root Cause
GitHub Projects V2 (the current version) has specific authentication requirements:

1. **Required Authentication Methods:**
   - Fine-grained Personal Access Tokens with `project` permissions
   - GitHub Apps with appropriate project permissions

2. **Not Supported:**
   - Classic Personal Access Tokens
   - Some OAuth token types

## Current Situation
- Issue #16 exists: "OSCAR TEST Add new issues" (ID: 3484057648)
- Required project fields:
  - Type: Feature
  - Priority: P1
  - Area: Realtime
  - Sprint (2w): Current
  - Estimate (pts): 3

## Workarounds

### Manual Approach
1. Navigate to the issue: https://github.com/ocaravaca73/RIMP/issues/16
2. Click on the Projects section in the right sidebar
3. Select "RIMP – Product & Delivery" project
4. Once added, set the fields manually

### API Approach (Requires Setup)
To enable API access, the repository owner needs to:

1. **Create a Fine-Grained Personal Access Token:**
   - Go to Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens
   - Generate new token with `project` scope
   - Grant access to the specific project

2. **Or use GitHub App Authentication:**
   - Create or use a GitHub App
   - Configure with project read/write permissions
   - Install the app on the repository/organization

## References
- [GitHub Projects API Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
- [Fine-grained PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

## Alternative: GraphQL API
The GitHub GraphQL API v4 also supports Projects V2, but requires the same authentication permissions:

```graphql
mutation {
  addProjectV2ItemById(input: {
    projectId: "PROJECT_NODE_ID"
    contentId: "ISSUE_NODE_ID"
  }) {
    item {
      id
    }
  }
}
```

However, this also requires proper authentication scopes.
