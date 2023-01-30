"""Methods for recognizing intents from text."""

import collections.abc
import itertools
import re
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional

from .expression import (
    Expression,
    ListReference,
    RuleReference,
    Sentence,
    Sequence,
    SequenceType,
    TextChunk,
)
from .intents import Intent, Intents, RangeSlotList, SlotList, TextSlotList
from .util import normalize_text, normalize_whitespace

NUMBER_START = re.compile(r"^(\s*-?[0-9]+)")

NON_WORD_START = re.compile(r"^\W+")


class HassilError(Exception):
    """Base class for hassil errors"""


class MissingListError(HassilError):
    """Error when a {slot_list} is missing."""


class MissingRuleError(HassilError):
    """Error when an <expansion_rule> is missing."""


@dataclass
class MatchEntity:
    """Named entity that has been matched from a {slot_list}"""

    name: str
    """Name of the entity."""

    value: Any
    """Value of the entity."""

    text: str
    """Original value text."""


@dataclass
class MatchContext:
    """Context passed to match_expression."""

    text: str
    """Input text remaining to be processed."""

    slot_lists: Dict[str, SlotList] = field(default_factory=dict)
    """Available slot lists mapped by name."""

    expansion_rules: Dict[str, Sentence] = field(default_factory=dict)
    """Available expansion rules mapped by name."""

    entities: List[MatchEntity] = field(default_factory=list)
    """Entities that have been found in input text."""

    intent_context: Dict[str, Any] = field(default_factory=dict)
    """Context items from outside or acquired during matching."""

    @property
    def is_match(self) -> bool:
        """True if no text is left that isn't just whitespace or non-word characters"""
        text = re.sub(r"\W+", "", self.text).strip()
        return not text


@dataclass
class RecognizeResult:
    """Result of recognition."""

    intent: Intent
    """Matched intent"""

    entities: Dict[str, MatchEntity] = field(default_factory=dict)
    """Matched entities mapped by name."""

    entities_list: List[MatchEntity] = field(default_factory=list)
    """Matched entities as a list (duplicates allowed)."""

    response: Optional[str] = None
    """Key for intent response."""


def recognize(
    text: str,
    intents: Intents,
    slot_lists: Optional[Dict[str, SlotList]] = None,
    expansion_rules: Optional[Dict[str, Sentence]] = None,
    skip_words: Optional[Iterable[str]] = None,
    intent_context: Optional[Dict[str, Any]] = None,
    default_response: Optional[str] = "default",
) -> Optional[RecognizeResult]:
    """Return the first match of input text/words against a collection of intents."""
    for result in recognize_all(
        text,
        intents,
        slot_lists=slot_lists,
        expansion_rules=expansion_rules,
        skip_words=skip_words,
        intent_context=intent_context,
        default_response=default_response,
    ):
        return result

    return None


