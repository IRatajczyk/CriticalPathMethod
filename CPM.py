"""
Created on %(21.04)s

@author: %(Igor Ratajczyk)s
"""
import math
import matplotlib.pyplot as plt
from typing import List,Union

class Event:
    
    def __init__(self,name_:str,before_list:List[Event]):
        self.name=name_
        self.number = 0
        self.early_time = 0
        self.late_time = math.inf
        self.before =before_list
        self.activ=[]
        self.prec_actv=[]

    def __str__(self)->str:
        return str(self.name)

           
class Activity:
    
    def __init__(self,time: Union[int,float]=0):
        self.precedessor = None
        self.successor = None
        self.time = time

    def __str__(self):
        return "("+str(self.precedessor)+":"+str(self.successor)+")"
    

class CPM:
    def __init__(self):
        """
        

        Returns
        -------
        None.

        """
        self.event_list = []
        self.activity_list=[]
        self.start = None
        self.finish = None
        self.number = 1
        
    def __str__(self)->str:
        acc=''
        for elem in self.event_list:
            acc+=str(elem)
        return acc
        
    def add_event(self,event:Event):
        """
        

        Parameters
        ----------
        event : Event
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.event_list.append(event)
        
    def update(self):
        new = []
        for event in self.event_list:
            if not event.before:
                new.append(event)
            else:
                flag = True
                for prec in event.before:
                    if prec not in new:
                        flag=False
                if flag:
                    new.append(event)
        for idx, elem in enumerate(new):
            elem.number = idx
        self.start=new[0]
        self.finish=new[-1]
        self.event_list=new
               

    def add_Activity(self,activity,precedessor,successor):
        activity.precedessor=precedessor
        activity.successor=successor
        precedessor.activ.append(activity)
        successor.prec_actv.append(activity)
        self.activity_list.append(activity)
        

    def forward(self):
        self.start.early_time = 0
        for elem in self.start.activ:
            self.forward_heart(elem.successor,self.start.early_time+elem.time)

            
    def forward_heart(self,node,early_start_):
        node.early_time = max(node.early_time,early_start_)
        for elem in node.activ:
            self.forward_heart(elem.successor,node.early_time+elem.time)

    def backward(self):
        self.finish.late_time = self.finish.early_time
        for elem in self.finish.prec_actv:
            self.backward_heart(elem.precedessor,self.finish.late_time-elem.time)
            
            
    def backward_heart(self, node, late_time_):
        node.late_time = min(node.late_time, late_time_)
        for elem in node.prec_actv:
            self.backward_heart(elem.precedessor,node.late_time-elem.time)
            

    def find_critical_path(self):
        for elem in self.start.activ:
            if elem.successor.late_time-self.start.early_time-elem.time == 0:
                return self.find_critical_path_heart(elem.successor,[self.start,elem.successor])

    
    def find_critical_path_heart(self,node,path):
        for elem in node.activ:
            if elem.successor.late_time-node.early_time-elem.time == 0:
                path.append(elem.successor)
                return self.find_critical_path_heart(elem.successor,path)
        return path

    def finish_time(self)->Union[int,float]:
        return self.finish.early_time

    def gantt_chart(self):
        A=10*(len(self.activity_list))
        fig, gnt = plt.subplots()
        gnt.set_ylim(0, A+10)
        gnt.set_xlim(self.start.early_time, self.finish.late_time)
        gnt.set_xlabel('time')
        gnt.set_ylabel('Activity')
        gnt.grid(True)
        for idx,elem in enumerate(self.activity_list):
            if elem.successor.late_time-elem.precedessor.early_time-elem.time == 0:
                gnt.broken_barh([(elem.precedessor.early_time, elem.precedessor.early_time+elem.time)], (A-10*(idx+1), 9), facecolors =('tab:red'))
            else:
                gnt.broken_barh([(elem.precedessor.early_time+elem.time, elem.successor.late_time)], (A-10*(idx+1), 9), facecolors =('tab:orange'))
                gnt.broken_barh([(elem.precedessor.early_time, elem.precedessor.early_time+elem.time)], (A-10*(idx+1), 9), facecolors =('tab:blue'))
        gnt.set_yticklabels([str(elem) for elem in self.activity_list])
        gnt.set_yticks([A-5-i for i in range(0,A,10)])
        gnt.set_title('Gantt chart')


Project = CPM()
A=Event('A',[])
B=Event('B',[A])
C=Event('C',[A])
D=Event('D',[A])
E=Event('E',[B,C,D])
F=Event('F',[B,C,D])
G=Event('G',[B,C,D])
H=Event('H',[E])
I=Event('I',[E,F,G])
J=Event('J',[G])
K=Event('K',[H,I,J])


Project.add_event(A)
Project.add_event(B)
Project.add_event(C)
Project.add_event(D)
Project.add_event(E)
Project.add_event(F)
Project.add_event(G)
Project.add_event(H)
Project.add_event(I)
Project.add_event(J)
Project.add_event(K)


Project.update()


Project.add_Activity(Activity(0),A,B)
Project.add_Activity(Activity(2),A,C)
Project.add_Activity(Activity(1),A,D)
Project.add_Activity(Activity(5),B,E)
Project.add_Activity(Activity(7),B,F)
Project.add_Activity(Activity(8),B,G)
Project.add_Activity(Activity(6),C,E)
Project.add_Activity(Activity(5),C,F)
Project.add_Activity(Activity(2),C,G)
Project.add_Activity(Activity(1),D,E)
Project.add_Activity(Activity(5),D,F)
Project.add_Activity(Activity(6),D,G)
Project.add_Activity(Activity(2),E,H)
Project.add_Activity(Activity(9),E,I)
Project.add_Activity(Activity(1),F,I)
Project.add_Activity(Activity(6),G,I)
Project.add_Activity(Activity(4),G,J)
Project.add_Activity(Activity(7),H,K)
Project.add_Activity(Activity(0),I,K)
Project.add_Activity(Activity(3),J,K)


Project.forward()

Project.backward()

for elem in Project.find_critical_path():
    print(elem)

Project.gantt_chart()