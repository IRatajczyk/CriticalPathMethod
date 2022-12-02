"""
Created on %(21.04)s

@author: %(Igor Ratajczyk)s
"""
from math import inf
from time import time
import matplotlib.pyplot as plt
from typing import List, Union, Optional

time_t = Union[int,float]

class Event:
    def __init__(
        self,   
        name: str,
        before_list: Optional[List] = None,
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
        self.number: int = -1
        self.early_time: time_t = 0
        self.late_time: time_t = inf
        self.before = before_list if before_list is not None else []
        self.activities: List = []
        self.predecessor_actvities: List = []

    def __str__(self) -> str:
        return self.name

           
class Activity:
    def __init__(
        self, 
        time: time_t = 0,
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
        self.predecessor: Event = None
        self.successor: Event = None
        self.time: time_t = time

    def __str__(self) -> str:
        return "("+str(self.predecessor)+":"+str(self.successor)+")"
    

class CriticalPathMethod:
    def __init__(self):
        self.activity_list: List[Activity] = []

        self.event_list: List[Event] = []
        self.root_event: Event = Event()
        self.final_event: Event = Event()

        self.number: int = -1
        
    def __str__(self) -> str:
        return ''.join(str(event) for event in self.event_list)
        
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
        self.root_event = ordered_events[0]
        self.final_event = ordered_events[-1]
        self.event_list = ordered_events
               

    def add_activity(
            self,        
            activity: Activity,
            predecessor: Event,
            successor: Event,
            ):
        """
        Add activity to a project, predecessor and successor of an activity are necessary to be specified.

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
        activity.predecessor = predecessor
        activity.successor = successor
        predecessor.activities.append(activity)
        successor.predecessor_actvities.append(activity)
        self.activity_list.append(activity)
        
    def proceed(self) -> None:
        """
        Update early and late time of every event, clue method of CPM algorithm.

        Returns
        -------
        None.

        """
        self._forward()
        self._backward()
        

    def _forward(self) -> None:
        self.root_event.early_time = 0
        for activity in self.root_event.activities:
            self._forward_heart(activity.successor, self.root_event.early_time + activity.time)
            
    def _forward_heart(self, node: Event, early_start: time_t) -> None:
        node.early_time = max(node.early_time, early_start)
        for activity in node.activities:
            self._forward_heart(activity.successor, node.early_time + activity.time)

    def _backward(self) -> None:
        self.final_event.late_time = self.final_event.early_time
        for activity in self.final_event.predecessor_actvities:
            self._backward_heart(activity.precedessor, self.final_event.late_time - activity.time)
            
    def _backward_heart(self, node: Event, late_time: time_t):
        node.late_time = min(node.late_time, late_time)
        for activity in node.predecessor_actvities:
            self._backward_heart(activity.precedessor, node.late_time - activity.time)
            

    def find_critical_path(self) -> List[Event, Activity]:
        """
        Find a critical path; series of Events that must be fishised with no delay when fastest possible finish of Project is concerned.

        Returns
        -------
        List[Event, Activity]
            Critical Path.

        """
        for activity in self.root_event.activities:
            if activity.successor.late_time - self.root_event.early_time - activity.time == 0:
                return self._find_critical_path_heart(activity.successor, [self.root_event, activity.successor])

    
    def _find_critical_path_heart(self, event: Event, path: List[Event, Activity]) -> List[Event, Activity]:
        for activity in event.activities:
            if activity.successor.late_time - event.early_time - event.time == 0:
                path.append(activity.successor)
                return self._find_critical_path_heart(activity.successor, path)
        return path

    def finish_time(self) -> time_t:
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

