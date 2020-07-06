import pyexifinfo as p


def GetType(image):
    type = p.get_json(image)[0]["File:FileTypeExtension"]
    return type

class ImageJPG:
    """
    Make an image object for JPG ONLY
    """
    def __init__(self, image):
        self.data = p.get_json(image)[0]
    
    def GetMime(self):
        return str(self.data["File:MIMEType"])
    
    def GetHeight(self):
        return str(self.data["File:ImageHeight"])
    
    def GetWidth(self):
        return str(self.data["File:ImageWidth"])

    def GetImageSize(self):
        return str(self.data["Composite:ImageSize"])
    
    def GetXRes(self):
        return str(self.data["JFIF:XResolution"])

    def GetYRes(self):
        return str(self.data["JFIF:YResolution"])

    def GetJFIFVersion(self):
        return str(self.data["JFIF:JFIFVersion"])
    
    def GetOrientation(self):
        return str(self.data["EXIF:Oreientation"])
    
    def GetResUnit(self):
        return str(self.data["JFIF:ResolutionUnit"])

    def GetFileSize(self):
        return str(self.data["File:FileSize"])

    def GetPerms(self):
        return str(self.data["File:FilePermissions"])

    def GetByteOrder(self):
        return str(self.data["File:ExifByteOrder"])

'''
class ImagePNG:
    def __init__(self, image):
        self.data = p.get_json(image)[0]

    def GetImageSize(self):
        return self.data["Composite:ImageSize"]

    def GetMime(self):
        return self.data["File:MIMEType"]
'''