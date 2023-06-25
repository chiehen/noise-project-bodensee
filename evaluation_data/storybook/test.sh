#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# edit storybook config (https://github.com/storybookjs/storybook/blob/472d37fdf7f65ce804f3ccec354761ca527dadeb/code/playwright.config.ts#L2)
# disable retry
sed -i '29d' /storybook/code/playwright.config.ts

export PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml
export CI=1

# Activate noise
noise-tool activate

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
    echo "[start] Test suite run $i"
    yarn task --task e2e-tests --template=react-vite/default-ts --start-from=auto
    mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
    echo "[finished] Test suite run $i"
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml