from .htmlelements import Text, Element # TODO: should probably place these in this file

class HTMLParser:

    def __init__(self):
        self.unfinished = []
        self.SELF_CLOSING_TAGS = [
            "area", "base", "br", "col", "embed", "hr", "img", "input",
            "link", "meta", "param", "source", "track", "wbr",
        ]

    def getAttributes(self, text):
        parts = text.split()
        tag = parts[0].lower()

        attributes = {}
        for part in parts[1:]:
            if "=" in part:
                idx = part.index("=")
                value = part[idx+1:]

                # Strip out quotes if value quoted
                if len(value) > 2 and value[0] in ["'", "\""]:
                    value = value[1:-1]

                key = part[:idx]
                attributes[key.lower()] = value
            else:
                attributes[part.lower()] = ""

        return tag, attributes

    def addText(self, text):
        if (text.isspace()): return

        # Grab the last item in unfinished,
        # since this is the parent of the current text
        parent = self.unfinished[-1]
        node = Text(text, parent)
        parent.children.append(node)
    
    def addTag(self, text):
        tag, attributes = self.getAttributes(text)
        if (tag.startswith("!")): return

        # Close tag
        if (tag.startswith("/")):
            if (len(self.unfinished) == 1): return
            node = self.unfinished.pop()
            parent = self.unfinished[-1]
            parent.children.append(node)
        elif tag in self.SELF_CLOSING_TAGS:
            parent = self.unfinished[-1]
            node = Element(tag=tag, parent=parent, attributes=attributes)
            parent.children.append(node)
        # Open tag
        else:
            parent = self.unfinished[-1] if self.unfinished else None
            node = Element(tag=tag, parent=parent, attributes=attributes)
            self.unfinished.append(node)

    def finish(self):
        while self.unfinished:
            node = self.unfinished.pop()
            if not self.unfinished: 
                return node
            parent = self.unfinished[-1]
            parent.children.append(node)

    def parse(self, html):

        text = ""
        in_bracket = False

        for idx, elem in enumerate(html):

            if elem == '<':
                in_bracket = True
                if (text):
                    self.addText(text)
                text = ""
            elif elem == '>':
                in_bracket = False
                self.addTag(text)
                text = ""
            else:
                text += elem

        if not in_bracket and text:
            self.addText(text)

        return self.finish()

    def printTree(self, node, indent=0):
        print(" " * indent, node)
        for child in node.children:
            self.print_tree(child, indent+2)

