from matplotlib.pyplot import show
import numpy as np
import random,sys,cv2,time
import matplotlib.pyplot as plt


class Point:
    def __init__(self,height,weight):
        self.height = height
        self.weight = weight
        self.cluster = False
        self.visit = False
    
    def distance(self,point):
        return ((self.height - point.height)**2 + (self.weight - point.weight)**2)**0.5

    def show(self):
        print("height:{}  weight:{}".format(self.height,self.weight))

def read_img(img_dir):
    img = cv2.imread(img_dir,cv2.IMREAD_GRAYSCALE)       #img[h][w][bgr]
    size = img.shape                  #size[0]=height,size[1]=weight
    global height,weight
    all_point = []
    for i in range(0,size[0]):
        for j in range(0,size[1]):
            if img[i][j] == 0:
                all_point.append(Point(i,j))
    return all_point,size



def getNeighbors(all_point,point,eps):
    count = 0
    neighbor = []
    for p in all_point:
        distance = ((point.height - p.height)**2 + (point.weight - p.weight)**2)**0.5
        if distance <= eps:
            neighbor.append(p)
    return neighbor



def expandCluster(all_point,point,neighborpts,eps,minpts):
    cluster = [point]
    for p in neighborpts:
        if p.visit == False:
            p.visit = True
            pneighbors = getNeighbors(all_point,p,eps)
            if len(pneighbors) >= minpts:
                neighborpts += pneighbors
        if p.cluster == False:
            if p not in cluster:
                cluster.append(p)
    return cluster



def dbscan(all_point,eps,minpts):
    C = []
    noise = []
    for point in all_point:
        point.show()
        if point.visit :
            continue
        point.visit = True
        neighborpts = getNeighbors(all_point,point,eps)
        if len(neighborpts) < minpts:
            point.cluster == True
            noise.append(point)
        else:
            C.append(expandCluster(all_point,point,neighborpts,eps,minpts))
    return C,noise



def write_img(cluster,noise,size):
    random.seed(12)
    color = []
    img = np.zeros((size[0], size[1], 3), dtype="uint8")
    img.fill(255)
    
    for i in range(0,len(cluster)):
        for p in cluster[i]:
            
            color.append([random.randint(0,255), random.randint(0,255), random.randint(0,255)])
            img[p.height,p.weight] = color[i]
    cv2.imwrite("result.jpg",img)
    print(len(cluster))



def main(eps,minpts):
    all_point,size = read_img("./Demo2.bmp")
    start = time.process_time()

    cluster,noise = dbscan(all_point,eps,minpts)
    write_img(cluster,noise,size)
    end = time.process_time()
    print("cost:{}s".format(end-start))
    

if __name__ == "__main__":
    eps = 1
    minpts = 7
    main(eps,minpts)