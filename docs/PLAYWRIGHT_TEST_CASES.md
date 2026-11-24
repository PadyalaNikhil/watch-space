# Netflix Watch Spaces — Playwright UI Automation Test Suite

Comprehensive end-to-end UI automation testing suite for the **Netflix Watch Spaces** application built with [Playwright Test](https://playwright.dev/).

---

## 1. Test Architecture & Overview

The UI automation test suite is structured into **7 modular specification files** covering **24 detailed test cases**, testing all core features:
- Authentication, Sign In / Sign Out, and Logged-in Profile Details
- Home Dashboard, Navigation, and Instant Catalog Search
- Watch Space Room Creation (2-step modal) & Code-based Joining
- Authoritative Room Playback, Synchronization Clock (<250ms drift), and Multi-source Video Player
- Real-time Room Chat and Grounded AI Co-Pilot RAG Interaction
- Content Studio Timeline Scrubber and Schema v1.2 SQL Validator
- Direct Netflix Movie Ingestion Modal

```
tests/
├── 01-auth-and-profile.spec.js          # TC-01 to TC-05: User profile, account settings, auth flows
├── 02-home-dashboard.spec.js           # TC-06 to TC-09: Hero banner, nav links, schedule, search
├── 03-room-creation.spec.js            # TC-10 to TC-12: Room setup modal, invite codes, join modal
├── 04-watch-room-playback.spec.js      # TC-13 to TC-16: Playback controls, sync clock, Netflix player
├── 05-chat-and-copilot.spec.js         # TC-17 to TC-19: Live chat messages, AI Co-Pilot, participants
├── 06-content-studio.spec.js           # TC-20 to TC-22: Scrubber markers, filters, SQL validation
└── 07-netflix-direct-import.spec.js    # TC-23 to TC-24: Netflix search, metadata preview, catalog import
```

---

## 2. Test Cases Matrix

| Test ID | Module | Title | Description | Expected Outcome |
| :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Auth & Profile | Navbar Avatar Verification | Verify user avatar displays initials `PR` with host styling | Avatar button visible with correct text and color |
| **TC-02** | Auth & Profile | Logged-in Details Only | Click avatar to verify profile card displays ONLY the logged-in user details (Priya Raman, email, ID, Plan, Status) and NO demo persona list | User details visible; demo persona switcher absent |
| **TC-03** | Auth & Profile | Profile Settings Modal | Open Account & Profile Settings modal, edit display name, and save | Changes persist and toast displays confirmation |
| **TC-04** | Auth & Profile | Sign Out Flow | Click "Sign Out of Watch Spaces" in user dropdown | Clears token and navigates cleanly to `#view-auth` |
| **TC-05** | Auth & Profile | Sign In Flow | Enter email and password on auth page and submit | Authenticates and returns to Home dashboard |
| **TC-06** | Home Dashboard | Navigation Bar Switching | Click "Home", "Watch spaces", and "Studio" tabs | Respective view containers toggle visibility without page reload |
| **TC-07** | Home Dashboard | Hero Banner & CTAs | Verify hero title, match %, tags, and primary action buttons | Hero metadata renders with "Start a watch space" CTA |
| **TC-08** | Home Dashboard | Scheduled & Continue Rows | Verify scheduled watch spaces rail (`.schedule-rail`) and continue watching rows | Grid cards render and respond to interaction |
| **TC-09** | Home Dashboard | Instant Catalog Search | Expand search via `#searchToggleBtn`, type "stranger" in `#headerSearchInput` | Live search dropdown renders matched title card |
| **TC-10** | Room Creation | Step 1 Room Configuration | Open modal, pick title, adjust participants, toggle AI verbosity and privacy | Controls respond and update selection state |
| **TC-11** | Room Creation | Step 2 Invite Code | Fill room name and submit room creation | Step 2 modal displays generated shareable room code |
| **TC-12** | Room Creation | Join Room with Code | Click "Join with a code" and input room invite code (`#joinInviteCodeInput`) | Join dialog accepts code and initiates room sync |
| **TC-13** | Watch Room | Synchronized Playback Bar | Inspect playback container (`#playerVideoContainer`), clock, and drift badge (`#driftBadge`) | Clock and "In sync (< 250ms)" badge visible |
| **TC-14** | Watch Room | Play/Pause Sync Control | Toggle play/pause button (`#playToggleBtn`) | Playback state toggles and sync toast notifies room |
| **TC-15** | Watch Room | Video Player Sources | Verify HTML5 direct stream, "Watch on Netflix.com ↗", and local file launcher (`#srcBtn_local`) | Source controls and direct Netflix link are active |
| **TC-16** | Watch Room | Subtitles & Synthesizer | Verify live dialogue subtitles overlay (`#subtitleText`) and synth audio button (`#audioToggleBtn`) | Subtitle text displays; Web Audio synth button toggles |
| **TC-17** | Chat & Co-Pilot | Send Room Chat Message | Type message in chat input and submit via `.btn-send-chat` | Bubble appears in `#chatMessagesStream` with user avatar and timestamp |
| **TC-18** | Chat & Co-Pilot | Ask AI Co-Pilot Query | Switch to Co-Pilot tab (`.scene-context-card`), activate "✦ Ask AI", and submit question | Input switches to Co-Pilot mode; grounded answers load |
| **TC-19** | Chat & Co-Pilot | Participant Roster | Switch to People tab (`#peopleListContainer .person-row`) | Participant list renders with status indicators and counts |
| **TC-20** | Content Studio | Title Switching | Select title from `#studioTitleSelect` | Studio timeline updates to reflect selected title metadata |
| **TC-21** | Content Studio | Events Table & Filters | Inspect `#studioEventsTbody` rows and toggle event type filter pills | Events populate; filter pills isolate trivia, characters, and variations |
| **TC-22** | Content Studio | Publish Timeline | Click "Validate & publish ✓" (`.btn-publish-schema`) | Validates schema v1.2 and triggers SQL commit toast |
| **TC-23** | Netflix Import | Import Dialog Inputs | Click "+ Import from Netflix" in Content Studio | Modal opens with search input and ingestion guidelines |
| **TC-24** | Netflix Import | Metadata Ingestion Preview | Search Netflix title via "Fetch from Netflix" | Renders candidate preview card (`#netflixPreviewCard`) with episodes, synopsis, and confirm CTA |

---

## 3. How to Run the Tests

### Prerequisites
1. Python Django backend installed and configured with SQLite database:
   ```powershell
   python manage.py migrate
   ```
2. Node.js dependencies installed:
   ```powershell
   npm install
   ```

### Execution Commands

- **Run all E2E tests (Headless mode)**:
  ```powershell
  npm run test:e2e
  # or
  npx playwright test
  ```

- **Run tests in Headed mode (visible browser window)**:
  ```powershell
  npm run test:e2e:headed
  # or
  npx playwright test --headed
  ```

- **Run tests with Playwright Interactive UI Mode**:
  ```powershell
  npm run test:e2e:ui
  # or
  npx playwright test --ui
  ```

- **Run a specific test specification**:
  ```powershell
  npx playwright test tests/01-auth-and-profile.spec.js
  npx playwright test tests/02-home-dashboard.spec.js
  npx playwright test tests/04-watch-room-playback.spec.js
  ```

- **Run tests on a specific browser**:
  ```powershell
  npx playwright test --project=chromium
  ```

- **View HTML Test Report**:
  ```powershell
  npm run test:e2e:report
  # or
  npx playwright show-report
  ```

---

## 4. Playwright Configuration (`playwright.config.js`)

The configuration is tuned for seamless integration with Django:
- **Base URL**: `http://127.0.0.1:8000`
- **Automatic Server Startup**: Uses Playwright's `webServer` option to launch `python manage.py runserver 127.0.0.1:8000 --noreload` automatically before test execution.
- **Artifacts on Failure**: Automatically captures screenshots, videos, and trace files (`trace: 'on-first-retry'`) when a test encounters an unexpected assertion failure.
