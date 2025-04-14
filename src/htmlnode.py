




class HTMLNode:
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


        
    def to_html(self):
        if self.value is None and not self.children:
            return f"<{self.tag}></{self.tag}>"

        if self.value is None:
            children_html = ""
            for child in self.children:
                children_html += child.to_html()
            return f"<{self.tag}>{children_html}</{self.tag}>"

        if not self.children:
            return f"<{self.tag}>{self.value}</{self.tag}>"

        # This case should not happen based on our implementation
        # but included for completeness
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}>{self.value}{children_html}</{self.tag}>"
        

    def props_to_html(self):
        props_to_string = ""
        if self.props != None:
            for key, value in self.props.items():
                props_to_string += f" {key}=\"{value}\""
        return props_to_string
    

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    




    





        
