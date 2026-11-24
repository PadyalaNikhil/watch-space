import json
from django.core.management.base import BaseCommand
from django.utils import timezone
from spaces.models import (
    WatchUser, Title, TimelineEvent, VariationOption,
    WatchSpace, WatchSpaceParticipant, ChatMessage,
    Interaction, SessionAnalytics
)


class Command(BaseCommand):
    help = 'Seeds database with realistic data matching Netflix Watch Spaces UI & PRD'

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding Netflix Watch Spaces database...")

        # 1. Users
        users_info = [
            {
                "id": "u_501",
                "email": "priya@netflix.com",
                "display_name": "Priya Raman",
                "role": "host",
                "avatar_initials": "PR",
                "avatar_color": "#E50914"
            },
            {
                "id": "u_maya",
                "email": "maya@example.com",
                "display_name": "Maya",
                "role": "viewer",
                "avatar_initials": "MA",
                "avatar_color": "#EAB308"
            },
            {
                "id": "u_dev",
                "email": "dev@example.com",
                "display_name": "Dev",
                "role": "viewer",
                "avatar_initials": "DV",
                "avatar_color": "#3B82F6"
            },
            {
                "id": "u_sofia",
                "email": "sofia@example.com",
                "display_name": "Sofia",
                "role": "viewer",
                "avatar_initials": "SO",
                "avatar_color": "#EC4899"
            },
            {
                "id": "u_marcus",
                "email": "marcus@example.com",
                "display_name": "Marcus",
                "role": "viewer",
                "avatar_initials": "MC",
                "avatar_color": "#10B981"
            },
            {
                "id": "u_admin",
                "email": "admin@netflix.com",
                "display_name": "Studio Admin",
                "role": "admin",
                "avatar_initials": "AD",
                "avatar_color": "#8B5CF6"
            }
        ]

        users = {}
        for u in users_info:
            user, _ = WatchUser.objects.update_or_create(
                id=u["id"],
                defaults={
                    "email": u["email"],
                    "display_name": u["display_name"],
                    "role": u["role"],
                    "avatar_initials": u["avatar_initials"],
                    "avatar_color": u["avatar_color"]
                }
            )
            user.set_password("password")
            user.save()
            users[u["id"]] = user

        # 2. Titles
        titles_info = [
            {
                "id": "t_stranger_things",
                "name": "Stranger Things",
                "episode_info": 'S4 · E1 "Chapter One: The Hellfire Club"',
                "duration_seconds": 4560,  # 1h 16m
                "synopsis": "When a young boy vanishes, a small town uncovers a mystery involving secret experiments, terrifying supernatural forces and one strange little girl.",
                "genres": ["Sci-Fi", "Horror", "Drama", "Mystery"],
                "match_percentage": 98,
                "rating_tag": "TV-MA",
                "year": 2024,
                "episodes_count": 9,
                "resolution_badge": "4K Ultra HD",
                "poster_url": "/static/images/poster-stranger-things.svg",
                "backdrop_url": "/static/images/backdrop-stranger-things.svg"
            },
            {
                "id": "t_jailer",
                "name": "Jailer",
                "episode_info": "Feature Film",
                "duration_seconds": 10080,  # 2h 48m
                "synopsis": "A retired prison warden goes on a ruthless manhunt when an eccentric antique idol smuggler kidnaps his son, unlocking a ferocious past his family never imagined.",
                "genres": ["Action", "Crime", "Thriller", "Indian"],
                "match_percentage": 98,
                "rating_tag": "TV-MA",
                "year": 2023,
                "episodes_count": 1,
                "resolution_badge": "4K Ultra HD",
                "poster_url": "/static/images/poster-jailer.svg",
                "backdrop_url": "/static/images/backdrop-jailer.svg"
            },
            {
                "id": "t_squid_game",
                "name": "Squid Game",
                "episode_info": 'S2 · E1 "Red Light, Green Light 2.0"',
                "duration_seconds": 3600,  # 60m
                "synopsis": "Hundreds of cash-strapped players accept a strange invitation to compete in children's games. Inside, a tempting prize awaits with deadly high stakes.",
                "genres": ["Thriller", "Suspense", "Drama", "Korean"],
                "match_percentage": 99,
                "rating_tag": "TV-MA",
                "year": 2025,
                "episodes_count": 6,
                "resolution_badge": "4K HDR",
                "poster_url": "/static/images/poster-squid-game.svg",
                "backdrop_url": "/static/images/backdrop-squid-game.svg"
            },
            {
                "id": "t_wednesday",
                "name": "Wednesday",
                "episode_info": 'S2 · E1 "Here We Woe Again"',
                "duration_seconds": 3120,  # 52m
                "synopsis": "Smart, sarcastic and a little dead inside, Wednesday Addams investigates a murder spree while making new friends — and foes — at Nevermore Academy.",
                "genres": ["Fantasy", "Comedy", "Mystery", "Teen"],
                "match_percentage": 96,
                "rating_tag": "TV-14",
                "year": 2025,
                "episodes_count": 8,
                "resolution_badge": "4K Ultra HD",
                "poster_url": "/static/images/poster-wednesday.svg",
                "backdrop_url": "/static/images/backdrop-wednesday.svg"
            },
            {
                "id": "t_money_heist",
                "name": "Money Heist",
                "episode_info": 'Part 5 · E1 "The End of the Road"',
                "duration_seconds": 2880,
                "synopsis": "Eight thieves take hostages and lock themselves in the Royal Mint of Spain as a criminal mastermind manipulates the police to carry out his plan.",
                "genres": ["Crime", "Thriller", "Action", "Spanish"],
                "match_percentage": 97,
                "rating_tag": "TV-MA",
                "year": 2021,
                "episodes_count": 13,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-money-heist.svg",
                "backdrop_url": "/static/images/backdrop-money-heist.svg"
            },
            {
                "id": "t_queens_gambit",
                "name": "The Queen's Gambit",
                "episode_info": 'Limited Series · E1 "Openings"',
                "duration_seconds": 3360,
                "synopsis": "Orphaned at the tender age of nine, prodigious introvert Beth Harmon discovers and masters the game of chess in 1960s USA.",
                "genres": ["Drama", "Cerebral", "Period Piece"],
                "match_percentage": 95,
                "rating_tag": "TV-MA",
                "year": 2020,
                "episodes_count": 7,
                "resolution_badge": "4K HDR",
                "poster_url": "/static/images/poster-queens-gambit.svg",
                "backdrop_url": "/static/images/backdrop-queens-gambit.svg"
            },
            {
                "id": "t_dark",
                "name": "Dark",
                "episode_info": 'S3 · E1 "Deja-vu"',
                "duration_seconds": 3180,
                "synopsis": "A missing child sets four families on a frantic hunt for answers as they unearth a mind-bending mystery that spans three generations.",
                "genres": ["Sci-Fi", "Mystery", "Crime", "German"],
                "match_percentage": 96,
                "rating_tag": "TV-MA",
                "year": 2020,
                "episodes_count": 10,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-dark.svg",
                "backdrop_url": "/static/images/backdrop-dark.svg"
            },
            {
                "id": "t_1001",
                "name": "The Salt Road",
                "episode_info": 'S1 · E4 "The Crossing"',
                "duration_seconds": 2730,  # 45m 30s
                "synopsis": "A courier with a memory she can't trust crosses a country of salt and silence to deliver a package that should not exist.",
                "genres": ["Thriller", "Neo-Noir", "Crime"],
                "match_percentage": 97,
                "rating_tag": "TV-MA",
                "year": 2026,
                "episodes_count": 6,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-salt-road.jpg",
                "backdrop_url": "/static/images/salt-road-backdrop.jpg"
            },
            {
                "id": "t_1002",
                "name": "Vela",
                "episode_info": 'S1 · E1 "Drift"',
                "duration_seconds": 6420,
                "synopsis": "A solo deep-space salvage operative encounters an uncharted automated freighter transmitting a signal in a forgotten frequency.",
                "genres": ["Sci-Fi", "Space", "Drama"],
                "match_percentage": 94,
                "rating_tag": "TV-14",
                "year": 2025,
                "episodes_count": 8,
                "resolution_badge": "4K HDR",
                "poster_url": "/static/images/poster-vela.jpg",
                "backdrop_url": "/static/images/poster-vela.jpg"
            },
            {
                "id": "t_1003",
                "name": "Midnight Cartography",
                "episode_info": 'S1 · E2 "Unlisted"',
                "duration_seconds": 3180,
                "synopsis": "In a rain-drenched coastal metropolis, an underground archivist maps secret sub-levels erased from city registry maps.",
                "genres": ["Neo-Noir", "Mystery", "Crime"],
                "match_percentage": 91,
                "rating_tag": "TV-MA",
                "year": 2026,
                "episodes_count": 10,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-midnight.jpg",
                "backdrop_url": "/static/images/poster-midnight.jpg"
            },
            {
                "id": "t_1004",
                "name": "Paper Tigers",
                "episode_info": "Feature Film",
                "duration_seconds": 7080,
                "synopsis": "High-stakes corporate espionage unfolds across Tokyo and Zurich as whistleblowers race against financial algorithms.",
                "genres": ["Drama", "Corporate", "Thriller"],
                "match_percentage": 88,
                "rating_tag": "R",
                "year": 2024,
                "episodes_count": 1,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-paper-tigers.jpg",
                "backdrop_url": "/static/images/poster-paper-tigers.jpg"
            },
            {
                "id": "t_1005",
                "name": "Northwind",
                "episode_info": 'Limited Series · S1',
                "duration_seconds": 3420,
                "synopsis": "A remote lighthouse off the northern Norwegian coast turns into an isolated fortress when an anomalous storm cuts off maritime radar.",
                "genres": ["Limited Series", "Mystery", "Nordic Noir"],
                "match_percentage": 86,
                "rating_tag": "TV-MA",
                "year": 2025,
                "episodes_count": 5,
                "resolution_badge": "4K",
                "poster_url": "/static/images/poster-northwind.jpg",
                "backdrop_url": "/static/images/poster-northwind.jpg"
            }
        ]

        titles = {}
        for t in titles_info:
            title, _ = Title.objects.update_or_create(
                id=t["id"],
                defaults=t
            )
            titles[t["id"]] = title

        # 3. 42 Timeline Events for "The Salt Road" matching the exact numbers in the screenshot:
        # Trivia: 15, Characters: 9, Variations: 3, Glossary: 12 = 42 total!
        salt_road = titles["t_1001"]
        salt_road.timeline_events.all().delete()

        raw_events = [
            # Glossary (15)
            {"ts": 160, "type": "glossary", "content": '"The Salt Road" — a smuggling route across the salar', "id": "evt_2276"},
            {"ts": 310, "type": "glossary", "content": '"Waypoints" — GPS dead-reckoning stakes placed during drought season', "id": "evt_2288"},
            {"ts": 520, "type": "glossary", "content": '"White Out" — blinding optical reflection on salt during sunrise', "id": "evt_2320"},
            {"ts": 920, "type": "glossary", "content": '"Salar" — a salt flat formed by evaporated lakes', "id": "evt_2491"},
            {"ts": 1180, "type": "glossary", "content": '"Lithium Vein" — mineral deposits causing compass anomalies', "id": "evt_2550"},
            {"ts": 1420, "type": "glossary", "content": '"Dead Frequency" — radio blackout zone along the tectonic ridge', "id": "evt_2610"},
            {"ts": 1690, "type": "glossary", "content": '"Courier Seal" — tamper-evident biometric clasp on the cargo', "id": "evt_2700"},
            {"ts": 1950, "type": "glossary", "content": '"Mirage Line" — heat distortion masking vehicle silhouettes', "id": "evt_2810"},
            {"ts": 2180, "type": "glossary", "content": '"Thermal Sink" — nighttime sub-zero ground drop in the basin', "id": "evt_2900"},
            {"ts": 2340, "type": "glossary", "content": '"Ghost Crossing" — unofficial border line surveyed in 1912', "id": "evt_2950"},
            {"ts": 2510, "type": "glossary", "content": '"Telemetry Ping" — encrypted beacon pulse sent every 10 minutes', "id": "evt_3010"},
            {"ts": 2600, "type": "glossary", "content": '"Brine Trench" — submerged drainage furrow hidden under salt crust', "id": "evt_3050"},
            {"ts": 2650, "type": "glossary", "content": '"Sub-Surface Density" — soil hardness measured by acoustic ground probes', "id": "evt_3070"},
            {"ts": 2680, "type": "glossary", "content": '"Extraction Point Alpha" — abandoned railway water tank depot', "id": "evt_3080"},
            {"ts": 2715, "type": "glossary", "content": '"Border Beacon" — radio azimuth beacon marking federal territory', "id": "evt_3095"},

            # Characters (9)
            {"ts": 252, "type": "character", "character_name": "Detective Rios", "content": "Detective Rios appears on the platform", "id": "evt_2291"},
            {"ts": 554, "type": "character", "character_name": "Ilse", "content": "Ilse's red thread reappears in the mirror shot", "id": "evt_2344"},
            {"ts": 718, "type": "character", "character_name": "Ilse", "content": "Tracking signal drops as Ilse leaves the marked route", "id": "evt_2482"},
            {"ts": 1050, "type": "character", "character_name": "Detective Rios", "content": "Rios cross-checks satellite thermal trails with border patrol", "id": "evt_2580"},
            {"ts": 1280, "type": "character", "character_name": "The Broker", "content": "The Broker answers from a satellite uplink in Santiago", "id": "evt_2650"},
            {"ts": 1540, "type": "character", "character_name": "Ilse", "content": "Ilse cuts off the auxiliary fuel pump to conserve battery", "id": "evt_2750"},
            {"ts": 1820, "type": "character", "character_name": "Detective Rios", "content": "Rios reaches the edge of the paved highway looking into the flats", "id": "evt_2850"},
            {"ts": 2100, "type": "character", "character_name": "Ilse", "content": "Ilse unholsters the flare pistol as headlights appear behind", "id": "evt_2930"},
            {"ts": 2420, "type": "character", "character_name": "Unknown Driver", "content": "Unidentified chase vehicle matches Rios's department issue", "id": "evt_2990"},

            # Trivia (15)
            {"ts": 75, "type": "trivia", "content": "Opening shot establishes the unmarked desert corridor in Bolivia.", "id": "evt_2210"},
            {"ts": 365, "type": "trivia", "content": "The red thread bracelet was improvised by the actor during rehearsal.", "id": "evt_3114"},
            {"ts": 610, "type": "trivia", "content": "The director used anamorphic lenses to emphasize isolation on the salt flat.", "id": "evt_3115"},
            {"ts": 812, "type": "trivia", "content": "The crossing sequence was filmed on the Salar de Uyuni over four nights — one car, no CGI.", "id": "evt_3118"},
            {"ts": 980, "type": "trivia", "content": "Ambient sound was captured using binaural hydrophones placed directly in brine pools.", "id": "evt_3122"},
            {"ts": 1120, "type": "trivia", "content": "The actor drove the stunt sedan herself during all high-speed drift sequences.", "id": "evt_3125"},
            {"ts": 1350, "type": "trivia", "content": "Lighting was provided exclusively by helium balloon lights suspended from cranes.", "id": "evt_3130"},
            {"ts": 1580, "type": "trivia", "content": "The temperature dropped to -14°C during this night shoot.", "id": "evt_3135"},
            {"ts": 1750, "type": "trivia", "content": "The cargo canister prop contains working mechanical counterweights.", "id": "evt_3140"},
            {"ts": 1900, "type": "trivia", "content": "The car sedan is the same vehicle used in the opening shot.", "id": "evt_3802"},
            {"ts": 2040, "type": "trivia", "content": "The camera crew wore specialized non-reflective white suits to avoid reflections on salt.", "id": "evt_3810"},
            {"ts": 2240, "type": "trivia", "content": "Composer utilized traditional Andean charango strings processed through modular synthesizers.", "id": "evt_3820"},
            {"ts": 2390, "type": "trivia", "content": "Over 200kg of edible salt had to be washed from the car undercarriage daily.", "id": "evt_3830"},
            {"ts": 2570, "type": "trivia", "content": "The sequence was shot chronologically to track real vehicle tire wear.", "id": "evt_3840"},
            {"ts": 2700, "type": "trivia", "content": "Final aerial frame was filmed at dawn from a stealth electric drone.", "id": "evt_3850"},

            # Variations (3)
            {
                "ts": 1324,  # 00:22:04
                "type": "variation_point",
                "variationId": "v_01",
                "content": "Subtitle variation v_01 · 2 pre-approved options",
                "id": "evt_3510",
                "options": [
                    {"id": "a", "label": '"We\'re not lost. We\'re just early."', "assetRef": "sub_v01_a"},
                    {"id": "b", "label": '"We\'re not lost. We\'re ahead of schedule."', "assetRef": "sub_v01_b"}
                ]
            },
            {
                "ts": 1840,
                "type": "variation_point",
                "variationId": "v_02",
                "content": "Narrative cut variation v_02 · Radio broadcast focus",
                "id": "evt_3520",
                "options": [
                    {"id": "a", "label": "Listen to weather frequency warning", "assetRef": "audio_alt_weather"},
                    {"id": "b", "label": "Listen to police emergency dispatch", "assetRef": "audio_alt_police"}
                ]
            },
            {
                "ts": 2450,
                "type": "variation_point",
                "variationId": "v_03",
                "content": "Lighting & color grading variant v_03 · Horizon tint",
                "id": "evt_3530",
                "options": [
                    {"id": "a", "label": "Cool indigo twilight grade", "assetRef": "lut_indigo"},
                    {"id": "b", "label": "Deep amber dawn grade", "assetRef": "lut_amber"}
                ]
            }
        ]

        created_count = 0
        for ev in raw_events:
            ev_obj = TimelineEvent.objects.create(
                id=ev["id"],
                title=salt_road,
                ts_seconds=ev["ts"],
                event_type=ev["type"],
                content=ev["content"],
                source_id=ev["id"],
                character_name=ev.get("character_name", ""),
                location="Salar de Uyuni · night exterior" if ev["ts"] > 500 else "Border Platform",
                payload=ev
            )
            created_count += 1

            if ev["type"] == "variation_point" and "options" in ev:
                for opt in ev["options"]:
                    VariationOption.objects.create(
                        timeline_event=ev_obj,
                        variation_id=ev["variationId"],
                        option_key=opt["id"],
                        label=opt["label"],
                        asset_ref=opt.get("assetRef", "")
                    )

        self.stdout.write(f"Created {created_count} timeline events for {salt_road.name}.")

        # 3b. Seed Timeline Events for real Netflix titles from NETFLIX_CATALOG_REPOSITORY
        from spaces.services.netflix_importer import NETFLIX_CATALOG_REPOSITORY
        for n_item in NETFLIX_CATALOG_REPOSITORY.values():
            t_obj = titles.get(n_item["id"])
            if not t_obj:
                continue
            t_obj.timeline_events.all().delete()
            for ev in n_item.get("events", []):
                ev_obj = TimelineEvent.objects.create(
                    id=ev["id"],
                    title=t_obj,
                    ts_seconds=ev["ts"],
                    event_type=ev["type"],
                    content=ev["content"],
                    source_id=ev["id"],
                    character_name=ev.get("character_name", ""),
                    location=n_item["name"],
                    payload=ev
                )
                if ev["type"] == "variation_point" and "options" in ev:
                    for opt in ev["options"]:
                        VariationOption.objects.create(
                            timeline_event=ev_obj,
                            variation_id=ev["variationId"],
                            option_key=opt["id"],
                            label=opt["label"],
                            asset_ref=opt.get("assetRef", "")
                        )

        # 4. Watch Space "Friday Noir Club" (NX-4Q7K)
        WatchSpace.objects.filter(id="ws_88231").delete()
        room = WatchSpace.objects.create(
            id="ws_88231",
            invite_code="NX-4Q7K",
            title=salt_road,
            host=users["u_501"],  # Priya
            room_name="Friday Noir Club",
            status="live",
            max_participants=15,
            ai_verbosity="normal",
            voting_enabled=True,
            privacy="invite_only",
            current_playback_ts=812.0,  # 00:13:32
            is_playing=True,
            active_variation={"v_01": "b"},
            active_vote={
                "variationId": "v_01",
                "timestamp": "00:22:04",
                "title": "Choose tonight's line.",
                "description": "Both options are pre-approved by the host. The winner is applied to all 5 viewers at the same timestamp — no desync.",
                "status": "closed",
                "options": [
                    {"id": "a", "label": '"We\'re not lost. We\'re just early."', "votes": 2, "percentage": 40},
                    {"id": "b", "label": '"We\'re not lost. We\'re ahead of schedule."', "votes": 3, "percentage": 60}
                ]
            }
        )

        # Participants: Priya (Host), Maya, Dev, Sofia, Marcus
        participants = [
            (users["u_501"], "host", "Excellent", 24),
            (users["u_maya"], "participant", "Excellent", 31),
            (users["u_dev"], "participant", "Good", 56),
            (users["u_sofia"], "participant", "Fair", 112),
            (users["u_marcus"], "participant", "Good", 54),
        ]
        for u, role, quality, drift in participants:
            WatchSpaceParticipant.objects.create(
                watch_space=room,
                user=u,
                role=role,
                connection_quality=quality,
                drift_ms=drift
            )

        # Chat messages matching Screenshot 10 & 11
        chat_script = [
            (None, "system", "Maya joined the room", 780),
            (users["u_maya"], "chat", "the salt flats at night. unreal.", 790),
            (None, "system", "Priya started playback for everyone · 00:13:32", 812),
            (users["u_dev"], "chat", "wait — is that the same car from the opening?", 812),
            (users["u_sofia"], "chat", "Who is the woman with the red thread?", 812),
            (None, "ai_answer", "That's Ilse, the courier. The red thread is her continuity marker — it appears in the opening and again at 00:09:14, which is how Rios recognises her later.", 812),
            (users["u_sofia"], "chat", "ok that answered it 😄", 812),
            (None, "system", "Trivia card surfaced · 00:13:32", 812),
            (None, "system", "Variation v_01 - option B applied to all 5 viewers", 812)
        ]

        for sender, m_type, body, ts in chat_script:
            source_events = ["evt_2291", "evt_2344"] if m_type == "ai_answer" else []
            ChatMessage.objects.create(
                watch_space=room,
                user=sender,
                msg_type=m_type,
                body=body,
                ts_seconds=ts,
                source_events=source_events,
                is_grounded=True if m_type == "ai_answer" else False,
                latency_ms=1400 if m_type == "ai_answer" else 0
            )

        # 5. Session Analytics
        SessionAnalytics.objects.update_or_create(
            watch_space=room,
            defaults={
                "watch_time_seconds": 6120,  # 1h 42m
                "peak_viewers": 8,
                "ai_questions_count": 23,
                "trivia_cards_count": 14,
                "chat_messages_count": 186,
                "sync_drift_avg_ms": 31,
                "sync_drift_peak_ms": 68,
                "variations_applied": [
                    {"label": "1 subtitle swap", "detail": "Option B applied"},
                    {"label": "1 group vote", "detail": "Tonight's line selected"}
                ],
                "top_ai_moments": [
                    {
                        "question": "Who is the woman with the red thread?",
                        "detail": "Grounded in Ilse's first appearance and the improvised bracelet trivia note.",
                        "sources": ["evt_2291", "evt_3114"],
                        "latency": "1.4s"
                    },
                    {
                        "question": "Where was the crossing filmed?",
                        "detail": "Surfaced the location trivia at 00:13:32 and cited the marker timestamp.",
                        "sources": ["evt_3118"],
                        "latency": "1.1s"
                    },
                    {
                        "question": "Is Rios the same detective from episode one?",
                        "detail": "Combined the character window with the glossary entry to confirm the identity.",
                        "sources": ["evt_2482"],
                        "latency": "1.3s"
                    }
                ],
                "chat_activity_distribution": [
                    {"time": "8:00", "volume": 12},
                    {"time": "8:20", "volume": 28},
                    {"time": "8:40", "volume": 65},
                    {"time": "9:00", "volume": 115, "peak": True},
                    {"time": "9:20", "volume": 42},
                    {"time": "9:40", "volume": 18}
                ]
            }
        )

        # 6. User Interactions for Hybrid Recommendation Model
        # Giving real Netflix blockbuster titles (Stranger Things, Jailer) top affinity for Priya and her circle
        interactions_data = [
            (users["u_501"], titles["t_stranger_things"], 4560, True, 5, ["u_maya", "u_dev", "u_sofia", "u_marcus"]),
            (users["u_501"], titles["t_jailer"], 10080, True, 5, ["u_maya", "u_dev", "u_marcus", "u_sofia"]),
            (users["u_501"], titles["t_squid_game"], 3600, True, 5, ["u_dev", "u_marcus"]),
            (users["u_501"], titles["t_wednesday"], 3120, True, 5, ["u_sofia", "u_maya"]),
            (users["u_501"], titles["t_money_heist"], 2880, True, 5, ["u_dev"]),
            (users["u_501"], titles["t_queens_gambit"], 3360, True, 5, ["u_maya"]),
            (users["u_501"], titles["t_dark"], 3180, True, 5, ["u_dev"]),
            (users["u_501"], titles["t_1001"], 2730, True, 5, ["u_maya", "u_dev"]),
            (users["u_maya"], titles["t_stranger_things"], 4560, True, 5, ["u_501", "u_dev", "u_sofia"]),
            (users["u_maya"], titles["t_jailer"], 10080, True, 5, ["u_501", "u_dev"]),
            (users["u_maya"], titles["t_wednesday"], 3120, True, 5, ["u_501", "u_sofia"]),
            (users["u_dev"], titles["t_stranger_things"], 4560, True, 5, ["u_501", "u_maya"]),
            (users["u_dev"], titles["t_jailer"], 10080, True, 5, ["u_501", "u_marcus", "u_maya"]),
            (users["u_dev"], titles["t_squid_game"], 3600, True, 5, ["u_501"]),
            (users["u_sofia"], titles["t_stranger_things"], 4560, True, 5, ["u_501", "u_maya"]),
            (users["u_sofia"], titles["t_jailer"], 10080, True, 5, ["u_501"]),
            (users["u_sofia"], titles["t_wednesday"], 3120, True, 5, ["u_501", "u_maya"]),
            (users["u_marcus"], titles["t_stranger_things"], 4560, True, 5, ["u_501"]),
            (users["u_marcus"], titles["t_jailer"], 10080, True, 5, ["u_dev", "u_501"]),
            (users["u_marcus"], titles["t_1004"], 7080, True, 4, ["u_dev"]),
        ]

        Interaction.objects.all().delete()
        for u, t, sec, comp, rat, cow in interactions_data:
            Interaction.objects.create(
                user=u,
                title=t,
                watched_seconds=sec,
                completed=comp,
                rating=rat,
                co_watched_with=cow
            )

        # 7. Write Sample Timeline Files to data/ for Studio Upload
        # Valid JSON
        valid_json = {
            "titleId": "t_1001",
            "titleName": "The Salt Road",
            "version": "v1.2",
            "durationSeconds": 2730,
            "events": raw_events
        }
        with open("data/salt-road.s104.json", "w", encoding="utf-8") as f:
            json.dump(valid_json, f, indent=2)

        # Malformed JSON (matching exact errors from Screenshot 2:
        # events[7].type must be one of: trivia, character, variationPoint, glossary.
        # Missing required field ts at events[12].
        # variationPoint v_02 has no approved options attached.)
        broken_events = list(raw_events[:14])
        broken_events[7]["type"] = "invalid_action_type"
        if "ts" in broken_events[12]:
            del broken_events[12]["ts"]
        broken_events.append({
            "ts": 1900,
            "type": "variationPoint",
            "variationId": "v_02",
            "content": "variationPoint without options",
            "options": []
        })

        malformed_json = {
            "titleId": "t_1001",
            "version": "v1.2",
            "durationSeconds": 2730,
            "events": broken_events
        }
        with open("data/salt-road.s104.broken.json", "w", encoding="utf-8") as f:
            json.dump(malformed_json, f, indent=2)

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with all titles, events, room, and sample files!"))
