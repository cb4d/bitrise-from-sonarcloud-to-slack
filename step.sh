#!/bin/bash
set -ex

function error_exit {
    echo
    echo "$@"
    exit 1
}

pip3 install requests || error_exit "Couldn\'t install python dependency \(requests\)"
python3 "$BITRISE_STEP_SOURCE_DIR/sonar-status.py" "${sonar_project_key}" "${sonar_api_token}" "${slack_webhook_url}" || error_exit "Failed to run sonar status script"
