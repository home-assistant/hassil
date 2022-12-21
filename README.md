# HassIL

The Home Assistant Intent Language (HassIL) parser for [intents](https://github.com/home-assistant/intents).


## Dependencies

* antlr4-python3-runtime
* PyYAML
* dataclasses-json


## Installation

Run the `script/setup` script to automatically create a virtual environment and install the requirements.


# Running

``` sh
python3 -m hassil <yaml_file_or_directory> [<yaml_file_or_directory> ...]
```

Once loaded, you may type in a sentence and see what intent it matches.
For example:

``` sh
python3 -m hassil examples/en.yaml
what is the temperature in the living room
{'intent': 'HassClimateGetTemperature', 'area': 'living room', 'domain': 'climate'}
```

By default, the areas "kitchen", "bedroom", and "living room" are available. You can override this with `--areas`. Device or entity names can be provided with `--names`.

``` sh
python3 -m hassil examples/en.yaml --areas office --names trapdoor
open the trapdoor in the office
{'intent': 'HassOpenCover', 'name': 'trapdoor', 'area': 'office'}
```


### Sampling Sentences

Sentences for each intent can be sampled from the intent YAML files:

``` sh
python3 -m hassil.sample examples/en.yaml -n 1
{"intent": "HassTurnOn", "text": "turn on the entity"}
{"intent": "HassTurnOff", "text": "turn off the entity"}
{"intent": "HassOpenCover", "text": "open the entity in the area"}
{"intent": "HassCloseCover", "text": "close the entity in the area"}
{"intent": "HassLightsSet", "text": "set the entity color to red"}
{"intent": "HassClimateSetTemperature", "text": "set temperature to 0 degree s in the area"}
{"intent": "HassClimateGetTemperature", "text": "what is the temperature in the area"}
```

The `--areas` and `--names` arguments are the same from `python3 -m hassil`, but default to generic "area" and "entity" terms.

Exclude the `-n` argument to sample all possible sentences.


## Sentence Templates

Parsed using a custom [ANTLR](https://www.antlr.org) grammar (see [`HassILGrammar.g4`](HassILGrammar.g4)).

* Alternative words or phrases
  * `(red | green | blue)`
* Optional words or phrases
  * `[the]`
  * `[this | that]`
* Slot Lists
  * `{list_name}`
  * `{list_name:slot_name}`
  * Refers to a pre-defined list of values in YAML (`lists`)
* Expansion Rules
  * `<rule_name>`
  * Refers to a pre-defined expansion rule in YAML (`expansion_rules`)
