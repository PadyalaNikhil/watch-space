import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

print("==================================================")
print("VERIFYING NATIVE DIRECT NETFLIX PLAYER INTEGRATION")
print("==================================================")

# 1. Check templates/index.html
index_path = os.path.join(BASE_DIR, 'templates', 'index.html')
with open(index_path, 'r', encoding='utf-8') as f:
    html = f.read()

required_html_ids = [
    'playerHtml5Video',
    'playerSourceSelectorBar',
    'directNetflixLinkBtn',
    'controlsNetflixDirectLink',
    'srcBtn_html5',
    'srcBtn_backdrop',
    'srcBtn_local',
    'localVideoFileInput',
    'centerPlayOverlay'
]

for el_id in required_html_ids:
    assert f'id="{el_id}"' in html, f"Missing HTML element #{el_id} in templates/index.html"
    print(f"✓ Found HTML element: #{el_id}")

# 2. Check static/js/app.js
app_js_path = os.path.join(BASE_DIR, 'static', 'js', 'app.js')
with open(app_js_path, 'r', encoding='utf-8') as f:
    js = f.read()

required_js_functions = [
    'function loadMovieVideo',
    'function switchVideoSource',
    'function triggerLocalVideoUpload',
    'function handleLocalVideoUpload',
    'function syncActiveVideoPlayerState',
    'function handleCenterPlayClick'
]

for fn in required_js_functions:
    assert fn in js, f"Missing JS function '{fn}' in static/js/app.js"
    print(f"✓ Found JS function: {fn}")

# Check Netflix URL configuration for Stranger Things
assert '80057281' in js, "Missing Stranger Things official Netflix ID 80057281 in app.js"
print("✓ Stranger Things official Netflix ID '80057281' and direct URL configured.")

# 3. Check static/css/styles.css
styles_path = os.path.join(BASE_DIR, 'static', 'css', 'styles.css')
with open(styles_path, 'r', encoding='utf-8') as f:
    css = f.read()

assert '.btn-netflix-open' in css, "Missing .btn-netflix-open CSS"
assert '.btn-netflix-mini' in css, "Missing .btn-netflix-mini CSS"
assert '.player-source-selector-bar' in css, "Missing .player-source-selector-bar CSS"
print("✓ Netflix player styling verified in styles.css")

print("==================================================")
print("ALL NATIVE NETFLIX PLAYER CHECKS PASSED!")
print("==================================================")
