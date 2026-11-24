import os
import sys
import django
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from spaces.models import WatchSpace, Title, WatchUser

client = Client()

print("==================================================")
print("VERIFYING STRANGER THINGS WATCH SPACE SYSTEM")
print("==================================================")

# 1. Verify Title in DB
st_title = Title.objects.filter(id='t_stranger_things').first()
assert st_title is not None, "Stranger Things title missing from database!"
print(f"✓ Title in DB: {st_title.name} (Duration: {st_title.duration_seconds}s, Backdrop: {st_title.backdrop_url})")

# 2. Test Dashboard API
resp = client.get('/api/v1/dashboard', HTTP_X_DEMO_USER='u_501')
assert resp.status_code == 200, f"Dashboard returned {resp.status_code}"
dash_data = resp.json()
print(f"✓ Dashboard Hero Title: {dash_data['heroTitle']['name']} (ID: {dash_data['heroTitle']['id']})")
if dash_data.get('activeRoom'):
    print(f"✓ Dashboard Active Room: {dash_data['activeRoom']['roomName']} -> {dash_data['activeRoom']['titleName']} ({dash_data['activeRoom']['backdropUrl']})")

# 3. Test Room Creation with Title ID
create_resp = client.post(
    '/api/v1/watch-spaces',
    data=json.dumps({
        'titleId': 't_stranger_things',
        'roomName': 'Hawkins AV Club Watch Night',
        'maxParticipants': 12,
        'startTs': 0.0
    }),
    content_type='application/json',
    HTTP_X_DEMO_USER='u_501'
)
assert create_resp.status_code in [200, 201], f"Creation failed: {create_resp.content}"
room_data = create_resp.json()
created_id = room_data['watchSpaceId']
print(f"✓ Created Room: {room_data['roomName']} (ID: {created_id}, Title: {room_data['titleName']}, Code: {room_data['inviteCode']})")

# 4. Test Room Detail API
detail_resp = client.get(f'/api/v1/watch-spaces/{created_id}', HTTP_X_DEMO_USER='u_501')
assert detail_resp.status_code == 200, f"Detail failed: {detail_resp.content}"
detail = detail_resp.json()
assert detail['title']['name'] == 'Stranger Things', f"Wrong title: {detail['title']['name']}"
assert detail['title']['backdropUrl'] == '/static/images/backdrop-stranger-things.svg', f"Wrong backdrop: {detail['title']['backdropUrl']}"
assert detail['playback']['currentPlaybackTs'] == 0.0, f"Wrong initial ts: {detail['playback']['currentPlaybackTs']}"
assert detail['title']['durationSeconds'] == 4560, f"Wrong duration: {detail['title']['durationSeconds']}"
print(f"✓ Room Detail Verified: Title='{detail['title']['name']}', Backdrop='{detail['title']['backdropUrl']}', CurrentTs={detail['playback']['currentPlaybackTs']}, Duration={detail['title']['durationSeconds']}s")

# 5. Test Room Creation with Title Inference from Room Name
infer_resp = client.post(
    '/api/v1/watch-spaces',
    data=json.dumps({
        'roomName': 'stranger things club'
    }),
    content_type='application/json',
    HTTP_X_DEMO_USER='u_501'
)
assert infer_resp.status_code in [200, 201]
infer_data = infer_resp.json()
assert infer_data['titleId'] == 't_stranger_things', f"Inference failed: {infer_data['titleId']}"
print(f"✓ Title Auto-Inference Verified: '{infer_data['roomName']}' correctly mapped to '{infer_data['titleName']}' ({infer_data['titleId']})")

# 6. Verify Existing User Room ws_43201
user_room_resp = client.get('/api/v1/watch-spaces/ws_43201', HTTP_X_DEMO_USER='u_501')
assert user_room_resp.status_code == 200
user_room = user_room_resp.json()
assert user_room['title']['name'] == 'Stranger Things'
print(f"✓ User's Room ws_43201 Verified: Title='{user_room['title']['name']}', Backdrop='{user_room['title']['backdropUrl']}'")

print("==================================================")
print("ALL VERIFICATION CHECKS PASSED SUCCESSFULLY!")
print("==================================================")
