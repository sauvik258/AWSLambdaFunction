#aws lambda code for CarvedRockFitness chatbot
import json

def validate(slots):

    if not slots['email']:
        return {
        'isValid': False,
        'violatedSlot': 'email'
        }   
        
    if not slots['ProductType']:
        return {
        'isValid': False,
        'violatedSlot': 'ProductType'
        } 

    return {'isValid': True}
    
def lambda_handler(event, context):
    
    print(event)
    slots = event['currentIntent']['slots']
    intent = event['currentIntent']['name']
    sentiment = event['sentimentResponse']['sentimentLabel']
    print(event['invocationSource'])
    print(slots)
    print(sentiment)
    validation_result = validate(slots)
    
    if sentiment == 'NEGATIVE':
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Sorry for the trouble. Let me transfer you to one of our specialists"
                }
            }
        }
        return response
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            response = {
                "dialogAction": {
                    "type": "ElicitSlot",
                    "intentName": intent,   
                    "slots": slots,
                    "slotToElicit":validation_result['violatedSlot']
                    }
            }
        else:
            response = {
                "dialogAction": {
                    "type": "Delegate", 
                    "slots": slots
                    }
            }
        return response        

    if event['invocationSource'] == 'FulfillmentCodeHook':
        response = {
            "dialogAction": {
                "type": "Close",
                "fulfillmentState": "Fulfilled",
                "message": {
                    "contentType": "PlainText",
                    "content": "Congrats, You have a new promotion coupon. Please check email for details"
                }
            }
        }
        return response