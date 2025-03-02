import tempfile
import uuid
from contextlib import contextmanager
from typing import Any, Generator, List, Optional

import pytest

from mypy_django_plugin.config import DjangoPluginConfig

TEMPLATE = """
(config)
...
[mypy.plugins.django_stubs]
    django_settings_module: str (required)
...
(django-stubs) mypy: error: {}
"""

TEMPLATE_TOML = """
(config)
...
[tool.django-stubs]
django_settings_module = str (required)
...
(django-stubs) mypy: error: {}
"""


@contextmanager
def write_to_file(file_contents: str, suffix: Optional[str] = None) -> Generator[str, None, None]:
    with tempfile.NamedTemporaryFile(mode="w+", suffix=suffix) as config_file:
        config_file.write(file_contents)
        config_file.seek(0)
        yield config_file.name


@pytest.mark.parametrize(
    ("config_file_contents", "message_part"),
    [
        pytest.param(
            ["[not-really-django-stubs]"],
            "no section [mypy.plugins.django-stubs] found",
            id="missing-section",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]", "\tnot_django_not_settings_module = badbadmodule"],
            "missing required 'django_settings_module' config",
            id="missing-settings-module",
        ),
        pytest.param(
            ["[mypy.plugins.django-stubs]"],
            "missing required 'django_settings_module' config",
            id="no-settings-given",
        ),
    ],
)
def test_misconfiguration_handling(capsys: Any, config_file_contents: List[str], message_part: str) -> None:
    """Invalid configuration raises `SystemExit` with a precise error message."""
    contents = "\n".join(config_file_contents).expandtabs(4)
    with write_to_file(contents) as filename:
        with pytest.raises(SystemExit, match="2"):
            DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE.format(message_part)
    assert error_message == capsys.readouterr().err


@pytest.mark.parametrize(
    "filename",
    [
        pytest.param(uuid.uuid4().hex, id="not matching an existing file"),
        pytest.param("", id="as empty string"),
        pytest.param(None, id="as none"),
    ],
)
def test_handles_filename(capsys: Any, filename: str) -> None:
    with pytest.raises(SystemExit, match="2"):
        DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE.format("mypy config file is not specified or found")
    assert error_message == capsys.readouterr().err


@pytest.mark.parametrize(
    ("config_file_contents", "message_part"),
    [
        pytest.param(
            """
            [tool.django-stubs]
            django_settings_module = 123
            """,
            "invalid 'django_settings_module': the setting must be a string",
            id="django_settings_module not string",
        ),
        pytest.param(
            """
            [tool.not-really-django-stubs]
            django_settings_module = "my.module"
            """,
            "no section [tool.django-stubs] found",
            id="missing django-stubs section",
        ),
        pytest.param(
            """
            [tool.django-stubs]
            not_django_not_settings_module = "badbadmodule"
            """,
            "missing required 'django_settings_module' config",
            id="missing django_settings_module",
        ),
        pytest.param(
            "tool.django-stubs]",
            "could not load configuration file",
            id="invalid toml",
        ),
    ],
)
def test_toml_misconfiguration_handling(capsys: Any, config_file_contents, message_part) -> None:
    with write_to_file(config_file_contents, suffix=".toml") as filename:
        with pytest.raises(SystemExit, match="2"):
            DjangoPluginConfig(filename)

    error_message = "usage: " + TEMPLATE_TOML.format(message_part)
    assert error_message == capsys.readouterr().err


def test_correct_toml_configuration() -> None:
    config_file_contents = """
    [tool.django-stubs]
    some_other_setting = "setting"
    django_settings_module = "my.module"
    """

    with write_to_file(config_file_contents, suffix=".toml") as filename:
        config = DjangoPluginConfig(filename)

    assert config.django_settings_module == "my.module"


def test_correct_configuration() -> None:
    """Django settings module gets extracted given valid configuration."""
    config_file_contents = "\n".join(
        [
            "[mypy.plugins.django-stubs]",
            "\tsome_other_setting = setting",
            "\tdjango_settings_module = my.module",
        ]
    ).expandtabs(4)
    with write_to_file(config_file_contents) as filename:
        config = DjangoPluginConfig(filename)

    assert config.django_settings_module == "my.module"
