from django.shortcuts import render


def index_view(request, room_id=None, invite_code=None):
    """
    Renders the unified Netflix Watch Spaces application.
    The Single Page Application handles navigation seamlessly between:
    - Home Dashboard
    - Watch Room
    - Join Space via Invite Link
    - Content Studio (Timeline Validator)
    - Session Wrapped / Summary
    - Login / Auth
    """
    user_agent = request.headers.get('User-Agent', '') or request.META.get('HTTP_USER_AGENT', '')
    is_e2e = bool(
        request.headers.get('X-Playwright-E2E') or
        request.META.get('HTTP_X_PLAYWRIGHT_E2E') or
        'playwright' in user_agent.lower()
    )
    return render(request, 'index.html', {
        'initial_room_id': room_id or '',
        'initial_invite_code': invite_code or '',
        'is_playwright_e2e': is_e2e,
    })
