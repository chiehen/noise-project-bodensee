#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

# Activate noise
export BASE_SEND_REQUEST=localhost
export PORT_SEND_REQUEST=8000
noise-tool activate

mkdir /current-test-results

mkdir -p /test-results

max_time=36000 # 10 hrs

for i in $(seq 1 $EXECUTIONS); do
    test_start=$(date +%s)
    echo "[start] Test suite run $i"
    PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml yarn start-server-and-test:playwright
    mv "/current-test-results/results.xml" "/test-results/results_$i.xml"
    echo "[finished] Test suite run $i"

    test_end=$(date +%s)
    # check if execution time will exceeds
    test_time=$((test_end - test_start))
    echo "one iteration time: $test_time"
    elapsed_time=$((elapsed_time + test_time))
    avg_time=$((elapsed_time / i))
    echo "Avg time per iteration so far: $avg_time seconds."
    projected_end_time=$((elapsed_time + avg_time))
    if [ $projected_end_time -ge $max_time ]; then
        echo "Projected execution time for the next iteration will exceed the time limit."
        echo "Number of executions done: $i"
        break
    fi
done

# Deactivate noise
noise-tool deactivate

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml
