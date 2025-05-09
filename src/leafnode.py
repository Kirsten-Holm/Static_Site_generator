from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        if self.tag == "img":
            return f"<{self.tag}{self.props_to_html()} />"
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
"""
This was the LeafNode Class i wrote, it's kinda bad because i forgot about the parent class HTMLNode's methods so i just took the one from boot.dev
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value is None:
            raise ValueError ("Error node has no value!")
        if self.tag is None:
            return f"{self.value}"
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return_string = f"<{self.tag} "
        for key, value in self.props.items():
            return_string += f"{key}=\"{value}\" "
        if self.tag == "img":
            return return_string +"/>" 
        return_string = return_string.strip() + ">"
        return return_string + f"{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag},{self.value},{self.props})"

"""