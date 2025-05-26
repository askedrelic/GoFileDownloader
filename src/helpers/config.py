"""Centralized configuration module for managing constants used across the project.

These configurations aim to improve modularity and readability by consolidating settings
into a single location.
"""

GOFILE_API = "https://api.gofile.io"            # The base URL for the GoFile API.
GOFILE_API_ACCOUNTS = f"{GOFILE_API}/accounts"  # The endpoint for GoFile account
                                                # related operations.
DOWNLOAD_FOLDER = "Downloads"                   # The folder where downloaded files
                                                # will be stored.
URLS_FILE = "URLs.txt"                          # The name of the file containing the
                                                # list of URLs to process.
SESSION_LOG = "session_log.txt"                 # The file used to log session errors.

# Constants for file sizes, expressed in bytes.
KB = 1024
MB = 1024 * KB

# Thresholds for file sizes and corresponding chunk sizes used during download.
# Each tuple represents: (file size threshold, chunk size to download in that range).
THRESHOLDS = [
    (1 * MB, 8 * KB),      # Less than 1 MB
    (10 * MB, 16 * KB),    # 1 MB to 10 MB
    (50 * MB, 64 * KB),    # 10 MB to 50 MB
    (100 * MB, 128 * KB),  # 50 MB to 100 MB
    (250 * MB, 256 * KB),  # 100 MB to 250 MB
]

# Default chunk size for files larger than the largest threshold.
LARGE_FILE_CHUNK_SIZE = 512 * KB

# HTTP status codes.
HTTP_STATUS_OK = 200
