from django.conf import settings

import navbar.models as navbar_models


def navbar(request):
    """Add the navbar specified in the settings to the context."""

    if 'navbar' in settings.INSTALLED_APPS:
        bar = navbar_models.Navbar.objects.filter(state=True).first()
        if bar:
            return {"navbar": bar}
    return {}
