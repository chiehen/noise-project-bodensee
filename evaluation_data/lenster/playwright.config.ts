import type { PlaywrightTestConfig } from '@playwright/test';
import { devices } from '@playwright/test';
import * as os from 'os';

const config: PlaywrightTestConfig = {
  testDir: './',
  timeout: 50 * 1000,
  expect: { timeout: 50000 },
  fullyParallel: true,
  maxFailures: 3,
  forbidOnly: Boolean(process.env.CI),
  retries: 0,
  workers: os.cpus().length === 1 ? 1 : os.cpus().length - 1,
  reporter: [['junit', { 'outputFile': "/current-test-results/results.xml"}]],
  use: { actionTimeout: 0, trace: 'on-first-retry' },
  projects: [{
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },]
};

export default config;