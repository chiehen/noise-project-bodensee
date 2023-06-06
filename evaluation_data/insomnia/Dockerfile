ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=16.20.0
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
    npm install -g npm

# Clone the docs repository and checkout a specific commit
WORKDIR /insomnia
RUN git init && \
    git remote add origin https://github.com/Kong/insomnia.git && \
    git fetch --depth 1 origin 1005897417c184d9f2d31a3c6d47e384869c2b48 && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /insomnia
RUN npm run bootstrap && npm run app-build


# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=25
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

