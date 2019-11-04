from libtiff import TIFF
import numpy as np
import shapefile as shp

import RasterPolygonEnumT 
import RPolygon
import TransFunc

import copy
import os

def main():
    print("main()")

    srcfile=TIFF.open("G:/11.tif",mode="r")
    img=srcfile.read_image();
    # img是四个维度的numpy.数组，[0,0,0,255] [255,255,255,255]
    # 使用的时候读取第一维就可以了
    xSize=np.size(img,1)
    ySize=np.size(img,0)
    print("ySize",ySize,"xSize",xSize)
    # bandNum=np.size(img,2)
    # os.system("pause")
    img.tolist()
    # print(len(img[0][0]))

    # [-1 band_data -1] 对齐
    panThisLineVal=[-1 for row in range(0,xSize+2)]
    panLastLineVal=[-1 for row in range(0,xSize+2)]
    panThisLineId=[-1 for row in range(xSize+2)]
    panLastLineId=[-1 for row in range(xSize+2)]
        
    # **************************                        
    # * first pass,get chain  *
    # **************************

    firstEnum=RasterPolygonEnumT.RasterPolygonEnumT()
    for iY in range(0,ySize):
        for iBand in range (1,xSize+1):
            panThisLineVal[iBand]=copy.deepcopy(img[iY][iBand-1][0])
        print("**  first pass line：",iY)
        firstEnum.ProcessLine(panLastLineVal, panThisLineVal, panLastLineId, panThisLineId, xSize,iY)
        panLastLineVal=copy.deepcopy(panThisLineVal)
        panLastLineId=copy.deepcopy(panThisLineId)
        
    firstEnum.CompleteMerges()
    print("after",firstEnum.nFinalPolyCount)
    print(firstEnum.panPolyIdMap)

    os.system("pause")

    # **************************                        
    # * second pass,add edges  *
    # **************************

    panThisLineVal=[-1 for row in range(0,xSize+2)]
    panLastLineVal=[-1 for row in range(0,xSize+2)]
    panThisLineId=[-1 for row in range(xSize+2)]
    panLastLineId=[-1 for row in range(xSize+2)]

    secondEnum=RasterPolygonEnumT.RasterPolygonEnumT()
    papoPoly=[RPolygon.RPolygon() for row in range(0,firstEnum.nNextPolygonId)]
    ADEG=TransFunc.TransFunc()
    for iY in range(0,ySize+1):
        if (iY < ySize):
            for iBand in range (1,xSize+1):
                panThisLineVal[iBand]=copy.deepcopy(img[iY][iBand-1][0])
 
        if (iY == ySize):
            panThisLineId = [-1 for row in range(0,xSize+2)]
        else:
            secondEnum.ProcessLine(panLastLineVal,panThisLineVal,panLastLineId,panThisLineId,xSize,iY)
            
        for iX in range(0,xSize+1):
            ADEG.AddEdges(panThisLineId,panLastLineId,firstEnum.panPolyIdMap,firstEnum.panPolyValue,papoPoly,iX,iY)

        panLastLineVal=copy.deepcopy(panThisLineVal)
        panLastLineId=copy.deepcopy(panThisLineId)
        print("second pass:",iY)

    """
    for iX in range(0,secondEnum.nNextPolygonId):
        if (papoPoly[iX].dfPolyValue!=-1):
            papoPoly[iX].Colesce()
            # ADEG.Clockwise(papoPoly[iX].aanXY)
            print("papoPoly:",iX)
            for iy in range(0,len(papoPoly[iX].aanXY)):
                print(papoPoly[iX].aanXY[iy][0]==papoPoly[iX].aanXY[iy][len(papoPoly[iX].aanXY[iy])-2] and papoPoly[iX].aanXY[iy][1]==papoPoly[iX].aanXY[iy][len(papoPoly[iX].aanXY[iy])-1])
                print("len(papoPoly[iX].aanXY)",len(papoPoly[iX].aanXY))
        if iX==26:
            papoPoly[iX].Trans()
            print(papoPoly[iX].polyXY)#[iy])
        if iX==43:
            papoPoly[iX].Trans()
            print(papoPoly[iX].polyXY)#[iy])
        if iX==92:
            papoPoly[iX].Trans()
            print(papoPoly[iX].polyXY)#[iy])
        if iX==101:
            papoPoly[iX].Trans()
            print(papoPoly[iX].polyXY)#[iy])
    """
    os.system("pause")
    
    shp_w=shp.Writer("G:/11_complete")
    field_std="polys"
    shp_w.field(field_std,"C")
    
    # os.system("pause")
    for iX in range(0,secondEnum.nNextPolygonId):
        print("papoPoly[iX].dfPolyValue",papoPoly[iX].dfPolyValue)
        if (papoPoly[iX].dfPolyValue!=-1):
            # print("!",papoPoly[iX].aanXY))
            papoPoly[iX].Colesce()
            # ADEG.Clockwise(papoPoly[iX].aanXY)
            papoPoly[iX].Trans()
            # print("poly_",iX,"::len(papoPoly[iX].polyXY)::",len(papoPoly[iX].polyXY))
            # print("papoPoly[iX].aanXY",papoPoly[iX].aanXY)
            # print("papoPoly[iX].polyXY",papoPoly[iX].polyXY)
            # os.system("pause")
            # shp_w.field(field_std+str(iX),"C")
            shp_w.poly(papoPoly[iX].polyXY)
            shp_w.record("polygon_"+str(iX))
            
    shp_w.balance()
    
    os.system("pause")

if __name__ == "__main__":
    main()

