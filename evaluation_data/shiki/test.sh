#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# Activate noise
noise-tool activate

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
    echo "[start] Test suite run $i"
    PLAYWRIGHT_JUNIT_OUTPUT_NAME=test-results/results.xml pnpm run test:e2e --reporter=junit
    mv "/shiki/test-results/results.xml" "/test-results/results_$i.xml"
    kill -9 $(lsof -t -i:3000)  # kill the server
    echo "[finished] Test suite run $i"
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results