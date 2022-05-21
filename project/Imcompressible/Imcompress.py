import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Imcompress:
    def __init__(self,_length=3.5,_width=2,_v=1,_r=1):
        self.length = _length
        self.width = _width
        self.v = _v
        self.r = _r
        #self.type = _type #type=1: stream function type =2: potential function
        self.Diff = 0
        data1 = {"length":self.length,"width":self.width}
        assert self.width<=self.length,'Invalid shape:{length}<={width}'.format(**data1)
        
        data2 = {"width":self.width,"r":self.r}
        assert self.r<=self.width,'Invalid radius:{width}<={r}'.format(**data2)
        
    
    
    def cal_stream(self, dx=0.1, dy=0.1, eps=1e-7, save_flag=0,max_iter=10000):
        '''
        :param x: step of x
        :param y: step of y
        :param eps: the error permission of the solution
        :return: difference stream function matrix
        '''  
        #定义参数
        x_num = len(np.arange(0,self.length,dx))
        y_num = len(np.arange(0,self.width,dy))
        
        #设定初始值
        Diff = np.zeros((y_num+1,x_num+1))
        
        print(np.shape(Diff))
        #设置第一类边界条件
        #i表示x方向点数，即列数；j表示y方向点数，即行数
        
        #ED边
        for i in range(x_num+1):
            Diff[y_num,i]=2
        
        #AE边    
        for j in range(y_num+1):
            Diff[j,0] = j*dy*self.v


        #AB、BC边上流函数值均为0(CD边在迭代中进行运算)
        #AB边长
        #x_num_reduce = r/dx
        #for i in range(x_num+1):
            #Diff[0,i] = 0
        
        #BC边
        #BC边的边界条件转换为BO边与OC边
        #y_num_OC = self.r//dy
        #for j in range(int(y_num_OC+1)):
            #Diff[j,x_num]=0
        

        print(Diff)
        
        #迭代求解
        #注意有三类不同的点：正则内点、非正则内点、CD边界上的点
        #注意分类方法，不同的迭代公式
        iter_num=0
        #phi = np.linalg.norm(Diff)
        temp = np.zeros((y_num+1,x_num+1))
        #print(phi)
        delta = 1
        while(delta>eps):
            iter_num+=1
            #如运行超过所需迭代次数，则证明初始条件指定不合适
            assert iter_num<=max_iter, 'Improper initial condition'
            
            for j in range(1,y_num):
                for  i in range(1,x_num+1):
                    
                    #可能出现非正则内点的点个数
                    #x_num_abnormal = self.r//dx
                    #y_num_abnormal = self.r//dy
                    #x_num_normal = x_num-x_num_abnormal
                    
                    if i*dx<self.length-self.r or j*dx >self.r:
                        if i !=x_num: #正则内点
                            Diff[j,i] = ((Diff[j,i+1]+Diff[j,i-1])/dx**2+(Diff[j+1,i]+Diff[j-1,i])/dy**2)/(2/dx**2+2/dy**2)
                        else:
                            Diff[j,i] = (2*Diff[j,i-1]+Diff[j-1,i]+Diff[j+1,i])/4
                            

                    else: #可能异常点，计算a、b判断点的类型
                        
                        #计算a、b
                        a = self.length-i*dx-np.sqrt(self.r**2-(j*dy)**2)
                        b = j*dy - np.sqrt(self.r**2-(self.length-i*dx)**2)
                        
                        if a<=0 or b<=0: #圆柱内或表面的点
                            Diff[j,i] = 0    
                        elif 0<a<dx and 0<b<dy: #非正则内点插值计算，此处用到了边界条件BC边上的流函数值为0
                            Diff[j,i] = (Diff[j,i-1]/(dx*(dx+a))+Diff[j+1,i]/(dy*(dy+b)))/(1/(a*dx)+1/(b*dy))
                        elif a>=dx and b<=dy:
                            Diff[j,i] = (Diff[j,i-1]/(dx*(dx+dx))+Diff[j+1,i]/(dy*(dy+b))+Diff[j,i+1]/(dx*(dx+dx)))/(1/(dx*dx)+1/(b*dy))
                        elif a<=dx and b>=dy:
                            Diff[j,i] = (Diff[j,i-1]/(dx*(a+dx))+Diff[j+1,i]/(dy*(dy+dy))+Diff[j-1,i]/(dy*(dy+dy)))/(1/(dx*a)+1/(dy*dy))
                        else: #正则内点
                            Diff[j,i] = ((Diff[j,i+1]+Diff[j,i-1])/dx**2+(Diff[j+1,i]+Diff[j-1,i])/dy**2)/(2/dx**2+2/dy**2)
                    
                    
            #phi1 = np.linalg.norm(Diff)
            #delta = abs(phi1-phi)
            #print(Diff)
            #print(temp)
            delta = np.max(np.absolute(Diff-temp))
            #print(Diff==temp)
            print(delta)
            #phi = phi1
            temp = Diff.copy()
            
        
        self.Diff=Diff
        #print(Diff)
        
        if save_flag==1:
            data =pd.DataFrame(Diff)
            data.to_excel('ouput.xlsx')
        
        #if(plot_flag==1):
            
            #x = np.arange(0,self.length+dx,dx)
            #y = np.arange(0,self.width+dy,dy)
            
            
            #plot
            #plt.figure(figsize=(8,6),dpi=80)
            #C=plt.contour(x,y,Diff,[0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8])
            #plt.clabel(C,inline=True,fontsize=10)
            #plt.show()
        
        return Diff
        
        
        
            