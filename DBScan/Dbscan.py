import matplotlib.pyplot as plt # plt 用於顯示圖片
import matplotlib.image as mpimg # mpimg 用於讀取圖片
import numpy as np
import random
import time



def findNei(j,X,eps):
    
    regionList = []
    aList =  X.tolist()
    
    
    
    arr = X[j]
    wid = arr[0]
    hig = arr[1]
    
    
    #先抓取在正方形範圍內的點
    for w in range(wid-int(eps)-1, wid + int(eps) +2):        
        for h in range(hig-int(eps)-1, hig + int(eps) +2):
            
            #判斷點是反為黑點
            if [w, h] in aList :
                temp=np.sqrt(np.sum(np.square(X[j]-[w, h])))    #距離計算
                #判斷是否為範圍內
                if(temp<=eps):
                    regionList.append(aList.index( [w, h] ))
               
    return regionList



    
    

def dbscan(X,eps,min_Pts):
    k=-1
    NeighborPts=[]      #儲存某點範圍內的其他點
    Ner_NeighborPts=[]
    fil=[]                                      #已訪問點
    gama=[x for x in range(len(X))]            #未訪未點
    cluster=[-1 for y in range(len(X))]
    while len(gama)>0:
        j=random.choice(gama)
        gama.remove(j)  #移除未訪問點
        fil.append(j)   #新增訪問點

        NeighborPts=findNei(j,X,eps)
        if len(NeighborPts) < min_Pts:
            cluster[j]=-1   #不屬於任何區域內的點
        else:
            k=k+1
            cluster[j]=k
            for i in NeighborPts:
                if i not in fil:
                    gama.remove(i)
                    fil.append(i)
                    Ner_NeighborPts=findNei(i,X,eps)
                    if len(Ner_NeighborPts) >= min_Pts:
                        for a in Ner_NeighborPts:
                            if a not in NeighborPts:
                                NeighborPts.append(a)
                    if (cluster[i]==-1):
                        cluster[i]=k
     
    return cluster

def LoadData():

    # load
    img = mpimg.imread('Demo2.bmp') 
    # show
    plt.imshow(img) # 顯示圖片
    plt.show()
    
    
    #h：高   w：寬   c：通道
    h,w,c = img.shape 
    
    Hi=[]
    Wo=[]
    
    #尋找黑點位置
    for i in range(h):
        for j in range(w):
            if((img[i,j] == [0,0,0]).all()):
                Hi.append(h - i)
                Wo.append(j)
                
    #將兩個一維合併成二維 並轉呈 array         
    X = np.array(list(zip(Wo,Hi)))
    
    return X

if __name__=='__main__':
    eps=1    #距離
    min_Pts=7  #至少包含
    
    time_start = time.time() #開始計時
    
    X = LoadData()
    C=dbscan(X,eps,min_Pts)
    
    time_end = time.time()    #結束計時
    
    
    #顯示圖片
    plt.figure(figsize=(5, 5), dpi=50)
    plt.scatter(X[:,0],X[:,1],c=C)
    plt.show()
    
    
    time_c= time_end - time_start   #執行所花時間
    print('time:', time_c, 's')