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
    lsof

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g pnpm

# Clone the docs repository and checkout a specific commit
WORKDIR /dev-roadmap
RUN git init && \
    git remote add origin https://github.com/kamranahmedse/developer-roadmap.git && \
    git fetch --depth 1 origin a48d39a8630d98677a52f448537520f217201964 && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /dev-roadmap
RUN pnpm install && \
    pnpm run build && \
    pnpm dlx playwright install-deps && \
    pnpm dlx playwright install


RUN touch ./dist/.nojekyll && \
    echo 'roadmap.sh' > ./dist/CNAME

# remove retries and change reporter to junit
RUN sed -i 's/process.env.CI ? 2 ://g' playwright.config.ts && sed -i "s/'html'/[['junit', { 'outputFile': '\/current-test-results\/results.xml'}]]/g" playwright.config.ts

RUN pnpm run test:e2e --update-snapshots || : # Allow test to fail
# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=25
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

