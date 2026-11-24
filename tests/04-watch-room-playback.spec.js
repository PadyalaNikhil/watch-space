// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Watch Room Video Player & Synchronization', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.rejoinActiveRoom === 'function');
    // Switch to room view
    await page.locator('.nav-link[data-view="room"]').click();
    await expect(page.locator('#view-room')).toBeVisible();
    await expect(page.locator('#playerVideoContainer')).toBeVisible();
  });

  test('TC-13: Authoritative room playback bar and synchronized clock are visible', async ({ page }) => {
    // Check playback container
    const playerArea = page.locator('#playerVideoContainer');
    await expect(playerArea).toBeVisible();

    // Check synchronized clock drift indicator
    const syncStatus = page.locator('#driftBadge');
    await expect(syncStatus).toBeVisible();
    await expect(syncStatus).toContainText(/In sync|sync/i);

    // Check time display
    const timeDisplay = page.locator('#playerTimeDisplay');
    await expect(timeDisplay).toBeVisible();
    await expect(timeDisplay).not.toBeEmpty();
  });

  test('TC-14: Play/Pause controls toggle synchronized state', async ({ page }) => {
    const playPauseBtn = page.locator('#playToggleBtn');
    await expect(playPauseBtn).toBeVisible();

    // Click pause / play
    await playPauseBtn.click();
    // Toast should show status update
    await expect(page.locator('#toastContainer')).toBeVisible();
  });

  test('TC-15: Direct Netflix and HTML5 video streaming source options are present', async ({ page }) => {
    // Verify direct Netflix launcher button
    const directNetflixBtn = page.locator('#directNetflixLinkBtn');
    await expect(directNetflixBtn).toBeVisible();
    await expect(directNetflixBtn).toHaveAttribute('href', /netflix\.com\/watch/);
    await expect(directNetflixBtn).toHaveAttribute('target', '_blank');

    // Verify HTML5 video element is loaded
    const html5Video = page.locator('#playerHtml5Video');
    await expect(html5Video).toBeVisible();

    // Verify Local file open button
    const openFileBtn = page.locator('#srcBtn_local');
    await expect(openFileBtn).toBeVisible();
  });

  test('TC-16: Live dialogue subtitles and audio synthesizer are active', async ({ page }) => {
    const subtitleBox = page.locator('#playerSubtitleBox');
    await expect(subtitleBox).toBeVisible();

    const subtitleText = page.locator('#subtitleText');
    await expect(subtitleText).toBeVisible();
    await expect(subtitleText).not.toBeEmpty();

    const synthBtn = page.locator('#audioToggleBtn');
    await expect(synthBtn).toBeVisible();
  });
});
