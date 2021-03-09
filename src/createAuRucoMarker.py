from cv2 import aruco
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib as mpl
from datetime import datetime
import xml.etree.ElementTree as ET
import os
import pickle



def createMarker(name,id,ConfigId):
    date = datetime.now()
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
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
    pathPDF = "../configs/"+ConfigId+'/marker/' + name + ".pdf"
    fig.savefig(pathPDF)

    return fig, date, pathPDF

def createMarkerCharuco(ConfigId):
    name = "CHARUCO"
    date = datetime.now()
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 5, 1, .8, aruco_dict)
    imboard = board.draw((2000, 2000))
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(imboard, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
    plt.text(0, -100, 'Marker: ' + name)
    plt.text(0, 0, 'Date:    ' + date.strftime("%d/%m/%Y %H:%M:%S"))
    plt.show()

    fig = fig
    pathPDF = "../configs/"+ConfigId+'/marker/' + name + ".pdf"
    fig.savefig(pathPDF)

    f = open("../configs/"+ConfigId+'/marker/' + name + ".chauruco", 'wb')
    pickle.dump(board, f)
    f.close()

    return fig, date, pathPDF

def fuckit():
    workdir = "../configs/Default/marker/"
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    board = aruco.CharucoBoard_create(7, 6, 1, .8, aruco_dict)
    imboard = board.draw((2000, 2000))
    cv.imwrite(workdir + "chessboard.tiff", imboard)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.imshow(imboard, cmap=mpl.cm.gray, interpolation="nearest")
    ax.axis("off")
    plt.show()

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
        fig, date, pathPDF = createMarker(markerAtrib['Name'], int(markerAtrib['Id']), xmlFile)
        marker.attrib['Date'] = date.strftime("%d/%m/%Y %H:%M:%S")
        marker.attrib['Filename'] = pathPDF
        tree.write('../configs/'+xmlFile+'.xml')

def setDimensions(xmlFile,id,dim):
    #Open xmlFile
    tree  = ET.parse('../configs/'+xmlFile+'.xml')
    MarkerXML = tree.find("marker/[@Id='"+str(id)+"']")
    MarkerXML.attrib['dimX'] = dim[0]
    MarkerXML.attrib['dimY'] = dim[1]
    print(MarkerXML.attrib)


if __name__ == '__main__':
    fuckit()
    #createMarkerCharuco('Default')

    #xmlFile = 'Default'
    #id = 0
    #setDimensions(xmlFile, id, [9.4, 9.4])
    #createFromXML(xmlFile)
