"""Background batch conversion: thread entrypoint and per-file export loop."""

import os
import threading
import time
import subprocess
import sys

from pydub import AudioSegment
from tkinter import messagebox

from converter11.audio_engine import (
    export_audio_segment,
    ffmpeg_available,
    fill_export_filename,
    sanitize_filename,
    unique_output_path,
)
from converter11.metadata_manager import embed_mutagen_tags, read_audio_meta
from converter11.security_utils import is_allowed_media_file
from converter11.ui_context import main_module


def run_conversion_thread() -> None:
    m = main_module()
    if m.is_converting or m.last_export_path == "NOT SET":
        messagebox.showwarning(m.t("window_title"), m.t("msg_warn_convert"))
        return
    if not m.selected_files_globally:
        messagebox.showwarning(m.t("window_title"), m.t("msg_warn_convert"))
        return
    marked = [
        p
        for p in m.selected_files_globally
        if m._norm_path_key(p) not in m.queue_excluded_from_convert
    ]
    if not marked:
        messagebox.showwarning(m.t("window_title"), m.t("msg_none_marked_convert"))
        return
    allow_v = bool(m.audio_settings.get("allow_video_extract"))
    eligible = [p for p in marked if is_allowed_media_file(p, allow_v)]
    if not eligible:
        messagebox.showwarning(m.t("window_title"), m.t("msg_invalid_files_all"))
        return
    if not ffmpeg_available():
        messagebox.showwarning(m.t("window_title"), m.t("msg_ffmpeg_missing"))
        return
    m.is_converting = True
    m.convert_btn.configure(text=m.t("btn_converting"), state="disabled")
    m.progress_bar.set(0)
    threading.Thread(target=process_files, daemon=True).start()


def process_files() -> None:
    m = main_module()
    try:
        from pydub.effects import normalize as pydub_normalize
    except Exception:
        pydub_normalize = None

    target = m.format_option.get().split()[0].lower()
    if "m4a" in target:
        target = "m4a"

    sr = int(m.audio_settings.get("sample_rate_hz", 44100))
    bd = str(m.audio_settings.get("pcm_bit_depth", "24"))

    allow_v = bool(m.audio_settings.get("allow_video_extract"))
    queue_list = []
    for x in m.selected_files_globally:
        if m._norm_path_key(x) in m.queue_excluded_from_convert:
            continue
        if is_allowed_media_file(x, allow_v):
            queue_list.append(x)
        else:
            m._append_local_log(f"convert skip (header): {x!r}")
    if not queue_list:
        m.selected_files_globally = []
        m.is_converting = False
        m.app.after(
            0,
            lambda: m.convert_btn.configure(text=m.t("btn_convert"), state="normal"),
        )
        m.app.after(
            0,
            lambda: messagebox.showwarning(
                m.t("window_title"), m.t("msg_invalid_files_all")
            ),
        )
        m.update_ui_paths()
        return

    total = len(queue_list)
    if not os.path.exists(m.last_export_path):
        os.makedirs(m.last_export_path)

    start_time = time.time()

    for i, f in enumerate(queue_list, 1):
        try:
            elapsed = time.time() - start_time
            avg_time_per_file = elapsed / i if i > 1 else elapsed
            remaining_files = total - i + 1
            eta_seconds = int(avg_time_per_file * remaining_files)

            eta_str = (
                f'{m.t("eta")} {time.strftime("%M:%S", time.gmtime(eta_seconds))}'
                if i > 1
                else m.t("eta_calc")
            )

            songs_done_before = i - 1
            done_pct = m._pct(songs_done_before, total)
            rem_pct = max(0, 100 - done_pct)
            m.update_progress(
                m.t(
                    "progress_active",
                    done=songs_done_before,
                    total=total,
                    done_pct=done_pct,
                    rem_pct=rem_pct,
                ),
                (i - 1) / total,
                eta_str,
            )

            meta = read_audio_meta(f)
            base_name = os.path.basename(f)
            song_name, src_ext = os.path.splitext(base_name)

            pat = m.audio_settings.get("name_pattern") or "{artist} - {title}"
            base_fn = fill_export_filename(pat, meta, song_name)
            base_fn = sanitize_filename(base_fn)

            out_root = m.last_export_path
            if m.audio_settings.get("split_by_format"):
                submap = {
                    "wav": "WAV",
                    "mp3": "MP3",
                    "flac": "FLAC",
                    "aiff": "AIFF",
                    "aif": "AIFF",
                    "m4a": "M4A",
                }
                sub = submap.get(target, "Export")
                out_root = os.path.join(m.last_export_path, sub)
                os.makedirs(out_root, exist_ok=True)

            ext_out = "m4a" if target == "m4a" else target
            out_path = unique_output_path(out_root, base_fn, ext_out)

            audio = AudioSegment.from_file(f)
            if m.audio_settings.get("normalize") and pydub_normalize:
                audio = pydub_normalize(audio)
            export_audio_segment(
                audio,
                out_path,
                target,
                sr,
                bd,
                aac_bitrate_kbps=int(
                    m.audio_settings.get("aac_bitrate_kbps", 256) or 256
                ),
            )
            del audio
            embed_mutagen_tags(
                out_path,
                meta,
                target,
                embed_metadata=bool(m.audio_settings.get("embed_metadata")),
            )
        except Exception as e:
            m._append_local_log(f"convert error: {e!r}")

    m.update_progress(m.t("progress_done"), 1.0, "")
    m.selected_files_globally = []
    m.is_converting = False
    m.app.after(
        0,
        lambda: m.convert_btn.configure(text=m.t("btn_convert"), state="normal"),
    )
    m.update_ui_paths(skip_progress_sync=True)

    # Open output folder when done (instant feedback).
    def _open_output_folder() -> None:
        try:
            out_dir = m.last_export_path
            if out_dir and out_dir != "NOT SET" and os.path.isdir(out_dir):
                if os.name == "nt":
                    os.startfile(out_dir)  # type: ignore[attr-defined]
                elif sys.platform == "darwin":
                    subprocess.run(["open", out_dir], check=False)
                else:
                    subprocess.run(["xdg-open", out_dir], check=False)
        except Exception:
            pass

    m.app.after(0, _open_output_folder)
