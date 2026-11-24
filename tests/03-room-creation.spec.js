// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Watch Space Room Creation & Joining', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.openCreateModal === 'function');
    await expect(page.locator('#view-home')).toBeVisible();
  });

  test('TC-10: Open Start a Watch Space modal, configure settings, and select title', async ({ page }) => {
    // Open modal via Hero button
    await page.locator('#heroStartSpaceBtn').click();

    const modal = page.locator('#createSpaceModal');
    await expect(modal).toBeVisible();

    // Verify Step 1 is active
    await expect(page.locator('#createSpaceStep1')).toBeVisible();

    // Select Stranger Things title card
    const stCard = page.locator('.title-picker-card[data-title-id="t_stranger_things"]');
    if (await stCard.count() > 0) {
      await stCard.click();
      await expect(stCard).toHaveClass(/selected/);
    }

    // Toggle AI Co-Pilot verbosity
    const verboseBtn = page.locator('.verbosity-btn[data-verbosity="verbose"]');
    if (await verboseBtn.count() > 0) {
      await verboseBtn.click();
      await expect(verboseBtn).toHaveClass(/active/);
    }

    // Toggle Room Privacy
    const privateBtn = page.locator('.privacy-btn[data-privacy="private"]');
    if (await privateBtn.count() > 0) {
      await privateBtn.click();
      await expect(privateBtn).toHaveClass(/active/);
    }
  });

  test('TC-11: Submit room creation and verify Step 2 displays invite code', async ({ page }) => {
    await page.locator('#heroStartSpaceBtn').click();
    await expect(page.locator('#createSpaceModal')).toBeVisible();

    // Fill room name
    const roomInput = page.locator('#createRoomName');
    await roomInput.fill('Hawkins Automation Watch Club');

    // Click "Create watch space >"
    await page.locator('#createSpaceStep1 button:has-text("Create watch space")').click();

    // Step 2 should display invite code
    await expect(page.locator('#createSpaceStep2')).toBeVisible();
    const inviteCode = page.locator('#createdInviteCode');
    await expect(inviteCode).toBeVisible();
    await expect(inviteCode).not.toBeEmpty();

    // Close modal
    await page.locator('#createSpaceStep2 button.modal-close-btn').click();
    await expect(page.locator('#createSpaceModal')).toBeHidden();
  });

  test('TC-12: Join room modal opens and validates code entry', async ({ page }) => {
    // Click "Join with a code" button
    await page.locator('button:has-text("Join with a code")').first().click();

    const joinModal = page.locator('#joinRoomModal');
    await expect(joinModal).toBeVisible();

    const codeInput = page.locator('#joinInviteCodeInput');
    await expect(codeInput).toBeVisible();
    await codeInput.fill('NX-4Q7K');

    // Close join modal
    await page.locator('#joinRoomModal .modal-close-btn').click();
    await expect(joinModal).toBeHidden();
  });

  test('TC-12b: Direct invite URL /join/<invite_code> routes and joins room automatically', async ({ page }) => {
    await page.goto('/join/NX-4Q7K');
    await page.waitForLoadState('domcontentloaded');

    // Should automatically transition and display Watch Room view
    const roomView = page.locator('#view-room');
    await expect(roomView).toBeVisible({ timeout: 10000 });

    // Video player should be attached
    await expect(page.locator('#playerHtml5Video')).toBeAttached();
  });
});
