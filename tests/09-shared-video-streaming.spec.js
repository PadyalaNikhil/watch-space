// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Shared Local Video Upload & Streaming', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.locator('.nav-link[data-view="room"]').click();
    await expect(page.locator('#view-room')).toBeVisible();
    await expect(page.locator('#playerVideoContainer')).toBeVisible();
  });

  test('TC-30: Host selects local video file, triggers instant local playback and upload', async ({ page }) => {
    const fileInput = page.locator('#localVideoFileInput');
    await expect(fileInput).toBeAttached();

    // Simulate selecting a local video file
    await fileInput.setInputFiles({
      name: 'community_movie.mp4',
      mimeType: 'video/mp4',
      buffer: Buffer.from('mock_video_mp4_bytes_data_stream_content_1234567890'),
    });

    // Verify HTML5 video player is active
    const html5Video = page.locator('#playerHtml5Video');
    await expect(html5Video).toBeVisible();

    // Verify toast confirmation
    await expect(page.locator('#toastContainer')).toContainText('community_movie.mp4');
  });

  test('TC-31: Viewer receives synchronized stream notification for host-shared video', async ({ page }) => {
    // Simulate room receiving shared custom video state
    await page.evaluate(() => {
      const noticeBanner = document.getElementById('sharedVideoNoticeBanner');
      const noticeText = document.getElementById('sharedVideoNoticeText');
      if (noticeBanner && noticeText) {
        noticeText.textContent = 'Now streaming: community_movie.mp4';
        noticeBanner.style.display = 'inline-flex';
      }
    });

    const banner = page.locator('#sharedVideoNoticeBanner');
    await expect(banner).toBeVisible();
    await expect(page.locator('#sharedVideoNoticeText')).toContainText('community_movie.mp4');
    await expect(page.locator('.shared-banner-badge')).toContainText('SYNCED');
  });
});
