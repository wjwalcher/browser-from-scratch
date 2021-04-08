# For now, simply print out the
# text within the response body
def renderBody(body):

    in_bracket = False
    in_body = False
    skip_iterations = 0
    for idx, elem in enumerate(body):
        if (skip_iterations > 0):
            skip_iterations -= 1
            continue

        if elem == '<' or elem == '>':
            in_bracket = not in_bracket
            if body[idx+1:idx+5] == "body":
                in_body = not in_body
        elif not in_bracket and in_body:
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
