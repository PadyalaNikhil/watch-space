import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from spaces.models import WatchSpace, Title, ChatMessage

st_title = Title.objects.filter(id='t_stranger_things').first()
if not st_title:
    print("Error: Stranger Things title not found in DB")
    sys.exit(1)

# Fix rooms named stranger things
rooms = WatchSpace.objects.filter(room_name__icontains='stranger')
count = 0
for r in rooms:
    r.title = st_title
    r.current_playback_ts = 0.0
    r.is_playing = True
    r.save()
    count += 1
    # Update or add system message
    ChatMessage.objects.filter(watch_space=r, msg_type='system').update(
        body=f"{r.host.display_name} created the room and started playback for 'Stranger Things'."
    )
    print(f"Updated room {r.id} ({r.room_name}) to Stranger Things (00:00:00)")

print(f"Total rooms updated: {count}")
