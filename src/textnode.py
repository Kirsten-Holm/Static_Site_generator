from enum import Enum






class TextType (Enum):
    Normal = "normal"
    Bold = "bold"
    Italic = "italic"
    Code = "code"
    Links = "link"
    Images =  "image"
    
    
class TextNode:
    def __init__(self,text,texttype,url=None):
        self.text = text
        self.TextType = TextType(texttype)
        self.url = url
        
        
    def __eg__(self,textNode):
        if self.text == textNode.text and self.TextType == textNode.TextType and self.url == textNode.url:
            return True
        return False
    
    def __repr__(self):
        
        return f"TextNode({self.text}, {self.TextType.value}, {self.url})"
        
        
    
    








