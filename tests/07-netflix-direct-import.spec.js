// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Direct Netflix Movie Ingestion Modal', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.switchView === 'function');
    await page.locator('.nav-link[data-view="studio"]').click();
    await expect(page.locator('#view-studio')).toBeVisible();
  });

  test('TC-23: Open Import from Netflix modal and verify ingestion inputs', async ({ page }) => {
    // Click "+ Import from Netflix" button
    const importBtn = page.locator('button:has-text("Import from Netflix")').first();
    await expect(importBtn).toBeVisible();
    await importBtn.click();

    const modal = page.locator('#netflixImportModal');
    await expect(modal).toBeVisible();

    const searchInput = page.locator('#netflixSearchInput');
    await expect(searchInput).toBeVisible();

    // Close modal
    await page.locator('#netflixImportModal .modal-close-btn').click();
    await expect(modal).toBeHidden();
  });

  test('TC-24: Search Netflix movie and verify metadata card preview', async ({ page }) => {
    // Open import modal
    await page.locator('button:has-text("Import from Netflix")').first().click();

    const searchInput = page.locator('#netflixSearchInput');
    await searchInput.fill('Stranger Things');

    // Click "Fetch from Netflix"
    await page.locator('button:has-text("Fetch from Netflix")').click();

    // Verify preview card appears with title and schema notice
    const previewCard = page.locator('#netflixPreviewCard');
    await expect(previewCard).toBeVisible();

    const previewName = page.locator('#netflixPreviewName');
    await expect(previewName).toContainText(/Stranger Things/i);

    // Verify Confirm Import button is shown
    const confirmBtn = page.locator('#btnConfirmNetflixImport');
    await expect(confirmBtn).toBeVisible();

    // Close modal
    await page.locator('#netflixImportModal .modal-close-btn').click();
    await expect(page.locator('#netflixImportModal')).toBeHidden();
  });
});
