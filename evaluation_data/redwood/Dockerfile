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

# Clone the redwood repository and checkout a specific commit
WORKDIR /redwood
RUN git init && \
    git remote add origin https://github.com/redwoodjs/redwood && \
    git fetch --depth 1 origin a8c7e4ab6db5a99c370b7191add8c492515b4739 && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /redwood
RUN yarn install --inline-builds
RUN yarn build
RUN npx playwright install --with-deps chromium

# Setup test project
RUN cp -r __fixtures__/test-project/ /test-project
RUN RWJS_CWD="/test-project" yarn project:deps
WORKDIR /test-project
RUN yarn install
WORKDIR /redwood
RUN RWJS_CWD="/test-project" yarn project:copy
WORKDIR /test-project
RUN yarn rw prisma migrate reset --force

RUN yarn rw g secret --raw
RUN echo -n SESSION_SECRET= >> test.txt && silent=true yarn rw g secret --raw >> .env
RUN yarn rw prisma migrate reset --force

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

ENV REDWOOD_TEST_PROJECT_PATH=/test-project
ENV REDWOOD_DISABLE_TELEMETRY=1
# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

