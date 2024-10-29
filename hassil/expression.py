"""Classes for representing sentence templates."""

import itertools
from abc import ABC
from collections.abc import Collection
from dataclasses import dataclass, field
from enum import Enum
from functools import partial
from typing import Dict, Iterator, List, Optional, Set


@dataclass
class Expression(ABC):
    """Base class for expressions."""


@dataclass
class TextChunk(Expression):
    """Contiguous chunk of text (with whitespace)."""

    # Text with casing/whitespace normalized
    text: str = ""

    # Set in __post_init__
    original_text: str = None  # type: ignore

    parent: "Optional[Sequence]" = None

    def __post_init__(self):
        if self.original_text is None:
            self.original_text = self.text

    @property
    def is_empty(self) -> bool:
        """True if the chunk is empty"""
        return self.text == ""

    @staticmethod
    def empty() -> "TextChunk":
        """Returns an empty text chunk"""
        return TextChunk()


class SequenceType(str, Enum):
    """Type of a sequence. Optionals are alternatives with an empty option."""

    # Sequence of expressions
    GROUP = "group"

    # Expressions where only one will be recognized
    ALTERNATIVE = "alternative"

    # Permutations of a set of expressions
    PERMUTATION = "permutation"


@dataclass
class Sequence(Expression):
    """Ordered sequence of expressions. Supports groups, optionals, and alternatives."""

    # Items in the sequence
    items: List[Expression] = field(default_factory=list)

    # Group or alternative
    type: SequenceType = SequenceType.GROUP

    is_optional: bool = False

    def text_chunk_count(self) -> int:
        """Return the number of TextChunk expressions in this sequence (recursive)."""
        num_text_chunks = 0
        for item in self.items:
            if isinstance(item, TextChunk):
                num_text_chunks += 1
            elif isinstance(item, Sequence):
                seq: Sequence = item
                num_text_chunks += seq.text_chunk_count()

        return num_text_chunks

    def list_names(
        self,
        expansion_rules: Optional[Dict[str, "Sentence"]] = None,
    ) -> Iterator[str]:
        """Return names of list references (recursive)."""
        for item in self.items:
            yield from self._list_names(item, expansion_rules)

    def _list_names(
        self,
        item: Expression,
        expansion_rules: Optional[Dict[str, "Sentence"]] = None,
    ) -> Iterator[str]:
        """Return names of list references (recursive)."""
        if isinstance(item, ListReference):
            list_ref: ListReference = item
            yield list_ref.list_name
        elif isinstance(item, Sequence):
            seq: Sequence = item
            yield from seq.list_names(expansion_rules)
        elif isinstance(item, RuleReference):
            rule_ref: RuleReference = item
            if expansion_rules and (rule_ref.rule_name in expansion_rules):
                rule_body = expansion_rules[rule_ref.rule_name]
                yield from self._list_names(rule_body, expansion_rules)


@dataclass
class RuleReference(Expression):
    """Reference to an expansion rule by <name>."""

    # Name of referenced rule
    rule_name: str = ""


@dataclass
class ListReference(Expression):
    """Reference to a list by {name}."""

    list_name: str = ""
    prefix: Optional[str] = None
    suffix: Optional[str] = None
    _slot_name: Optional[str] = None

    def __post_init__(self):
        if ":" in self.list_name:
            # list_name:slot_name
            self.list_name, self._slot_name = self.list_name.split(":", maxsplit=1)
        else:
            self._slot_name = self.list_name

    @property
    def slot_name(self) -> str:
        """Name of slot to put list value into."""
        assert self._slot_name is not None
        return self._slot_name


@dataclass
class Sentence(Sequence):
    """Sequence representing a complete sentence template."""

    text: Optional[str] = None
    _required_keywords: Optional[List[Set[str]]] = None

    def matches_required_keywords(
        self,
        keywords: Collection[str],
        expansion_rules: Optional[Dict[str, "Sentence"]] = None,
    ) -> bool:
        """Return False if provided keywords could not possibly match the sentence template."""
        if self._required_keywords is None:
            # Generate lists of required keywords
            self._required_keywords = []

            # Process each alternative sentence separately because they may have
            # very different keywords.
            for sentence_text in self._sample_required_text(self, expansion_rules):
                sentence_keywords = set(sentence_text.split())
                if not sentence_keywords:
                    # No required keywords
                    self._required_keywords = []
                    break

                self._required_keywords.append(sentence_keywords)

        if not self._required_keywords:
            # No required keywords
            return True

        for sentence_keywords in self._required_keywords:
            # We can't use issubset here because we skip optionals during text
            # generation, and template fragments like "light[s]" will not
            # generate "light" and "lights".
            #
            # Including optionals makes the keyword checking slower than the
            # original recognizer.
            if not sentence_keywords.isdisjoint(keywords):
                return True

        return False

    def _sample_required_text(
        self,
        expression: Expression,
        expansion_rules: Optional[Dict[str, "Sentence"]] = None,
    ):
        """Generate possible sentences, but skip optionals."""
        if isinstance(expression, TextChunk):
            chunk: TextChunk = expression
            yield chunk.text
        elif isinstance(expression, Sequence):
            seq: Sequence = expression
            if seq.is_optional:
                # Skip optionals
                yield ""
            elif seq.type == SequenceType.ALTERNATIVE:
                for item in seq.items:
                    yield from self._sample_required_text(item, expansion_rules)
            elif seq.type == SequenceType.GROUP:
                seq_sentences = map(
                    partial(
                        self._sample_required_text,
                        expansion_rules=expansion_rules,
                    ),
                    seq.items,
                )
                sentence_texts = itertools.product(*seq_sentences)
                for sentence_words in sentence_texts:
                    yield "".join(sentence_words)
        elif isinstance(expression, RuleReference):
            # <rule>
            rule_ref: RuleReference = expression

            rule_body: Optional[Sentence] = None
            if expansion_rules:
                rule_body = expansion_rules.get(rule_ref.rule_name)

            if rule_body is None:
                raise ValueError(f"Missing expansion rule <{rule_ref.rule_name}>")

            yield from self._sample_required_text(rule_body, expansion_rules)
        else:
            yield ""
