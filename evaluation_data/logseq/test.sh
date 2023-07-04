#!/bin/bash

# Get the number of test executions from the first command line argument
EXECUTIONS=$1

export PLAYWRIGHT_JUNIT_OUTPUT_NAME=/current-test-results/results.xml
export CI=true
export LOGSEQ_CI=true
export DEBUG="pw:api"
export RELEASE=true # skip dev only test

# edit https://github.com/logseq/logseq/blob/839917dbf8f44c6a031a7314df7e9d0ef40660b5/playwright.config.ts
sed -i '8d' /logseq/playwright.config.ts
sed -i '5d' /logseq/playwright.config.ts
sed -i "5i reporter: 'junit'," /logseq/playwright.config.ts

# Activate noise
noise-tool activate


mkdir /current-test-results
max_time=36000 # 10 hrs
elapsed_time=0

mkdir -p /test-results
for i in $(seq 1 $EXECUTIONS); do
   test_start=$(date +%s)
   echo "[start] Test suite run $i"
   Xvfb :1 -screen 0 1024x768x24 >/dev/null 2>&1 &
   DISPLAY=:1.0 fluxbox >/dev/null 2>&1 &
   DISPLAY=:1.0 npx playwright test --reporter junit
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