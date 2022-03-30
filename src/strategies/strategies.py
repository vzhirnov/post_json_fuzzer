basic_cases = [
    "Îäíàæäû",
    -1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162,
    -0.1,
    -1,
    0,
    1,
    1.0,
    1623761273615273651762351726357162357162357162357162537165237162537615237615273651726351726176235716357162357162,
    "",
    "a",
    None,
    True,
    False,
    [],
    ["test"],
    [0],
    "\n",
    "\0"  # TODO b'' ?
]

STRATEGY_2 = [101, 102, 103, 104, 105]
STAR = [777, 888, 999, 101010, 111111]


def fun():
    return 1


ready_strategies = {
    'basic_cases': basic_cases,
    'STAR': STAR,
    'STRATEGY_2': STRATEGY_2
}

strategy_methods = {
    'increment_every_item':
        lambda item, val: [x + val for x in item if isinstance(x, int)] if isinstance(item, list) else item,
    'fun': fun
}