def recognize_all(
    text: str,
    intents: Intents,
    slot_lists: Optional[Dict[str, SlotList]] = None,
    expansion_rules: Optional[Dict[str, Sentence]] = None,
    skip_words: Optional[Iterable[str]] = None,
    intent_context: Optional[Dict[str, Any]] = None,
    default_response: Optional[str] = "default",
) -> Iterable[RecognizeResult]:
    """Return all matches for input text/words against a collection of intents."""
    text = normalize_text(text)

    if skip_words is None:
        skip_words = intents.skip_words
    else:
        # Combine skip words
        skip_words = itertools.chain(skip_words, intents.skip_words)

    if skip_words:
        text = _remove_skip_words(text, skip_words)

    text += " "

    if slot_lists is None:
        slot_lists = intents.slot_lists
    else:
        # Combine with intents
        slot_lists = {**intents.slot_lists, **slot_lists}

    if slot_lists is None:
        slot_lists = {}

    if expansion_rules is None:
        expansion_rules = intents.expansion_rules
    else:
        # Combine rules
        expansion_rules = {**intents.expansion_rules, **expansion_rules}

    if intent_context is None:
        intent_context = {}

    # Check sentence against each intent.
    # This should eventually be done in parallel.
    for intent in intents.intents.values():
        for intent_data in intent.data:
            for intent_sentence in intent_data.sentences:
                # Create initial context
                match_context = MatchContext(
                    text=text,
                    slot_lists=slot_lists,
                    expansion_rules=expansion_rules,
                    intent_context=intent_context,
                )
                maybe_match_contexts = match_expression(match_context, intent_sentence)
                for maybe_match_context in maybe_match_contexts:
                    if maybe_match_context.is_match:
                        skip_match = False

                        # Verify excluded context
                        if intent_data.excludes_context:
                            for (
                                context_key,
                                context_value,
                            ) in intent_data.excludes_context.items():
                                actual_value = maybe_match_context.intent_context.get(
                                    context_key
                                )
                                if actual_value == context_value:
                                    # Exact match to context value
                                    skip_match = True
                                    break

                                if (
                                    isinstance(
                                        context_value, collections.abc.Collection
                                    )
                                    and not isinstance(context_value, str)
                                    and (actual_value in context_value)
                                ):
                                    # Actual value was in context value list
                                    skip_match = True
                                    break

                        # Verify required context
                        if (not skip_match) and intent_data.requires_context:
                            for (
                                context_key,
                                context_value,
                            ) in intent_data.requires_context.items():
                                actual_value = maybe_match_context.intent_context.get(
                                    context_key
                                )

                                if (
                                    actual_value == context_value
                                    and context_value is not None
                                ):
                                    # Exact match to context value, except when context value is required and not provided
                                    continue

                                if context_value is None and actual_value is not None:
                                    # Any value matches, as long as it's set
                                    continue

                                if (
                                    isinstance(
                                        context_value, collections.abc.Collection
                                    )
                                    and not isinstance(context_value, str)
                                    and (actual_value in context_value)
                                ):
                                    # Actual value was in context value list
                                    continue

                                # Did not match required context
                                skip_match = True
                                break

                        if skip_match:
                            # Intent context did not match
                            continue

                        # Add fixed entities
                        for slot_name, slot_value in intent_data.slots.items():
                            maybe_match_context.entities.append(
                                MatchEntity(name=slot_name, value=slot_value, text="")
                            )

                        # Return the first match
                        response = default_response
                        if intent_data.response is not None:
                            response = intent_data.response

                        yield RecognizeResult(
                            intent=intent,
                            entities={
                                entity.name: entity
                                for entity in maybe_match_context.entities
                            },
                            entities_list=maybe_match_context.entities,
                            response=response,
                        )


def is_match(
    text: str,
    sentence: Sentence,
    slot_lists: Optional[Dict[str, SlotList]] = None,
    expansion_rules: Optional[Dict[str, Sentence]] = None,
    skip_words: Optional[Iterable[str]] = None,
    entities: Optional[Dict[str, Any]] = None,
    intent_context: Optional[Dict[str, Any]] = None,
) -> Optional[MatchContext]:
    """Return the first match of input text/words against a sentence expression."""
    text = normalize_text(text)

    if skip_words:
        text = _remove_skip_words(text, skip_words)

    text = text + " "

    if slot_lists is None:
        slot_lists = {}

    if expansion_rules is None:
        expansion_rules = {}

    if intent_context is None:
        intent_context = {}

    match_context = MatchContext(
        text=text,
        slot_lists=slot_lists,
        expansion_rules=expansion_rules,
        intent_context=intent_context,
    )

    for maybe_match_context in match_expression(match_context, sentence):
        if maybe_match_context.is_match:
            return maybe_match_context

    return None


def _remove_skip_words(text: str, skip_words: Iterable[str]) -> str:
    """Remove skip words from text."""

    # It's critical that skip words are processed longest first, since they may
    # share prefixes.
    for skip_word in sorted(skip_words, key=len, reverse=True):
        skip_word = normalize_text(skip_word)
        text = re.sub(rf"\b{re.escape(skip_word)}\b", "", text)

    text = normalize_whitespace(text)
    text = text.strip()

    return text


