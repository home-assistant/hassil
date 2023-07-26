import io
from typing import cast

import pytest

from hassil import Intents, recognize, recognize_all
from hassil.expression import TextChunk
from hassil.intents import TextSlotList
from hassil.recognize import MISSING_ENTITY, UnmatchedRangeEntity, UnmatchedTextEntity

TEST_YAML = """
language: "en"
intents:
  TurnOnTV:
    data:
      - sentences:
          - "turn on [the] TV in <area>"
          - "turn on <area> TV"
        slots:
          domain: "media_player"
          name: "roku"
  SetBrightness:
    data:
      - sentences:
          - "set [the] brightness in <area> to <brightness>"
        slots:
          domain: "light"
          name: "all"
      - sentences:
          - "set [the] brightness of <name> to <brightness>"
        requires_context:
          domain: "light"
        slots:
          domain: "light"
  GetTemperature:
    data:
      - sentences:
          - "<what_is> [the] temperature in <area>"
        slots:
          domain: "climate"
  CloseCover:
    data:
      - sentences:
          - "close <name>"
        requires_context:
          domain: "cover"
        slots:
          domain: "cover"
  Play:
    data:
      - sentences:
          - "play <name>"
        excludes_context:
          domain:
            - "cover"
            - "light"
  CloseCurtains:
    data:
      - sentences:
          - "close [the] curtains [in <area>]"
        slots:
          domain: "cover"
          device_class: "curtain"
        requires_context:
          area:
expansion_rules:
  area: "[the] {area}"
  name: "[the] {name}"
  brightness: "{brightness_pct}[%| percent]"
  what_is: "(what's | whats | what is)"
lists:
  brightness_pct:
    range:
      type: percentage
      from: 0
      to: 100
skip_words:
  - "please"
"""


@pytest.fixture
def intents():
    with io.StringIO(TEST_YAML) as test_file:
        return Intents.from_yaml(test_file)


@pytest.fixture
def slot_lists():
    return {
        "area": TextSlotList.from_tuples(
            [("kitchen", "area.kitchen"), ("living room", "area.living_room")]
        ),
        "name": TextSlotList.from_tuples(
            [
                ("hue", "light.hue", {"domain": "light"}),
                (
                    "garage door",
                    "cover.garage_door",
                    {"domain": "cover"},
                ),
                (
                    "blue curtains",
                    "cover.blue_curtains",
                    {
                        "domain": "cover",
                        "device_class": "curtain",
                        "area": "living_room",
                    },
                ),
                (
                    "roku",
                    "media_player.roku",
                    {"domain": "media_player"},
                ),
            ]
        ),
    }


# pylint: disable=redefined-outer-name
def test_turn_on(intents, slot_lists):
    result = recognize("turn on kitchen TV, please", intents, slot_lists=slot_lists)
    assert result is not None
    assert result.intent.name == "TurnOnTV"

    area = result.entities["area"]
    assert area.name == "area"
    assert area.value == "area.kitchen"

    # From YAML
    assert result.entities["domain"].value == "media_player"
    assert result.entities["name"].value == "roku"


# pylint: disable=redefined-outer-name
def test_brightness_area(intents, slot_lists):
    result = recognize(
        "set the brightness in the living room to 75%", intents, slot_lists=slot_lists
    )
    assert result is not None
    assert result.intent.name == "SetBrightness"

    assert result.entities["area"].value == "area.living_room"
    assert result.entities["brightness_pct"].value == 75

    # From YAML
    assert result.entities["domain"].value == "light"
    assert result.entities["name"].value == "all"


# pylint: disable=redefined-outer-name
def test_brightness_name(intents, slot_lists):
    result = recognize(
        "set brightness of the hue to 50%", intents, slot_lists=slot_lists
    )
    assert result is not None
    assert result.intent.name == "SetBrightness"

    assert result.entities["name"].value == "light.hue"
    assert result.entities["brightness_pct"].value == 50

    # From YAML
    assert result.entities["domain"].value == "light"


# pylint: disable=redefined-outer-name
def test_brightness_not_cover(intents, slot_lists):
    result = recognize(
        "set brightness of the garage door to 50%", intents, slot_lists=slot_lists
    )
    assert result is None


# pylint: disable=redefined-outer-name
def test_temperature(intents, slot_lists):
    result = recognize(
        "what is the temperature in the living room?", intents, slot_lists=slot_lists
    )
    assert result is not None
    assert result.intent.name == "GetTemperature"

    assert result.entities["area"].value == "area.living_room"

    # From YAML
    assert result.entities["domain"].value == "climate"


