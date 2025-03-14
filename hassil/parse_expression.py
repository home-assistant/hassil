import re
from dataclasses import dataclass
from typing import Optional

from .expression import (
    Alternative,
    Expression,
    Group,
    ListReference,
    Permutation,
    RuleReference,
    Sentence,
    Sequence,
    TextChunk,
)
from .parser import (
    GROUP_END,
    GROUP_START,
    LIST_END,
    LIST_START,
    OPT_END,
    OPT_START,
    RULE_END,
    RULE_START,
    ParseChunk,
    ParseError,
    ParseType,
    next_chunk,
)
from .util import normalize_text


@dataclass
class ParseMetadata:
    """Debug metadata for more helpful parsing errors."""

    file_name: str
    line_number: int
    intent_name: Optional[str] = None


class ParseExpressionError(ParseError):
    def __init__(self, chunk: ParseChunk, metadata: Optional[ParseMetadata] = None):
        super().__init__()
        self.chunk = chunk
        self.metadata = metadata

    def __str__(self) -> str:
        return f"Error in chunk {self.chunk} at {self.metadata}"


def _ensure_alternative(grp: Group) -> Alternative:
    if isinstance(grp, Alternative):
        return grp
    # Collapse items into a single group
    return Alternative(items=[grp])


def _ensure_permutation(grp: Group) -> Permutation:
    if isinstance(grp, Permutation):
        return grp
    # Collapse items into a single group
    return Permutation(items=[grp])


def parse_group(
    grp_chunk: ParseChunk, metadata: Optional[ParseMetadata] = None
) -> Group:
    grp: Group = Sequence()
    if grp_chunk.parse_type == ParseType.GROUP:
        grp_text = _remove_delimiters(grp_chunk.text, GROUP_START, GROUP_END)
    elif grp_chunk.parse_type == ParseType.OPT:
        grp_text = _remove_delimiters(grp_chunk.text, OPT_START, OPT_END)
    else:
        raise ParseExpressionError(grp_chunk, metadata=metadata)

    item_chunk = next_chunk(grp_text)
    last_grp_text = grp_text

    while item_chunk is not None:
        if item_chunk.parse_type in (
            ParseType.WORD,
            ParseType.GROUP,
            ParseType.OPT,
            ParseType.LIST,
            ParseType.RULE,
        ):
            # Chunk text ends with explicit whitespace
            is_end_of_word = (item_chunk.end_index < len(grp_text)) and grp_text[
                item_chunk.end_index
            ].isspace()

            item = parse_expression(
                item_chunk, metadata=metadata, is_end_of_word=is_end_of_word
            )

            if isinstance(grp, (Alternative, Permutation)):
                # Add to the most recent sequence
                last_item = grp.items[-1]
                if not isinstance(last_item, Sequence):
                    raise ParseExpressionError(grp_chunk, metadata=metadata)

                last_item.items.append(item)
            else:
                # Add to parent group
                grp.items.append(item)

                if isinstance(item, TextChunk):
                    item_tc: TextChunk = item
                    item_tc.parent = grp

        elif item_chunk.parse_type == ParseType.ALT:
            grp = _ensure_alternative(grp)

            # Begin new sequence
            grp.items.append(Sequence())
        elif item_chunk.parse_type == ParseType.PERM:
            grp = _ensure_permutation(grp)

            # Begin new sequence
            grp.items.append(Sequence())
        else:
            raise ParseExpressionError(grp_chunk, metadata=metadata)

        # Next chunk
        grp_text = grp_text[item_chunk.end_index :]

        if grp_text == last_grp_text:
            # No change, unable to proceed
            raise ParseExpressionError(grp_chunk, metadata=metadata)

        item_chunk = next_chunk(grp_text)
        last_grp_text = grp_text

    if isinstance(grp, Permutation):
        _add_spaces_between_items(grp)

    return grp