def match_expression(
    context: MatchContext, expression: Expression
) -> Iterable[MatchContext]:
    """Yield matching contexts for an expresion"""
    if isinstance(expression, TextChunk):
        chunk: TextChunk = expression
        chunk_text = chunk.text.lstrip()

        if chunk.is_empty:
            # Skip empty chunk
            yield context
        elif context.text.startswith(chunk_text):
            # Successful match for chunk
            context_text = context.text[len(chunk_text) :]
            context_text = context_text.lstrip()
            yield MatchContext(
                text=context_text,
                # Copy over
                slot_lists=context.slot_lists,
                expansion_rules=context.expansion_rules,
                entities=context.entities,
                intent_context=context.intent_context,
            )
        else:
            # Remove non-word characters and try again
            match = NON_WORD_START.match(context.text)
            if match is not None:
                context_text = context.text[len(match[0]) :].lstrip()
                if context_text.startswith(chunk_text):
                    context_text = context_text[len(chunk_text) :]
                    context_text = context_text.lstrip()
                    yield MatchContext(
                        text=context_text,
                        # Copy over
                        slot_lists=context.slot_lists,
                        expansion_rules=context.expansion_rules,
                        entities=context.entities,
                        intent_context=context.intent_context,
                    )

    elif isinstance(expression, Sequence):
        seq: Sequence = expression
        if seq.type == SequenceType.ALTERNATIVE:
            # Any may match (words | in | alternative)
            # NOTE: [optional] = (optional | )
            for item in seq.items:
                yield from match_expression(context, item)

        elif seq.type == SequenceType.GROUP:
            # All must match (words in group)
            if seq.items:
                group_contexts = [context]
                for item in seq.items:
                    # Next step
                    group_contexts = [
                        item_context
                        for group_context in group_contexts
                        for item_context in match_expression(group_context, item)
                    ]
                    if not group_contexts:
                        break

                for group_context in group_contexts:
                    yield group_context
        else:
            raise ValueError(f"Unexpected sequence type: {seq}")

    elif isinstance(expression, ListReference):
        # {list}
        list_ref: ListReference = expression
        if (not context.slot_lists) or (list_ref.list_name not in context.slot_lists):
            raise MissingListError(f"Missing slot list {{{list_ref.list_name}}}")

        slot_list = context.slot_lists[list_ref.list_name]
        if isinstance(slot_list, TextSlotList):
            text_list: TextSlotList = slot_list

            if context.text:
                # Any value may match
                for slot_value in text_list.values:
                    value_contexts = match_expression(
                        MatchContext(
                            # Copy over
                            text=context.text,
                            slot_lists=context.slot_lists,
                            expansion_rules=context.expansion_rules,
                            entities=context.entities,
                            intent_context=context.intent_context,
                        ),
                        slot_value.text_in,
                    )

                    for value_context in value_contexts:
                        entities = context.entities + [
                            MatchEntity(
                                name=list_ref.slot_name,
                                value=slot_value.value_out,
                                text=context.text[: -len(value_context.text)]
                                if value_context.text
                                else context.text,
                            )
                        ]

                        if slot_value.context:
                            # Merge context from matched list value
                            yield MatchContext(
                                entities=entities,
                                intent_context={
                                    **context.intent_context,
                                    **slot_value.context,
                                },
                                # Copy over
                                text=value_context.text,
                                slot_lists=value_context.slot_lists,
                                expansion_rules=value_context.expansion_rules,
                            )
                        else:
                            yield MatchContext(
                                entities=entities,
                                # Copy over
                                text=value_context.text,
                                slot_lists=value_context.slot_lists,
                                expansion_rules=value_context.expansion_rules,
                                intent_context=value_context.intent_context,
                            )

        elif isinstance(slot_list, RangeSlotList):
            # List that represents a number range.
            # Numbers must currently be digits ("1" not "one").
            range_list: RangeSlotList = slot_list
            if context.text:
                number_match = NUMBER_START.match(context.text)
                if number_match is not None:
                    number_text = number_match[1]
                    word_number = int(number_text)
                    if range_list.step == 1:
                        # Unit step
                        in_range = range_list.start <= word_number <= range_list.stop
                    else:
                        # Non-unit step
                        in_range = word_number in range(
                            range_list.start, range_list.stop + 1, range_list.step
                        )

                    if in_range:
                        entities = context.entities + [
                            MatchEntity(
                                name=list_ref.slot_name,
                                value=word_number,
                                text=context.text.split()[0],
                            )
                        ]

                        yield MatchContext(
                            text=context.text[len(number_text) :].lstrip(),
                            entities=entities,
                            # Copy over
                            slot_lists=context.slot_lists,
                            expansion_rules=context.expansion_rules,
                            intent_context=context.intent_context,
                        )

        else:
            raise ValueError(f"Unexpected slot list type: {slot_list}")

    elif isinstance(expression, RuleReference):
        # <rule>
        rule_ref: RuleReference = expression
        if (not context.expansion_rules) or (
            rule_ref.rule_name not in context.expansion_rules
        ):
            raise MissingRuleError(f"Missing expansion rule <{rule_ref.rule_name}>")

        yield from match_expression(
            context, context.expansion_rules[rule_ref.rule_name]
        )
    else:
        raise ValueError(f"Unexpected expression: {expression}")
