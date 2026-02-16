"""
 @file
 @brief Shared AI Tools context-menu builder for project files and timeline.
"""

import os
from functools import partial

from PyQt5.QtGui import QIcon

from classes.app import get_app
from classes import info
from .menu import StyledContextMenu


def _trigger_generation(win, template_id, source_file=None, open_dialog=False):
    win.generation_service.action_generate_trigger(
        source_file=source_file,
        template_id=template_id,
        open_dialog=open_dialog,
    )


def _icon(name):
    icon_path = os.path.join(info.PATH, "themes", "cosmic", "images", name)
    if os.path.exists(icon_path):
        return QIcon(icon_path)
    return QIcon()


def add_ai_tools_menu(win, parent_menu, source_file=None):
    _ = get_app()._tr
    media_type = str(source_file.data.get("media_type", "")) if source_file else ""

    if source_file:
        ai_menu = StyledContextMenu(title=_("Enhance with AI"), parent=parent_menu)
        ai_menu.setIcon(_icon("tool-generate-sparkle.svg"))

        if media_type == "image":
            action = ai_menu.addAction(_("Increase Resolution (4x)"))
            action.setIcon(_icon("ai-action-upscale.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "upscale-realesrgan-x4", source_file, False)
            )
            ai_menu.addSeparator()
            action = ai_menu.addAction(_("Change Image Style..."))
            action.setIcon(_icon("ai-action-restyle.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "img2img-basic", source_file, True)
            )
            parent_menu.addMenu(ai_menu)
            return ai_menu

        elif media_type == "video":
            action = ai_menu.addAction(_("Increase Resolution (4x)"))
            action.setIcon(_icon("ai-action-upscale.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "video-upscale-gan", source_file, False)
            )
            action = ai_menu.addAction(_("Smooth Motion (2x Frame Rate)"))
            action.setIcon(_icon("ai-action-smooth.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "video-frame-interpolation-rife2x", source_file, False)
            )
            action = ai_menu.addAction(_("Split into Scenes"))
            action.setIcon(_icon("ai-action-scenes.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "video-segment-scenes-transnet", source_file, False)
            )
            action = ai_menu.addAction(_("Add Captions from Speech"))
            action.setIcon(_icon("ai-action-captions.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "video-whisper-srt", source_file, False)
            )
            ai_menu.addSeparator()
            action = ai_menu.addAction(_("Change Video Style..."))
            action.setIcon(_icon("ai-action-restyle.svg"))
            action.triggered.connect(
                partial(_trigger_generation, win, "video2video-basic", source_file, True)
            )
        else:
            action = ai_menu.addAction(_("No AI enhancement actions available yet."))
            action.setEnabled(False)

        parent_menu.addMenu(ai_menu)
        return ai_menu

    ai_menu = StyledContextMenu(title=_("Create with AI"), parent=parent_menu)
    ai_menu.setIcon(_icon("tool-generate-sparkle.svg"))
    action = ai_menu.addAction(_("Image..."))
    action.setIcon(_icon("ai-action-create-image.svg"))
    action.triggered.connect(partial(_trigger_generation, win, "txt2img-basic", source_file, True))
    action = ai_menu.addAction(_("Video..."))
    action.setIcon(_icon("ai-action-create-video.svg"))
    action.triggered.connect(partial(_trigger_generation, win, "txt2video-svd", source_file, True))
    action = ai_menu.addAction(_("Audio..."))
    action.setIcon(_icon("ai-action-create-audio.svg"))
    action.triggered.connect(partial(_trigger_generation, win, "txt2audio-stable-open", source_file, True))

    parent_menu.addMenu(ai_menu)
    return ai_menu
