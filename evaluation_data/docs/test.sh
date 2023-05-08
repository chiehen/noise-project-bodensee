#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1


sed -i "36i reporter: 'junit'," /docs/playwright.config.ts

export ELASTICSEARCH_URL=http://localhost:9200/
mkdir /current-test-results

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
   echo "[start] Test suite run $i"
   PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml npm run playwright-test --reporter=junit
   mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
   echo "[finished] Test suite run $i"
done
