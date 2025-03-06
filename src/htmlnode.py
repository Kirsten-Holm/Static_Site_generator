




class HTMLNode:
    def __init__(self,tag = None,value = None,children = None,props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props



    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_to_string = ""
        if self.props != None:
            for key, value in self.props.items():
                props_to_string += f" {key}=\"{value}\""
        return props_to_string
    

    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"
    




    





        
