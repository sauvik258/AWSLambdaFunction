#aws lambda code for OrderPizza chatbot
import json
import datetime
import time

def validate(slots):

    valid_pizzatype = ['veg','non veg']
    valid_pizzasize = ['regular','medium','large']
    valid_pizzacrust = ['thin','cheese burst','thick']
    
    if not slots['Name']:
        return {
        'isValid': False,
        'violatedSlot': 'Name'
        }   
        
    if not slots['PizzaType']:
        return {
        'isValid': False,
        'violatedSlot': 'PizzaType'
        } 
        
    if slots['PizzaType']['value']['originalValue'].lower() not in  valid_pizzatype:
        
        return {
        'isValid': False,
        'violatedSlot': 'PizzaType',
        'message': 'We currently serve only {} pizza.'.format(", ".join(valid_pizzatype))
        }
        
    if not slots['PizzaSize']:
        
        return {
        'isValid': False,
        'violatedSlot': 'PizzaSize',
    }
    
    if slots['PizzaSize']['value']['originalValue'].lower() not in  valid_pizzasize:
        
        return {
        'isValid': False,
        'violatedSlot': 'PizzaSize',
        'message': 'We currently serve only {} sized pizza'.format(", ".join(valid_pizzasize))
        }
        
    if not slots['PizzaCrust']:
        return {
        'isValid': False,
        'violatedSlot': 'PizzaCrust'
    }
    
    if slots['PizzaCrust']['value']['originalValue'].lower() not in  valid_pizzacrust:
        
        return {
        'isValid': False,
        'violatedSlot': 'PizzaCrust',
        'message': 'We currently serve only {} crust pizza'.format(", ".join(valid_pizzacrust))
        }
        
    if not slots['PizzaSides']:
        return {
        'isValid': False,
        'violatedSlot': 'PizzaSides'
    }
    
    if not slots['DeliveryTime']:
        return {
        'isValid': False,
        'violatedSlot': 'DeliveryTime'
    }

    return {'isValid': True}
    
def lambda_handler(event, context):
    
    # print(event)
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    print(event['invocationSource'])
    print(slots)
    print(intent)
    validation_result = validate(event['sessionState']['intent']['slots'])
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                }
               } 
    
            return response
           
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
            return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        # Add order in Database
        
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "Thanks, I have placed your order for pizza"
            }
        ]
    }
            
        return response