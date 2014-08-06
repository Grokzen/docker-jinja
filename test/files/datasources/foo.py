from djinja.env import global_function


@global_function
def bar(name):
    return " - {} - ".format(name)
