import pytest
from RecordLib.ruledefs.seal import Decision
import json
from RecordLib.serializers import to_serializable

def test_decision_boolean():
    want_pizza = Decision(name="Do I want pizza?", value=True, reasoning="Pizza is good.")
    assert bool(want_pizza) is True
    want_snakes = Decision(name="Do I want snakes", value=None, reasoning="Snakes can be scary")
    assert bool(want_snakes) is False
    assert want_snakes.value is None

def test_decision_equality():
    want_pizza = Decision(name="Want pizza?", value="Yes I do", reasoning="yummm")
    want_candy = Decision(name="want candy?", value="Yes I do", reasoning="ooh, yumm.")
    assert (want_pizza == want_candy)

def test_decision_composes():
    want_pizza = Decision(name="want pizza?", value=True, reasoning="Pizza is good.")
    want_ice_cream = Decision(name="want ice cream?", value=True, reasoning="Ice cream is good")
    go_to_birra = Decision(
        name="Should we go to Birra?",
        value=(want_pizza and want_ice_cream),
        reasoning=[want_pizza.as_dict(), want_ice_cream.as_dict()]
    )
    assert go_to_birra.value == True
    assert go_to_birra.reasoning == [
        {"name": "want pizza?",
         "value": True,
         "reasoning": "Pizza is good.",
        },
        {"name": "want ice cream?",
         "value": True,
         "reasoning": "Ice cream is good",
        },
    ]

def test_decision_json_encodeable():
    want_pizza = Decision(name="want pizza?", value=True, reasoning="Pizza is good.")
    want_ice_cream = Decision(name="want ice cream?", value=True, reasoning="Ice cream is good")
    go_to_birra = Decision(
        name="Should we go to Birra?",
        value=(True if want_pizza and want_ice_cream else False),
        reasoning=[want_pizza.as_dict(), want_ice_cream.as_dict()]
    )
    try:
        res = json.dumps(go_to_birra, default=to_serializable, indent=4)
    except TypeError:
        pytest.fail("Decision object can't be json-encoded.")
