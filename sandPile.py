# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:21:05 2020

@author: Louie
"""

import numpy as np
import matplotlib.pyplot as plt
import time as time
import random as rand
from matplotlib import colors
from matplotlib.animation import FuncAnimation
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
from tqdm import tqdm
import sys



class Pile():
    
    def __init__(self,n):
        self.n=n
        self.m=(n+2)*(n+2)
        self.into=0
        self.grid=[]
        self.threshold=np.ones((self.m),dtype=int)*3
        self.heights=np.zeros((self.m),dtype=int)
        self.relaxed=np.ones((self.m),dtype=bool)
        self.indicies=[]
        self.edge=np.zeros((self.m),dtype=bool)
    
    def active(self):
        self.edge[0:(self.n+2)]=True
        self.edge[-(self.n+2):]=True
        self.edge[0::(self.n+2)]=True
        self.edge[self.n+1::self.n+2]=True
    def relax_test(self):
        
        start=time.time()
        
        temp=self.threshold-self.heights
        #print(temp)
        self.relaxed=temp<0
        #print(self.relaxed)
        #print(self.edge)
        self.relaxed[self.edge]=False
        #print(self.relaxed)
        if len(self.heights[self.relaxed])>0:
            #print("unstable in %s"%(time.time()-start))
            return False
        if len(self.heights[self.relaxed])==0:
            #print("stable in %s"%(time.time()-start))  
            
            return True
            
        
    def test_heights(self):
        self.heights=np.random.randint(6, size=(self.m))
        return self.heights 

    def relax(self):
        for i in range(self.n):
            for j in range(self.n):
                if self.relaxed[i][j]==True:    
                    self.heights[i][j]=self.heights[i][j]-4
                    if i==0:
                        
                        if j==0:
                            self.heights[i][j+1]=self.heights[i][j+1]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                        if j==self.n-1:
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                        else:
                            self.heights[i][j+1]=self.heights[i][j+1]+1
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                            
                    if i==self.n-1:
                        if j==0:
                            self.heights[i][j+1]=self.heights[i][j+1]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                        if j==self.n-1:
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                        else:
                            self.heights[i][j+1]=self.heights[i][j+1]+1
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                    else:
                        
                        if j==0:
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                        if j==self.n-1:
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                        else:
                            self.heights[i][j+1]=self.heights[i][j+1]+1
                            self.heights[i][j-1]=self.heights[i][j-1]+1
                            self.heights[i-1][j]=self.heights[i-1][j]+1
                            self.heights[i+1][j]=self.heights[i+1][j]+1
                            

        return self.heights
    
        
    def relax_vector(self):
        
        self.relaxed[self.edge]=False
        self.heights[self.relaxed]=self.heights[self.relaxed]-4
        temp=np.where(self.relaxed)
        index=[(i+1,i-1,i+self.n+2,i-self.n-2) for i in temp]
        index=np.array(index)
        index=index.ravel()
        
        #self.heights[index]=self.heights[index]+1
        for i in index:
            self.heights[i]=self.heights[i]+1
    
        return self.heights
        
        
    def drive(self,m,x=0,y=0):
        org=int((self.m-1)/2)
        self.heights[org+x+self.m*y]=self.heights[org+x+self.m*y]+1
       
    
    
    def run(self,N,x=0,y=0):
        count=0
        
        self.active()
        pbar = tqdm(total = N+1)
        while count<N:
            self.drive(1,x,y)
            self.into=self.into+1
            while not self.relax_test():
                self.relax_vector()
                
            count=count+1
            pbar.update(1)
        self.height()
        pbar.close()
      
    def run_anim(self,N):
        
        self.drive(1)
        self.into=self.into+1
        while not self.relax_test():
            self.relax()
           
        
        plot=self.plot()  
        return plot
    
    def height(self):
        temp=self.heights[~self.edge]
        print(sum(temp))
       
    def multi_run(self,N,x,y):
        count=0
        while count<N:
            self.drive(1,+x,+y)
            self.drive(1,-x,-y)
            self.drive(1,-x,y)
            self.drive(1,x,-y)
            self.drive(1,2*x,0)
            self.drive(1,0,2*y)
            self.drive(1,-2*x,0)
            self.drive(1,0,-2*y)
            self.drive(1,0,0)
            self.into=self.into+1
            while not self.relax_test():
                self.relax()
                
            count=count+1    
    def plot(self):
        
        #fig, ax = plt.subplots() 
        fig=plt.figure(4)
        plt.axis('off')
        ax = fig.add_subplot(1,1,1)
        norm=plt.Normalize(0,3)
        colors_list=["white","#08F593","#00A35F","#F03513"]
        cmap= colors.ListedColormap(colors_list)  
        temp=self.heights[~self.edge]
        temp=np.reshape(temp,(self.n,self.n))
        x=np.linspace(0,self.n,self.n+1)
        y=np.linspace(0,self.n,self.n+1)
       
        plot=ax.pcolormesh(x, y, temp,cmap=cmap,alpha=0.8)
        #plot=ax.pcolormesh(x, y, temp,color=colors_list)
        #plot=ax.contorf(x,y,temp,cmap=cmap)
        return plot
    


def animate(N):
    a=Pile(81)
    count=0
    while count<N:
        a.multi_run(1,10,5)
        plot=a.plot()
        plt.savefig("%s"%(count))
        count=count+1
        
        
#FuncAnimation(fig, a.run_anim, frames=10)
#plt.show()

#animate(1000)



def main(size,grains):
    s=time.time()    
    a=Pile(size)
    a.run(grains)
    a.plot()     
    print(time.time()-s) 
    plt.show()
         
    
size=int((sys.argv[1]))
grains=int((sys.argv[2]))
main(size,grains)    