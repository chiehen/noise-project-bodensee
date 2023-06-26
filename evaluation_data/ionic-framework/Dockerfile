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
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libxkbcommon0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm && \
    npm install --g yarn

# Clone the ionic-framework repository and checkout a specific commit
WORKDIR /ionic-framework
RUN git init && \
    git remote add origin https://github.com/ionic-team/ionic-framework && \
    git fetch --depth 1 origin cb013df7f5ab937c7815195def5c5d4b266b994d && \
    git checkout FETCH_HEAD

WORKDIR /ionic-framework/core

# Remove retries property from playwright config
RUN sed -i '/retries: process.env.CI ? 2 : 0/d' playwright.config.ts

# Install dependencies and build the project
RUN npm install --legacy-peer-deps
RUN npx playwright install
RUN npx playwright install-deps

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=10
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

