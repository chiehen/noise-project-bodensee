#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# Activate noise
noise-tool activate

export ELASTICSEARCH_URL=http://localhost:9200/
mkdir /current-test-results

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
   echo "[start] Test suite run $i"
   pnpm run test:e2e
   mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
   echo "[finished] Test suite run $i"
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml