"""The `__about__` module exposes the version of the `{{ cookiecutter.project_slug }}` package:

Example:

```python
from {{ cookiecutter.project_slug }}.__about__ import __version__
print(__version__)
```

Note that container version can also be imported directly from `{{ cookiecutter.project_slug }}` package:

Example:

```python
from {{ cookiecutter.project_slug }} import __version__
print(__version__)
```
"""
__version__ = "0.1.0"
