from cv2 import aruco
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import xml.etree.ElementTree as ET
import os

aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)

class aurucoMarker():
    def __init__(self, id, name):
        self.name = name
        self.id = id
        self.date = datetime.now()

        print('GENERATE AuRuco marker...')
        print('Generate maerker: '+name+' with Id:'+str(id))

        self.img = aruco.drawMarker(aruco_dict,id, 500)

    def createMarker(self):
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        ax.imshow(self.img, cmap=mpl.cm.gray, interpolation="nearest")
        ax.axis("off")
        plt.text(0, -60, 'Marker: '+self.name)
        plt.text(0, -40, 'Id:         ' + str(self.id))
        plt.text(0, -20, 'Date:    ' + self.date.strftime("%d/%m/%Y %H:%M:%S"))

        plt.show()
        self.fig = fig
        self.fig.savefig("../configs/marker/"+self.name+".pdf")

def createMarker(name,id,ConfigId):
    date = datetime.now()
    img = aruco.drawMarker(aruco_dict, id, 500)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(img, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
    plt.text(0, -60, 'Marker: ' + name)
    plt.text(0, -40, 'Id:         ' + str(id))
    plt.text(0, -20, 'Date:    ' + date.strftime("%d/%m/%Y %H:%M:%S"))

    plt.show()
    fig = fig
    fig.savefig("../configs/"+ConfigId+'/marker/' + name + ".pdf")

    return date

def createFromXML(xmlFile):
    try:
        os.makedirs("../configs/"+xmlFile+"/marker")
    except(OSError):
        print('Faild to create Dir')
    else:
        print('Successfully created Dir')
    tree = ET.parse('../configs/'+xmlFile+'.xml')
    MarkerXML = tree.findall('marker')
    for marker in MarkerXML:
        markerAtrib = marker.attrib
        date = createMarker(markerAtrib['Name'], int(markerAtrib['Id']), xmlFile)
        marker.attrib['Date'] = date.strftime("%d/%m/%Y %H:%M:%S")
        tree.write('../configs/'+xmlFile+'.xml')

if __name__ == '__main__':
    createFromXML('Default')
