FROM ubuntu:22.04
ARG noise='noise-tool adddummynoise'
RUN apt-get update && apt-get install --no-install-recommends -y \
    git curl build-essential python3.10 python3-pip stress-ng iproute2
RUN pip install aggregate-test-results --index-url https://gitlab.lrz.de/api/v4/projects/140733/packages/pypi/simple

# Copy noise project to the container
COPY dist /noise-project
RUN pip install /noise-project/noise_tool-0.0.0-py3-none-any.whl

# Set configuration for noise
RUN eval ${noise}