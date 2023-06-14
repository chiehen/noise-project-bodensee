#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# edit playwright config
sed -i '38c const headed = false;' /playwright/tests/library/playwright.config.ts
sed -i '70c retries: 0,' /playwright/tests/library/playwright.config.ts
sed -i "71c reporter: 'junit'," /playwright/tests/library/playwright.config.ts
export CI=1
export PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml

# Activate noise
noise-tool activate

mkdir /current-test-results

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
   echo "[start] Test suite run $i"
   PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml npm run ctest -- --reporter=junit
   mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
   echo "[finished] Test suite run $i"
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml