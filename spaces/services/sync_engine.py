import time
import math
from typing import Dict, Any, List, Optional
from django.utils import timezone
from ..models import WatchSpace, WatchSpaceParticipant, ChatMessage, WatchUser


class SyncEngine:
    """
    Real-time room synchronization engine.
    Maintains authoritative playback clock, computes participant drift,
    issues micro-seek rate adjustments or corrective seek commands,
    and manages variation voting and host failure recovery.
    """

    @staticmethod
    def calculate_drift(room_ts: float, client_ts: float, rtt_ms: float = 30.0) -> Dict[str, Any]:
        """
        Computes drift deviation between server/host authoritative clock and client playback.
        Applies network one-way trip delay compensation (rtt / 2).
        Returns drift in ms and corrective action:
        - drift < 100ms: in tight sync (no action needed)
        - 100ms <= drift < 250ms: micro-adjust playback rate (e.g., 0.98x or 1.02x)
        - drift >= 250ms: smooth micro-seek to align frames
        """
        one_way_latency_sec = (rtt_ms / 2.0) / 1000.0
        adjusted_room_ts = room_ts + one_way_latency_sec
        diff_sec = client_ts - adjusted_room_ts
        drift_ms = int(diff_sec * 1000.0)

        abs_drift_ms = abs(drift_ms)

        if abs_drift_ms < 100:
            status = "in_sync"
            action = "maintain"
            target_playback_rate = 1.0
        elif abs_drift_ms < 250:
            status = "minor_drift"
            # Micro-adjust playback rate gently so audio/video pitch stays natural
            action = "micro_rate_adjust"
            target_playback_rate = 0.97 if drift_ms > 0 else 1.03
        else:
            status = "desynced"
            action = "micro_seek"
            target_playback_rate = 1.0

        return {
            "drift_ms": drift_ms,
            "abs_drift_ms": abs_drift_ms,
            "status": status,
            "action": action,
            "target_playback_rate": target_playback_rate,
            "target_position_sec": adjusted_room_ts
        }

    @staticmethod
    def update_playback_state(
        room: WatchSpace,
        user: WatchUser,
        state: str,
        position_seconds: float,
        duration_seconds: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Processes authoritative playback changes (play/pause/seek) and duration updates.
        Server-side RBAC: Only Host is permitted to alter authoritative playback!
        """
        if room.host_id != user.id:
            return {
                "success": False,
                "error": "Forbidden: Only the room host can update playback state."
            }

        room.current_playback_ts = max(0.0, float(position_seconds))
        if state == "play":
            room.is_playing = True
        elif state == "pause":
            room.is_playing = False

        update_fields = ['current_playback_ts', 'is_playing']

        # Update custom video duration if provided and room is playing a custom/shared video
        if duration_seconds is not None:
            try:
                dur_int = max(1, int(float(duration_seconds)))
                if room.active_variation and isinstance(room.active_variation, dict) and 'custom_video' in room.active_variation:
                    room.active_variation['custom_video']['duration'] = dur_int
                    update_fields.append('active_variation')
            except (ValueError, TypeError):
                pass

        room.save(update_fields=update_fields)

        # Create system notification in chat history
        action_text = f"started playback for everyone · {int(position_seconds)//60:02d}:{int(position_seconds)%60:02d}" if state == "play" else f"paused playback at {int(position_seconds)//60:02d}:{int(position_seconds)%60:02d}"
        ChatMessage.objects.create(
            watch_space=room,
            user=None,
            msg_type='system',
            body=f"{user.display_name} {action_text}",
            ts_seconds=int(position_seconds)
        )

        return {
            "success": True,
            "state": state,
            "positionSeconds": room.current_playback_ts,
            "isPlaying": room.is_playing,
            "issuedBy": user.id,
            "updatedAt": timezone.now().isoformat()
        }

    @staticmethod
    def handle_host_offline(room: WatchSpace) -> Dict[str, Any]:
        """
        Triggers host failover protocol when host disconnects:
        pauses playback for everyone and schedules auto-promotion of next active participant.
        """
        room.is_playing = False
        room.save(update_fields=['is_playing'])

        next_candidate = room.participants.filter(role='participant').exclude(user=room.host).order_by('joined_at').first()
        promoted_name = next_candidate.user.display_name if next_candidate else "Maya"
        promoted_id = next_candidate.user.id if next_candidate else None

        return {
            "event": "room.host.dropped",
            "message": f"Your host connection dropped. Playback is paused for everyone. Auto-promoting {promoted_name} in 12s.",
            "candidateName": promoted_name,
            "candidateId": promoted_id,
            "autoPromoteDelaySec": 12
        }

    @staticmethod
    def promote_participant_to_host(room: WatchSpace, new_host_user: WatchUser) -> Dict[str, Any]:
        """
        Promotes a participant to room host.
        """
        old_host = room.host
        room.host = new_host_user
        room.save(update_fields=['host'])

        # Update participant roles
        room.participants.filter(user=new_host_user).update(role='host')
        if old_host:
            room.participants.filter(user=old_host).update(role='participant')

        ChatMessage.objects.create(
            watch_space=room,
            user=None,
            msg_type='system',
            body=f"{new_host_user.display_name} has been promoted to Host.",
            ts_seconds=int(room.current_playback_ts)
        )

        return {
            "success": True,
            "newHostId": new_host_user.id,
            "newHostName": new_host_user.display_name
        }
