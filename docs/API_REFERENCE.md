# REST API & Real-Time Event Reference

This document provides the complete API specification for **Netflix Watch Spaces**. All endpoints use JSON payloads and enforce server-side validation and JWT authentication.

---

## 1. Authentication Endpoints

### 1.1 User Login
`POST /api/v1/auth/login`

Authenticates a registered user and returns a signed JWT token.

**Request:**
```json
{
  "email": "priya@netflix.com",
  "password": "password"
}
```

**Response `200 OK`:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "u_501",
    "email": "priya@netflix.com",
    "displayName": "Priya Raman",
    "role": "host",
    "avatarInitials": "PR",
    "subtitleLocale": "en-US"
  }
}
```

---

### 1.2 Switch Demo Persona
`POST /api/v1/auth/demo-switch`

Switches active persona to one of the seeded test personas (Priya [Host], Maya [Viewer], Dev [Viewer], Sofia [Viewer], Marcus [Viewer], Admin).

**Request:**
```json
{
  "userId": "u_maya"
}
```

**Response `200 OK`:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "u_maya",
    "displayName": "Maya",
    "role": "viewer",
    "avatarInitials": "MA"
  }
}
```

---

## 2. Watch Spaces (Rooms) Endpoints

### 2.1 Create Watch Space
`POST /api/v1/watch-spaces`

Creates a new Watch Space. Requires Host or registered user.

**Request:**
```json
{
  "titleId": "t_1001",
  "roomName": "Friday Noir Club",
  "maxParticipants": 15,
  "aiVerbosity": "normal",
  "votingEnabled": true,
  "privacy": "invite_only"
}
```

**Response `201 Created`:**
```json
{
  "watchSpaceId": "ws_88231",
  "inviteCode": "NX-4Q7K",
  "roomName": "Friday Noir Club",
  "titleId": "t_1001",
  "titleName": "The Salt Road",
  "status": "live",
  "hostUserId": "u_501",
  "maxParticipants": 15,
  "aiVerbosity": "normal",
  "votingEnabled": true,
  "privacy": "invite_only",
  "createdAt": "2026-11-21T20:12:00Z"
}
```

---

### 2.2 Get Watch Space Details
`GET /api/v1/watch-spaces/{id_or_code}`

Fetches authoritative playback status, participants list, and recent chat history.

**Response `200 OK`:**
```json
{
  "id": "ws_88231",
  "inviteCode": "NX-4Q7K",
  "roomName": "Friday Noir Club",
  "status": "live",
  "title": {
    "id": "t_1001",
    "name": "The Salt Road",
    "episodeInfo": "S1 · E4 \"The Crossing\"",
    "durationSeconds": 2730
  },
  "host": {
    "id": "u_501",
    "displayName": "Priya Raman",
    "avatarInitials": "PR"
  },
  "playback": {
    "currentPlaybackTs": 812.0,
    "currentPlaybackFormatted": "13:32",
    "isPlaying": true,
    "activeVariation": { "v_01": "b" }
  },
  "participantsCount": 5,
  "participants": [
    { "id": "u_501", "displayName": "Priya Raman", "role": "host", "driftMs": 24 },
    { "id": "u_maya", "displayName": "Maya", "role": "participant", "driftMs": 31 }
  ]
}
```

---

### 2.3 Join Room with Code
`POST /api/v1/watch-spaces/{code}/join`

Validates capacity and joins participant to the room.

**Response `200 OK`:**
```json
{
  "success": true,
  "watchSpaceId": "ws_88231",
  "inviteCode": "NX-4Q7K",
  "role": "participant",
  "playbackPosition": 812.0,
  "isPlaying": true,
  "driftToleranceMs": 250
}
```

---

### 2.4 Update Authoritative Playback
`POST /api/v1/watch-spaces/{id}/playback`

Updates play/pause state or seeks to timestamp. Enforces Host RBAC.

**Request:**
```json
{
  "state": "play",
  "positionSeconds": 812.0
}
```

**Response `200 OK` (when Host):**
```json
{
  "success": true,
  "state": "play",
  "positionSeconds": 812.0,
  "isPlaying": true,
  "issuedBy": "u_501"
}
```

**Response `403 Forbidden` (when Non-Host):**
```json
{
  "success": false,
  "error": "Forbidden: Only the room host can update playback state."
}
```

---

### 2.5 Participant Drift Sync Heartbeat
`POST /api/v1/watch-spaces/{id}/sync`

Reports local playback timestamp and calculates drift deviation.

**Request:**
```json
{
  "clientTs": 812.035,
  "rttMs": 30.0
}
```

**Response `200 OK`:**
```json
{
  "roomTs": 812.0,
  "isPlaying": true,
  "drift": {
    "drift_ms": 20,
    "abs_drift_ms": 20,
    "status": "in_sync",
    "action": "maintain",
    "target_playback_rate": 1.0,
    "target_position_sec": 812.015
  }
}
```

---

## 3. AI Co-Pilot & Content Engine Endpoints

### 3.1 Grounded Q&A
`POST /api/v1/watch-spaces/{id}/ai/ask`

Submits natural-language inquiry to the AI Co-Pilot for the current scene.

