# For now, simply print out the
# text within the response body
def renderBody(body, scheme=""):

    in_bracket = False
    in_body = False
    view_source = scheme == "view-source:"

    skip_iterations = 0
    for idx, elem in enumerate(body):
        if (skip_iterations > 0):
            skip_iterations -= 1
            continue

        if elem == '<' or elem == '>':
            in_bracket = not in_bracket
            if body[idx+1:idx+5] == "body":
                in_body = not in_body
            if (view_source):
                print(elem, end="")
        elif (not in_bracket and in_body) or view_source:
            # Convert entities &lt; and &gt; to < and >
            if elem == "&":
                if body[idx+1:idx+4] == "gt;":
                    print(">", end="")
                    skip_iterations = 3
                    continue
                elif body[idx+1:idx+4] == "lt;":
                    print("<", end="")
                    skip_iterations = 3
                    continue

            print(elem, end="")
