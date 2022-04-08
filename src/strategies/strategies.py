from src.utils.strategy.modifiers import mutate


default = [
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
    ";",
    "#",
    "\n",
    "\0"
]


def fun():
    return 1


strategies = {
    'default': default,
}

methods = {
    'mutate': mutate,
    'increment_every_item':
        lambda item, val: [x + val for x in item if isinstance(x, int)] if isinstance(item, list) else item,
    'fun': fun
}


def register_strategy(name, data) -> None:  # TODO make types for all functions
    strategies.update({name: data})


def register_method(name, data) -> None:  # TODO make types for all functions
    methods.update({name: data})