**Request:**
```json
{
  "question": "Who is the woman with the red thread?",
  "currentTs": 812
}
```

**Response `200 OK`:**
```json
{
  "answer": "That's Ilse, the courier. The red thread is her continuity marker — it appears in the opening and again at 00:09:14, which is how Rios recognises her later.",
  "sourceEvents": ["evt_2291", "evt_2344"],
  "isGrounded": true,
  "latencyMs": 1400,
  "generatedAt": "2026-11-21T20:13:34Z"
}
```

---

### 3.2 Real-Time Scene Context
`GET /api/v1/watch-spaces/{id}/ai/context?ts=812`

Returns current scene metadata, characters on-screen, location, and suggested prompt chips.

**Response `200 OK`:**
```json
{
  "timestamp": 812,
  "timestamp_formatted": "13:32",
  "scene_title": "The crossing — Ilse leaves the marked route",
  "location": "Salar de Uyuni · night exterior",
  "on_screen": "Ilse, Detective Rios",
  "glossary": "\"The Salt Road\" — smuggling route across the salar",
  "prompt_chips": [
    "Who is Detective Rios?",
    "Where was this filmed?",
    "What just happened?",
    "What does 'The Salt Road' mean?"
  ]
}
```

---

### 3.3 Variation Voting
`POST /api/v1/watch-spaces/{id}/ai/variation/vote`

Supports opening a vote, voting for an option, and closing the vote.

**Cast Vote Request:**
```json
{
  "action": "vote",
  "optionId": "b"
}
```

**Response `200 OK`:**
```json
{
  "variationId": "v_01",
  "status": "open",
  "options": [
    { "id": "a", "label": "\"We're not lost. We're just early.\"", "votes": 2, "percentage": 40 },
    { "id": "b", "label": "\"We're not lost. We're ahead of schedule.\"", "votes": 3, "percentage": 60 }
  ]
}
```

---

## 4. Content Studio & Admin Endpoints

### 4.1 Validate Timeline Schema v1.2
`POST /api/v1/titles/{id}/timeline/validate`

Validates timeline JSON/YAML against Schema v1.2.

**Malformed Request Response `400 Bad Request`:**
```json
{
  "valid": false,
  "errorsCount": 3,
  "errors": [
    "events[7].type must be one of: trivia, character, variationPoint, glossary.",
    "Missing required field ts at events[12].",
    "variationPoint v_02 has no approved options attached."
  ]
}
```

**Valid Request Response `200 OK`:**
```json
{
  "valid": true,
  "message": "Schema valid",
  "details": [
    "✓ 42 events parsed across 4 types.",
    "✓ All timestamps fall within the 45:30 runtime.",
    "✓ 3 variation points reference approved asset variants."
  ]
}
```

---

### 4.2 Publish Timeline Schema
`POST /api/v1/titles/{id}/timeline/publish`

Admin-only endpoint to persist validated timeline to SQL database. Non-admin tokens are rejected with `403 Forbidden`.

---

## 5. Direct Netflix Ingestion Endpoints

### 5.1 Search & Fetch Metadata Directly from Netflix
`POST /api/v1/titles/import/netflix/search`

Searches or extracts real title metadata from Netflix by title name, Netflix URL (`https://www.netflix.com/title/80057281`), or numeric ID.

**Request:**
```json
{
  "query": "Stranger Things"
}
```
*or by Netflix URL:*
```json
{
  "url": "https://www.netflix.com/title/80057281"
}
```

**Response `200 OK`:**
```json
{
  "results": [
    {
      "id": "t_stranger_things",
      "netflix_id": "80057281",
      "name": "Stranger Things",
      "episode_info": "S4 · E1 \"Chapter One: The Hellfire Club\"",
      "duration_seconds": 4560,
      "synopsis": "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
      "genres": ["Sci-Fi", "Horror", "Drama", "Mystery"],
      "match_percentage": 98,
      "rating_tag": "TV-MA",
      "year": 2024,
      "poster_url": "https://images.unsplash.com/...",
      "direct_url": "https://www.netflix.com/title/80057281",
      "events": [
        { "ts": 90, "type": "glossary", "content": "\"The Upside Down\" — an alternate dimension..." },
        { "ts": 210, "type": "character", "character_name": "Eleven", "content": "Eleven displays telekinetic resonance..." },
        { "ts": 480, "type": "trivia", "content": "The Duffer Brothers used vintage Leica lenses..." }
      ]
    }
  ]
}
```

---

### 5.2 Confirm & Persist Netflix Title into SQL Database
`POST /api/v1/titles/import/netflix/confirm`

Saves the fetched Netflix title to the `spaces_title` table and auto-generates the initial AI Co-Pilot timeline events (`spaces_timelineevent` and `spaces_variationoption`).

**Response `201 Created`:**
```json
{
  "success": true,
  "message": "Successfully imported 'Stranger Things' directly from Netflix with 7 AI Co-Pilot timeline events!",
  "title": {
    "id": "t_stranger_things",
    "name": "Stranger Things",
    "episodeInfo": "S4 · E1 \"Chapter One: The Hellfire Club\"",
    "durationSeconds": 4560,
    "eventsCount": 7
  }
}
```

