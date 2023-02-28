# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import pandas
import json

# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List

from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Text, List, Optional
from rasa_sdk.forms import FormValidationAction
from tower import *

class ActionSaySLineName(Action):

    def name(self) -> Text:
        return "action_ask_line_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        station_name = tracker.get_slot("station_name")
        if station_name:
            buttons=buttons_lines(station_name)
            #buttons=[
             #  {"payload":"Vemagiri - Simhadri 400kV D/c","title":"Vemagiri - Simhadri 400kV D/c"},
              # {"payload":"Vemagiri - Simhadri 400kV D/c","title":"Vemagiri - Simhadri 400kV S/c"}
             #]
            dispatcher.utter_message(text=f"Please select one line", buttons=buttons)
        else:
            dispatcher.utter_message(text="Station information is not available.")
        return []

class ActionSayFaultLocation(Action):

    def name(self) -> Text:
        return "action_say_fault_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        line_name =  tracker.get_slot("line_name")
        input_cat=tracker.get_slot("input_category")
        if(input_cat == "Tower_loc"):
            tower=tracker.get_slot("tower_loc")
            msg=tower_location_dat(line_name,tower)   
        else:
            fault_distance = tracker.get_slot("fault_distance")
            msg = fault_location_number(line_name,float(fault_distance))
        dispatcher.utter_message(msg)
        return[]
        # excel_data_df = pandas.read_excel('D:\\ML Course\\SR1_ML_Project\\Programs_Final\\VMG_TLM.xlsx', sheet_name='Sheet1')
        # TLM_juris = excel_data_df[excel_data_df['Name_Of_Line2']==line_name]['CUM'].max()
        
        # try:
        #     if  TLM_juris<float(fault_distance) or float(fault_distance) <0 :
        #         dispatcher.utter_message("fault is", round((fault_distance-TLM_juris),2), "Kms beyond Vemagiri TLM jurisdiction")
        # except:
        #     dispatcher.utter_message(text="Please enter distance in Km. Eg: If fault distance is 20km, enter 20")
        #     return[]

        # if fault_distance and line_name:
        #     msg= fault_location_number(line_name,float(fault_distance))
        #     #buttons=buttons_lines("Vemagiri")
        #     dispatcher.utter_message(msg)
        # else:
        #     dispatcher.utter_message(text="Details submitted are not correct")
        #return []



class ValidateBookingForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_name_form"

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        
        updated_slots = domain_slots.copy()
        if tracker.slots.get("input_category") == "Tower_loc":
            # If the user is an existing customer,
            # do not request the `email_address` slot
            updated_slots.remove("fault_distance")
        else:
            updated_slots.remove("tower_loc")
            
        return updated_slots

    def validate_tower_loc(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
        ) -> Dict[Text, Any]:
            
        #tower=tracker.get_slot("tower_loc")
        line =  tracker.get_slot("line_name")
        if line != None:
            msg=tower_valid(slot_value,line)
            if(msg == "Value Found"):
                return {"tower_loc": slot_value}
            else:
                dispatcher.utter_message(msg)
                return {"tower_loc": None}
            
    def validate_fault_distance(
            self,
            slot_value: Text,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: "DomainDict",
        ) -> Dict[Text, Any]:
            
        #tower=tracker.get_slot("tower_loc")
        line =  tracker.get_slot("line_name")
        if line != None:
            msg=distance_valid(slot_value,line)
            #msg=tower_valid(slot_value,line)
            if(msg == "VALID"):
                return {"fault_distance": slot_value}
            else:
                dispatcher.utter_message(msg)
                return {"fault_distance": None}
                

        
