# roads/signals.py
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import GameBoard, GamePath
from .events import push_event

@receiver(post_save, sender=GameBoard)
def broadcast_new_board(sender, instance, created, **kwargs):
    if not created:
        return

    payload = {
        "board_id": instance.id,
        "board_name": instance.name,          # lub instance.title, jak masz pole
        "creator_username": instance.user.username
    }
    ev = (
        "event: newBoard\n"
        f"data: {json.dumps(payload)}\n\n"
    )
    push_event(ev)

@receiver(post_save, sender=GamePath)
def broadcast_new_path(sender, instance, created, **kwargs):
    if not created:
        return
    payload = {
        "path_id": instance.id,
        "board_id": instance.board.id,
        "board_name": instance.board.name,
        "user_username": instance.user.username
    }
    ev = (
        "event: newPath\n"
        f"data: {json.dumps(payload)}\n\n"
    )
    push_event(ev)
