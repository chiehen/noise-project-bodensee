ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"
ENV CLOJURE_VERSION=1.10.1.763
ENV JAVA_VERSION=11

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y \
    rlwrap \
    default-jre-headless \
    fluxbox \
    xvfb


# Install Node.js and yarn
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm \
    npm install --global yarn

# Install
RUN curl -O https://download.clojure.org/install/linux-install-${CLOJURE_VERSION}.sh
RUN chmod +x linux-install-${CLOJURE_VERSION}.sh
RUN ./linux-install-${CLOJURE_VERSION}.sh

# Clone the docs repository and checkout a specific commit
WORKDIR /logseq
RUN git init && \
    git remote add origin https://github.com/logseq/logseq.git && \
    git fetch --depth 1 origin 839917dbf8f44c6a031a7314df7e9d0ef40660b5 && \
    git checkout FETCH_HEAD

# edit fixture.ts (https://github.com/logseq/logseq/blob/839917dbf8f44c6a031a7314df7e9d0ef40660b5/e2e-tests/fixtures.ts)
# to prevent launch fail
RUN sed -i "57i env: { ...process.env, NODE_ENV: 'development' }," /logseq/e2e-tests/fixtures.ts

# Fetch Clojure deps
RUN clojure -A:cljs -P

# Install dependencies and build the project
ENV PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=true
RUN npx playwright install-deps
RUN yarn install

# the app to be build with DEV-RELEASE flag
RUN yarn gulp:build && clojure -M:cljs release app electron --config-merge "{:closure-defines {frontend.config/DEV-RELEASE true}}" --debug

RUN (cd static && yarn install && yarn rebuild:all)
# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

