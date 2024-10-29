"""Utility methods"""

import collections
import re
import unicodedata
from typing import Any, Dict, Optional

_WHITESPACE_PATTERN = re.compile(r"(\s+)")
_WHITESPACE_SEPARATOR = " "

_TEMPLATE_SYNTAX = re.compile(r".*[(){}<>\[\]|].*")


def merge_dict(base_dict, new_dict):
    """Merges new_dict into base_dict."""
    for key, value in new_dict.items():
        if key in base_dict:
            old_value = base_dict[key]
            if isinstance(old_value, collections.abc.MutableMapping):
                # Combine dictionary
                assert isinstance(
                    value, collections.abc.Mapping
                ), f"Not a dict: {value}"
                merge_dict(old_value, value)
            elif isinstance(old_value, collections.abc.MutableSequence):
                # Combine list
                assert isinstance(
                    value, collections.abc.Sequence
                ), f"Not a list: {value}"
                old_value.extend(value)
            else:
                # Overwrite
                base_dict[key] = value
        else:
            base_dict[key] = value


def remove_escapes(text: str) -> str:
    """Remove backslash escape sequences."""
    return re.sub(r"\\(.)", r"\1", text)


def normalize_whitespace(text: str) -> str:
    """Makes all whitespace inside a string single spaced."""
    return _WHITESPACE_PATTERN.sub(_WHITESPACE_SEPARATOR, text)


def normalize_text(text: str) -> str:
    """Normalize whitespace and unicode forms."""
    text = normalize_whitespace(text)
    text = text.casefold()
    text = unicodedata.normalize("NFC", text)

    return text


def is_template(text: str) -> bool:
    """True if text contains template syntax"""
    return _TEMPLATE_SYNTAX.match(text) is not None


def check_required_context(
    required_context: Dict[str, Any],
    match_context: Optional[Dict[str, Any]],
    allow_missing_keys: bool = False,
) -> bool:
    """Return True if match context does not violate required context.

    Setting allow_missing_keys to True only checks existing keys in match
    context.
    """
    for (
        required_key,
        required_value,
    ) in required_context.items():
        if (not match_context) or (required_key not in match_context):
            # Match is missing key
            if allow_missing_keys:
                # Only checking existing keys
                continue

            return False

        if isinstance(required_value, collections.abc.Mapping):
            # Unpack dict
            # <context_key>:
            #   value: ...
            required_value = required_value.get("value")

        # Ensure value matches
        actual_value = match_context[required_key]

        if isinstance(actual_value, collections.abc.Mapping):
            # Unpack dict
            # <context_key>:
            #   value: ...
            actual_value = actual_value.get("value")

        if (not isinstance(required_value, str)) and isinstance(
            required_value, collections.abc.Collection
        ):
            if actual_value not in required_value:
                # Match value not in required list
                return False
        elif (required_value is not None) and (actual_value != required_value):
            # Match value doesn't equal required value
            return False

    return True


def check_excluded_context(
    excluded_context: Dict[str, Any], match_context: Optional[Dict[str, Any]]
) -> bool:
    """Return True if match context does not violate excluded context."""
    for (
        excluded_key,
        excluded_value,
    ) in excluded_context.items():
        if (not match_context) or (excluded_key not in match_context):
            continue

        if isinstance(excluded_value, collections.abc.Mapping):
            # Unpack dict
            # <context_key>:
            #   value: ...
            excluded_value = excluded_value.get("value")

        # Ensure value does not match
        actual_value = match_context[excluded_key]

        if isinstance(actual_value, collections.abc.Mapping):
            # Unpack dict
            # <context_key>:
            #   value: ...
            actual_value = actual_value.get("value")

        if (not isinstance(excluded_value, str)) and isinstance(
            excluded_value, collections.abc.Collection
        ):
            if actual_value in excluded_value:
                # Match value is in excluded list
                return False
        elif actual_value == excluded_value:
            # Match value equals excluded value
            return False

    return True
