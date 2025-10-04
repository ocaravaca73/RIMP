#!/bin/bash

# Script to validate label patterns against the workflow mappings
# Usage: ./validate-labels.sh label1 label2 label3 ...

set -e

echo "🏷️  Label Validation for project-sync.yml"
echo "==========================================="
echo ""

# Define valid patterns
TYPE_PATTERN="^type:(feature|spike|task|bug|chore)$"
AREA_PATTERN="^area:(app|backend|realtime|telemetry|data|ux|ops)$"
PRIO_PATTERN="^prio:P[0-3]$"
SPRINT_PATTERN="^sprint:current$"
ESTIMATE_PATTERN="^estimate:[0-9]+$"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Track validation results
valid_count=0
invalid_count=0
declare -a invalid_labels

# Check if any labels provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 label1 label2 label3 ..."
    echo ""
    echo "Examples:"
    echo "  $0 type:feature area:telemetry prio:P1 estimate:5"
    echo "  $0 type:bug area:telemetry sprint:current"
    echo ""
    echo "Valid label patterns:"
    echo "  Type:     type:feature, type:spike, type:task, type:bug, type:chore"
    echo "  Area:     area:app, area:backend, area:realtime, area:telemetry, area:data, area:ux, area:ops"
    echo "  Priority: prio:P0, prio:P1, prio:P2, prio:P3"
    echo "  Sprint:   sprint:current"
    echo "  Estimate: estimate:<number> (e.g., estimate:5)"
    exit 1
fi

echo "Validating ${#} label(s)..."
echo ""

# Validate each label
for label in "$@"; do
    valid=false
    category=""
    
    if [[ $label =~ $TYPE_PATTERN ]]; then
        valid=true
        category="Type"
        value=$(echo "$label" | cut -d':' -f2)
        mapping="$(tr '[:lower:]' '[:upper:]' <<< ${value:0:1})${value:1}"
    elif [[ $label =~ $AREA_PATTERN ]]; then
        valid=true
        category="Area"
        value=$(echo "$label" | cut -d':' -f2)
        mapping="$(tr '[:lower:]' '[:upper:]' <<< ${value:0:1})${value:1}"
    elif [[ $label =~ $PRIO_PATTERN ]]; then
        valid=true
        category="Priority"
        value=$(echo "$label" | cut -d':' -f2)
        mapping="$value"
    elif [[ $label =~ $SPRINT_PATTERN ]]; then
        valid=true
        category="Sprint"
        mapping="Current iteration"
    elif [[ $label =~ $ESTIMATE_PATTERN ]]; then
        valid=true
        category="Estimate"
        value=$(echo "$label" | cut -d':' -f2)
        mapping="${value} points"
    fi
    
    if [ "$valid" = true ]; then
        echo -e "${GREEN}✅${NC} '$label' → ${category} = ${mapping}"
        valid_count=$((valid_count + 1))
    else
        echo -e "${RED}❌${NC} '$label' → Invalid label format"
        invalid_labels+=("$label")
        invalid_count=$((invalid_count + 1))
    fi
done

echo ""
echo "==========================================="
echo -e "Results: ${GREEN}${valid_count} valid${NC}, ${RED}${invalid_count} invalid${NC}"

if [ ${invalid_count} -gt 0 ]; then
    echo ""
    echo -e "${RED}Invalid labels detected:${NC}"
    for invalid_label in "${invalid_labels[@]}"; do
        echo "  - $invalid_label"
    done
    echo ""
    echo "Valid patterns:"
    echo "  Type:     type:(feature|spike|task|bug|chore)"
    echo "  Area:     area:(app|backend|realtime|telemetry|data|ux|ops)"
    echo "  Priority: prio:P[0-3]"
    echo "  Sprint:   sprint:current"
    echo "  Estimate: estimate:<number>"
    exit 1
fi

echo ""
echo -e "${GREEN}✅ All labels are valid!${NC}"
exit 0
