#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# edit theia config (https://github.com/eclipse-theia/theia/blob/b59581b411f33c639bfd68f23ec357280b9fdadf/examples/playwright/playwright.config.ts)
# set reporter
sed -i "43c ? [['junit']]" /theia/examples/playwright/playwright.config.ts
# repeateach
sed -i '27d' /theia/examples/playwright/playwright.config.ts
# retry
sed -i '25d' /theia/examples/playwright/playwright.config.ts

export PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml
export CI=1

# Activate noise
noise-tool activate

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
    echo "[start] Test suite run $i"
    yarn --cwd examples/playwright theia:start &
    yarn --cwd examples/playwright ui-tests
    mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
    kill -9 $(lsof -t -i:3000)  # kill the server
    echo "[finished] Test suite run $i"
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml