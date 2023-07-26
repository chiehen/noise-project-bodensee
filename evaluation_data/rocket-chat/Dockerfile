ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=14.21.3
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y \
    g++ build-essential git curl python2-minimal npm

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm && \
    npm install --g yarn

RUN curl https://install.meteor.com/ | sh
RUN npx playwright@1.22.2 install
RUN npx playwright@1.22.2 install chrome

# Clone the material-ui repository and checkout a specific commit
WORKDIR /rocket-chat
RUN git init && \
    git remote add origin https://github.com/RocketChat/Rocket.Chat.git && \
    git fetch --depth 1 origin b9795304af333a6f3b87126504fa700392c50fe0 && \
    git checkout FETCH_HEAD
RUN npm install -g meteor

# Remove maxFailures from playwright.config.ts
RUN sed -i '/maxFailures: process.env.CI ? 5 : undefined/d' apps/meteor/playwright.config.ts

# Install dependencies and build the project
WORKDIR /rocket-chat
RUN yarn
RUN yarn build

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh
COPY --chmod=0755 SendRequest.py /SendRequest.py

# Run the test script
ENV EXECUTIONS=100
WORKDIR /rocket-chat
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

