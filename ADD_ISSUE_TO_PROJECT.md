# Adding Issue to GitHub Project - Manual Instructions

## Issue Details
- **Issue Number:** #16
- **Issue Title:** OSCAR TEST Add new issues
- **Issue ID:** 3484057648
- **Issue Node ID:** I_kwDOP8MbO87PqoAw

## Required Project Configuration
- **Project Name:** RIMP – Product & Delivery
- **Fields to Set:**
  - Type: Feature
  - Priority: P1
  - Area: Realtime
  - Sprint (2w): Current
  - Estimate (pts): 3

## Step-by-Step Manual Instructions

### Option 1: Using GitHub Web Interface (Easiest)

1. **Navigate to the issue:**
   - Go to: https://github.com/ocaravaca73/RIMP/issues/16

2. **Add to Project:**
   - Look at the right sidebar
   - Find the "Projects" section
   - Click the gear icon or "Add to projects" button
   - Select "RIMP – Product & Delivery" from the dropdown
   - Click to add

3. **Set Field Values:**
   - Once added, the issue will appear in the project board
   - Navigate to the project board
   - Find the issue in the board
   - Click on the issue card
   - Set each field:
     - Type → Feature
     - Priority → P1
     - Area → Realtime
     - Sprint (2w) → Current
     - Estimate (pts) → 3

### Option 2: Using GitHub CLI (gh) with Proper Token

If you have a fine-grained PAT with project permissions:

```bash
# Set your token
export GITHUB_TOKEN="your_fine_grained_token_here"

# First, get the project ID
gh project list --owner ocaravaca73

# Add the issue to the project (replace PROJECT_NUMBER)
gh project item-add PROJECT_NUMBER --owner ocaravaca73 --url https://github.com/ocaravaca73/RIMP/issues/16

# Set fields (you'll need to get field IDs first)
gh api graphql -f query='
  query {
    user(login: "ocaravaca73") {
      projectV2(number: PROJECT_NUMBER) {
        fields(first: 20) {
          nodes {
            ... on ProjectV2Field {
              id
              name
            }
            ... on ProjectV2SingleSelectField {
              id
              name
              options {
                id
                name
              }
            }
          }
        }
      }
    }
  }
'
```

### Option 3: Using GraphQL API Directly

If you have proper authentication:

```bash
# Get project ID
curl -H "Authorization: bearer YOUR_TOKEN" -X POST \
  -d '{"query":"query { user(login: \"ocaravaca73\") { projectV2(number: YOUR_PROJECT_NUMBER) { id } } }"}' \
  https://api.github.com/graphql

# Add issue to project
curl -H "Authorization: bearer YOUR_TOKEN" -X POST \
  -d '{"query":"mutation { addProjectV2ItemById(input: {projectId: \"PROJECT_ID\", contentId: \"I_kwDOP8MbO87PqoAw\"}) { item { id } } }"}' \
  https://api.github.com/graphql

# Update field values (requires field IDs and option IDs)
curl -H "Authorization: bearer YOUR_TOKEN" -X POST \
  -d '{"query":"mutation { updateProjectV2ItemFieldValue(input: {projectId: \"PROJECT_ID\", itemId: \"ITEM_ID\", fieldId: \"FIELD_ID\", value: {singleSelectOptionId: \"OPTION_ID\"}}) { projectV2Item { id } } }"}' \
  https://api.github.com/graphql
```

## Why API Access Failed

The GitHub Projects V2 API has strict authentication requirements:

1. **Not Supported:**
   - Classic Personal Access Tokens
   - Many OAuth token types
   - Some GitHub App tokens without proper scopes

2. **Required:**
   - Fine-grained Personal Access Token with `project` read/write permissions
   - GitHub App with project permissions properly configured

3. **Token Scope Must Include:**
   - `project` (for Projects V2)
   - `read:project` and `write:project` specifically

## Creating Proper Authentication

### For Fine-Grained PAT:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Fine-grained tokens
2. Click "Generate new token"
3. Set token name and expiration
4. Under "Repository access", select the repositories you need
5. Under "Permissions" → "Repository permissions", set:
   - Issues: Read and write
   - Projects: Read and write (this is the key permission)
6. Generate and save the token securely

## Verification

After adding the issue to the project, verify:

1. ✅ Issue appears in project board
2. ✅ Type field = Feature
3. ✅ Priority field = P1
4. ✅ Area field = Realtime
5. ✅ Sprint (2w) field = Current
6. ✅ Estimate (pts) field = 3

## References

- [GitHub Projects V2 API Documentation](https://docs.github.com/en/issues/planning-and-tracking-with-projects/automating-your-project/using-the-api-to-manage-projects)
- [Fine-grained PAT Documentation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- [GitHub GraphQL API Explorer](https://docs.github.com/en/graphql/overview/explorer)
