ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y\
    libglib2.0-0\
    libnss3\
    libnspr4\
    libatk1.0-0\
    libatk-bridge2.0-0\
    libcups2\
    libdrm2\
    libdbus-1-3\
    libatspi2.0-0\
    libxcomposite1\
    libxdamage1\
    libxfixes3\
    libxrandr2\
    libgbm1\
    libxkbcommon0\
    libpango-1.0-0\
    libcairo2\
    libasound2

# Install Node.js and NPM
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash && \
    . "$NVM_DIR/nvm.sh" && \
    nvm install ${NODE_VERSION} && \
    nvm use v${NODE_VERSION} && \
    nvm alias default v${NODE_VERSION} && \
    npm install -g npm && \
    npm install --g yarn

# Clone the material-ui repository and checkout a specific commit
WORKDIR /floating-ui
RUN git init && \
    git remote add origin https://github.com/floating-ui/floating-ui.git && \
    git fetch --depth 1 origin 947b4d5aadd59d40f4add43700483818ee55a96f && \
    git checkout FETCH_HEAD

# Install dependencies and build the project
WORKDIR /floating-ui
RUN npm install
RUN npx playwright install
RUN npm run build

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh
COPY --chmod=0755 SendRequest.py /SendRequest.py

# Run the test script
ENV EXECUTIONS=100
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]


