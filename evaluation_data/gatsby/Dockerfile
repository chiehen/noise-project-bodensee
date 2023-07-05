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
    libglib2.0-0\
    libnss3\
    libnspr4\
    libatk1.0-0\
    libatk-bridge2.0-0\
    libcups2\
    libdrm2\
    libdbus-1-3\
    libxcb1\
    libxkbcommon0\
    libatspi2.0-0\
    libx11-6\
    libxcomposite1\
    libxdamage1\
    libxext6\
    libxfixes3\
    libxrandr2\
    libgbm1\
    libpango-1.0-0\
    libcairo2\
    libasound2\
    xvfb

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm && \
    npm install --g yarn

# Clone the docs repository and checkout a specific commit
WORKDIR /gatsby
RUN git init && \
    git remote add origin https://github.com/gatsbyjs/gatsby && \
    git fetch --depth 1 origin 7adb331a113cb8541124fd15e2943ccd580b6399 && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /gatsby
RUN yarn

WORKDIR /gatsby/e2e-tests/development-runtime/
RUN sed -i "s/process.env.CI ? 2 : 0/0/g" playwright.config.ts
RUN sed -i "s/process.env.CI/true/g" playwright.config.ts
RUN sed -i "s/html/junit/g" playwright.config.ts
RUN yarn

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

