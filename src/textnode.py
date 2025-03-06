from enum import Enum






class TextType (Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE =  "image"
    
    
class TextNode:
    def __init__(self,text,texttype,url=None):
        self.text = text
        self.TextType = TextType(texttype)
        self.url = url
        
        
    def __eq__(self,textNode):
        if self.text == textNode.text and self.TextType == textNode.TextType and self.url == textNode.url:
            return True
        return False
    
    def __repr__(self):
        
        return f"TextNode({self.text}, {self.TextType.value}, {self.url})"
        
        
    
    








