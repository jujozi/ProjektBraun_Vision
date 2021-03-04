import xml.etree.ElementTree as ET

def BasicStructur():
    Configuration = ET.Element('Configuration')
    ConfigVideo = ET.SubElement(Configuration, 'Video')

    ConfigVideo.set('Device', 'Webcam')
    ConfigVideo.set('adress', '0')
    ConfigVideo.set('x1', '0')
    ConfigVideo.set('y1', '0')
    ConfigVideo.set('x2', '0')
    ConfigVideo.set('y2', '0')
    ConfigVideo.set('Date', '0')

    marker = ET.SubElement(Configuration, 'marker')
    marker.set('Name', 'Object')
    marker.set('Id', '0')
    marker.set('Date', '0')
    marker.set('Filename', '0')

    marker = ET.SubElement(Configuration, 'marker')
    marker.set('Name', 'Reference_Cam1')
    marker.set('Id', '1')
    marker.set('Date', '0')
    marker.set('Filename', '0')


    return ET.tostring(Configuration).decode("utf-8")

def createConfigDefault(name):
    mydata = BasicStructur()
    # create a new XML file with the results
    myfile = open("../configs/"+name+".xml", "w")
    print(mydata)
    myfile.write(mydata)
    myfile.close()

if __name__ == '__main__':
    createConfigDefault('Default')
    tree = ET.parse("../configs/Default.xml")
    CamConfig = tree.findall('marker')
    for Cam in CamConfig:
        print(Cam.attrib)

