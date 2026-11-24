import time
import json
from django.test import TestCase, Client
from django.utils import timezone
from .models import (
    WatchUser, Title, TimelineEvent, VariationOption,
    WatchSpace, WatchSpaceParticipant, ChatMessage,
    Interaction, SessionAnalytics
)
from .services.copilot import CoPilotEngine
from .services.sync_engine import SyncEngine
from .services.recommendations import RecommendationEngine
from .services.timeline_validator import validate_timeline_payload, SCHEMA_V1_2
from .auth_utils import generate_jwt_token


class NetflixWatchSpacesTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Users
        self.host_user = WatchUser.objects.create(
            id="u_test_host",
            email="priya.test@netflix.com",
            display_name="Priya Raman",
            role="host",
            avatar_initials="PR"
        )
        self.host_user.set_password("password")
        self.host_user.save()
        self.host_token = generate_jwt_token(self.host_user)

        self.viewer_user = WatchUser.objects.create(
            id="u_test_viewer",
            email="maya.test@example.com",
            display_name="Maya",
            role="viewer",
            avatar_initials="MA"
        )
        self.viewer_user.set_password("password")
        self.viewer_user.save()
        self.viewer_token = generate_jwt_token(self.viewer_user)

        self.admin_user = WatchUser.objects.create(
            id="u_test_admin",
            email="admin.test@netflix.com",
            display_name="Studio Admin",
            role="admin",
            avatar_initials="AD"
        )
        self.admin_user.set_password("password")
        self.admin_user.save()
        self.admin_token = generate_jwt_token(self.admin_user)

        # Title
        self.title = Title.objects.create(
            id="t_test_1001",
            name="The Salt Road",
            episode_info='S1 · E4 "The Crossing"',
            duration_seconds=2730,
            synopsis="A courier crosses a country of salt.",
            genres=["Thriller", "Neo-Noir", "Crime"],
            match_percentage=97
        )

        # Timeline Events
        self.evt_rios = TimelineEvent.objects.create(
            id="evt_2291",
            title=self.title,
            ts_seconds=252,
            event_type="character",
            content="Detective Rios appears on the platform",
            source_id="evt_2291",
            character_name="Detective Rios"
        )

        self.evt_ilse = TimelineEvent.objects.create(
            id="evt_2344",
            title=self.title,
            ts_seconds=554,
            event_type="character",
            content="Ilse's red thread reappears in the mirror shot",
            source_id="evt_2344",
            character_name="Ilse"
        )

        self.evt_trivia = TimelineEvent.objects.create(
            id="evt_3118",
            title=self.title,
            ts_seconds=812,
            event_type="trivia",
            content="The crossing sequence was filmed on the Salar de Uyuni over four nights — one car, no CGI.",
            source_id="evt_3118"
        )

        self.evt_variation = TimelineEvent.objects.create(
            id="evt_3510",
            title=self.title,
            ts_seconds=1324,
            event_type="variation_point",
            content="Subtitle variation v_01",
            source_id="evt_3510"
        )

        VariationOption.objects.create(
            timeline_event=self.evt_variation,
            variation_id="v_01",
            option_key="a",
            label="We're not lost. We're just early."
        )
        VariationOption.objects.create(
            timeline_event=self.evt_variation,
            variation_id="v_01",
            option_key="b",
            label="We're not lost. We're ahead of schedule."
        )

        # Room
        self.room = WatchSpace.objects.create(
            id="ws_test_88231",
            invite_code="NX-TEST",
            title=self.title,
            host=self.host_user,
            room_name="Friday Noir Club",
            status="live",
            max_participants=15,
            current_playback_ts=812.0,
            is_playing=True
        )

        WatchSpaceParticipant.objects.create(
            watch_space=self.room,
            user=self.host_user,
            role="host",
            drift_ms=24
        )

        WatchSpaceParticipant.objects.create(
            watch_space=self.room,
            user=self.viewer_user,
            role="participant",
            drift_ms=31
        )

        # Seed Interactions
        Interaction.objects.create(
            user=self.host_user,
            title=self.title,
            watched_seconds=2730,
            completed=True,
            rating=5,
            co_watched_with=[self.viewer_user.id]
        )

    # ----------------------------------------------------------------------
    # 1. Playback State Machine & Synchronization Tests
    # ----------------------------------------------------------------------

    def test_host_can_update_playback(self):
        """Authoritative playback state machine: Host play/pause/seek succeeds."""
        res = SyncEngine.update_playback_state(self.room, self.host_user, 'pause', 820.0)
        self.assertTrue(res['success'])
        self.assertEqual(res['state'], 'pause')
        self.assertEqual(res['positionSeconds'], 820.0)

        self.room.refresh_from_db()
        self.assertFalse(self.room.is_playing)
        self.assertEqual(self.room.current_playback_ts, 820.0)

    def test_viewer_cannot_update_authoritative_playback(self):
        """Server-side RBAC: Non-host is rejected from altering playback clock."""
        res = SyncEngine.update_playback_state(self.room, self.viewer_user, 'pause', 900.0)
        self.assertFalse(res['success'])
        self.assertIn("Forbidden", res['error'])

    def test_client_drift_calculation_within_kpi(self):
        """Playback Sync Drift: must calculate drift and micro-adjustments < 250ms target."""
        # 40ms drift
        report = SyncEngine.calculate_drift(812.0, 812.040, rtt_ms=30.0)
        self.assertLess(report['abs_drift_ms'], 250)
        self.assertEqual(report['status'], 'in_sync')

        # 180ms drift -> micro rate adjust
        report_mid = SyncEngine.calculate_drift(812.0, 812.180, rtt_ms=30.0)
        self.assertEqual(report_mid['action'], 'micro_rate_adjust')

        # 400ms drift -> micro seek
        report_desync = SyncEngine.calculate_drift(812.0, 812.400, rtt_ms=30.0)
        self.assertEqual(report_desync['action'], 'micro_seek')

    def test_host_failover_and_promotion(self):
        """Host drop triggers auto-promotion candidate detection."""
        failover = SyncEngine.handle_host_offline(self.room)
        self.assertEqual(failover['event'], 'room.host.dropped')
        self.assertEqual(failover['candidateName'], 'Maya')

        promo_res = SyncEngine.promote_participant_to_host(self.room, self.viewer_user)
        self.assertTrue(promo_res['success'])
        self.room.refresh_from_db()
        self.assertEqual(self.room.host.id, self.viewer_user.id)

    # ----------------------------------------------------------------------
    # 2. AI Content Engine & RAG Grounding Tests
    # ----------------------------------------------------------------------

    def test_ai_copilot_grounded_answer_and_sources(self):
        """Grounded Q&A cites exact source events and answers accurately."""
        start = time.time()
        res = CoPilotEngine.ask_copilot(self.title, 812, "Who is the woman with the red thread?")
        duration_sec = time.time() - start

        self.assertTrue(res['isGrounded'])
        self.assertIn("Ilse", res['answer'])
        self.assertIn("evt_2291", res['sourceEvents'])
        self.assertIn("evt_2344", res['sourceEvents'])
        # KPI: Latency < 3.0 seconds
        self.assertLess(duration_sec, 3.0)

    def test_ai_copilot_location_trivia(self):
        """AI surfaces filmed location trivia with citation."""
        res = CoPilotEngine.ask_copilot(self.title, 812, "Where was this filmed?")
        self.assertTrue(res['isGrounded'])
        self.assertIn("Salar de Uyuni", res['answer'])
        self.assertIn("evt_3118", res['sourceEvents'])

    def test_timeline_trivia_trigger_at_timestamp(self):
        """Trivia card appears when crossing authored marker timestamp."""
        card = CoPilotEngine.get_trivia_card(self.title, 812, tolerance_sec=2)
        self.assertIsNotNone(card)
        self.assertEqual(card['eventId'], 'evt_3118')
        self.assertIn("Salar de Uyuni", card['content'])

    # ----------------------------------------------------------------------
    # 3. Timeline Schema v1.2 Validator Tests
    # ----------------------------------------------------------------------

    def test_timeline_validator_valid_schema(self):
        """Schema v1.2 accepts valid metadata payload."""
        valid_payload = {
            "titleId": "t_test_1001",
            "durationSeconds": 2730,
            "version": "v1.2",
            "events": [
                {"ts": 812, "type": "trivia", "content": "Sample trivia note.", "source_id": "evt_1"},
                {"ts": 1324, "type": "variationPoint", "variationId": "v_01", "content": "Alt lines",
                 "options": [{"id": "a", "label": "Option A"}, {"id": "b", "label": "Option B"}]}
            ]
        }
        is_valid, errors, summary = validate_timeline_payload(valid_payload, 2730)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
        self.assertEqual(summary['total_events'], 2)

    def test_timeline_validator_rejects_malformed_with_field_errors(self):
        """Schema v1.2 rejects malformed uploads matching Screenshot 2 errors."""
        malformed_payload = {
            "titleId": "t_test_1001",
            "durationSeconds": 2730,
            "events": [
                {"ts": 10, "type": "trivia", "content": "Valid event 0"},
                {"ts": 20, "type": "trivia", "content": "Valid event 1"},
                {"ts": 30, "type": "trivia", "content": "Valid event 2"},
                {"ts": 40, "type": "trivia", "content": "Valid event 3"},
                {"ts": 50, "type": "trivia", "content": "Valid event 4"},
                {"ts": 60, "type": "trivia", "content": "Valid event 5"},
                {"ts": 70, "type": "trivia", "content": "Valid event 6"},
                {"ts": 80, "type": "invalid_type", "content": "Event 7 with invalid type"},
                {"ts": 90, "type": "trivia", "content": "Valid event 8"},
                {"ts": 100, "type": "trivia", "content": "Valid event 9"},
                {"ts": 110, "type": "trivia", "content": "Valid event 10"},
                {"ts": 120, "type": "trivia", "content": "Valid event 11"},
                {"type": "trivia", "content": "Missing ts at event 12"},
                {"ts": 140, "type": "variationPoint", "variationId": "v_02", "content": "No options", "options": []}
            ]
        }
        is_valid, errors, summary = validate_timeline_payload(malformed_payload, 2730)
        self.assertFalse(is_valid)
        self.assertGreaterEqual(len(errors), 3)

        # Check field-level error messages
        type_err = any("events[7].type must be one of" in err for err in errors)
        ts_err = any("Missing required field ts at events[12]" in err for err in errors)
        var_err = any("variationPoint v_02 has no approved options attached" in err for err in errors)

        self.assertTrue(type_err, "Should flag events[7].type")
        self.assertTrue(ts_err, "Should flag missing ts at events[12]")
        self.assertTrue(var_err, "Should flag variationPoint v_02")

    # ----------------------------------------------------------------------
    # 4. Recommendation Engine & Precision@5 Tests
    # ----------------------------------------------------------------------

    def test_recommendation_precision_at_5(self):
        """Precision@5 metric meets PRD target (>= 0.60)."""
        precision = RecommendationEngine.evaluate_precision_at_k(self.host_user, k=5)
        self.assertGreaterEqual(precision, 0.60)

    def test_recommendation_ranking_returns_rail(self):
        """Recommendation rail generates ranked titles with match percentage."""
        recs = RecommendationEngine.get_recommendations_for_user(self.host_user, limit=5)
        self.assertGreaterEqual(len(recs), 1)
        self.assertIn("match_percentage", recs[0])
        self.assertGreaterEqual(recs[0]["match_percentage"], 75)

    # ----------------------------------------------------------------------
    # 5. REST API & Server-Side RBAC Enforcement Tests
    # ----------------------------------------------------------------------

    def test_admin_rbac_enforcement(self):
        """Viewer role rejected from publishing timeline schema (403 Forbidden)."""
        url = f"/api/v1/titles/{self.title.id}/timeline/publish"
        payload = {"titleId": self.title.id, "durationSeconds": 2730, "events": []}

        # Request with viewer token
        res_viewer = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.viewer_token}"
        )
        self.assertEqual(res_viewer.status_code, 403)
        self.assertIn("Forbidden", res_viewer.json()['error'])

        # Request with admin token
        res_admin = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.admin_token}"
        )
        self.assertEqual(res_admin.status_code, 200)

    def test_host_moderation_rbac_enforcement(self):
        """Non-host cannot mute or remove participants."""
        url = f"/api/v1/watch-spaces/{self.room.id}/moderate"
        payload = {"action": "mute", "targetUserId": self.viewer_user.id}

        res_viewer = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.viewer_token}"
        )
        self.assertEqual(res_viewer.status_code, 403)

        res_host = self.client.post(
            url,
            data=json.dumps(payload),
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.host_token}"
        )
        self.assertEqual(res_host.status_code, 200)

    def test_api_latency_under_target(self):
        """API latency for non-AI endpoints satisfies < 200ms target."""
        start = time.time()
        res = self.client.get('/api/v1/dashboard')
        latency_ms = (time.time() - start) * 1000.0

        self.assertEqual(res.status_code, 200)
        self.assertLess(latency_ms, 200.0)

    # ----------------------------------------------------------------------
    # 6. Direct Netflix Ingestion Tests
    # ----------------------------------------------------------------------

    def test_netflix_direct_search(self):
        """Direct Netflix Search: finds real title by name and by URL."""
        # By title name
        res_name = self.client.post(
            '/api/v1/titles/import/netflix/search',
            data=json.dumps({'query': 'Stranger Things'}),
            content_type='application/json'
        )
        self.assertEqual(res_name.status_code, 200)
        results = res_name.json()['results']
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Stranger Things')
        self.assertEqual(results[0]['netflix_id'], '80057281')

        # By Netflix URL
        res_url = self.client.post(
            '/api/v1/titles/import/netflix/search',
            data=json.dumps({'url': 'https://www.netflix.com/title/81040344'}),
            content_type='application/json'
        )
        self.assertEqual(res_url.status_code, 200)
        results_url = res_url.json()['results']
        self.assertEqual(results_url[0]['name'], 'Squid Game')

    def test_netflix_direct_import_creates_title_and_timeline(self):
        """Direct Netflix Ingestion: imports title and auto-generates AI Co-Pilot timeline."""
        search_res = self.client.post(
            '/api/v1/titles/import/netflix/search',
            data=json.dumps({'query': 'Wednesday'}),
            content_type='application/json'
        )
        wednesday_data = search_res.json()['results'][0]

        confirm_res = self.client.post(
            '/api/v1/titles/import/netflix/confirm',
            data=json.dumps(wednesday_data),
            content_type='application/json'
        )
        self.assertEqual(confirm_res.status_code, 201)
        imported = confirm_res.json()['title']
        self.assertEqual(imported['name'], 'Wednesday')

        # Verify SQL persistence
        title_db = Title.objects.get(id=imported['id'])
        self.assertEqual(title_db.name, 'Wednesday')
        self.assertGreaterEqual(title_db.timeline_events.count(), 3)

