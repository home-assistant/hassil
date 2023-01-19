"""Tests for Hassil parser"""

from hassil.parser import ParseChunk, ParseType, next_chunk


def test_word():
    text = "test"
    assert next_chunk(text) == ParseChunk(
        text="test",
        parse_type=ParseType.WORD,
        start_index=0,
        end_index=len(text),
    )


def test_word_escape():
    text = "test\\(2\\)"
    assert next_chunk(text) == ParseChunk(
        text="test(2)",
        parse_type=ParseType.WORD,
        start_index=0,
        end_index=len(text),
    )


def test_group():
    text = "(test test2)"
    assert next_chunk(text) == ParseChunk(
        text="(test test2)",
        parse_type=ParseType.GROUP,
        start_index=0,
        end_index=len(text),
    )


def test_optional():
    text = "[test test2]"
    assert next_chunk(text) == ParseChunk(
        text="[test test2]",
        parse_type=ParseType.OPT,
        start_index=0,
        end_index=len(text),
    )


def test_list_reference():
    text = "{test}"
    assert next_chunk(text) == ParseChunk(
        text="{test}",
        parse_type=ParseType.LIST,
        start_index=0,
        end_index=len(text),
    )


def test_list_escape():
    text = "\\{test\\}"
    assert next_chunk(text) == ParseChunk(
        text="{test}",
        parse_type=ParseType.WORD,
        start_index=0,
        end_index=len(text),
    )


def test_rule_reference():
    text = "<test>"
    assert next_chunk(text) == ParseChunk(
        text="<test>",
        parse_type=ParseType.RULE,
        start_index=0,
        end_index=len(text),
    )


def test_rule_escape():
    text = "\\<test\\>"
    assert next_chunk(text) == ParseChunk(
        text="<test>",
        parse_type=ParseType.WORD,
        start_index=0,
        end_index=len(text),
    )