# pylint: disable=redefined-outer-name
def test_close_name(intents, slot_lists):
    result = recognize("close the garage door", intents, slot_lists=slot_lists)
    assert result is not None
    assert result.intent.name == "CloseCover"

    assert result.entities["name"].value == "cover.garage_door"

    # From YAML
    assert result.entities["domain"].value == "cover"


# pylint: disable=redefined-outer-name
def test_close_not_light(intents, slot_lists):
    result = recognize("close the hue", intents, slot_lists=slot_lists)
    assert result is None


# pylint: disable=redefined-outer-name
def test_play(intents, slot_lists):
    result = recognize("play roku", intents, slot_lists=slot_lists)
    assert result is not None
    assert result.intent.name == "Play"

    assert result.entities["name"].value == "media_player.roku"

    # From context
    assert result.context["domain"] == "media_player"


# pylint: disable=redefined-outer-name
def test_play_no_cover(intents, slot_lists):
    result = recognize("play the garage door", intents, slot_lists=slot_lists)
    assert result is None


# pylint: disable=redefined-outer-name
def test_requires_context_implicit(intents, slot_lists):
    intent_context = {"area": "living room"}

    result = recognize(
        "close the curtains",
        intents,
        slot_lists=slot_lists,
        intent_context=intent_context,
    )
    assert result is not None
    assert result.intent.name == "CloseCurtains"

    assert result.entities["domain"].value == "cover"
    assert result.entities["device_class"].value == "curtain"


# pylint: disable=redefined-outer-name
def test_requires_context_none_provided(intents, slot_lists):
    result = recognize("close the curtains", intents, slot_lists=slot_lists)
    assert result is None


def test_lists_no_template() -> None:
    """Ensure list values without template syntax are plain text."""
    yaml_text = """
    language: "en"
    intents: {}
    lists:
      test:
        values:
          - "test value"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    test_list = cast(TextSlotList, intents.slot_lists["test"])
    text_in = test_list.values[0].text_in
    assert isinstance(text_in, TextChunk)
    assert text_in.text == "test value"


def test_list_text_normalized() -> None:
    """Ensure list text in values are normalized."""
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "run {test_name}"
    lists:
      test_name:
        values:
          - "tEsT    1"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    result = recognize("run test 1", intents)
    assert result is not None
    assert result.entities["test_name"].value == "tEsT    1"


def test_skip_prefix() -> None:
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "run {test_name}"
    lists:
      test_name:
        values:
          - "test"
    skip_words:
      - "the"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    result = recognize("run the test", intents)
    assert result is not None
    assert result.entities["test_name"].value == "test"


def test_skip_sorted() -> None:
    """Ensure skip words are processed longest first"""
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "run {test_name}"
    lists:
      test_name:
        values:
          - "test"
    skip_words:
      - "could"
      - "could you"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    result = recognize("could you run test", intents)
    assert result is not None
    assert result.entities["test_name"].value == "test"


def test_response_key() -> None:
    """Check response key in intent data"""
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "this is a test"
            response: "test_response"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    result = recognize("this is a test", intents)
    assert result is not None
    assert result.response == "test_response"


def test_entity_text() -> None:
    """Ensure original text is returned as well as substituted list value"""
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "run test {name} [now]"
              - "{name} test"
    lists:
      name:
        values:
          - in: "alpha "
            out: "A"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    for sentence in ("run test alpha, now", "run test alpha!", "alpha test"):
        result = recognize(sentence, intents)
        assert result is not None, sentence
        assert result.entities["name"].value == "A"
        assert result.entities["name"].text_clean == "alpha"


def test_number_text() -> None:
    """Ensure original text is returned as well as substituted number"""
    yaml_text = """
    language: "en"
    intents:
      TestIntent:
        data:
          - sentences:
              - "set {percentage}[%] [now]"
              - "{percentage}[%] set"
    lists:
      percentage:
        range:
          from: 0
          to: 100
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    for sentence in ("set 50% now", "set 50%", "50% set"):
        result = recognize(sentence, intents)
        assert result is not None, sentence
        assert result.entities["percentage"].value == 50
        assert result.entities["percentage"].text.strip() == "50%"


