import uuid
from django.db import models
from django.contrib.auth.models import User


class GalharufaUser(User):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        app_label = 'galharufa'
