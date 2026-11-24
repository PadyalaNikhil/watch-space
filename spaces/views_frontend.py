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
    return render(request, 'index.html', {
        'initial_room_id': room_id or '',
        'initial_invite_code': invite_code or '',
    })
