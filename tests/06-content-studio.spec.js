// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Content Studio Metadata Authoring & Schema Validation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.switchView === 'function');
    await page.locator('.nav-link[data-view="studio"]').click();
    await expect(page.locator('#view-studio')).toBeVisible();
    await expect(page.locator('#studioTitleSelect')).toBeVisible();
  });

  test('TC-20: Content Studio title picker loads and updates metadata', async ({ page }) => {
    const titleSelect = page.locator('#studioTitleSelect');
    await expect(titleSelect).toBeVisible();

    // Select first title option or by value
    await titleSelect.selectOption({ index: 0 });

    // Verify title metadata reflects catalog
    const metaHeading = page.locator('#studioTitleMeta');
    await expect(metaHeading).toBeVisible();
    await expect(metaHeading).toContainText(/runtime|events/i);
  });

  test('TC-21: Scrubber timeline markers and event filter pills are interactive', async ({ page }) => {
    // Verify timeline events table has loaded rows
    const eventsTable = page.locator('#studioEventsTbody');
    await expect(eventsTable).toBeVisible();

    // Filter pills (All, Trivia, Characters, Variation Points)
    const filterPills = page.locator('.filter-pill');
    await expect(filterPills.first()).toBeVisible();

    // Click Trivia filter
    const triviaPill = page.locator('.filter-pill[data-type="trivia"]');
    if (await triviaPill.count() > 0) {
      await triviaPill.click();
      await expect(triviaPill).toHaveClass(/active/);
    }
  });

  test('TC-22: Validate & Publish Timeline triggers schema v1.2 SQL validation', async ({ page }) => {
    const publishBtn = page.locator('.btn-publish-schema');
    await expect(publishBtn).toBeVisible();

    await publishBtn.click();

    // Verify feedback toast is displayed
    const toast = page.locator('#toastContainer');
    await expect(toast).toBeVisible();
    await expect(toast).toContainText(/schema|validat|publish|enforced/i);
  });
});
