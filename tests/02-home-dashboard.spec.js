// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Home Dashboard & Navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.switchView === 'function');
    await expect(page.locator('#view-home')).toBeVisible();
  });

  test('TC-06: Brand header and top navigation links switch views correctly', async ({ page }) => {
    // Check brand logo in header
    const logo = page.locator('.main-header .netflix-logo');
    await expect(logo).toBeVisible();
    await expect(logo).toHaveText('NETFLIX');

    // Click "Watch spaces" tab
    await page.locator('.nav-link[data-view="room"]').click();
    await expect(page.locator('#view-room')).toBeVisible();
    await expect(page.locator('#view-home')).toBeHidden();

    // Click "Studio" tab
    await page.locator('.nav-link[data-view="studio"]').click();
    await expect(page.locator('#view-studio')).toBeVisible();
    await expect(page.locator('#view-room')).toBeHidden();

    // Click "Home" tab to return
    await page.locator('.nav-link[data-view="home"]').click();
    await expect(page.locator('#view-home')).toBeVisible();
  });

  test('TC-07: Hero Banner displays featured title with metadata and action CTAs', async ({ page }) => {
    const heroTitle = page.locator('#heroTitle');
    await expect(heroTitle).toBeVisible();
    await expect(heroTitle).not.toBeEmpty();

    const startSpaceBtn = page.locator('#heroStartSpaceBtn');
    await expect(startSpaceBtn).toBeVisible();

    const joinCodeBtn = page.locator('button:has-text("Join with a code")');
    await expect(joinCodeBtn).toBeVisible();
  });

  test('TC-08: Scheduled Watch Spaces and Continue Watching cards are visible', async ({ page }) => {
    // Verify scheduled spaces rail
    const scheduledRail = page.locator('.schedule-rail');
    await expect(scheduledRail).toBeVisible();

    const scheduleCards = page.locator('.schedule-card');
    const count = await scheduleCards.count();
    expect(count).toBeGreaterThan(0);

    // Verify continue watching row
    const continueRail = page.locator('.continue-rail');
    await expect(continueRail).toBeVisible();
  });

  test('TC-09: Header Instant Search filters catalog titles dynamically', async ({ page }) => {
    // Click search icon button to expand search bar
    await page.locator('#searchToggleBtn').click();

    const searchInput = page.locator('#headerSearchInput');
    await expect(searchInput).toBeVisible();
    await searchInput.fill('stranger');

    // Search results dropdown should become visible
    const dropdown = page.locator('#searchResultsDropdown');
    await expect(dropdown).toBeVisible();

    const resultsList = page.locator('#searchResultsList');
    await expect(resultsList).toContainText('Stranger Things');
  });
});
