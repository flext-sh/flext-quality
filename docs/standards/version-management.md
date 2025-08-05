# Version Management Standard

## Overview

All FLEXT projects must use a centralized version management system where version information is read from the package metadata. This ensures consistency and prevents version mismatches.

## Implementation

### 1. Create `__version__.py`

Each project must have a `src/<project_name>/__version__.py` file that reads metadata from the installed package:

```python
"""Version information for <Project Title>.

This file reads version from pyproject.toml metadata.
All version references should import from this file.
"""

import importlib.metadata

# Get metadata from the installed package
_metadata = importlib.metadata.metadata("<project-name>")
__version__ = _metadata["Version"]
__project__ = _metadata["Name"]
__description__ = _metadata["Summary"]
__author__ = _metadata["Author"]
__author_email__ = _metadata["Author-email"].split("<")[1].rstrip(">") if "<" in _metadata.get("Author-email", "") else ""
__maintainer__ = _metadata.get("Maintainer", __author__)
__maintainer_email__ = _metadata.get("Maintainer-email", __author_email__)
__license__ = _metadata.get("License", "MIT")

# Parse version info
_parts = __version__.split(".")
__version_info__ = tuple(int(p) if p.isdigit() else p for p in _parts)
__version_tuple__ = __version_info__

# Fixed metadata
__copyright__ = "Copyright (c) 2025 FLEXT Team. All rights reserved."

# Build information (can be populated by CI/CD)
__build__ = ""
__commit__ = ""
__branch__ = ""

# All exported symbols
__all__ = [
    "__version__",
    "__version_info__",
    "__version_tuple__",
    "__project__",
    "__description__",
    "__author__",
    "__author_email__",
    "__maintainer__",
    "__maintainer_email__",
    "__license__",
    "__copyright__",
    "__build__",
    "__commit__",
    "__branch__",
]
```

### 2. Import in `__init__.py`

The project's `__init__.py` must import version information:

```python
from <project_name>.__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __maintainer__,
    __maintainer_email__,
    __project__,
    __version__,
    __version_info__,
)
```

### 3. Use in CLI

For CLI applications using Click:

```python
@click.group()
@click.version_option()  # Automatically uses __version__ from the package
def cli():
    """Your CLI description."""
```

### 4. Update `pyproject.toml`

The version in `pyproject.toml` is the single source of truth:

```toml
[project]
name = "your-project"
version = "1.0.0"  # This is the only place to update version
```

## Benefits

1. **Single Source of Truth**: Version is defined only in `pyproject.toml`
2. **No Manual Sync**: Version is automatically read from package metadata
3. **Consistent Metadata**: All project metadata is centralized
4. **CI/CD Ready**: Build information can be injected during builds
5. **Type Safe**: All version attributes are properly typed

## Migration Guide

To migrate existing projects:

1. Create `src/<project_name>/__version__.py` using the template
2. Replace `<project-name>` with your actual project name from `pyproject.toml`
3. Update `__init__.py` to import from `__version__.py`
4. Remove any hardcoded version strings from the codebase
5. Update CLI to use `@click.version_option()` without arguments

## Examples

### Reading Version in Code

```python
from myproject import __version__

print(f"Running version {__version__}")
```

### Version Tuple for Comparisons

```python
from myproject import __version_info__

if __version_info__ >= (2, 0, 0):
    # Use v2 features
    pass
```

### Build Information

During CI/CD, you can inject build information:

```python
# In your build script
import myproject
myproject.__build__ = "build-123"
myproject.__commit__ = "abc123def"
myproject.__branch__ = "main"
```

## Template Location

A template file is available at: `flext-quality/templates/__version__.py.template`
