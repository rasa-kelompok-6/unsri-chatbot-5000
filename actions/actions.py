# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


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
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker, FormValidationAction
from rasa_sdk.types import DomainDict

# Time
from datetime import datetime

# Database
import sqlite3


class ActionGetTime(Action):

    def name(self) -> Text:
        return "action_get_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print_time = "The time now is " + current_time
        dispatcher.utter_message(text=print_time)

        return []

class ActionReset(Action):

     def name(self) -> Text:
            return "action_reset"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         dispatcher.utter_message("Slots == reset!")

         return [AllSlotsReset()]

class ActionSetData(Action):

     def name(self) -> Text:
            return "action_set_data"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
         name = tracker.get_slot("name")
         nim = tracker.get_slot("nim")
         semester = tracker.get_slot("semester")
         ipk = tracker.get_slot("ipk")
         
        #  print(name, nim, semester, ipk)

         conn = sqlite3.connect('mahasiswa.db')
         conn.execute('''
                      CREATE TABLE IF NOT EXISTS data_mahasiswa(name text, 
                      nim text,
                      semester text, 
                      ipk text);''')
         
         conn.execute("INSERT INTO data_mahasiswa VALUES('{0}', '{1}', '{2}', '{3}');" .format(name, nim, semester, ipk))

         conn.commit()
         conn.close()
         
         dispatcher.utter_message(template="utter_data_thanks", name=name, nim=nim, semester=semester, ipk=ipk)

         return []

class ActionGetData(Action):

     def name(self) -> Text:
            return "action_get_data"

     def run(self, dispatcher: CollectingDispatcher,
             tracker: Tracker,
             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

         conn = sqlite3.connect('mahasiswa.db')
         
         name = '%'
         nim = '%'
         semester = '%'
         ipk = '%'
                 
         for e in tracker.latest_message['entities']:
            if e['entity'] == 'name':
                name = e['value']  
                if name is None:
                    name = '%'
            if e['entity'] == 'nim':
                nim = e['value']
                if nim is None:
                    nim = '%'
            if e['entity'] == 'semester':
                semester = e['value']
                if semester is None:
                    semester = '%'
            if e['entity'] == 'ipk':
                ipk = e['value']
                if ipk is None:
                    ipk = '%'

         cursor = conn.execute(''' SELECT * 
                                   FROM data_mahasiswa
                                   WHERE name LIKE '%{0}%' AND nim LIKE '%{1}%' AND semester LIKE '%{2}%' and ipk LIKE '%{3}%';'''
                                    .format(name, nim, semester, ipk))
        
         cursor = cursor.fetchall()
        #  data = ''.join(check)
         if not cursor:
            dispatcher.utter_message(text="Maaf kami tidak menemui data tersebut :(")
         else:
            i = 0
            for row in cursor:
                cursor[i] = list(row)
                i = i + 1
            l_string = ""
            for sublist in cursor:
                for item in sublist:
                    item = str(item)
                    l_string += item + " "
                l_string += "\n"
            
            print(l_string)
            dispatcher.utter_message(text=l_string)            
         
         conn.close()

         return []