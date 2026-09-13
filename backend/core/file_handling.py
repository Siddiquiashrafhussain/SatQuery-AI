import os
from pathlib import Path
from typing import IO
from .errors import InvalidFileError, UnsupportedFormatError

ALLOWED_EXTENSIONS = {".tif", ".tiff", ".geojson"}
MAX_FILE_SIZE_BYTES = 500 * 1024 * 1024  # 500 MB

def secure_filename(filename: str) -> str:
    """
    Sanitizes a filename to ensure it only contains safe characters.
    """
    filename = os.path.basename(filename)
    safe_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")
    sanitized = "".join(c for c in filename if c in safe_chars)
    if not sanitized:
        raise InvalidFileError("Filename is invalid after sanitization.")
    return sanitized

def validate_and_save_upload(file_obj: IO, filename: str, destination_dir: Path) -> Path:
    """
    Securely validates file type, limits size, and prevents path traversal.
    """
    sanitized_name = secure_filename(filename)
    ext = Path(sanitized_name).suffix.lower()
    
    if ext not in ALLOWED_EXTENSIONS:
        raise UnsupportedFormatError(f"File extension '{ext}' is not allowed for security reasons.")
        
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_path = destination_dir / sanitized_name
    
    # Security: Resolve absolute paths to prevent directory traversal attacks
    resolved_dest = destination_path.resolve()
    resolved_dir = destination_dir.resolve()
    
    if not str(resolved_dest).startswith(str(resolved_dir)):
        raise InvalidFileError("Path traversal attempt detected.")
        
    # Security: Write file in chunks and monitor size
    bytes_written = 0
    with open(resolved_dest, "wb") as out_file:
        while chunk := file_obj.read(8192):
            bytes_written += len(chunk)
            if bytes_written > MAX_FILE_SIZE_BYTES:
                resolved_dest.unlink(missing_ok=True) # Cleanup on failure
                raise InvalidFileError(f"File exceeds maximum allowed size of {MAX_FILE_SIZE_BYTES} bytes.")
            out_file.write(chunk)
            
    return resolved_dest
