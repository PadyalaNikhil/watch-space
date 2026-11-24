// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Watch Room Real-Time Voice Chat & Spatial Audio', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await page.waitForFunction(() => typeof window.rejoinActiveRoom === 'function');
    
    // Switch to room view
    await page.locator('.nav-link[data-view="room"]').click();
    await expect(page.locator('#view-room')).toBeVisible();
    await expect(page.locator('#playerVideoContainer')).toBeVisible();
  });

  test('TC-27: Room header displays Voice Chat island with status and mute controls', async ({ page }) => {
    const voiceIsland = page.locator('#roomVoiceIsland');
    await expect(voiceIsland).toBeVisible();

    const voiceStatusBtn = page.locator('#voiceToggleConnectBtn');
    await expect(voiceStatusBtn).toBeVisible();
    await expect(voiceStatusBtn).toContainText(/Voice/i);

    const micBtn = page.locator('#voiceMicBtn');
    await expect(micBtn).toBeVisible();

    const deafenBtn = page.locator('#voiceDeafenBtn');
    await expect(deafenBtn).toBeVisible();
  });

  test('TC-28: Microphone toggle controls mute and unmute states', async ({ page }) => {
    const micBtn = page.locator('#voiceMicBtn');
    await expect(micBtn).toBeVisible();

    // Toggle mute
    await micBtn.click();
    await expect(page.locator('#toastContainer')).toContainText(/Microphone/i);
    await expect(micBtn).toHaveClass(/muted/);

    // Toggle unmute
    await micBtn.click();
    await expect(page.locator('#toastContainer')).toContainText(/Microphone/i);
    await expect(micBtn).not.toHaveClass(/muted/);
  });

  test('TC-29: Sidebar Voice tab displays voice stage and participant cards', async ({ page }) => {
    // Click on Voice tab in sidebar
    const voiceTabBtn = page.locator('#sidebarTabVoice');
    await expect(voiceTabBtn).toBeVisible();
    await voiceTabBtn.click();

    // Voice tab content should be visible
    const voiceTabContent = page.locator('#tabContent-voice');
    await expect(voiceTabContent).toBeVisible();

    // Verify voice participants grid
    const voiceGrid = page.locator('#voiceParticipantsGrid');
    await expect(voiceGrid).toBeVisible();

    // Verify participant cards exist
    const cards = page.locator('.voice-card');
    await expect(cards.first()).toBeVisible();
    const count = await cards.count();
    expect(count).toBeGreaterThan(0);

    // Verify input mode selector and mic level meter
    await expect(page.locator('#voiceModeSelect')).toBeVisible();
    await expect(page.locator('#voiceLiveMeterFill')).toBeVisible();
  });

  test('TC-30: In-video floating speaker badge appears during active speech', async ({ page }) => {
    // Trigger simulated speech
    await page.evaluate(() => {
      window.simulateParticipantSpeaking();
    });

    // Check that floating speaker badge on the player is visible
    const speakerBadge = page.locator('#playerVoiceSpeakerBadge');
    await expect(speakerBadge).toBeVisible();
    await expect(speakerBadge).toContainText(/speaking/i);
  });

  test('TC-31: Keyboard shortcut "M" toggles microphone mute state', async ({ page }) => {
    const micBtn = page.locator('#voiceMicBtn');
    
    // Press 'M' key
    await page.keyboard.press('m');
    await expect(page.locator('#toastContainer')).toContainText(/Microphone/i);
    await expect(micBtn).toHaveClass(/muted/);

    // Press 'M' key again to unmute
    await page.keyboard.press('m');
    await expect(page.locator('#toastContainer')).toContainText(/Microphone/i);
    await expect(micBtn).not.toHaveClass(/muted/);
  });
});
