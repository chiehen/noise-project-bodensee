FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    git curl build-essential python3.10 python3-pip
RUN pip install aggregate-test-results --index-url https://gitlab.lrz.de/api/v4/projects/140733/packages/pypi/simple

# Set configuration for noise; we will replace the hardcoded values later (feel free to do this now if it helps you)
# RUN noise-tool fuzz-load --load 30 \
#     noise-tool interrupt-network -i -t 20
