# ios-like phone simulator (UI mock) using PySide6
# NOTE: This does NOT emulate iOS. It only mimics the look/feel for demos.
# Run:  pip install PySide6
#       python phone.py

import sys, os, glob
from PySide6.QtCore import Qt, QSize, QUrl
from PySide6.QtGui import QFont, QPixmap, QFontMetrics
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QPushButton, QLabel, QStackedWidget, QFrame, QSizePolicy, QSlider
)
from PySide6.QtMultimedia import QMediaDevices, QCamera, QMediaCaptureSession, QImageCapture, QSoundEffect
from PySide6.QtMultimediaWidgets import QVideoWidget

APP_GRID = [
    ("Messages", "💬"), ("Calendar", "📅"), ("Photos", "🖼️"), ("Camera", "📷"),
    ("Mail", "✉️"), ("Clock", "⏰"), ("Maps", "🗺️"), ("Notes", "📝"),
    ("Reminders", "✅"), ("App Store", "🛒"), ("Music", "🎵"), ("Settings", "⚙️"),
]

# Project-local photo storage
PHOTOS_DIR = os.path.join(os.path.dirname(__file__), "photos")
os.makedirs(PHOTOS_DIR, exist_ok=True)

# Single short "peep" tone (WAV) for keypad clicks — generated on first run
PEEP_PATH = os.path.join(os.path.dirname(__file__), "peep.wav")

def _ensure_peep_wav(path=PEEP_PATH, freq=1200, duration_s=0.09, sr=22050, amp=10000):
    if os.path.exists(path):
        return path
    import wave, struct, math
    n = int(duration_s*sr)
    with wave.open(path, 'w') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(sr)
        for i in range(n):
            t = i/sr
            val = int(amp*math.sin(2*math.pi*freq*t))
            w.writeframes(struct.pack('<h', val))
    return path

class TonePlayer:
    def __init__(self):
        _ensure_peep_wav()
        self.eff = QSoundEffect()
        self.eff.setSource(QUrl.fromLocalFile(PEEP_PATH))
        self.eff.setLoopCount(1)
        self.set_volume(0.6)
    def set_volume(self, v: float):
        # clamp 0..1
        self.eff.setVolume(max(0.0, min(1.0, float(v))))
    def play(self):
        if self.eff.isPlaying():
            self.eff.stop()
        self.eff.play()

