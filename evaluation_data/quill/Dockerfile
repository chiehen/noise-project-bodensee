ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update


# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm && \
    npm install --g yarn
RUN apt-get install -y lsof

# Clone the material-ui repository and checkout a specific commit
WORKDIR /quill
RUN git init && \
    git remote add origin https://github.com/quilljs/quill.git && \
    git fetch --depth 1 origin d4907043b7ec96a784a1ec748fbfb13836b41ed2 && \
    git checkout FETCH_HEAD

# https://github.com/microsoft/playwright/issues/13724
RUN sed -i '/{ name: '\''Edge'\'', use: { channel: '\''msedge'\'' } },/d' ./playwright.config.ts

# Remove retries property from playwright config
RUN sed -i '/retries: process.env.CI ? 2 : 0/d' playwright.config.ts

# Install dependencies and build the project
WORKDIR /quill
RUN npm ci
RUN npx playwright install --with-deps

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh
COPY --chmod=0755 SendRequest.py /SendRequest.py

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