def test_recognize_all() -> None:
    """Test recognize_all method for returning all matches."""
    yaml_text = """
    language: "en"
    intents:
      TestIntent1:
        data:
          - sentences:
              - "run test"
      TestIntent2:
        data:
          - sentences:
              - "run test"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    results = list(recognize_all("run test", intents))
    assert len(results) == 2
    assert {result.intent.name for result in results} == {
        "TestIntent1",
        "TestIntent2",
    }


def test_ignore_whitespace() -> None:
    """Test option to ignore whitespace during matching."""
    yaml_text = """
    language: "en"
    settings:
      ignore_whitespace: true
    intents:
      TestIntent1:
        data:
          - sentences:
              - "run [the] test"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    for sentence in ("runtest", "runthetest", "r u n t h e t e s t"):
        result = recognize(sentence, intents)
        assert result is not None, sentence


def test_skip_words_ignore_whitespace() -> None:
    """Test option to ignore whitespace with skip words during matching."""
    yaml_text = """
    language: "en"
    settings:
      ignore_whitespace: true
    intents:
      TestIntent1:
        data:
          - sentences:
              - "ad"
    skip_words:
      - "bc"
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    result = recognize("abcd", intents)
    assert result is not None


def test_local_expansion_rules() -> None:
    """Test local expansion rules, defined at the intent level"""
    yaml_text = """
    language: "en"
    intents:
      GetSmokeState:
        data:
          - expansion_rules:
              verb: "(are|is)"
              subject: "[all] [the] light[s]"
              state: "on"
              location: "[in <area>]"
            sentences:
              - "<verb> <subject> <state> <location>"
              - "<verb> <subject> <location> <state>"
    expansion_rules:
      area: "[the] {area}"
    lists:
      area:
        values:
          - kitchen
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    for sentence in (
        "are the lights on in the kitchen",
        "are the lights in the kitchen on",
    ):
        result = recognize(sentence, intents)
        assert result is not None, sentence
        assert result.intent.name == "GetSmokeState"


def test_unmatched_entity() -> None:
    """Test allow_unmatched_entities option to provide better feedback."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "set [all] {domain} in {area} to {percent}[%] now"
              - "set {area} {domain} to {percent}"
    lists:
      area:
        values:
          - kitchen
          - bedroom
      domain:
        values:
          - lights
      percent:
        range:
          type: percentage
          from: 0
          to: 100
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "set fans in living room to 101% now"

    # Should fail without unmatched entities enabled
    result = recognize(sentence, intents, allow_unmatched_entities=False)
    assert result is None, f"{sentence} should not match"

    # Should succeed now
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"domain", "area", "percent"}
    domain = result.unmatched_entities["domain"]
    assert isinstance(domain, UnmatchedTextEntity)
    assert domain.text == "fans "

    area = result.unmatched_entities["area"]
    assert isinstance(area, UnmatchedTextEntity)
    assert area.text == "living room "

    percent = result.unmatched_entities["percent"]
    assert isinstance(percent, UnmatchedRangeEntity)
    assert percent.value == 101

    sentence = "set all lights in kitchen to blah blah blah now"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"percent"}

    percent = result.unmatched_entities["percent"]
    assert isinstance(percent, UnmatchedTextEntity)
    assert percent.text == "blah blah blah "

    # Test with unmatched entity at end of sentence
    sentence = "set kitchen lights to fifty"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"percent"}

    percent = result.unmatched_entities["percent"]
    assert isinstance(percent, UnmatchedTextEntity)
    assert percent.text == "fifty"


def test_no_empty_unmatched_entity() -> None:
    """Test that unmatched entities are not empty."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "turn on {name}[ please]"
              - "illuminate all[ {area}] lights"
              - "activate {name} now"
    lists:
      name:
        values:
          - light
      area:
        values:
          - bedroom
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "turn on "
    results = list(recognize_all(sentence, intents, allow_unmatched_entities=True))
    assert not results, f"{sentence} should not match"

    # With optional word at end
    sentence = "turn on please"
    results = list(recognize_all(sentence, intents, allow_unmatched_entities=True))
    assert not results, f"{sentence} should not match"

    sentence = "illuminate all lights"
    results = list(recognize_all(sentence, intents, allow_unmatched_entities=True))
    assert results, f"{sentence} should match"
    assert len(results) == 1, "Only 1 result expected"
    assert not results[0].unmatched_entities, "No unmatched entities expected"

    sentence = "illuminate all kitchen lights"
    results = list(recognize_all(sentence, intents, allow_unmatched_entities=True))
    assert results, f"{sentence} should match"
    assert len(results) == 1, "Only 1 result expected"
    result = results[0]
    assert set(result.unmatched_entities.keys()) == {"area"}
    area = result.unmatched_entities["area"]
    assert isinstance(area, UnmatchedTextEntity)
    assert area.text == "kitchen "

    # With required word at end
    sentence = "activate now"
    results = list(recognize_all(sentence, intents, allow_unmatched_entities=True))
    assert not results, f"{sentence} should not match"


