ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

# require Node.js 16+ and NPM 8+
ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"


# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm i -g npm@latest

# Clone the playwright repository and checkout a specific commit
WORKDIR /playwright
RUN git init && \
    git remote add origin https://github.com/microsoft/playwright.git && \
    git fetch --depth 1 origin e4a1273afa41ba8055c0d82ff29225488e5c0eb1 && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /playwright
RUN npm ci && \
    npm run build && \
    npx playwright install --with-deps chromium

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=1
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

