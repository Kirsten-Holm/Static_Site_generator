from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)


    def to_html(self):
        
        if self.tag is None:
            raise ValueError ("Error no tag set!")
        if self.children is None:
            raise ValueError ("Error no children, perhaps they've been kidnapped!")
        return_string = ""
        for child in self.children:
            return_string += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{return_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"