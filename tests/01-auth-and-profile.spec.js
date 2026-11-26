// @ts-check
import { test, expect } from '@playwright/test';

test.describe('Authentication & User Profile Dropdown', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
  });

  test('TC-00: Unauthenticated visitors start directly on login and signup page', async ({ browser }) => {
    const context = await browser.newContext();
    const page = await context.newPage();
    await page.addInitScript(() => {
      localStorage.clear();
      localStorage.setItem('isLoggedOut', 'true');
    });
    await page.goto('/');
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('#view-auth')).toBeVisible();
    await expect(page.locator('.main-header')).toBeHidden();
    await expect(page.locator('#authLoginForm')).toBeVisible();
    await expect(page.locator('#authTabSignIn')).toBeVisible();
    await expect(page.locator('#authTabRegister')).toBeVisible();
    await context.close();
  });

  test('TC-Join: Friend opens /join/:code directly and connects to watch room without 404', async ({ page }) => {
    await page.goto('/join/NX-C4LN');
    await page.waitForLoadState('domcontentloaded');
    await expect(page.locator('#view-room')).toBeVisible();
  });

  test('TC-01: Verify navbar displays the logged-in user avatar initials', async ({ page }) => {
    const avatarBtn = page.locator('#headerAvatarBtn');
    await expect(avatarBtn).toBeVisible();
    await expect(avatarBtn).toHaveText(/PR/i);
  });

  test('TC-02: User dropdown menu displays ONLY logged-in person details without demo persona list', async ({ page }) => {
    const avatarBtn = page.locator('#headerAvatarBtn');
    await avatarBtn.click();

    const dropdown = page.locator('#userMenuDropdown');
    await expect(dropdown).toBeVisible();

    // Verify Logged-in User Profile Header
    await expect(page.locator('#dropdownUserName')).toContainText('Priya');
    await expect(page.locator('#dropdownUserEmail')).toContainText('priya@netflix.com');
    await expect(page.locator('#dropdownUserRole')).toContainText('Host');

    // Verify Account Details Box
    await expect(page.locator('#dropdownUserId')).toContainText('u_501');
    await expect(page.locator('#dropdownUserPlan')).toContainText('Ultra HD 4K');
    await expect(page.locator('#dropdownUserLocale')).toContainText('English');

    // Verify that the old demo switcher is completely absent
    await expect(page.locator('text=Switch Demo Persona')).toHaveCount(0);
    await expect(page.locator('text=Maya (Viewer)')).toHaveCount(0);
    await expect(page.locator('text=Dev (Viewer)')).toHaveCount(0);
  });

  test('TC-03: Open Account Settings modal and update display name', async ({ page }) => {
    await page.locator('#headerAvatarBtn').click();
    await expect(page.locator('#userMenuDropdown')).toBeVisible();

    await page.locator('text=Account & Profile Settings').click();

    // Verify modal opened
    const modal = page.locator('#accountSettingsModal');
    await expect(modal).toBeVisible();
    await expect(page.locator('#settingsModalName')).toContainText('Priya');
    await expect(page.locator('#settingsModalEmail')).toHaveText('priya@netflix.com');

    // Update display name
    const nameInput = page.locator('#settingsDisplayNameInput');
    await nameInput.fill('Priya R.');
    await page.locator('#accountSettingsModal button:has-text("Save Changes")').click();

    // Modal should close and toast appear
    await expect(modal).toBeHidden();
    await expect(page.locator('#toastContainer')).toContainText('Profile and account preferences updated');

    // Verify updated name in user menu
    await page.locator('#headerAvatarBtn').click();
    await expect(page.locator('#dropdownUserName')).toHaveText('Priya R.');
  });

  test('TC-04: Sign out flow transitions to sign-in view', async ({ page }) => {
    await page.locator('#headerAvatarBtn').click();
    await expect(page.locator('#userMenuDropdown')).toBeVisible();

    await page.locator('text=Sign Out of Watch Spaces').click();

    // Verify redirected to Auth view
    await expect(page.locator('#view-auth')).toBeVisible();
    await expect(page.locator('#toastContainer')).toContainText('Signed out');
  });

  test('TC-05: Sign in flow authenticates and redirects to Home dashboard', async ({ page }) => {
    // Navigate to auth view
    await page.evaluate(() => window.switchView('auth'));
    await expect(page.locator('#view-auth')).toBeVisible();

    // Fill credentials
    await page.locator('#authLoginEmail').fill('priya@netflix.com');
    await page.locator('#authLoginPassword').fill('password');
    await page.locator('#authLoginForm button[type="submit"]').click();

    // Expect return to Home view
    await expect(page.locator('#view-home')).toBeVisible();
  });

  test('TC-05b: Create account flow registers new user and authenticates', async ({ page }) => {
    // Navigate to auth view
    await page.evaluate(() => window.switchView('auth'));
    await expect(page.locator('#view-auth')).toBeVisible();

    // Click "Create account" tab
    await page.locator('#authTabRegister').click();
    await expect(page.locator('#authRegisterContainer')).toBeVisible();

    // Fill registration form
    const uniqueEmail = `user_${Date.now()}@netflix.com`;
    await page.locator('#authRegisterName').fill('Alex Mercer');
    await page.locator('#authRegisterEmail').fill(uniqueEmail);
    await page.locator('#authRegisterPassword').fill('secretpass');
    await page.locator('#authRegisterForm button[type="submit"]').click();

    // Expect return to Home view and avatar to display AM
    await expect(page.locator('#view-home')).toBeVisible();
    await expect(page.locator('#headerAvatarBtn')).toContainText('AM');
  });

  test('TC-05c: Complete 3-step Signup: Send OTP, verify OTP code, and customize user profile', async ({ page }) => {
    await page.evaluate(() => {
      window.switchView('auth');
      window.__MANUAL_OTP_TEST__ = true;
    });
    await expect(page.locator('#view-auth')).toBeVisible();

    // 1. Step 1: Open Register tab and enter credentials
    await page.locator('#authTabRegister').click();
    await expect(page.locator('#authRegisterStep1')).toBeVisible();

    const uniqueEmail = `otp_user_${Date.now()}@netflix.com`;
    await page.locator('#authRegisterName').fill('Marcus Vance');
    await page.locator('#authRegisterEmail').fill(uniqueEmail);
    await page.locator('#authRegisterPassword').fill('secretpassword123');

    // Click Send Verification Code
    await page.locator('#authRegisterSubmitBtn').click();

    // 2. Step 2: Verify Step 2 is shown with OTP input
    await expect(page.locator('#authRegisterStep2')).toBeVisible();
    await expect(page.locator('#authOtpTargetEmail')).toContainText(uniqueEmail);

    // Enter 6-digit verification code
    const otpInput = page.locator('#authOtpInput');
    await expect(otpInput).toBeVisible();
    await otpInput.fill('123456');

    // Click Verify Code
    await page.locator('#authVerifyOtpBtn').click();

    // 3. Step 3: Verify Step 3 Profile Setup is shown
    await expect(page.locator('#authRegisterStep3')).toBeVisible();
    const profileName = page.locator('#authProfileName');
    await expect(profileName).toBeVisible();
    await expect(profileName).toHaveValue('Marcus Vance');

    // Select blue avatar color
    const blueChip = page.locator('.avatar-color-chip[data-color="#3B82F6"]');
    if (await blueChip.count() > 0) {
      await blueChip.click();
    }

    // Complete profile
    await page.locator('#authCompleteProfileBtn').click();

    // Verify redirected to Home dashboard and profile avatar displays MV
    await expect(page.locator('#view-home')).toBeVisible();
    await expect(page.locator('#headerAvatarBtn')).toContainText('MV');
  });
});
