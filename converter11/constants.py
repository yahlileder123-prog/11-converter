"""Paths, defaults, and shared literals (no UI)."""

CONFIG_FILE = "config.txt"
COLOR_CONFIG_FILE = "color_config.txt"
APPEARANCE_FILE = "appearance.txt"
HISTORY_FILE = "track_history.json"
LANGUAGE_FILE = "language.txt"
AUDIO_SETTINGS_FILE = "audio_settings.json"

ACCENT_DEFAULT = "#FF7A00"

AUDIO_EXT = (".wav", ".mp3", ".flac", ".aiff", ".aif", ".m4a", ".ogg")
VIDEO_EXT = (".mp4", ".mkv", ".mov", ".webm", ".m4v")

# Human-readable type labels for title bar / UI (extension → label).
EXT_KIND_LABEL = {
    ".mp3": "MP3",
    ".wav": "WAV",
    ".flac": "FLAC",
    ".aiff": "AIFF",
    ".aif": "AIFF",
    ".m4a": "M4A",
    ".ogg": "OGG",
    ".mp4": "MP4",
    ".mkv": "MKV",
    ".mov": "MOV",
    ".webm": "WebM",
    ".m4v": "M4V",
}

# Read only this many bytes for magic-byte / container sniffing (never execute user files).
MEDIA_HEADER_BYTES = 64

AUDIO_SETTINGS_DEFAULT = {
    "sample_rate_hz": 44100,
    "pcm_bit_depth": "24",
    "mp3_cbr_320": True,
    "aac_bitrate_kbps": 256,
    "embed_metadata": True,
    "normalize": False,
    "name_pattern": "{artist} - {title}",
    "name_pattern_parts": ["artist", "title", "skip", "skip"],
    "name_pattern_sep": " - ",
    "name_pattern_advanced": False,
    "name_pattern_format_version": 2,
    "split_by_format": False,
    "allow_video_extract": False,
}

PATTERN_PART_ORDER = ("skip", "artist", "title", "album", "bpm", "key")
PATTERN_SEP_CHOICES = (" - ", " — ", "_", ", ", " · ")
VALID_NAME_PARTS = {"artist", "title", "album", "bpm", "key"}
PATTERN_PREVIEW_META = {
    "artist": "Artist Name",
    "title": "Track Title",
    "album": "Album",
    "bpm": "120",
    "key": "8A",
}

LOCAL_LOG_FILE = "converter11.log"
