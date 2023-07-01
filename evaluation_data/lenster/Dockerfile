ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y \
    openssl \
    libssl-dev \
    lsof \
    libc++1

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g pnpm

# Clone the docs repository and checkout a specific commit
WORKDIR /lenster
RUN git init && \
    git remote add origin https://github.com/lensterxyz/lenster.git && \
    git fetch --depth 1 origin a2a84f1c5cf6912f42b04375798c4e04a679373f && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /lenster
RUN pnpm install
RUN pnpm codegen
RUN ./script/bootstrap
# Install browser
RUN pnpm dlx playwright@1.34.3 install chrome
RUN pnpm run build
RUN rm ./tests/playwright.config.ts

COPY  playwright.config.ts /lenster/tests/playwright.config.ts

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

