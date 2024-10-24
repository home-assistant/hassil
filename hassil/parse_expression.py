import re
from dataclasses import dataclass
from itertools import permutations
from typing import List, Optional

from .expression import (
    Expression,
    ListReference,
    RuleReference,
    Sentence,
    Sequence,
    SequenceType,
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


def _ensure_alternative(seq: Sequence):
    if seq.type != SequenceType.ALTERNATIVE:
        seq.type = SequenceType.ALTERNATIVE

        # Collapse items into a single group
        seq.items = [
            Sequence(
                type=SequenceType.GROUP,
                items=seq.items,
            )
        ]


def _ensure_permutation(seq: Sequence):
    if seq.type != SequenceType.PERMUTATION:
        seq.type = SequenceType.PERMUTATION

        # Collapse items into a single group
        seq.items = [
            Sequence(
                type=SequenceType.GROUP,
                items=seq.items,
            )
        ]


def parse_group_or_alt_or_perm(
    seq_chunk: ParseChunk, metadata: Optional[ParseMetadata] = None
) -> Sequence:
    seq = Sequence(type=SequenceType.GROUP)
    if seq_chunk.parse_type == ParseType.GROUP:
        seq_text = _remove_delimiters(seq_chunk.text, GROUP_START, GROUP_END)
    elif seq_chunk.parse_type == ParseType.OPT:
        seq_text = _remove_delimiters(seq_chunk.text, OPT_START, OPT_END)
    else:
        raise ParseExpressionError(seq_chunk, metadata=metadata)

    item_chunk = next_chunk(seq_text)
    last_seq_text = seq_text

    while item_chunk is not None:
        if item_chunk.parse_type in (
            ParseType.WORD,
            ParseType.GROUP,
            ParseType.OPT,
            ParseType.LIST,
            ParseType.RULE,
        ):
            item = parse_expression(item_chunk, metadata=metadata)

            if seq.type in (SequenceType.ALTERNATIVE, SequenceType.PERMUTATION):
                # Add to most recent group
                if not seq.items:
                    seq.items.append(Sequence(type=SequenceType.GROUP))

                # Must be group or alternative
                last_item = seq.items[-1]
                if not isinstance(last_item, Sequence):
                    raise ParseExpressionError(seq_chunk, metadata=metadata)

                last_item.items.append(item)
            else:
                # Add to parent group
                seq.items.append(item)
        elif item_chunk.parse_type == ParseType.ALT:
            _ensure_alternative(seq)

            # Begin new group
            seq.items.append(Sequence(type=SequenceType.GROUP))
        elif item_chunk.parse_type == ParseType.PERM:
            _ensure_permutation(seq)

            # Begin new group
            seq.items.append(Sequence(type=SequenceType.GROUP))
        else:
            raise ParseExpressionError(seq_chunk, metadata=metadata)

        # Next chunk
        seq_text = seq_text[item_chunk.end_index :]

        if seq_text == last_seq_text:
            # No change, unable to proceed
            raise ParseExpressionError(seq_chunk, metadata=metadata)

        item_chunk = next_chunk(seq_text)
        last_seq_text = seq_text

    if seq.type == SequenceType.PERMUTATION:
        permuted_items: List[Expression] = []

        for permutation in permutations(seq.items):
            permutation_with_spaces = _add_spaces_between_items(list(permutation))
            permuted_items.append(
                Sequence(type=SequenceType.GROUP, items=permutation_with_spaces)
            )

        seq = Sequence(type=SequenceType.ALTERNATIVE, items=permuted_items)

    return seq


def parse_expression(
    chunk: ParseChunk, metadata: Optional[ParseMetadata] = None
) -> Expression:
    if chunk.parse_type == ParseType.WORD:
        original_text = _remove_escapes(chunk.text)
        text = normalize_text(original_text)
        return TextChunk(text=text, original_text=original_text)

    if chunk.parse_type == ParseType.GROUP:
        return parse_group_or_alt_or_perm(chunk, metadata=metadata)

    if chunk.parse_type == ParseType.OPT:
        seq = parse_group_or_alt_or_perm(chunk, metadata=metadata)
        _ensure_alternative(seq)
        seq.items.append(TextChunk(text=""))
        return seq

    if chunk.parse_type == ParseType.LIST:
        text = _remove_escapes(chunk.text)
        list_name = _remove_delimiters(text, LIST_START, LIST_END)
        return ListReference(list_name=list_name)

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

    # Wrap in a group because sentences need to always be sequences.
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

    seq = parse_expression(chunk, metadata=metadata)
    if not isinstance(seq, Sequence):
        raise ParseError(f"Expected Sequence, got: {seq}")

    # Unpack redundant sequence
    if len(seq.items) == 1:
        first_item = seq.items[0]
        if isinstance(first_item, Sequence):
            seq = first_item

    return Sentence(
        type=seq.type, items=seq.items, text=original_text if keep_text else None
    )


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


def _add_spaces_between_items(items: List[Expression]) -> List[Expression]:
    """Add spaces between each 2 items of a sequence, used for permutations"""

    spaced_items: List[Expression] = []

    for item in items:
        spaced_items = spaced_items + [TextChunk(text=" ")] + [item]

    spaced_items.append(TextChunk(text=" "))
    items = spaced_items

    return items
