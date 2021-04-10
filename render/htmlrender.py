from dataclasses import dataclass

@dataclass
class Text:
    text: str

@dataclass
class Tag:
    tag: str

def grabBody(html):
    found_body = False
    body_start_idx = 0
    body_end_idx = 0

    for idx, elem in enumerate(html):
        if elem == '<' and html[idx:idx+len("<body")] == "<body":
            found_body = True
            body_start_idx = idx
        if found_body and html[idx:idx+len("</body>")] == "</body>":
            body_end_idx = idx + len("</body>")
    
    if (found_body):
        return html[body_start_idx:body_end_idx]
    else:
        raise Exception("No body in page")
        

def lex(body):

    output = []
    text = ""
    in_bracket = False

    for idx, elem in enumerate(body):
        if elem == '<':
            in_bracket = True
            if (text):
                output.append(Text(text))
            text = ""
        elif elem == '>':
            in_bracket = False
            output.append(Tag(text))
            text = ""
        else:
            text += elem

    if not in_bracket and text:
        output.append(Text(text))
    
    return output
