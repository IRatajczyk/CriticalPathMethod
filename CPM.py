"""
Created on %(21.04)s

@author: %(Igor Ratajczyk)s
"""
from math import inf
import matplotlib.pyplot as plt

from typing import List, Union, Optional

time_t = Union[int,float]

class Event:
    def __init__(self,
                 name: str,
                 before_list: = None,
                ):
        """
        

        Parameters
        ----------
        name_ : str
            The very name of event, for the sake of clarity.
        before_list : Optional[List[Event]]
            List of events necessary to start particular event. If event need no earlier events nor activities pass [] or leave.
            
        Returns
        -------
        None.

        """
        self.name: str = name
        self.number = 0
        self.early_time: time_t = 0
        self.late_time = inf
        self.before = before_list if before_list is not None else []
        self.activ = []
        self.prec_actv = []

    def __str__(self) -> str:
        return self.name

           
class Activity:
    
    def __init__(self, 
                 time: time_t = 0
                ):
        """
        

        Parameters
        ----------
        time : Union[int,float], optional
            The default is 0. Time required to finish completely particular activity.

        Returns
        -------
        None.

        """
        self.precedessor = None
        self.successor = None
        self.time: time_t = time

    def __str__(self) -> str:
        return "("+str(self.precedessor)+":"+str(self.successor)+")"
    

class CPM:
    def __init__(self):
        self.event_list: List[Event] = []
        self.activity_list: List[Activity] = []
        self.start = None
        self.finish = None
        self.number = 1
        
    def __str__(self) -> str:
        acc=''
        for elem in self.event_list:
            acc+=str(elem)
        return acc
        
    def add_event(self,
                  event: Event
                 ) -> None:
        """
        Add event to whole project.

        Parameters
        ----------
        event : Event
            Add event as an Event object.

        Returns
        -------
        None.

        """
        self.event_list.append(event)
        
    def update(self) -> None:
        """
        Update whole project so Events can be placed in right order.

        Returns
        -------
        None.

        """
    ordered_events: List[Event] = []
    for event in self.event_list:
        if not event.before:
            ordered_events.append(event)
        elif all((predecessor not in ordered_events for predecessor in event.before)):
            ordered_events.append(event)
    for idx, elem in enumerate(ordered_events):
        elem.number = idx
    self.start = ordered_events[0]
    self.finish = ordered_events[-1]
    self.event_list = ordered_events
               

    def add_Activity(
            self,
                     
            activity:Activity,precedessor:Event,successor:Event):
        """
        Add activity to a project, precedessor and successor of an activity are necessary to be specified.

        Parameters
        ----------
        activity : Activity
            Activity object.
        precedessor : Event
            Specify precedessor of an activity; the very event that occurs right before activity.
        successor : Event
            Specify succesor of an activity; the very event that occurs right after activity.

        Returns
        -------
        None.

        """
        activity.precedessor = precedessor
        activity.successor = successor
        precedessor.activ.append(activity)
        successor.prec_actv.append(activity)
        self.activity_list.append(activity)
        
    def update_times(self):
        """
        Update early and late time of every event, clue method of CPM algorithm.

        Returns
        -------
        None.

        """
        self.forward()
        self.backward()
        

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
            

    def find_critical_path(self)->List[Event]:
        """
        Find a critical path; series of Events that must be fishised with no delay when fastest possible finish of Project is concerned.

        Returns
        -------
        List[Event]
            Critical Path.

        """
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
        """
        Calculate duration of whole project and/or finish time, starting at time 0 is assumed.

        Returns
        -------
        Union[int,float]
            Finish time

        """
        return self.finish.early_time

    def gantt_chart(self):
        """
        Plot a Gantt chart, red colour is for critical activities, blue is for earliest possible time of performing and finishing particular activity, and orange mrks time when activity is accepable to being done.

        Returns
        -------
        None.

        """
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

def Example_project(): #As far as author's experience is concerned, such exemplary codes are unspeakably convenient.
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
    
if __name__ == '__main__':
    Example_project()
