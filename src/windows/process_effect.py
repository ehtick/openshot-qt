"""
 @file
 @brief This file loads the Initialize Effects / Pre-process effects dialog
 @author Jonathan Thomas <jonathan@openshot.org>

 @section LICENSE

 Copyright (c) 2008-2018 OpenShot Studios, LLC
 (http://www.openshotstudios.com). This file is part of
 OpenShot Video Editor (http://www.openshot.org), an open-source project
 dedicated to delivering high quality video editing and animation solutions
 to the world.

 OpenShot Video Editor is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 OpenShot Video Editor is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with OpenShot Library.  If not, see <http://www.gnu.org/licenses/>.
 """

import os
import time
import json
import functools
import webbrowser
import hashlib
import urllib.request
import zipfile

from qt_api import Qt, pyqtSignal, QCoreApplication
from qt_api import QPainter
from qt_api import (
    QPushButton, QDialog, QLabel, QDoubleSpinBox, QSpinBox, QLineEdit,
    QCheckBox, QComboBox, QDialogButtonBox, QSizePolicy, QMessageBox,
    QFileDialog, QProgressDialog, QWidget, QHBoxLayout,
)
import openshot  # Python module for libopenshot (required video editing module installed separately)

from classes import info
from classes import ui_util
from classes.app import get_app
from classes.logger import log
from classes.metrics import *

YOLO5_DOWNLOAD_URL = "https://www.openshot.org/static/files/yolov5/yolov5s-openshot.zip"
YOLO5_DOWNLOAD_SHA256 = "cd401831d6a700cb827b4470ec0a505fb8802a85075fcd55c279cb4b73e02c69"
YOLO5_DIR = os.path.join(info.YOLO_PATH, "Yolo5")
YOLO5_MODEL_PATH = os.path.join(YOLO5_DIR, "yolov5s.onnx")
YOLO5_CLASSES_PATH = os.path.join(YOLO5_DIR, "obj.names")
YOLO5_MODEL_SHA256 = "ffcac948408e3731ba6b0059e125f3d759672830771b72d5081fb6244ff47e5d"
YOLO5_CLASSES_SHA256 = "bd17f1ee35d5f3c862a4894605855abbb9dda4b0621fdb0ac4c2c8c7bb7e730a"
YOLO5_MODEL_MIN_SIZE = 20 * 1024 * 1024


class RegionButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.qimage = None

    def setImage(self, qimage):
        self.qimage = qimage
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.qimage:
            painter = QPainter(self)
            resized_qimage = self.qimage.scaled(self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
            painter.drawImage(0, 0, resized_qimage)
        else:
            super().paintEvent(event)  # Draw the normal button


class ProcessEffect(QDialog):
    """ Choose Profile Dialog """
    progress = pyqtSignal(int)

    # Path to ui file
    ui_path = os.path.join(info.PATH, 'windows', 'ui', 'process-effect.ui')

    def __init__(self, clip_id, effect_class, effect_params):

        if not openshot.Clip().COMPILED_WITH_CV:
            raise ModuleNotFoundError("Openshot not compiled with OpenCV")

        # Create dialog class
        super().__init__()
        # Track effect details
        self.clip_id = clip_id
        self.effect_name = ""
        self.effect_class = effect_class
        self.context = {}
        self.file_fields = {}

        # Get all effect JSON data, and find effect's display name (based on the class name)
        raw_effects_list = json.loads(openshot.EffectInfo.Json())
        for raw_effect in raw_effects_list:
            if raw_effect.get("class_name") == self.effect_class:
                self.effect_name = raw_effect.get("name")
                break

        # Access C++ timeline and find the Clip instance which this effect should be applied to
        timeline_instance = get_app().window.timeline_sync.timeline
        for clip_instance in timeline_instance.Clips():
            if clip_instance.Id() == self.clip_id:
                self.clip_instance = clip_instance
                break

        # Load UI from designer & init
        ui_util.load_ui(self, self.ui_path)
        ui_util.init_ui(self)

        # get translations
        _ = get_app()._tr

        # Update window title
        self.setWindowTitle(self.windowTitle() % _(self.effect_name))

        # Pause playback
        get_app().window.PauseSignal.emit()

        # Track metrics
        track_metric_screen("process-effect-screen")

        # Loop through options and create widgets
        form_layout = self.scrollAreaWidgetContents.layout()
        for param in effect_params:
            if (
                param["type"] == "download-yolo5"
                and self.yolo5_default_files_ready()
            ):
                continue

            # Create Label
            widget = None
            label = QLabel()
            label.setText(_(param["title"]))
            label.setToolTip(_(param["title"]))

            if param["type"] == "link":
                # create a clickable link
                label.setText('<a href="%s" style="color: #FFFFFF">%s</a>' % (param["value"], _(param["title"])))
                label.setTextInteractionFlags(Qt.TextBrowserInteraction)
                label.linkActivated.connect(functools.partial(self.link_activated, widget, param))

            if param["type"] == "download-yolo5":
                widget = QPushButton(_("Download"))
                widget.setToolTip(_("Download the YOLOv5 ONNX model and class names."))
                widget.clicked.connect(functools.partial(self.download_yolo5_clicked, widget, param))

            if param["type"] == "spinner":
                # create QDoubleSpinBox
                widget = QDoubleSpinBox()
                widget.setMinimum(float(param["min"]))
                widget.setMaximum(float(param["max"]))
                widget.setValue(float(param["value"]))
                widget.setSingleStep(1.0)
                widget.setToolTip(_(param["title"]))
                widget.valueChanged.connect(functools.partial(self.spinner_value_changed, widget, param))

                # Set initial context
                self.context[param["setting"]] = float(param["value"])

            if param["type"] == "rect":
                # create QPushButton which opens up a display of the clip, with ability to select Rectangle
                widget = RegionButton(_("Click to Select"))
                widget.setMinimumHeight(80)
                widget.setToolTip(_(param["title"]))
                widget.clicked.connect(functools.partial(self.rect_select_clicked, widget, param))

                # Set initial context
                self.context[param["setting"]] = {"button-clicked": False, "x": 0, "y": 0, "width": 0, "height": 0}

            if param["type"] == "spinner-int":
                # create QDoubleSpinBox
                widget = QSpinBox()
                widget.setMinimum(int(param["min"]))
                widget.setMaximum(int(param["max"]))
                widget.setValue(int(param["value"]))
                widget.setSingleStep(1)
                widget.setToolTip(_(param["title"]))
                widget.valueChanged.connect(functools.partial(self.spinner_value_changed, widget, param))

                # Set initial context
                self.context[param["setting"]] = int(param["value"])

            elif param["type"] == "text":
                # create QLineEdit
                widget = QLineEdit()
                widget.setText(_(param["value"]))
                widget.textChanged.connect(functools.partial(self.text_value_changed, widget, param))

                # Set initial context
                self.context[param["setting"]] = param["value"]

            elif param["type"] == "file":
                widget = QWidget()
                widget_layout = QHBoxLayout(widget)
                widget_layout.setContentsMargins(0, 0, 0, 0)
                widget_layout.setSpacing(6)

                path_widget = QLineEdit()
                path_widget.setText(param["value"])
                path_widget.setToolTip(_(param["title"]))
                path_widget.textChanged.connect(functools.partial(self.file_value_changed, path_widget, param))

                status_widget = QLabel()
                status_widget.setMinimumWidth(20)
                status_widget.setToolTip(_("File has not been validated yet."))

                browse_button = QPushButton(_("Browse"))
                browse_button.setToolTip(_("Choose a file from disk."))
                browse_button.clicked.connect(functools.partial(self.file_browse_clicked, path_widget, param))

                path_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
                status_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
                browse_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)

                widget_layout.addWidget(path_widget, 1, Qt.AlignVCenter)
                widget_layout.addWidget(status_widget, 0, Qt.AlignVCenter)
                widget_layout.addWidget(browse_button, 0, Qt.AlignVCenter)

                self.context[param["setting"]] = param["value"]
                self.file_fields[param["setting"]] = {
                    "param": param,
                    "path": path_widget,
                    "status": status_widget,
                }

            elif param["type"] == "bool":
                # create spinner
                widget = QCheckBox()
                if param["value"] == True:
                    widget.setCheckState(Qt.Checked)
                    self.context[param["setting"]] = True
                else:
                    widget.setCheckState(Qt.Unchecked)
                    self.context[param["setting"]] = False
                widget.stateChanged.connect(functools.partial(self.bool_value_changed, widget, param))

            elif param["type"] == "dropdown":

                # create spinner
                widget = QComboBox()

                # Get values
                value_list = param["values"]

                # Add normal values
                box_index = 0
                for value_item in value_list:
                    k = value_item["name"]
                    v = value_item["value"]
                    i = value_item.get("icon", None)

                    # add dropdown item
                    widget.addItem(_(k), v)

                    # select dropdown (if default)
                    if v == param["value"]:
                        widget.setCurrentIndex(box_index)

                        # Set initial context
                        self.context[param["setting"]] = param["value"]
                    box_index = box_index + 1

                widget.currentIndexChanged.connect(functools.partial(self.dropdown_index_changed, widget, param))

            # Add Label and Widget to the form
            if widget and label:
                # Add minimum size
                label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

                form_layout.addRow(label, widget)

            elif not widget and label:
                label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
                label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                form_layout.addRow(label)

        # Add error field
        self.error_label = QLabel("", self)
        self.error_label.setStyleSheet("color: red;")
        form_layout.addRow(self.error_label)

        # Add buttons
        self.cancel_button = QPushButton(_('Cancel'))
        self.process_button = QPushButton(_('Process Effect'))
        self.buttonBox.addButton(self.process_button, QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.cancel_button, QDialogButtonBox.RejectRole)
        self.update_file_validation()

        # flag to close the clip processing thread
        self.cancel_clip_processing = False
        self.effect = None

    def link_activated(self, widget, param, value):
        """Link activated"""
        webbrowser.open(value, new=1)

    def spinner_value_changed(self, widget, param, value):
        """Spinner value change callback"""
        self.context[param["setting"]] = value
        log.info(self.context)

    def bool_value_changed(self, widget, param, state):
        """Boolean value change callback"""
        if state == Qt.Checked:
            self.context[param["setting"]] = True
        else:
            self.context[param["setting"]] = False
        log.info(self.context)

    def dropdown_index_changed(self, widget, param, index):
        """Dropdown value change callback"""
        value = widget.itemData(index)
        self.context[param["setting"]] = value
        log.info(self.context)

    def text_value_changed(self, widget, param, value=None):
        """Textbox value change callback"""
        try:
            # Attempt to load value from QTextEdit (i.e. multi-line)
            if not value:
                value = widget.toPlainText()
        except:
            log.debug('Failed to get plain text from widget')

        self.context[param["setting"]] = value
        log.info(self.context)

    def file_value_changed(self, widget, param, value=None):
        """File path textbox change callback"""
        if value is None:
            value = widget.text()
        self.context[param["setting"]] = value
        self.update_file_validation()
        log.info(self.context)

    def file_browse_clicked(self, widget, param):
        """Browse for a file path."""
        _ = get_app()._tr
        current_path = widget.text()
        start_dir = os.path.dirname(current_path) if current_path else info.USER_PATH
        selected_path = QFileDialog.getOpenFileName(
            self,
            _("Choose %s") % _(param["title"]),
            start_dir,
            param.get("file-filter", _("All files (*)")),
        )[0]
        if selected_path:
            widget.setText(selected_path)

    def validate_file_param(self, param, path):
        """Validate a pre-processing file field."""
        if param.get("required") and not path:
            return False, "Required file"
        if not path:
            return True, ""
        if not os.path.isfile(path):
            return False, "File not found"

        validator = param.get("validator")
        if validator == "onnx":
            if not path.lower().endswith(".onnx"):
                return False, "Expected .onnx file"
            file_size = os.path.getsize(path)
            if file_size < 1024 * 1024:
                return False, "ONNX file is too small"
            if os.path.abspath(path) == os.path.abspath(YOLO5_MODEL_PATH) and file_size < YOLO5_MODEL_MIN_SIZE:
                return False, "Expected an FP32 YOLOv5s ONNX model. Please download the compatible model."
        elif validator == "classes":
            try:
                with open(path, "r", encoding="utf-8") as classes_file:
                    class_names = [line.strip() for line in classes_file if line.strip()]
            except OSError:
                return False, "Unable to read class names"
            if not class_names:
                return False, "Class names file is empty"
        return True, "Ready"

    def yolo5_default_files_ready(self):
        """Return whether the default YOLOv5 files exist and pass lightweight validation."""
        model_valid, _ = self.validate_file_param(
            {"validator": "onnx", "required": True},
            YOLO5_MODEL_PATH,
        )
        classes_valid, _ = self.validate_file_param(
            {"validator": "classes", "required": True},
            YOLO5_CLASSES_PATH,
        )
        return model_valid and classes_valid

    def update_file_validation(self):
        """Update validation indicators and Process button state."""
        all_valid = True
        for setting, field in self.file_fields.items():
            path = field["path"].text()
            valid, message = self.validate_file_param(field["param"], path)
            status = field["status"]
            status.setText("✓" if valid else "✕")
            status.setStyleSheet("color: #4caf50; font-weight: bold;" if valid else "color: #e53935; font-weight: bold;")
            status.setToolTip(message)
            all_valid = all_valid and valid

        if hasattr(self, "process_button"):
            self.process_button.setEnabled(all_valid)

    def file_sha256(self, path):
        """Return the SHA256 checksum of a file."""
        digest = hashlib.sha256()
        with open(path, "rb") as input_file:
            for chunk in iter(lambda: input_file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    def download_yolo5_clicked(self, widget, param):
        """Download the default YOLOv5 model files."""
        _ = get_app()._tr
        os.makedirs(YOLO5_DIR, exist_ok=True)

        progress = QProgressDialog(
            _("Downloading YOLOv5 model..."),
            _("Cancel"),
            0,
            100,
            self,
        )
        progress.setWindowTitle(_("Download YOLOv5 Files"))
        progress.setWindowModality(Qt.WindowModal)
        progress.setMinimumDuration(0)

        def report_hook(block_count, block_size, total_size):
            if total_size > 0:
                progress.setValue(min(100, int(block_count * block_size * 100 / total_size)))
                QCoreApplication.processEvents()
            if progress.wasCanceled():
                raise RuntimeError("Download cancelled")

        try:
            zip_download_path = os.path.join(YOLO5_DIR, "yolov5s-openshot.zip.download")
            model_download_path = "{}.download".format(YOLO5_MODEL_PATH)
            classes_download_path = "{}.download".format(YOLO5_CLASSES_PATH)

            urllib.request.urlretrieve(YOLO5_DOWNLOAD_URL, zip_download_path, report_hook)
            if self.file_sha256(zip_download_path) != YOLO5_DOWNLOAD_SHA256:
                raise ValueError("Downloaded YOLOv5 archive checksum did not match")

            with zipfile.ZipFile(zip_download_path) as yolo5_zip:
                for member_name, destination_path in (
                    ("yolov5s.onnx", model_download_path),
                    ("obj.names", classes_download_path),
                ):
                    with yolo5_zip.open(member_name) as source_file, open(destination_path, "wb") as output_file:
                        output_file.write(source_file.read())

            if self.file_sha256(model_download_path) != YOLO5_MODEL_SHA256:
                raise ValueError("Downloaded YOLOv5 model checksum did not match")
            if self.file_sha256(classes_download_path) != YOLO5_CLASSES_SHA256:
                raise ValueError("Downloaded YOLOv5 class names checksum did not match")

            os.replace(model_download_path, YOLO5_MODEL_PATH)
            os.replace(classes_download_path, YOLO5_CLASSES_PATH)
        except Exception as ex:
            for path in (
                os.path.join(YOLO5_DIR, "yolov5s-openshot.zip.download"),
                "{}.download".format(YOLO5_MODEL_PATH),
                "{}.download".format(YOLO5_CLASSES_PATH),
            ):
                if os.path.exists(path):
                    os.remove(path)
            QMessageBox.warning(self, _("Download Failed"), str(ex))
            log.error("Failed to download YOLOv5 files: %s", ex)
            self.update_file_validation()
            return
        finally:
            zip_download_path = os.path.join(YOLO5_DIR, "yolov5s-openshot.zip.download")
            if os.path.exists(zip_download_path):
                os.remove(zip_download_path)
            progress.close()

        for setting, path in (
            (param.get("model-setting"), YOLO5_MODEL_PATH),
            (param.get("classes-setting"), YOLO5_CLASSES_PATH),
        ):
            field = self.file_fields.get(setting)
            if field:
                field["path"].setText(path)
        self.update_file_validation()

    def rect_select_clicked(self, widget, param):
        """Rect select button clicked"""
        _ = get_app()._tr
        self.context[param["setting"]].update({"button-clicked": True})

        # show dialog
        from windows.region import SelectRegion
        from classes.query import File, Clip

        c = Clip.get(id=self.clip_id)
        reader_path = c.data.get('reader', {}).get('path','')
        f = File.get(path=reader_path)
        if f:
            win = SelectRegion(f, self.clip_instance, parent=self)
            # Run the dialog event loop - blocking interaction on this window during that time
            result = win.exec_()
            if result == QDialog.Accepted:
                # self.first_frame = win.current_frame
                # Region selected (get coordinates if any)
                selected_rect = win.selected_rect_normalized() if hasattr(win, "selected_rect_normalized") else None
                if selected_rect:
                    x1 = float(selected_rect.get("normalized_x", 0.0))
                    y1 = float(selected_rect.get("normalized_y", 0.0))
                    xw = float(selected_rect.get("normalized_width", 0.0))
                    yh = float(selected_rect.get("normalized_height", 0.0))
                else:
                    topLeft = win.videoPreview.regionTopLeftHandle
                    bottomRight = win.videoPreview.regionBottomRightHandle
                    curr_frame_size = win.videoPreview.curr_frame_size
                    if not topLeft or not bottomRight or not curr_frame_size:
                        QMessageBox.warning(
                            self,
                            _("Invalid Region"),
                            _("Please draw a rectangle region before clicking Select Region."),
                        )
                        return
                    x1 = topLeft.x() / curr_frame_size.width()
                    y1 = topLeft.y() / curr_frame_size.height()
                    x2 = bottomRight.x() / curr_frame_size.width()
                    y2 = bottomRight.y() / curr_frame_size.height()
                    xw = x2 - x1
                    yh = y2 - y1

                # Get QImage of region
                region_qimage = win.selected_region_qimage() if hasattr(win, "selected_region_qimage") else None
                if region_qimage is None and win.videoPreview.region_qimage:
                    region_qimage = win.videoPreview.region_qimage
                if region_qimage:

                    # Resize QImage to match button size
                    resized_qimage = region_qimage.scaled(widget.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

                    # Remove button text (so region QImage is more visible)
                    widget.setImage(resized_qimage)
                    widget.setText("")

                # If data found, add to context
                self.context[param["setting"]].update({"normalized_x": x1, "normalized_y": y1,
                                                       "normalized_width": xw,
                                                       "normalized_height": yh,
                                                       "first-frame": win.current_frame,
                                                       })
                log.info(self.context)

        else:
            log.error('No file found with path: %s' % reader_path)

    def accept(self):
        """ Start processing effect """
        self.update_file_validation()
        if self.file_fields and not self.process_button.isEnabled():
            return

        # Enable ProgressBar
        self.progressBar.setEnabled(True)
        self.process_button.setEnabled(False)

        # Print effect settings
        log.info(self.context)

        # Create effect Id and protobuf data path
        ID = get_app().project.generate_id()

        # Create protobuf data path
        protobufPath = os.path.join(info.PROTOBUF_DATA_PATH, ID + '.data')
        if os.name == 'nt' : protobufPath = protobufPath.replace("\\", "/")

        self.context["protobuf_data_path"] = protobufPath

        # Load into JSON string info about protobuf data path
        jsonString = json.dumps(self.context)

        # Generate processed data
        processing = openshot.ClipProcessingJobs(self.effect_class, jsonString)
        processing.processClip(self.clip_instance, jsonString)

        # TODO: This is just a temporary fix. We need to find a better way to allow the user to fix the error
        # The while loop is handling the error message. If pre-processing returns an error, a message
        # will be displayed for 3 seconds and the effect will be closed.
        start = time.time()
        while processing.GetError():
            self.error_label.setText(processing.GetErrorMessage())
            self.error_label.repaint()
            if (time.time() - start) > 3:
                self.exporting = False
                processing.CancelProcessing()
                while(not processing.IsDone() ):
                    continue
                super(ProcessEffect, self).reject()

        # get processing status
        while(not processing.IsDone() ):
            # update progressbar
            progressionStatus = processing.GetProgress()
            self.progressBar.setValue(int(progressionStatus))
            time.sleep(0.01)

            # Process any queued events
            QCoreApplication.processEvents()

            # if the cancel button was pressed, close the processing thread
            if(self.cancel_clip_processing):
                processing.CancelProcessing()

        if(not self.cancel_clip_processing):
            # Load processed data into effect
            self.effect = openshot.EffectInfo().CreateEffect(self.effect_class)
            self.effect.SetJson( '{"protobuf_data_path": "%s"}' % protobufPath )
            self.effect.Id(ID)

            # Accept dialog
            super(ProcessEffect, self).accept()

    def reject(self):
        # Cancel dialog
        self.exporting = False
        self.cancel_clip_processing = True
        super(ProcessEffect, self).reject()
