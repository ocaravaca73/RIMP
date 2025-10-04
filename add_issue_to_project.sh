#!/bin/bash

# Script to add Issue #16 to GitHub Project and set fields
# Requires: Fine-grained GitHub PAT with project permissions
# Usage: GITHUB_TOKEN=your_token_here ./add_issue_to_project.sh

set -e

# Configuration
OWNER="ocaravaca73"
REPO="RIMP"
ISSUE_NUMBER=16
ISSUE_NODE_ID="I_kwDOP8MbO87PqoAw"
PROJECT_NAME="RIMP – Product & Delivery"

# Field values to set
FIELD_TYPE="Feature"
FIELD_PRIORITY="P1"
FIELD_AREA="Realtime"
FIELD_SPRINT="Current"
FIELD_ESTIMATE="3"

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN environment variable is not set"
    echo "Usage: GITHUB_TOKEN=your_token_here $0"
    exit 1
fi

echo "🔍 Finding project: $PROJECT_NAME"

# Step 1: List projects to find the project number
PROJECTS=$(gh api graphql -f query='
query {
  user(login: "'$OWNER'") {
    projectsV2(first: 20) {
      nodes {
        id
        number
        title
      }
    }
  }
}' 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Failed to list projects. Make sure your token has 'project' scope."
    echo "$PROJECTS"
    exit 1
fi

echo "$PROJECTS" | jq .

# Extract project ID and number (you'll need to identify which one matches "RIMP – Product & Delivery")
PROJECT_ID=$(echo "$PROJECTS" | jq -r '.data.user.projectsV2.nodes[] | select(.title == "'"$PROJECT_NAME"'") | .id')
PROJECT_NUMBER=$(echo "$PROJECTS" | jq -r '.data.user.projectsV2.nodes[] | select(.title == "'"$PROJECT_NAME"'") | .number')

if [ -z "$PROJECT_ID" ] || [ "$PROJECT_ID" = "null" ]; then
    echo "❌ Could not find project: $PROJECT_NAME"
    echo "Available projects:"
    echo "$PROJECTS" | jq -r '.data.user.projectsV2.nodes[] | "  - \(.title) (number: \(.number))"'
    exit 1
fi

echo "✅ Found project: $PROJECT_NAME (ID: $PROJECT_ID, Number: $PROJECT_NUMBER)"

# Step 2: Add issue to project
echo ""
echo "➕ Adding issue #$ISSUE_NUMBER to project..."

ADD_RESULT=$(gh api graphql -f query='
mutation {
  addProjectV2ItemById(input: {
    projectId: "'$PROJECT_ID'"
    contentId: "'$ISSUE_NODE_ID'"
  }) {
    item {
      id
    }
  }
}' 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Failed to add issue to project"
    echo "$ADD_RESULT"
    exit 1
fi

ITEM_ID=$(echo "$ADD_RESULT" | jq -r '.data.addProjectV2ItemById.item.id')

if [ -z "$ITEM_ID" ] || [ "$ITEM_ID" = "null" ]; then
    echo "❌ Issue might already be in the project or failed to add"
    echo "$ADD_RESULT" | jq .
else
    echo "✅ Added issue to project (Item ID: $ITEM_ID)"
fi

# Step 3: Get field IDs
echo ""
echo "🔍 Getting project field IDs..."

FIELDS=$(gh api graphql -f query='
query {
  node(id: "'$PROJECT_ID'") {
    ... on ProjectV2 {
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
}' 2>&1)

if [ $? -ne 0 ]; then
    echo "❌ Failed to get field IDs"
    echo "$FIELDS"
    exit 1
fi

echo "Available fields:"
echo "$FIELDS" | jq -r '.data.node.fields.nodes[] | "  - \(.name) (ID: \(.id))"'

# Step 4: Update fields
# Note: This part requires parsing the field structure and finding the right option IDs
# For each field, you need to:
# 1. Find the field ID by name
# 2. Find the option ID by option name
# 3. Call updateProjectV2ItemFieldValue mutation

echo ""
echo "⚠️  Manual field update required"
echo "The script has added the issue to the project."
echo "Please manually set these fields in the GitHub UI:"
echo "  - Type: $FIELD_TYPE"
echo "  - Priority: $FIELD_PRIORITY"
echo "  - Area: $FIELD_AREA"
echo "  - Sprint (2w): $FIELD_SPRINT"
echo "  - Estimate (pts): $FIELD_ESTIMATE"
echo ""
echo "Or extend this script to automatically set fields using the field IDs above."

# Function to update a single select field (example)
update_field() {
    local field_name=$1
    local option_name=$2
    
    # Get field ID
    local field_id=$(echo "$FIELDS" | jq -r '.data.node.fields.nodes[] | select(.name == "'"$field_name"'") | .id')
    
    # Get option ID
    local option_id=$(echo "$FIELDS" | jq -r '.data.node.fields.nodes[] | select(.name == "'"$field_name"'") | .options[]? | select(.name == "'"$option_name"'") | .id')
    
    if [ -z "$field_id" ] || [ "$field_id" = "null" ]; then
        echo "⚠️  Field not found: $field_name"
        return 1
    fi
    
    if [ -z "$option_id" ] || [ "$option_id" = "null" ]; then
        echo "⚠️  Option not found: $option_name for field $field_name"
        return 1
    fi
    
    echo "Setting $field_name = $option_name..."
    
    gh api graphql -f query='
    mutation {
      updateProjectV2ItemFieldValue(input: {
        projectId: "'$PROJECT_ID'"
        itemId: "'$ITEM_ID'"
        fieldId: "'$field_id'"
        value: {
          singleSelectOptionId: "'$option_id'"
        }
      }) {
        projectV2Item {
          id
        }
      }
    }' > /dev/null 2>&1
    
    if [ $? -eq 0 ]; then
        echo "✅ Set $field_name = $option_name"
    else
        echo "❌ Failed to set $field_name"
    fi
}

# Uncomment and adjust these if you want to auto-update fields
# Make sure the field names and option names match exactly
# update_field "Type" "$FIELD_TYPE"
# update_field "Priority" "$FIELD_PRIORITY"
# update_field "Area" "$FIELD_AREA"
# update_field "Sprint (2w)" "$FIELD_SPRINT"
# update_field "Estimate (pts)" "$FIELD_ESTIMATE"

echo ""
echo "✅ Done! Visit: https://github.com/ocaravaca73/RIMP/issues/16"
