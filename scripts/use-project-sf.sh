#!/usr/bin/env bash

# Use a project-local HOME for Salesforce CLI so org auth does not leak across repos.
PROJECT_HOME_DIR="${SF_PROJECT_HOME:-$PWD/.sf-home}"
mkdir -p "$PROJECT_HOME_DIR"

export SF_PROJECT_HOME="$PROJECT_HOME_DIR"
export HOME="$PROJECT_HOME_DIR"

echo "HOME=$HOME"
echo "Project-local Salesforce auth is now active for this shell."
echo "Next step: sf org login web -a carmax-demo-sdo"