def parse_expression(
    chunk: ParseChunk,
    metadata: Optional[ParseMetadata] = None,
    is_end_of_word: bool = True,
) -> Expression:
    if chunk.parse_type == ParseType.WORD:
        original_text = _remove_escapes(chunk.text)
        text = normalize_text(original_text)
        return TextChunk(text=text, original_text=original_text)

    if chunk.parse_type == ParseType.GROUP:
        return parse_group(chunk, metadata=metadata)

    if chunk.parse_type == ParseType.OPT:
        grp = parse_group(chunk, metadata=metadata)
        alt = _ensure_alternative(grp)
        alt.is_optional = True
        alt.items.append(TextChunk(text="", parent=grp))
        grp = alt
        return grp

    if chunk.parse_type == ParseType.LIST:
        text = _remove_escapes(chunk.text)
        list_name = _remove_delimiters(text, LIST_START, LIST_END)
        return ListReference(list_name=list_name, is_end_of_word=is_end_of_word)

    if chunk.parse_type == ParseType.RULE:
        text = _remove_escapes(chunk.text)
        rule_name = _remove_delimiters(text, RULE_START, RULE_END)
        return RuleReference(rule_name=rule_name)

    raise ParseExpressionError(chunk, metadata=metadata)


def parse_sentence(
    text: str, keep_text=False, metadata: Optional[ParseMetadata] = None
) -> Sentence:
    """Parse a single sentence."""
    original_text = text
    text = text.strip()
    # text = fix_pattern_whitespace(text.strip())

    # Wrap in a group because sentences need to always be groups.
    text = f"({text})"

    chunk = next_chunk(text)
    if chunk is None:
        raise ParseError(f"Unexpected empty chunk in: {text}")

    if chunk.parse_type != ParseType.GROUP:
        raise ParseError(f"Expected (group) in: {text}")

    if chunk.start_index != 0:
        raise ParseError(f"Expected (group) to start at index 0 in: {text}")

    if chunk.end_index != len(text):
        raise ParseError(f"Expected chunk to end at index {chunk.end_index} in: {text}")

    grp = parse_expression(chunk, metadata=metadata)
    if not isinstance(grp, Group):
        raise ParseError(f"Expected Group, got: {grp}")

    # Unpack redundant group
    if len(grp.items) == 1:
        first_item = grp.items[0]
        if isinstance(first_item, Group):
            grp = first_item

    return Sentence(
        expression=grp,
        text=original_text if keep_text else None,
    )


# def fix_pattern_whitespace(text: str) -> str:
#     if PERM_SEP in text:
#         # Fix within permutations
#         text = PERM_SEP.join(
#             GROUP_START + fix_pattern_whitespace(perm_chunk) + GROUP_END
#             for perm_chunk in text.split(PERM_SEP)
#         )

#     # Recursively process (group)
#     group_start_index = text.find(GROUP_START)
#     while group_start_index > 0:
#         # TODO: Can't cross OPT boundary
#         group_end_index = find_end_delimiter(
#             text, group_start_index + 1, GROUP_START, GROUP_END
#         )
#         if group_end_index is None:
#             return text  # will fail parsing

#         before_group, text_without_group, after_group = (
#             text[:group_start_index],
#             text[group_start_index + 1 : group_end_index - 1],
#             text[group_end_index:],
#         )

#         text = (
#             fix_pattern_whitespace(before_group)
#             + GROUP_START
#             + fix_pattern_whitespace(text_without_group)
#             + GROUP_END
#             + fix_pattern_whitespace(after_group)
#         )
#         group_start_index = text.find(GROUP_START, group_end_index)

#     # Fix whitespace after optional (beginning of sentence)
#     left_text, right_text = "", text
#     while right_text.startswith(OPT_START):
#         opt_end_index = find_end_delimiter(right_text, 1, OPT_START, OPT_END)
#         if (opt_end_index is None) or (opt_end_index >= len(right_text)):
#             break

