# For now, simply print out the
# text within the response body
def renderBody(body):

    in_bracket = False
    for c in body:
        if c == '<':
            in_bracket = True
        elif c == '>':
            in_bracket = False
        elif not in_bracket:
            print(c, end="")
