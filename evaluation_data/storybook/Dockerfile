ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=16.17.1
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
# RUN apt-get update && \
#     apt-get install -y \
#     openssl \
#     libssl-dev \
#     lsof

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm
RUN node --version
RUN npm --version

# Clone the storybook repository and checkout a specific commit
WORKDIR /storybook
RUN git init && \
    git remote add origin https://github.com/storybookjs/storybook.git && \
    git fetch --depth 1 origin ed105890826fd37ea20c4613d3bee700bcb31079 && \
    git checkout FETCH_HEAD


RUN npx playwright install-deps

# install yarn with specific version
RUN corepack enable && corepack prepare yarn@stable --activate && yarn set version 3.5.1 && yarn install
RUN yarn --version

# build the project
RUN yarn task --task build --template=react-vite/default-ts --start-from=auto

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=1
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

