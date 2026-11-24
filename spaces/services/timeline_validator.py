import re
from typing import Dict, Any, List, Tuple
from ..models import Title, TimelineEvent, VariationOption


SCHEMA_V1_2 = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "WatchSpacesTimelineSchema",
    "version": "1.2",
    "type": "object",
    "required": ["titleId", "durationSeconds", "events"],
    "properties": {
        "titleId": {"type": "string"},
        "version": {"type": "string", "default": "v1.2"},
        "durationSeconds": {"type": "integer", "minimum": 1},
        "events": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["ts", "type", "content"],
                "properties": {
                    "id": {"type": "string"},
                    "ts": {"type": "integer", "minimum": 0},
                    "type": {
                        "type": "string",
                        "enum": ["trivia", "character", "variationPoint", "variation_point", "glossary"]
                    },
                    "content": {"type": "string"},
                    "character_name": {"type": "string"},
                    "location": {"type": "string"},
                    "source_id": {"type": "string"},
                    "options": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["id", "label"],
                            "properties": {
                                "id": {"type": "string"},
                                "label": {"type": "string"},
                                "assetRef": {"type": "string"}
                            }
                        }
                    }
                }
            }
        }
    }
}


def validate_timeline_payload(data: Dict[str, Any], max_duration: int = 2730) -> Tuple[bool, List[str], Dict[str, Any]]:
    """
    Validates a timeline JSON/YAML dictionary against Schema v1.2.
    Returns: (is_valid, error_list, summary_stats)
    """
    errors = []
    
    if not isinstance(data, dict):
        return False, ["Root object must be a valid JSON dictionary."], {}

    title_id = data.get("titleId")
    duration = data.get("durationSeconds", max_duration)
    events = data.get("events")

    if not title_id:
        errors.append("Missing required field 'titleId' at root.")
    if not isinstance(duration, (int, float)) or duration <= 0:
        errors.append("Missing or invalid field 'durationSeconds' at root.")
    if events is None or not isinstance(events, list):
        errors.append("Missing required array 'events' at root.")
        return False, errors, {}

    valid_types = {"trivia", "character", "variationPoint", "variation_point", "glossary"}
    type_counts = {"trivia": 0, "character": 0, "variationPoint": 0, "glossary": 0}
    variation_points_count = 0

    for idx, evt in enumerate(events):
        if not isinstance(evt, dict):
            errors.append(f"events[{idx}] must be a JSON object.")
            continue

        # Check type
        raw_type = evt.get("type")
        if not raw_type or raw_type not in valid_types:
            errors.append(f"events[{idx}].type must be one of: trivia, character, variationPoint, glossary.")
        else:
            normalized_type = "variationPoint" if raw_type in ("variationPoint", "variation_point") else raw_type
            type_counts[normalized_type] = type_counts.get(normalized_type, 0) + 1

        # Check ts
        if "ts" not in evt:
            errors.append(f"Missing required field ts at events[{idx}].")
        elif not isinstance(evt["ts"], (int, float)) or evt["ts"] < 0 or evt["ts"] > duration:
            errors.append(f"events[{idx}].ts ({evt.get('ts')}) must be an integer between 0 and {duration}s.")

        # Check content or text
        content = evt.get("content") or evt.get("text")
        if not content or not str(content).strip():
            errors.append(f"Missing required content or text at events[{idx}].")

        # Variation point checks
        if raw_type in ("variationPoint", "variation_point"):
            variation_id = evt.get("variationId") or evt.get("id") or f"v_{idx}"
            options = evt.get("options")
            if not options or not isinstance(options, list) or len(options) < 2:
                errors.append(f"variationPoint {variation_id} has no approved options attached.")
            else:
                variation_points_count += 1
                for opt_idx, opt in enumerate(options):
                    if not isinstance(opt, dict) or not opt.get("id") or not opt.get("label"):
                        errors.append(f"variationPoint {variation_id} option[{opt_idx}] must have 'id' and 'label'.")

    is_valid = (len(errors) == 0)
    summary = {
        "total_events": len(events),
        "type_counts": type_counts,
        "variation_points": variation_points_count,
        "duration_seconds": duration,
        "duration_formatted": f"{int(duration)//60:02d}:{int(duration)%60:02d}",
        "schema_version": data.get("version", "v1.2")
    }

    return is_valid, errors, summary


def ingest_timeline_to_db(title: Title, data: Dict[str, Any]) -> Tuple[int, int]:
    """
    Ingests validated timeline into Title, TimelineEvent, and VariationOption models.
    """
    events = data.get("events", [])
    created_events = 0
    created_variations = 0

    # Clean existing timeline events for this title
    title.timeline_events.all().delete()

    for idx, evt in enumerate(events):
        raw_type = evt.get("type", "trivia")
        if raw_type == "variationPoint":
            event_type = "variation_point"
        elif raw_type in ("trivia", "character", "glossary", "variation_point"):
            event_type = raw_type
        else:
            event_type = "trivia"

        evt_id = evt.get("id") or evt.get("source_id") or f"evt_{2200 + idx}"
        ts_seconds = int(evt.get("ts", 0))
        content = evt.get("content") or evt.get("text", "")
        source_id = evt.get("source_id") or evt_id
        char_name = evt.get("character_name", "")
        location = evt.get("location", "")

        event_obj = TimelineEvent.objects.create(
            id=evt_id,
            title=title,
            ts_seconds=ts_seconds,
            event_type=event_type,
            content=content,
            source_id=source_id,
            character_name=char_name,
            location=location,
            payload=evt
        )
        created_events += 1

        # Variation options
        if event_type == "variation_point" and "options" in evt:
            var_id = evt.get("variationId", f"v_{idx:02d}")
            for opt in evt["options"]:
                VariationOption.objects.create(
                    timeline_event=event_obj,
                    variation_id=var_id,
                    option_key=opt.get("id", "a"),
                    label=opt.get("label", ""),
                    asset_ref=opt.get("assetRef", "")
                )
                created_variations += 1

    title.is_published = True
    title.schema_version = data.get("version", "v1.2")
    title.save()

    return created_events, created_variations
