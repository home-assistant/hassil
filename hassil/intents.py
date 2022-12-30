"""Classes/methods for loading YAML intent files."""

from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import IO, Any, Dict, Iterable, List, Optional, Tuple, Union, cast

from dataclasses_json import dataclass_json
from yaml import safe_load

from .expression import Sentence, TextChunk
from .parse import parse_sentences
from .util import normalize_text


class ResponseType(str, Enum):
    SUCCESS = "success"
    NO_INTENT = "no_intent"
    NO_AREA = "no_area"
    NO_DOMAIN = "no_domain"
    NO_DEVICE_CLASS = "no_device_class"
    NO_ENTITY = "no_entity"
    HANDLE_ERROR = "handle_error"


@dataclass
class IntentData:
    """Block of sentences and known slots for an intent."""

    sentence_texts: List[str]
    """Sentence templates that match this intent."""

    slots: Dict[str, Any] = field(default_factory=dict)
    """Slot values that are assumed if intent is matched."""

    requires_context: Optional[Dict[str, Any]] = None
    """Context items required before match is successful."""

    excludes_context: Optional[Dict[str, Any]] = None
    """Context items that must not be present for match to be successful."""

    _sentences: Optional[List[Sentence]] = None
    """Sentences after they are parsed."""

    @property
    def sentences(self) -> List[Sentence]:
        """Sentence templates that match this intent."""
        if self._sentences is None:
            self._sentences = parse_sentences(self.sentence_texts, keep_text=True)

        return self._sentences


@dataclass_json
@dataclass
class Intent:
    """A named intent with sentences + slots."""

    name: str
    data: List[IntentData] = field(default_factory=list)


class SlotList(ABC):
    """Base class for slot lists."""


class RangeType(str, Enum):
    """Number range type."""

    NUMBER = "number"
    PERCENTAGE = "percentage"
    TEMPERATURE = "temperature"


@dataclass
class RangeSlotList(SlotList):
    """Slot list for a range of numbers."""

    start: int
    stop: int
    step: int = 1
    type: RangeType = RangeType.NUMBER

    def __post_init__(self):
        """Validate number range"""
        assert self.start < self.stop, "start must be less than stop"
        assert self.step > 0, "step must be positive"


@dataclass_json
@dataclass
class TextSlotValue:
    """Single value in a text slot list."""

    text_in: TextChunk
    """Input text for this value"""

    value_out: Any
    """Output value put into slot"""

    context: Optional[Dict[str, Any]] = None
    """Items added to context if value is matched"""

    @staticmethod
    def from_tuple(
        value_tuple: Union[Tuple[str, Any], Tuple[str, Any, Dict[str, Any]]]
    ) -> "TextSlotValue":
        """Construct text slot value from a tuple."""
        text_in, value_out, context = value_tuple[0], value_tuple[1], None

        if len(value_tuple) > 2:
            context = cast(Tuple[str, Any, Dict[str, Any]], value_tuple)[2]

        return TextSlotValue(
            text_in=TextChunk(normalize_text(text_in)),
            value_out=value_out,
            context=context,
        )


@dataclass
class TextSlotList(SlotList):
    """Slot list with pre-defined text values."""

    values: List[TextSlotValue]

    @staticmethod
    def from_strings(strings: Iterable[str]) -> "TextSlotList":
        """
        Construct a text slot list from strings.

        Input and output values are the same text.
        """
        return TextSlotList(
            values=[
                TextSlotValue(text_in=TextChunk(normalize_text(text)), value_out=text)
                for text in strings
            ],
        )

    @staticmethod
    def from_tuples(
        tuples: Iterable[Union[Tuple[str, Any], Tuple[str, Any, Dict[str, Any]]]]
    ) -> "TextSlotList":
        """
        Construct a text slot list from text/value pairs.

        Input values are the left (text), output values are the right (any).
        """
        return TextSlotList(
            values=[TextSlotValue.from_tuple(value_tuple) for value_tuple in tuples],
        )


@dataclass
class Intents:
    """Collection of intents, rules, and lists for a language."""

    language: str
    """Language code (e.g., en)."""

    intents: Dict[str, Intent]
    """Intents mapped by name."""

    slot_lists: Dict[str, SlotList] = field(default_factory=dict)
    """Slot lists mapped by name."""

    expansion_rules: Dict[str, Sentence] = field(default_factory=dict)
    """Expansion rules mapped by name."""

    skip_words: List[str] = field(default_factory=list)
    """Words that can be skipped during recognition."""

    @staticmethod
    def from_yaml(yaml_file: IO[str]) -> "Intents":
        """Load intents from a YAML file."""
        return Intents.from_dict(safe_load(yaml_file))

    @staticmethod
    def from_dict(input_dict: Dict[str, Any]) -> "Intents":
        """Parse intents from a dict."""
        # language: "<code>"
        # intents:
        #   IntentName:
        #     data:
        #       - sentences:
        #           - "<sentence>"
        #         slots:
        #           <slot_name>: <slot value>
        #           <slot_name>:
        #             - <slot value>
        # expansion_rules:
        #   <rule_name>: "<rule body>"
        # lists:
        #   <list_name>:
        #     values:
        #       - "<value>"
        #
        return Intents(
            language=input_dict["language"],
            intents={
                intent_name: Intent(
                    name=intent_name,
                    data=[
                        IntentData(
                            sentence_texts=data_dict["sentences"],
                            slots=data_dict.get("slots", {}),
                            requires_context=data_dict.get("requires_context"),
                            excludes_context=data_dict.get("excludes_context"),
                        )
                        for data_dict in intent_dict["data"]
                    ],
                )
                for intent_name, intent_dict in input_dict["intents"].items()
            },
            slot_lists={
                list_name: _parse_list(list_dict)
                for list_name, list_dict in input_dict.get("lists", {}).items()
            },
            expansion_rules={
                rule_name: parse_sentences([rule_body], keep_text=True)[0]
                for rule_name, rule_body in input_dict.get(
                    "expansion_rules", {}
                ).items()
            },
            skip_words=input_dict.get("skip_words", []),
        )


def _parse_list(list_dict: Dict[str, Any]) -> SlotList:
    """Parses a slot list from a dict."""
    if "values" in list_dict:
        # Text values
        text_values: List[TextSlotValue] = []
        for value in list_dict["values"]:
            if isinstance(value, str):
                # String value
                text_values.append(
                    TextSlotValue(
                        text_in=TextChunk(normalize_text(value)), value_out=value
                    )
                )
            else:
                # Object with "in" and "out"
                text_values.append(
                    TextSlotValue(
                        text_in=TextChunk(normalize_text(value["in"])),
                        value_out=value["out"],
                        context=value.get("context"),
                    )
                )

        return TextSlotList(text_values)

    if "range" in list_dict:
        # Number range
        range_dict = list_dict["range"]
        return RangeSlotList(
            type=RangeType(range_dict.get("type", "number")),
            start=int(range_dict["from"]),
            stop=int(range_dict["to"]),
            step=int(range_dict.get("step", 1)),
        )

    raise ValueError(f"Unknown slot list type: {list_dict}")