#         if not right_text[opt_end_index].isspace():
#             # No adjustment needed
#             break

#         # Move whitespace into optional and group
#         left_text += (
#             OPT_START
#             + GROUP_START
#             + right_text[1 : opt_end_index - 1]
#             + GROUP_END
#             + " "
#             + OPT_END
#         )
#         right_text = right_text[opt_end_index:].lstrip()

#     text = left_text + right_text

#     # Fix whitespace before optional (end of sentence)
#     left_text, right_text = text, ""
#     while left_text.endswith(OPT_END):
#         opt_end_index = len(left_text)
#         opt_start_index = left_text.rfind(OPT_START)
#         maybe_opt_end_index: Optional[int] = None

#         # Keep looking back for the "[" that starts this optional
#         while opt_start_index > 0:
#             maybe_opt_end_index = find_end_delimiter(
#                 left_text, opt_start_index + 1, OPT_START, OPT_END
#             )
#             if maybe_opt_end_index == opt_end_index:
#                 break  # found the matching "["

#             # Look farther back
#             opt_start_index = left_text.rfind(OPT_START, 0, opt_start_index)

#         if (maybe_opt_end_index != opt_end_index) or (opt_start_index <= 0):
#             break

#         if not left_text[opt_start_index - 1].isspace():
#             # No adjustment needed
#             break

#         # Move whitespace into optional and group
#         right_text = (
#             (OPT_START + " " + GROUP_START + left_text[opt_start_index + 1 : -1])
#             + GROUP_END
#             + OPT_END
#             + right_text
#         )

#         left_text = left_text[:opt_start_index].rstrip()

#     text = left_text + right_text

#     # Fix whitespace around optional (middle of a sentence)
#     left_text, right_text = "", text
#     match = re.search(rf"\s({re.escape(OPT_START)})", right_text)
#     while match is not None:
#         opt_start_index = match.start(1)
#         opt_end_index = find_end_delimiter(
#             right_text, opt_start_index + 1, OPT_START, OPT_END
#         )
#         if (opt_end_index is None) or (opt_end_index >= len(text)):
#             break

#         if right_text[opt_end_index].isspace():
#             # Move whitespace inside optional, add group
#             left_text += (
#                 right_text[: opt_start_index - 1]
#                 + OPT_START
#                 + " "
#                 + GROUP_START
#                 + right_text[opt_start_index + 1 : opt_end_index - 1].lstrip()
#                 + GROUP_END
#                 + OPT_END
#             )
#         else:
#             left_text += right_text[:opt_end_index]

#         right_text = right_text[opt_end_index:]
#         if not right_text:
#             break

#         match = re.search(rf"\s({re.escape(OPT_START)})", right_text)

#     text = left_text + right_text

#     return text


def _remove_delimiters(
    text: str, start_char: str, end_char: Optional[str] = None
) -> str:
    """Removes the surrounding delimiters in text."""
    if end_char is None:
        assert len(text) > 1, "Text is too short"
        assert text[0] == start_char, "Wrong start char"
        return text[1:]

    assert len(text) > 2, "Text is too short"
    assert text[0] == start_char, "Wrong start char"
    assert text[-1] == end_char, "Wrong end char"
    return text[1:-1]


def _remove_escapes(text: str) -> str:
    """Remove backslash escape sequences"""
    return re.sub(r"\\(.)", r"\1", text)


def _escape_text(text: str) -> str:
    """Escape parentheses, etc."""
    return re.sub(r"([()\[\]{}<>])", r"\\\1", text)


def _add_spaces_between_items(perm: Permutation) -> None:
    """Add spaces between each 2 items of a permutation"""
    for seq in perm.items:
        assert isinstance(seq, Sequence), "Item is not a sequence"
        seq.items.insert(0, TextChunk(text=" "))
        seq.items.append(TextChunk(text=" "))
