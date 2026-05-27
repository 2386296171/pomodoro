import tkinter as tk
from tkinter import ttk
import winsound
from dataclasses import dataclass
from typing import Literal

Mode = Literal["focus", "short_break", "long_break"]
State = Literal["idle", "running", "paused"]


@dataclass
class ModeConfig:
    name: str
    minutes: int
    color: str


MODES: dict[Mode, ModeConfig] = {
    "focus": ModeConfig("工作中", 25, "#e74c3c"),
    "short_break": ModeConfig("短休息", 5, "#2ecc71"),
    "long_break": ModeConfig("长休息", 15, "#3498db"),
}

FOCUS_PER_LONG_BREAK = 4

BG = "#1e1e2e"
FG = "#cdd6f4"
BTN_BG = "#45475a"
BTN_ACTIVE_BG = "#585b70"
FONT = "Microsoft YaHei"
FONT_MONO = "Consolas"
BTN_KWARGS = {"bg": BTN_BG, "fg": FG, "relief": "flat",
              "activebackground": BTN_ACTIVE_BG, "activeforeground": FG}


class PomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("番茄钟")
        self.root.geometry("320x380")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.configure(bg=BG)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.mode: Mode = "focus"
        self.state: State = "idle"
        self.remaining = MODES["focus"].minutes * 60
        self.focus_count = 0
        self._after_id: str = ""

        self._create_widgets()
        self._update_display()
        self.root.mainloop()

    def _make_btn(self, parent, text, command, font_size=10, width=8, **extra):
        return tk.Button(parent, text=text, font=(FONT, font_size),
                         width=width, command=command, **BTN_KWARGS, **extra)

    def _create_widgets(self):
        self.title_label = tk.Label(
            self.root, text="🍅 番茄钟", font=(FONT, 16, "bold"),
            bg=BG, fg=FG,
        )
        self.title_label.pack(pady=(20, 10))

        self.mode_label = tk.Label(
            self.root, text="", font=(FONT, 12), bg=BG,
        )
        self.mode_label.pack(pady=(0, 10))

        self.timer_label = tk.Label(
            self.root, text="25:00", font=(FONT_MONO, 48, "bold"),
            bg=BG, fg=FG,
        )
        self.timer_label.pack(pady=(0, 10))

        style = ttk.Style()
        style.theme_use("default")
        style.configure("TProgressbar", thickness=8)
        self.progress = ttk.Progressbar(
            self.root, mode="determinate", length=240, style="TProgressbar",
        )
        self.progress.pack(pady=(0, 15))

        self.count_label = tk.Label(
            self.root, text="", font=(FONT, 11),
            bg=BG, fg="#f5c2e7",
        )
        self.count_label.pack(pady=(0, 20))

        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack()

        self.start_btn = self._make_btn(btn_frame, "开始", self._start_timer)
        self.start_btn.pack(side=tk.LEFT, padx=4)

        self.pause_btn = self._make_btn(btn_frame, "暂停", self._pause_timer, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=4)

        self.reset_btn = self._make_btn(btn_frame, "重置", self._reset_timer)
        self.reset_btn.pack(side=tk.LEFT, padx=4)

        self.skip_btn = tk.Button(
            self.root, text="跳过休息", font=(FONT, 9),
            width=10, bg="#313244", fg="#a6adc8", relief="flat",
            activebackground=BTN_ACTIVE_BG, activeforeground=FG,
            command=self._skip_break,
        )
        self.skip_btn.pack(pady=(12, 0))
        self.skip_btn.pack_forget()

    def _start_timer(self):
        if self.state in ("idle", "paused"):
            self.state = "running"
            self._tick()
        self._update_buttons()

    def _pause_timer(self):
        if self.state == "running":
            self.state = "paused"
            if self._after_id:
                self.root.after_cancel(self._after_id)
                self._after_id = ""
        self._update_buttons()

    def _reset_timer(self):
        self.state = "idle"
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = ""
        self.remaining = MODES[self.mode].minutes * 60
        self._update_display()
        self._update_buttons()

    def _skip_break(self):
        if self.mode in ("short_break", "long_break"):
            if self._after_id:
                self.root.after_cancel(self._after_id)
                self._after_id = ""
            self.state = "idle"
            self.mode = "focus"
            self.remaining = MODES["focus"].minutes * 60
            self._update_display()
            self._update_buttons()

    def _tick(self):
        if self.state != "running":
            return
        if self.remaining > 0:
            self.remaining -= 1
            self._update_display()
            self._after_id = self.root.after(1000, self._tick)
        else:
            self._on_timer_end()

    def _on_timer_end(self):
        self.state = "idle"
        self._after_id = ""
        self._notify()

        if self.mode == "focus":
            self.focus_count += 1
            if self.focus_count % FOCUS_PER_LONG_BREAK == 0:
                self.mode = "long_break"
            else:
                self.mode = "short_break"
        else:
            self.mode = "focus"

        self.remaining = MODES[self.mode].minutes * 60
        self._update_display()
        self._update_buttons()

    def _notify(self):
        try:
            winsound.MessageBeep(winsound.MB_ICONINFORMATION)
        except Exception:
            pass
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def _update_display(self):
        mins, secs = divmod(self.remaining, 60)
        self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

        cfg = MODES[self.mode]
        self.mode_label.config(text=cfg.name, fg=cfg.color)

        total = cfg.minutes * 60
        elapsed = total - self.remaining
        self.progress["value"] = (elapsed / total) * 100

        tomatoes = "🍅" * self.focus_count if self.focus_count > 0 else "—"
        self.count_label.config(text=f"已完成: {tomatoes}  ({self.focus_count})")

    def _update_buttons(self):
        if self.state == "running":
            self.start_btn.config(state=tk.DISABLED)
            self.pause_btn.config(state=tk.NORMAL)
            self.reset_btn.config(state=tk.NORMAL)
        elif self.state == "paused":
            self.start_btn.config(text="继续", state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.NORMAL)
        else:
            self.start_btn.config(text="开始", state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.reset_btn.config(state=tk.NORMAL)

        if self.mode in ("short_break", "long_break") and self.state in ("idle", "running"):
            self.skip_btn.pack(pady=(12, 0))
        else:
            self.skip_btn.pack_forget()

    def _on_close(self):
        if self._after_id:
            self.root.after_cancel(self._after_id)
        self.root.destroy()


if __name__ == "__main__":
    PomodoroTimer()
