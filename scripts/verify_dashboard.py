import os
import sys
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.test import RequestFactory
from spaces.views_api import dashboard_data

rf = RequestFactory()
req = rf.get('/api/v1/dashboard')
res = dashboard_data(req)
data = json.loads(res.content)

print("=" * 60)
print("NETFLIX DASHBOARD API VERIFICATION")
print("=" * 60)
print(f"Status Code: {res.status_code}")
print(f"Hero Banner Title: {data['heroTitle']['name']}")
print(f"Hero Match: {data['heroTitle']['matchPercentage']}%")
print(f"Hero Backdrop: {data['heroTitle']['backdropUrl']}")
print("-" * 60)
print(f"Recommendations ({len(data['recommendations'])} titles):")
for i, r in enumerate(data['recommendations'], 1):
    print(f"  {i}. {r['name']} ({r['match_percentage']}% match) [{r['badge']}] -> {r['poster_url']}")
print("-" * 60)
print(f"Top 10 Trending ({len(data['top10'])} titles):")
for t in data['top10']:
    print(f"  #{t['rank']} {t['name']} ({t['match_percentage']}%) [{t['badge']}]")
print("-" * 60)
print("Continue Watching:")
for c in data['continueWatching']:
    print(f"  • {c['name']} - {c['episodeInfo']} ({c['timeLeft']}, {c['progressPercent']}%)")
print("-" * 60)
print("Upcoming Watch Spaces:")
for s in data['upcomingSpaces']:
    print(f"  • {s['roomName']} ({s['titleName']}) hosted by {s['host']} at {s['time']}")
print("=" * 60)
