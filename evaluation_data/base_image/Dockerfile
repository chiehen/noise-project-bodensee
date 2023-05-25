FROM ubuntu:22.04
RUN apt-get update && apt-get install -y \
    git curl build-essential python3.10 python3-pip
RUN pip install aggregate-test-results --index-url https://gitlab.lrz.de/api/v4/projects/140733/packages/pypi/simple


# Copy noise project to the container
COPY dist /noise-project
RUN pip install /noise-project/noise_tool-0.0.0-py3-none-any.whl

# Install stress-ng
RUN apt-get install -y stress-ng

# Set configuration for noise
RUN noise-tool adddummynoise
RUN noise-tool stress-ng add "^^cpu 0 ^l 5 ^^copy-file 5 ^^copy-file-bytes 2G"
