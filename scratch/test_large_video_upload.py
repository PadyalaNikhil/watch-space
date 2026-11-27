import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import django
import io

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from spaces.models import WatchUser, WatchSpace, UserVideo
from spaces.auth_utils import generate_jwt_token
from spaces.views_api import format_file_size

def run_tests():
    print(f"=== Testing Video Upload Limits & Auth ===")
    print(f"DATA_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 'Not Set')} bytes ({getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 0) / (1024*1024*1024):.2f} GB)")
    print(f"FILE_UPLOAD_MAX_MEMORY_SIZE: {getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 'Not Set')} bytes ({getattr(settings, 'FILE_UPLOAD_MAX_MEMORY_SIZE', 0) / (1024*1024):.1f} MB)")
    
    assert getattr(settings, 'DATA_UPLOAD_MAX_MEMORY_SIZE', 0) >= 2 * 1024 * 1024 * 1024, "Limit must be at least 2GB"

    # Test format_file_size helper
    assert format_file_size(1500 * 1024 * 1024) == "1.46 GB"
    assert format_file_size(2 * 1024 * 1024 * 1024) == "2.00 GB"
    assert format_file_size(25 * 1024 * 1024) == "25.0 MB"
    print("format_file_size tests passed!")

    client = Client()
    space = WatchSpace.objects.first()
    host_user = space.host
    print(f"Host user for room {space.id}: {host_user.display_name} ({host_user.id})")
    
    token = generate_jwt_token(host_user)

    # 0. Test file > 2GB rejection
    print("\n0. Testing file > 2 GB rejection...")
    from django.test import RequestFactory
    import json
    from spaces.views_api import profile_video_upload
    rf = RequestFactory()
    req = rf.post('/api/v1/profile/videos/upload', HTTP_AUTHORIZATION=f"Bearer {token}")
    oversized_file = SimpleUploadedFile("huge_movie.mp4", b"dummy_content", content_type="video/mp4")
    oversized_file.size = 2147483648 + 1048576  # 2 GB + 1 MB
    req.FILES['video'] = oversized_file
    rej_res = profile_video_upload(req)
    print(f"Oversized file response: {rej_res.status_code} - {json.loads(rej_res.content)}")
    assert rej_res.status_code == 400
    assert "exceeds maximum allowed size of 2 GB" in json.loads(rej_res.content).get('error', '')
    
    # 1. Test Large Video Upload (25 MB)
    print("\n1. Testing 25 MB video upload to profile vault...")
    twentyfive_mb_bytes = b"0" * (25 * 1024 * 1024)  # 25 MB
    uploaded_file = SimpleUploadedFile("sample_movie_25mb.mp4", twentyfive_mb_bytes, content_type="video/mp4")
    
    res = client.post(
        '/api/v1/profile/videos/upload',
        {'video': uploaded_file, 'title': 'Sample Movie 25MB'},
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    print(f"Upload response status: {res.status_code}")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}: {res.content}"
    data = res.json()
    assert data.get('success') is True, "Upload failed"
    video_id = data['video']['id']
    print(f"Successfully uploaded: {data['video']['title']} ({data['video']['fileSizeFormatted']}) with ID: {video_id}")
    
    # Verify file saved on disk
    user_video = UserVideo.objects.get(id=video_id)
    assert os.path.exists(user_video.file_path), "File does not exist on disk!"
    assert os.path.getsize(user_video.file_path) == len(twentyfive_mb_bytes), "File size on disk does not match!"
    print(f"Disk file verified: {user_video.file_path} ({os.path.getsize(user_video.file_path)} bytes)")

    # 2. Test Profile Video Listing
    print("\n2. Testing profile video listing...")
    list_res = client.get('/api/v1/profile/videos', HTTP_AUTHORIZATION=f"Bearer {token}")
    assert list_res.status_code == 200
    list_data = list_res.json()
    assert any(v['id'] == video_id for v in list_data['videos']), "Uploaded video not in list"
    print(f"Verified video in vault listing. Total videos: {len(list_data['videos'])}")

    # 3. Test Room Video Upload (direct room upload with 4 MB file)
    print("\n3. Testing 4 MB room video upload...")
    space = WatchSpace.objects.first()
    four_mb_bytes = b"1" * (4 * 1024 * 1024)
    room_file = SimpleUploadedFile("room_movie_4mb.mp4", four_mb_bytes, content_type="video/mp4")
    room_up_res = client.post(
        f"/api/v1/watch-spaces/{space.id}/video/upload",
        {'video': room_file},
        HTTP_AUTHORIZATION=f"Bearer {token}",
        HTTP_X_DEMO_USER=host_user.id
    )
    print(f"Room upload status: {room_up_res.status_code}")
    assert room_up_res.status_code == 200, f"Room upload failed: {room_up_res.content}"
    print(f"Room video stream URL: {room_up_res.json().get('videoUrl')}")

    # 4. Test Setting Profile Video in Room & Streaming for Visitors
    print("\n4. Testing setting profile video to room and visitor range streaming...")
    set_res = client.post(
        f"/api/v1/watch-spaces/{space.id}/set-profile-video",
        data='{"videoId": "' + str(video_id) + '"}',
        content_type='application/json',
        HTTP_AUTHORIZATION=f"Bearer {token}"
    )
    print(f"Set profile video status: {set_res.status_code}")
    assert set_res.status_code == 200, f"Set profile video failed: {set_res.content}"

    # Visitor requests range stream
    stream_res = client.get(
        f"/api/v1/profile/videos/{video_id}/stream",
        HTTP_RANGE="bytes=0-1048575"  # First 1 MB
    )
    assert stream_res.status_code == 206, f"Expected 206 Partial Content, got {stream_res.status_code}"
    assert stream_res.get('Content-Range') == f"bytes 0-1048575/{len(twentyfive_mb_bytes)}"
    stream_chunk = b''.join(stream_res.streaming_content)
    assert len(stream_chunk) == 1048576, f"Expected 1MB chunk, got {len(stream_chunk)}"
    print(f"HTTP 206 range stream verified: returned {len(stream_chunk)} bytes with header {stream_res.get('Content-Range')}")

    # 5. Test Cleanup / Delete
    print("\n5. Testing profile video deletion...")
    del_res = client.delete(f"/api/v1/profile/videos/{video_id}", HTTP_AUTHORIZATION=f"Bearer {token}")
    assert del_res.status_code == 200
    assert not os.path.exists(user_video.file_path), "File should be removed from disk"
    assert not UserVideo.objects.filter(id=video_id).exists(), "Record should be removed from DB"
    print("Video successfully deleted from vault and disk.")

    print("\nALL TESTS PASSED SUCCESSFULLY! Large video uploads are working flawlessly!")

if __name__ == '__main__':
    run_tests()
