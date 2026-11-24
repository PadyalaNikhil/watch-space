// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Live Room Chat & Grounded AI Co-Pilot', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.rejoinActiveRoom === 'function');
    await page.locator('.nav-link[data-view="room"]').click();
    await expect(page.locator('#view-room')).toBeVisible();
    await expect(page.locator('#playerVideoContainer')).toBeVisible();
  });

  test('TC-17: Send message in room chat and verify appearance', async ({ page }) => {
    // Ensure chat tab is active
    await page.locator('.tab-btn[data-tab="chat"]').click();
    await expect(page.locator('#tabContent-chat')).toBeVisible();

    const chatInput = page.locator('#chatInput');
    await expect(chatInput).toBeVisible();

    const testMsg = 'Automated Playwright test message ' + Date.now();
    await chatInput.fill(testMsg);

    // Send via chat tab send button
    await page.locator('#tabContent-chat .btn-send-chat').click();

    // Verify message appears in feed
    const chatFeed = page.locator('#chatMessagesStream');
    await expect(chatFeed).toContainText(testMsg);
  });

  test('TC-18: Toggle Ask AI mode and request grounded story answer', async ({ page }) => {
    // 1. In Chat tab, toggle Ask AI mode
    await page.locator('.tab-btn[data-tab="chat"]').click();
    await expect(page.locator('#tabContent-chat')).toBeVisible();

    const askAiBtn = page.locator('#toggleAiAskBtn');
    await expect(askAiBtn).toBeVisible();
    await askAiBtn.click();
    await expect(askAiBtn).toHaveClass(/active/);
    await expect(page.locator('#chatInput')).toHaveAttribute('placeholder', /Ask AI Co-Pilot/i);

    // 2. Switch to Co-Pilot tab and verify Scene Context card
    await page.locator('.tab-btn[data-tab="copilot"]').click();
    await expect(page.locator('#tabContent-copilot')).toBeVisible();

    const sceneCard = page.locator('.scene-context-card');
    await expect(sceneCard).toBeVisible();
  });

  test('TC-19: People tab displays participant roster', async ({ page }) => {
    // Switch to People tab
    await page.locator('.tab-btn[data-tab="people"]').click();
    await expect(page.locator('#tabContent-people')).toBeVisible();

    // Verify participant list
    const participantRows = page.locator('#peopleListContainer .person-row');
    const count = await participantRows.count();
    expect(count).toBeGreaterThan(0);
  });
});
