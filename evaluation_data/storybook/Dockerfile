ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=16.17.1
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"


# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm
RUN node --version
RUN npm --version

RUN npm install -g yarn

# Clone the storybook repository and checkout a specific commit
WORKDIR /storybook
RUN git init && \
    git remote add origin https://github.com/storybookjs/storybook.git && \
    git fetch --depth 1 origin 4f7342b509d4a396e42afc9a215047bed0a42c7b && \
    git checkout FETCH_HEAD


RUN npx playwright install-deps

# build the project
RUN yarn task --task build --template=react-vite/default-ts --start-from=auto

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=25
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