def test_unmatched_entity_context() -> None:
    """Test that unmatched entities work with requires/excludes context."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "open {name}"
            requires_context:
              domain: cover
    lists:
      name:
        values:
          - garage door
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "open garage door"

    # Should fail when unmatched entities aren't allowed
    result = recognize(sentence, intents, allow_unmatched_entities=False)
    assert result is None, f"{sentence} should not match"

    # Should succeed now with an unmatched domain entity
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"domain"}
    domain = result.unmatched_entities["domain"]
    assert isinstance(domain, UnmatchedTextEntity)
    assert domain.text == MISSING_ENTITY

    # Now both entities are unmatched
    sentence = "open back door"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"domain", "name"}

    domain = result.unmatched_entities["domain"]
    assert isinstance(domain, UnmatchedTextEntity)
    assert domain.text == MISSING_ENTITY

    name = result.unmatched_entities["name"]
    assert isinstance(name, UnmatchedTextEntity)
    assert name.text == "back door"


def test_unmatched_slot_name() -> None:
    """Test that unmatched entities use slot name instead of list name."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "run {script_name:name}"
              - "execute script {script_number:number}"
    lists:
      script_name:
        values:
          - stealth mode
      script_number:
        range:
          from: 1
          to: 100
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "run missing name"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"name"}

    sentence = "execute script wrong number"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"number"}

    # Outside range
    sentence = "execute script 0"
    result = recognize(sentence, intents, allow_unmatched_entities=True)
    assert result is not None, f"{sentence} should match"
    assert set(result.unmatched_entities.keys()) == {"number"}


def test_wildcard() -> None:
    """Test wildcard slot lists/entities."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "play {album} by {artist}[ please] now"
              - "start {album} by {artist}"
              - "begin {album} by artist {artist}"
    lists:
      album:
        wildcard: true
      artist:
        wildcard: true
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "play the white album by the beatles please now"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"album", "artist"}
    assert result.entities["album"].value == "the white album "
    assert result.entities["artist"].value == "the beatles "

    # Wildcards cannot be empty
    sentence = "play by please now"
    result = recognize(sentence, intents)
    assert result is None, f"{sentence} should not match"

    # Test without text at the end
    sentence = "start the white album by the beatles"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"album", "artist"}
    assert result.entities["album"].value == "the white album "
    assert result.entities["artist"].value == "the beatles"

    # Test use of next word in wildcard
    sentence = "play day by day by taken by trees now"
    results = list(recognize_all(sentence, intents))
    assert results, f"{sentence} should match"
    assert len(results) == 3  # 3 "by" words

    # Verify each combination of album/artist is present
    album_artist = {
        (result.entities["album"].value, result.entities["artist"].value)
        for result in results
    }
    assert album_artist == {
        ("day ", "day by taken by trees "),
        ("day by day ", "taken by trees "),
        ("day by day by taken ", "trees "),
    }

    # Add "artist" word
    sentence = "begin day by day by artist taken by trees"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"album", "artist"}
    assert result.entities["album"].value == "day by day "
    assert result.entities["artist"].value == "taken by trees"


def test_optional_wildcard() -> None:
    """Test optional wildcard slot list."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "play {album}[by {artist}]"
    lists:
      album:
        wildcard: true
      artist:
        wildcard: true
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    # With all wildcards
    sentence = "play the white album by the beatles"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"album", "artist"}
    assert result.entities["album"].value == "the white album "
    assert result.entities["artist"].value == "the beatles"

    # Missing one wildcard
    sentence = "play the white album"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"album"}
    assert result.entities["album"].value == "the white album"


def test_wildcard_slot_name() -> None:
    """Test wildcard uses slot instead of list name."""
    yaml_text = """
    language: "en"
    intents:
      Test:
        data:
          - sentences:
              - "run {script_name:name}"
    lists:
      script_name:
        wildcard: true
    """

    with io.StringIO(yaml_text) as test_file:
        intents = Intents.from_yaml(test_file)

    sentence = "run script 1"
    result = recognize(sentence, intents)
    assert result is not None, f"{sentence} should match"
    assert set(result.entities.keys()) == {"name"}
    assert result.entities["name"].value == "script 1"
