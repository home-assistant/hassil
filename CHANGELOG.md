# Changelog

## 1.7.0

- Add multiplier to range

## 1.6.1

- Allow context values to be dicts

## 1.6.0

- Add metadata to sentences
- Add metadata to list items

## 1.5.3

- Restrict unmatched entities to contiguous blocks of non-literal text
- Automatically use intents language for number words if supported

## 1.5.2

- Add local slots (under data sentences)
- Add literal text chunk count and matched sentence template to results

## 1.5.1

- Expand `requires_context` to allow copying value to a slot

## 1.5.0

- Add fuzzy matching using edit distance

## 1.4.0

- Sort wildcard sentences so they are processed by most literal text chunks first

## 1.3.0

- Add number to word generation using [unicode-rbnf](https://github.com/rhasspy/unicode-rbnf) for range lists

## 1.2.5

- Fix degenerate wildcard case
