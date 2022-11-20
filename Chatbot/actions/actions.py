# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
import json
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from neo4j import GraphDatabase
################# Credentials ######################""
# Connection parameters
uri = "bolt://localhost:7687"
conn = GraphDatabase.driver(uri, auth=("neo4j", "password"), encrypted=False)

print("Connected")

class ActionWordDef(Action):

    def name(self) -> Text:
        return "action_word_definition"   # !!!! this return value must match line 55 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        prediction = tracker.latest_message['entities'][0]['value']
        
        if prediction:
            query_response = conn.runInstalledQuery("get_definition",{"word_query": prediction})
            
            r=query_response[0]
            w=r["words"]
            vals=[]
            for wd in w:
                vals.append(wd["attributes"]["definition"])
            value = "\n".join(vals)
        
        counts = len(vals)
        if counts > 0:
            dispatcher.utter_message(text="Here is the list of definitions:")
            dispatcher.utter_message(text=value)
            dispatcher.utter_message(text="========================")
        else:
            dispatcher.utter_message(text="no definition found")

        return []

class ActionHypernym(Action):

    def name(self) -> Text:
        return "action_hypernym"   # !!!! this return value must match line 55 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.latest_message)
        result_restaurant = []
    
        def test_rasa_restaurant(tx, cuisine):
            query = '''MATCH (philip:Person {name:"Philip"}),
                    (philip)-[:IS_FRIEND_OF]-(friend),
                    (restaurant:Restaurant)-[:LOCATED_IN]->(:City {name:"New York"}),
                    (restaurant)-[:SERVES]->(:Cuisine {name:$cuisine}),
                    (friend)-[:LIKES]->(restaurant)
                    RETURN restaurant.name, collect(friend.name) AS likers, count(*) AS occurence
                    ORDER BY occurence DESC'''

            for record in tx.run(query, cuisine=cuisine):
                result_restaurant.append(record['restaurant.name'])
                # print(record['restaurant.name'])

        with conn.session() as session:
            session.read_transaction(test_rasa_restaurant, "Sushi")

        dispatcher.utter_message('Recommended Restaurant is ')
        for i in result_restaurant:
            dispatcher.utter_message(i)

        return []

class ActionHyponym(Action):

    def name(self) -> Text:
        return "action_hyponym"   # !!!! this return value must match line 55 of domain.yml  [ Step 4.a ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']

        if prediction:
            query_response = conn.runInstalledQuery("get_hyponyms",{"word_query": prediction})
            r=query_response[0]
            w=r["definition"]
            vals=[]
            for wd in w:
                vals.append(wd)
            value = "\n".join(vals)
            dispatcher.utter_message(text="Here is the list of hyponyms:")
            dispatcher.utter_message(text=value)
            # dispatcher.utter_message(words[0])
            dispatcher.utter_message(text="========================")

        return []

class ActionAntonyms(Action):

    def name(self) -> Text:
        return "action_antonym"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']

        if prediction:
            query_response = conn.runInstalledQuery("get_antonyms",{"word_query": prediction})
            r=query_response[0]
            w=r["definition"]
            vals=[]
            for wd in w:
                vals.append(wd)
            value = "\n".join(vals)
            dispatcher.utter_message(text="Here is the list of antonyms:")
            dispatcher.utter_message(text=value)
            # dispatcher.utter_message(words[0])
            dispatcher.utter_message(text="========================")

        return []

class ActionAllConnections(Action):

    def name(self) -> Text:
        return "action_all_connections"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:


        print(tracker.latest_message)
        prediction = tracker.latest_message['entities'][0]['value']

        if prediction:
            query_response = conn.runInstalledQuery("get_all_connections",{"word_query": prediction})
            r=query_response[0]
            w=r["definition"]
            vals=[]
            for wd in w:
                vals.append(wd)
            value = "\n".join(vals)
            dispatcher.utter_message(text="Here is the list of related words:")
            dispatcher.utter_message(text=value)
            # dispatcher.utter_message(words[0])
            dispatcher.utter_message(text="========================")

        return []