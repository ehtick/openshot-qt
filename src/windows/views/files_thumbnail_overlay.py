"""
 @file
 @brief Dynamic media-type overlay painter for project file thumbnails.
"""

import os

from PyQt5.QtCore import QRectF, Qt
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtSvg import QSvgRenderer

from classes import info


_OVERLAY_ICON_NAMES = {
    "image": "ai-action-create-image.svg",
    "audio": "ai-action-create-audio.svg",
    "video": "ai-action-create-video.svg",
}


def _overlay_icon_path(media_type):
    icon_name = _OVERLAY_ICON_NAMES.get(str(media_type or "").strip().lower())
    if not icon_name:
        return ""
    return os.path.join(info.PATH, "themes", "cosmic", "images", icon_name)


def paint_media_overlay(painter, deco_rect, media_type):
    """Paint a translucent media-type badge over a thumbnail decoration rect."""
    if not deco_rect or not deco_rect.isValid():
        return

    icon_path = _overlay_icon_path(media_type)
    if not icon_path or not os.path.exists(icon_path):
        return

    painter.save()
    painter.setRenderHint(QPainter.Antialiasing, True)

    badge_size = max(14.0, min(deco_rect.width(), deco_rect.height()) * 0.32)
    margin = max(3.0, min(deco_rect.width(), deco_rect.height()) * 0.06)
    badge_rect = QRectF(
        deco_rect.right() - badge_size - margin + 1.0,
        deco_rect.bottom() - badge_size - margin + 1.0,
        badge_size,
        badge_size,
    )

    painter.setPen(Qt.NoPen)
    painter.setBrush(QColor(18, 24, 31, 112))
    painter.drawRoundedRect(badge_rect, badge_size * 0.24, badge_size * 0.24)

    glyph_rect = badge_rect.adjusted(badge_size * 0.16, badge_size * 0.16, -badge_size * 0.16, -badge_size * 0.16)
    renderer = QSvgRenderer(icon_path)
    renderer.render(painter, glyph_rect)

    painter.restore()
