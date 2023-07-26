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

# start browser on http://localhost:3000
yarn --cwd examples/playwright theia:start &

# Activate noise
export BASE_SEND_REQUEST=localhost
export PORT_SEND_REQUEST=3000
noise-tool activate

mkdir -p /test-results
max_time=36000 # 10 hrs
elapsed_time=0
for i in $(seq 1 $EXECUTIONS); do
    test_start=$(date +%s)

    echo "[start] Test suite run $i"
    yarn --cwd examples/playwright ui-tests
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

kill -9 $(lsof -t -i:3000)  # kill the server

# Get test outputs
aggregate-test-results parse-junit-xml /test-results
# Create artifacts
aggregate-test-results create-artifacts /test-results /experiment-artifacts --aggregation-format junit-xml