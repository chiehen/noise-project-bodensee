ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

# Node.js >= 16.14.0 and < 17
ENV NODE_VERSION=16.20.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    libx11-dev \
    libxkbfile-dev \
    libsecret-1-dev


# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm \
    npm install --global yarn
RUN node --version
RUN npm --version
RUN yarn --version

# Clone the theia repository and checkout a specific commit
WORKDIR /theia
RUN git init && \
    git remote add origin https://github.com/eclipse-theia/theia.git && \
    git fetch --depth 1 origin b59581b411f33c639bfd68f23ec357280b9fdadf && \
    git checkout FETCH_HEAD

# Build Browser
RUN yarn config set script-shell /bin/bash
RUN NODE_ENV=development yarn install --production=false
RUN yarn install --check-files
RUN yarn download:plugins
RUN yarn browser build

# Build Playwright
RUN yarn --cwd examples/playwright build
RUN npx playwright install --with-deps chromium

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