class Pill(QFrame):
    def __init__(self, w=120, h=5):
        super().__init__()
        self.setFixedSize(w, h)
        self.setStyleSheet("background: rgba(255,255,255,.9); border-radius: %dpx;" % (h//2))

class Notch(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(38)
        self.setStyleSheet("background: black; border-bottom-left-radius: 20px; border-bottom-right-radius: 20px;")

class StatusBar(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.setContentsMargins(12, 6, 12, 6)
        time = QLabel("09:41")
        time.setStyleSheet("color: white; font-weight: 600;")
        right = QLabel("📶  📡  🔋")
        right.setStyleSheet("color: white;")
        self.addWidget(time)
        self.addStretch(1)
        self.addWidget(right)


class ToggleButton(QPushButton):
    def __init__(self, label, emoji, initial=False, on_toggle=None):
        super().__init__(f"{emoji}\n{label}")
        self.active = initial
        self.on_toggle = on_toggle
        self.setCheckable(True)
        self.setChecked(initial)
        self.setCursor(Qt.PointingHandCursor)
        self.setMinimumSize(72, 72)
        self.refresh()
        self.clicked.connect(self.flip)

    def flip(self):
        self.active = not self.active
        self.refresh()
        if self.on_toggle:
            self.on_toggle(self.active)

    def refresh(self):
        bg = "rgba(255,255,255,.28)" if self.active else "rgba(255,255,255,.12)"
        br = 18
        self.setStyleSheet(
            f"""
            QPushButton {{ background: {bg}; color: white; border: none; border-radius: {br}px; padding: 8px; font-weight:600; }}
            QPushButton:pressed {{ background: rgba(255,255,255,.35); }}
            """
        )

class ControlCenter(QFrame):
    """A translucent full-window overlay with a CC panel.
    Click outside the panel or press Esc to dismiss.
    """
    def __init__(self, host_window):
        super().__init__(host_window)
        self.host = host_window
        self.setObjectName("cc_backdrop")
        self.setStyleSheet(
            """
            QFrame#cc_backdrop { background: rgba(0,0,0,.45); }
            QFrame#cc_panel {
                background: rgba(20,24,35,.92);
                border-radius: 24px; border: 1px solid rgba(255,255,255,.08);
            }
            QLabel { color: white; }
            """
        )
        self.setAttribute(Qt.WA_TransparentForMouseEvents, False)

        # Container layout
        root = QVBoxLayout(self)
        root.setContentsMargins(16, 16, 16, 24)
        root.addStretch(1)

        # Panel
        self.panel = QFrame(self)
        self.panel.setObjectName("cc_panel")
        panel_layout = QVBoxLayout(self.panel)
        panel_layout.setContentsMargins(16, 16, 16, 16)

        grid = QGridLayout(); grid.setSpacing(10)

        # row 0: connectivity toggles
        self.wifi = ToggleButton("Wi‑Fi", "📶", True)
        self.bt   = ToggleButton("Bluetooth", "🅱️")
        self.ap   = ToggleButton("Airplane", "✈️")
        self.lock = ToggleButton("Rotation", "🔒")
        grid.addWidget(self.wifi, 0, 0)
        grid.addWidget(self.bt,   0, 1)
        grid.addWidget(self.ap,   0, 2)
        grid.addWidget(self.lock, 0, 3)

        # row 1: brightness + volume sliders
        sliders = QHBoxLayout()
        b_wrap = QVBoxLayout(); b_label = QLabel("Brightness");
        self.brightness = QSlider(Qt.Horizontal); self.brightness.setRange(0,100); self.brightness.setValue(80)
        self.brightness.setStyleSheet("QSlider { color: white; }")
        b_wrap.addWidget(b_label); b_wrap.addWidget(self.brightness)

        v_wrap = QVBoxLayout(); v_label = QLabel("Volume");
        self.volume = QSlider(Qt.Horizontal); self.volume.setRange(0,100); self.volume.setValue(60)
        self.volume.setStyleSheet("QSlider { color: white; }")
        v_wrap.addWidget(v_label); v_wrap.addWidget(self.volume)

        sliders.addLayout(b_wrap)
        sliders.addSpacing(12)
        sliders.addLayout(v_wrap)

        # row 2: utilities
        util = QHBoxLayout()
        self.focus = ToggleButton("Focus", "🛌")
        self.dark  = ToggleButton("Dark Mode", "🌙", True, on_toggle=self.toggle_dark)
        self.flash = ToggleButton("Flashlight", "🔦")
        self.calc  = ToggleButton("Calculator", "🧮")
        util.addWidget(self.focus)
        util.addWidget(self.dark)
        util.addWidget(self.flash)
        util.addWidget(self.calc)

        panel_layout.addLayout(grid)
        panel_layout.addSpacing(8)
        panel_layout.addLayout(sliders)
        panel_layout.addSpacing(8)
        panel_layout.addLayout(util)

        root.addWidget(self.panel)

    def toggle_dark(self, active: bool):
        # Switch overall window background subtly
        if active:
            self.host.setStyleSheet(self.host.styleSheet().replace("#f5f7fb", "#0b0f1a"))
        else:
            self.host.setStyleSheet(self.host.styleSheet().replace("#0b0f1a", "#f5f7fb"))

    def resize_to_parent(self):
        self.setGeometry(0, 0, self.host.width(), self.host.height())
        # panel width ~ 90% of window, height ~ 45%
        pw = int(self.host.width()*0.92)
        ph = int(self.host.height()*0.46)
        self.panel.setFixedSize(pw, ph)

    def mousePressEvent(self, e):
        # Dismiss when clicking outside panel
        if not self.panel.geometry().contains(e.pos()):
            self.hide()
        super().mousePressEvent(e)

class AppIcon(QPushButton):
    def __init__(self, label, emoji, on_open):
        super().__init__(f"{emoji}\n{label}")
        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(64, 64)
        self.setStyleSheet(
            """
            QPushButton { background: rgba(255,255,255,.15); color: white; border: none; border-radius: 18px; padding: 6px; }
            QPushButton:hover { background: rgba(255,255,255,.25); }
            """
        )
        self.clicked.connect(on_open)

class NavBar(QHBoxLayout):
    def __init__(self, title, on_home):
        super().__init__()
        self.setContentsMargins(0,0,0,0)
        back = QPushButton("◁ Home")
        back.setCursor(Qt.PointingHandCursor)
        back.setStyleSheet("color: white; background: transparent; border: none; padding: 10px 14px; font-weight:600;")
        back.clicked.connect(on_home)
        t = QLabel(title)
        t.setStyleSheet("color: white; font-weight: 700;")
        self.addWidget(back)
        self.addStretch(1)
        self.addWidget(t)
        self.addStretch(10)

class AppPage(QWidget):
    def __init__(self, title, body_text, on_home):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16,16,16,16)
        navbar = QHBoxLayout()
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar(title, on_home))
        lay.addWidget(navbar_widget)

        content = QLabel(body_text)
        content.setWordWrap(True)
        content.setStyleSheet("color: white; font-size: 16px;")
        lay.addSpacing(12)
        lay.addWidget(content)
        lay.addStretch(1)


class DialerPage(QWidget):
    def __init__(self, on_home, host_shell):
        super().__init__()
        self.on_home = on_home
        self.host = host_shell
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16,16,16,16)

        # Nav bar
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Phone", on_home))
        lay.addWidget(navbar_widget)

        # Number display
        self.display = QLabel("")
        self.display.setAlignment(Qt.AlignCenter)
        self.display.setWordWrap(False)
        self.display.setStyleSheet("color:white; font-size:24px; letter-spacing:2px; font-weight:600;")
        self.display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.display.setMinimumHeight(40)
        self.display.setMaximumHeight(48)
        lay.addWidget(self.display)
        self.metrics = QFontMetrics(self.display.font())
        self._full_number = ""

        grid = QGridLayout(); grid.setSpacing(10)
        keys = [
            ['1','2','3'],
            ['4','5','6'],
            ['7','8','9'],
            ['*','0','#']
        ]
        for r, row in enumerate(keys):
            for c, k in enumerate(row):
                btn = QPushButton(k)
                btn.setMinimumSize(80,80)
                btn.setMaximumHeight(88)
                btn.setCursor(Qt.PointingHandCursor)
                btn.setStyleSheet(
                    """
                    QPushButton { 
                        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(255,255,255,.20), stop:1 rgba(255,255,255,.12));
                        color:white; border:none; border-radius:28px; font-size:22px; font-weight:600; padding:14px 0; 
                    }
                    QPushButton:pressed { background: rgba(255,255,255,.28); }
                    """
                )
                btn.clicked.connect(lambda _, ch=k: self.press(ch))
                grid.addWidget(btn, r, c)
        grid_wrap = QWidget(); grid_wrap.setLayout(grid)
        lay.addWidget(grid_wrap, 1)

        # bottom actions
        actions = QHBoxLayout()
        del_btn = QPushButton('⌫')
        del_btn.setFixedSize(60,60)
        del_btn.setStyleSheet("color:white; background: rgba(255,255,255,.16); border:none; border-radius:30px; font-size:22px;")
        del_btn.clicked.connect(self.backspace)

        call_btn = QPushButton('📞')
        call_btn.setFixedSize(72,72)
        call_btn.setStyleSheet("background:#34C759; color:#0b0f1a; border:none; border-radius:36px; font-size:26px; font-weight:700;")
        call_btn.clicked.connect(self.call)

        actions.addStretch(1)
        actions.addWidget(del_btn)
        actions.addSpacing(18)
        actions.addWidget(call_btn)
        actions.addStretch(1)
        act_wrap = QWidget(); act_wrap.setLayout(actions)
        lay.addWidget(act_wrap)
        lay.addStretch(1)

        # simple keypad tone (peep)
        self.tone = TonePlayer()

    def press(self, ch):
        self._full_number += ch
        elided = self.metrics.elidedText(self._full_number, Qt.ElideLeft, self.display.width()-16)
        self.display.setText(elided)
        # volume ties to Control Center slider if present
        try:
            vol = self.host.control_center.volume.value()/100.0
        except Exception:
            vol = 0.6
        self.tone.set_volume(vol)
        self.tone.play()

    def backspace(self):
        if self._full_number:
            self._full_number = self._full_number[:-1]
            elided = self.metrics.elidedText(self._full_number, Qt.ElideLeft, self.display.width()-16)
            self.display.setText(elided)

    def call(self):
        # Simple fake call feedback
        number = self._full_number or "(empty)"
        self.display.setText(f"Calling {number}…")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        elided = self.metrics.elidedText(self._full_number, Qt.ElideLeft, self.display.width()-16)
        self.display.setText(elided)


# === App Pages (moved here for better organization) ===
class MessagesPage(QWidget):
    def __init__(self, on_home):
        super().__init__()
        lay = QVBoxLayout(self)
        lay.setContentsMargins(16,16,16,16)
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Messages", on_home))
        lay.addWidget(navbar_widget)
        list_layout = QVBoxLayout()
        for name in ["Finn", "Pace", "Teacher", "Mom"]:
            btn = QPushButton(f"💬  {name}")
            btn.setStyleSheet("color:white; background: rgba(255,255,255,.12); border:none; border-radius:12px; padding:12px; text-align:left;")
            btn.clicked.connect(lambda _, n=name: self.open_chat(n))
            list_layout.addWidget(btn)
        wrap = QWidget(); wrap.setLayout(list_layout)
        lay.addWidget(wrap)
        lay.addStretch(1)

    def open_chat(self, name):
        dlg = QLabel(f"Chat with {name}:\nThis is a demo conversation.")
        dlg.setStyleSheet("color:white; padding:12px;")
        dlg.setWindowTitle("Chat")
        dlg.setMinimumWidth(260)
        dlg.show()
        self._last = dlg

class PhotosPage(QWidget):
    def __init__(self, on_home):
        super().__init__()
        self.on_home = on_home
        self.grid_wrap = QWidget()
        self.grid = QGridLayout(); self.grid.setSpacing(8)
        lay = QVBoxLayout(self); lay.setContentsMargins(16,16,16,16)
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Photos", on_home))
        lay.addWidget(navbar_widget)
        self.grid_wrap.setLayout(self.grid)
        lay.addWidget(self.grid_wrap)
        lay.addStretch(1)
        self.refresh()

    def refresh(self):
        # Clear grid
        while self.grid.count():
            item = self.grid.takeAt(0)
            w = item.widget()
            if w:
                w.setParent(None)
        # Load images
        files = sorted(glob.glob(os.path.join(PHOTOS_DIR, "*.jpg")) + glob.glob(os.path.join(PHOTOS_DIR, "*.png")), reverse=True)
        if not files:
            ph = QLabel("No photos yet. Capture from Camera app.")
            ph.setStyleSheet("color: #cccccc;")
            self.grid.addWidget(ph, 0, 0)
            return
        # Add thumbnails
        col_count = 4
        for i, path in enumerate(files):
            pix = QPixmap(path)
            if not pix.isNull():
                thumb = pix.scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                lbl = QLabel(); lbl.setPixmap(thumb); lbl.setMinimumSize(80,80)
                lbl.setStyleSheet("background: #111; border-radius: 8px;")
                self.grid.addWidget(lbl, i // col_count, i % col_count)

    def showEvent(self, ev):
        super().showEvent(ev)
        # Refresh thumbnails every time Photos is shown
        self.refresh()

class SafariPage(QWidget):
    def __init__(self, on_home):
        super().__init__()
        import webbrowser
        lay = QVBoxLayout(self); lay.setContentsMargins(16,16,16,16)
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Safari", on_home))
        lay.addWidget(navbar_widget)
        hint = QLabel("Open external link in your default browser:")
        hint.setStyleSheet("color:white;")
        lay.addWidget(hint)
        open_btn = QPushButton("Open https://example.com")
        open_btn.setStyleSheet("color:#0b0f1a; background:white; border:none; border-radius:10px; padding:12px; font-weight:700;")
        open_btn.clicked.connect(lambda: webbrowser.open("https://example.com"))
        lay.addWidget(open_btn)
        lay.addStretch(1)

class MusicPage(QWidget):
    def __init__(self, on_home):
        super().__init__()
        lay = QVBoxLayout(self); lay.setContentsMargins(16,16,16,16)
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Music", on_home))
        lay.addWidget(navbar_widget)
        self.state = QLabel("Stopped")
        self.state.setAlignment(Qt.AlignCenter)
        self.state.setStyleSheet("color:white; font-size:22px;")
        lay.addWidget(self.state)
        controls = QHBoxLayout()
        play = QPushButton("Play/Pause")
        play.setStyleSheet("color:white; background: rgba(255,255,255,.15); border:none; border-radius:12px; padding:12px;")
        play.clicked.connect(self.toggle)
        ctr_wrap = QWidget(); ctr_wrap.setLayout(controls)
        controls.addStretch(1); controls.addWidget(play); controls.addStretch(1)
        lay.addWidget(ctr_wrap)
        lay.addStretch(1)

    def toggle(self):
        self.state.setText("Playing" if self.state.text() != "Playing" else "Paused")


# === Camera Page ===
class CameraPage(QWidget):
    def __init__(self, on_home):
        super().__init__()
        lay = QVBoxLayout(self); lay.setContentsMargins(16,16,16,16)
        navbar_widget = QWidget(); navbar_widget.setLayout(NavBar("Camera", on_home))
        lay.addWidget(navbar_widget)

        # Video preview
        self.video = QVideoWidget()
        self.video.setMinimumHeight(360)
        lay.addWidget(self.video, 1)

        # Capture controls
        controls = QHBoxLayout()
        capture_btn = QPushButton("Capture")
        capture_btn.setStyleSheet("color:#0b0f1a; background:white; border:none; border-radius:10px; padding:12px; font-weight:700;")
        capture_btn.clicked.connect(self.capture)

        flip_btn = QPushButton("Flip Camera")
        flip_btn.setStyleSheet("color:white; background: rgba(255,255,255,.15); border:none; border-radius:10px; padding:12px;")
        flip_btn.clicked.connect(self.flip_camera)

        mirror_btn = QPushButton("Mirror Preview")
        mirror_btn.setCheckable(True)
        mirror_btn.setStyleSheet("color:white; background: rgba(255,255,255,.15); border:none; border-radius:10px; padding:12px;")
        mirror_btn.toggled.connect(self.set_mirrored)

        controls.addStretch(1)
        controls.addWidget(flip_btn)
        controls.addSpacing(8)
        controls.addWidget(mirror_btn)
        controls.addSpacing(8)
        controls.addWidget(capture_btn)
        controls.addStretch(1)
        ctr = QWidget(); ctr.setLayout(controls)
        lay.addWidget(ctr)

        # Set up camera(s)
        try:
            self.devices = list(QMediaDevices.videoInputs())
            self.current_index = 0
            # Prefer a front-facing device if present
            for i, dev in enumerate(self.devices):
                try:
                    if hasattr(dev, 'position') and dev.position() == dev.Position.FrontFace:
                        self.current_index = i
                        break
                except Exception:
                    pass

            self.session = QMediaCaptureSession()
            self.imageCapture = QImageCapture()
            self.session.setImageCapture(self.imageCapture)
            self.session.setVideoOutput(self.video)

            self.camera = None
            self.apply_camera(self.current_index)
        except Exception as e:
            err = QLabel(f"Camera unavailable: {e}")
            err.setStyleSheet("color:#ffb3b3;")
            lay.addWidget(err)

    def capture(self):
        from datetime import datetime
        fname = datetime.now().strftime("iossim_%Y%m%d_%H%M%S.jpg")
        out = os.path.join(PHOTOS_DIR, fname)
        try:
            self.imageCapture.captureToFile(out)
            msg = QLabel(f"Saved to {out}")
            msg.setStyleSheet("color:white; padding:6px;")
            self.layout().addWidget(msg)
            self._last_msg = msg
            # If a PhotosPage exists in the shell, ask it to refresh next time
            try:
                self.host = self.parent()
            except Exception:
                self.host = None
        except Exception as e:
            msg = QLabel(f"Failed to save: {e}")
            msg.setStyleSheet("color:#ffb3b3; padding:6px;")
            self.layout().addWidget(msg)
            self._last_msg = msg

    def apply_camera(self, idx: int):
        # Stop previous camera
        try:
            if self.camera:
                self.camera.stop()
        except Exception:
            pass
        self.current_index = max(0, min(idx, len(self.devices)-1))
        dev = self.devices[self.current_index] if self.devices else None
        self.camera = QCamera(dev) if dev is not None else QCamera()
        self.session.setCamera(self.camera)
        self.camera.start()

    def flip_camera(self):
        if not getattr(self, 'devices', None):
            return
        next_idx = (self.current_index + 1) % len(self.devices)
        self.apply_camera(next_idx)

    def set_mirrored(self, on: bool):
        # QVideoWidget has no direct mirror; we can rotate/transform using stylesheet hacks.
        # Use scaleX(-1) via Qt's graphics transform by flipping with Qt property on the widget.
        self.video.setStyleSheet("transform: scaleX(-1);" if on else "")

class HomePage(QWidget):
    def __init__(self, open_app):
        super().__init__()
        v = QVBoxLayout(self)
        v.setContentsMargins(18,10,18,10)

        # Status bar over gradient
        status_wrap = QWidget(); status_layout = QVBoxLayout(status_wrap); status_layout.setContentsMargins(0,0,0,0)
        notch = Notch()
        status_bar = QWidget(); status_bar.setLayout(StatusBar())
        status_wrap_layout = QVBoxLayout(); status_wrap_layout.setContentsMargins(0,0,0,0)
        status_wrap_layout.addWidget(notch)
        status_wrap_layout.addWidget(status_bar)
        status_wrap.setLayout(status_wrap_layout)
        v.addWidget(status_wrap)

        grid = QGridLayout(); grid.setSpacing(14)
        row, col = 0, 0
        for name, emoji in APP_GRID:
            def make_open(n=name):
                return lambda: open_app(n)
            grid.addWidget(AppIcon(name, emoji, make_open()), row, col)
            col += 1
            if col == 4:
                col = 0; row += 1
        grid_wrap = QWidget(); grid_wrap.setLayout(grid)
        v.addWidget(grid_wrap)
        v.addStretch(1)

        dock = QHBoxLayout()
        for name in ["Phone", "Safari", "Music", "Settings"]:
            def make_open(n=name):
                return lambda: open_app(n)
            btn = AppIcon(
                name,
                "📱" if name=="Phone" else ("🧭" if name=="Safari" else ("🎵" if name=="Music" else "⚙️")),
                make_open()
            )
            btn.setFixedHeight(70)
            dock.addWidget(btn)
        dock_wrap = QFrame(); dock_wrap.setLayout(dock)
        dock_wrap.setStyleSheet("background: rgba(0,0,0,.25); border-radius: 24px; padding: 10px;")
        v.addWidget(dock_wrap)

        v.addSpacing(8)
        v.addWidget(Pill(120,5), alignment=Qt.AlignHCenter)

class PhoneShell(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("iOS‑like Simulator (Python)")
        self.resize(420, 860)
        self.setStyleSheet(
            """
            QMainWindow { background: #0b0f1a; } /* dark default; toggler may swap to #f5f7fb */
            QWidget#glass {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #1c2541, stop:0.5 #3a506b, stop:1 #0b132b);
                border-radius: 36px; border: 1px solid rgba(255,255,255,.08);
            }
            """
        )

        # prepare Control Center overlay (hidden by default)
        self.control_center = ControlCenter(self)

        # phone body
        body = QFrame(); body.setObjectName("glass")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(0, 10, 0, 14)

        self.pages = QStackedWidget()
        self.home = HomePage(self.open_app)
        self.pages.addWidget(self.home)

        body_layout.addWidget(self.pages)

        wrap = QVBoxLayout()
        wrap.setContentsMargins(14,14,14,14)
        wrap.addWidget(body)

        root = QWidget(); root.setLayout(wrap)
        self.setCentralWidget(root)

        # Ensure overlay matches window size
        self.control_center.resize_to_parent()

        # Pre-create a few app pages
        self.app_pages = {}
        self.ensure_app("Settings", "All your toggles live here.\nThis is a demo UI – not a real iOS emulator.")
        self.ensure_app("Messages", "")
        self.ensure_app("Photos", "")
        self.ensure_app("Camera", "")
        self.ensure_app("Music", "")
        self.ensure_app("Phone", "")
        self.ensure_app("Safari", "")

    def ensure_app(self, name, body):
        if name in self.app_pages:
            return
        if name == "Phone":
            page = DialerPage(self.go_home, self)
        elif name == "Messages":
            page = MessagesPage(self.go_home)
        elif name == "Photos":
            page = PhotosPage(self.go_home)
        elif name == "Camera":
            page = CameraPage(self.go_home)
        elif name == "Music":
            page = MusicPage(self.go_home)
        elif name == "Safari":
            page = SafariPage(self.go_home)
        else:
            page = AppPage(name, body, self.go_home)
        self.app_pages[name] = page
        self.pages.addWidget(page)

    def open_app(self, name):
        self.ensure_app(name, f"{name} app placeholder.")
        self.pages.setCurrentWidget(self.app_pages[name])

    def go_home(self):
        self.pages.setCurrentWidget(self.home)

    def toggle_control_center(self, show: bool | None = None):
        if show is None:
            show = not self.control_center.isVisible()
        if show:
            self.control_center.resize_to_parent()
            self.control_center.raise_()
            self.control_center.show()
        else:
            self.control_center.hide()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'control_center'):
            self.control_center.resize_to_parent()

    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Escape, Qt.Key_Home):
            self.go_home()
        elif e.key() == Qt.Key_C:  # quick toggle Control Center
            self.toggle_control_center()
        else:
            super().keyPressEvent(e)

    def mousePressEvent(self, e):
        pos = e.position() if hasattr(e, 'position') else e.localPos()
        x = pos.x(); y = pos.y()
        if y <= 90 and x >= self.width() * 0.65:
            self.toggle_control_center(True)
            return
        super().mousePressEvent(e)


def main():
    app = QApplication(sys.argv)
    try:
        f = QFont("SF Pro Text")
        if f.family() and f.family() != ".AppleSystemUIFont":
            app.setFont(f)
    except Exception:
        pass
    w = PhoneShell()
    w.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()