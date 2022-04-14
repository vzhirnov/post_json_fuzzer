from src.strategies.data_sets import default


def fun():
    return 1


data_sets = {
    'default': default,
}

methods = {
    # 'mutate': mutate,
    'increment_every_item':
        lambda item, val: [x + val for x in item if isinstance(x, int)] if isinstance(item, list) else item,
    'fun': fun
}

generators = {

}