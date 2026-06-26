from typing import Any

from pyiron_snippets import retrieve, versions


def recreate_type(
    module_name: str, qualname: str, version: str, strict_version_check: bool = False
) -> Any:
    if strict_version_check:
        actual_version = versions.get_version(module_name)
        if actual_version != version:
            raise ValueError(f"Version mismatch: {version} != {actual_version}")
    return retrieve.import_from_string(f"{module_name}.{qualname}")


def recreate_obj(
    module: str, qualname: str, version: str, init_args: dict[str, Any]
) -> Any:
    return retrieve.import_from_string(f"{module}.{qualname}")(**init_args)
