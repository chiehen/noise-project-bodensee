ARG tag=latest
FROM gitlab.lrz.de:5005/robust-devops/students/noise-project-bodensee/base_image${tag}

ENV NODE_VERSION=18.16.0
ENV NVM_DIR=/root/.nvm
ENV PATH="${NVM_DIR}/versions/node/v${NODE_VERSION}/bin:${PATH}"

# Install required packages and dependencies
RUN apt-get update && \
    apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
    libatspi2.0-0 \
    libx11-6\
    libxcomposite1 \
    libxdamage1 \
    libxext6\
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxcb1\
    libxkbcommon0\
    libpango-1.0-0 \
    libcairo2 \
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
WORKDIR /cal-com
RUN git init && \
    git remote add origin https://github.com/calcom/cal.com.git && \
    git fetch --depth 1 origin a21f0c46c72f269f9de56445ed8f409fa56e0bd3 && \
    git checkout FETCH_HEAD

# Copy .env.example to .env
RUN mv .env.example .env

# Generate the NEXTAUTH_SECRET key
RUN NEXTAUTH_SECRET=$(openssl rand -base64 32) && echo "NEXTAUTH_SECRET=$NEXTAUTH_SECRET" >> .env

# Generate the CALENDSO_ENCRYPTION_KEY
RUN CALENDSO_ENCRYPTION_KEY=$(openssl rand -base64 24) && echo "CALENDSO_ENCRYPTION_KEY=$CALENDSO_ENCRYPTION_KEY" >> .env

# Modify playwright config
RUN sed -i -e 's/\r$//' playwright.config.ts
RUN sed -i 's/headless,/headless: true,/g' playwright.config.ts
RUN sed -i '/retries: process.env.CI ? 2 : 0,/d' playwright.config.ts
RUN sed -i '/maxFailures: headless ? 10 : undefined,/d' playwright.config.ts

# Install dependencies and build the project
WORKDIR /cal-com
RUN yarn install --inline-builds
RUN yarn prisma generate
RUN yarn playwright install
RUN yarn build

ENV DEBIAN_FRONTEND noninteractive

# Install Docker CLI dependencies
RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository
RUN echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker CLI
RUN apt-get update && \
    apt-get install -y docker-ce-cli

# Install Docker Compose
RUN curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && \
    chmod +x /usr/local/bin/docker-compose
VOLUME /var/run/docker.sock:/var/run/docker.sock

# Copy the test script to the container
COPY --chmod=0755 test.sh /test.sh

# Run the test script
ENV EXECUTIONS=100
ENV DATABASE_URL="postgresql://postgres:@postgres:5450/cal-saml"


RUN sed -i -e 's/\r$//' /test.sh
CMD ["/bin/bash", "-c", "/test.sh $EXECUTIONS"]

