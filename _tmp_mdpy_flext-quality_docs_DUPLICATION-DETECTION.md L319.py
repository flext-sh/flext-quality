# from flext-quality/docs/DUPLICATION-DETECTION.md:319
from __future__ import annotations


class Quality:
    class Analysis:
        SIMILARITY_THRESHOLD: float = 0.8  # 80% line overlap
        MIN_FILE_SIZE_FOR_DUPLICATION_CHECK: int = 100
        MIN_FILES_FOR_PAIR_COMPARISON: int = 2  # Need ≥2 files
