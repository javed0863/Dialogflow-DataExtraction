import os
import json
import csv

GDF_BOT = 'SomeBot'
INTENTS_RESPONSE_FILE = GDF_BOT + '_Intents&Responses.csv'
TRAINING_PHRASES_FILE = GDF_BOT + '_Training&Phrases.csv'
INTENT_DIR = 'C:/Users/javedameen/Downloads/GDF/'+GDF_BOT+'/intents/'
entries = os.listdir(INTENT_DIR)

with open(INTENTS_RESPONSE_FILE, 'w', encoding="utf-8", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Intent Name", "Response", "Input Contexts", "Output Contexts", "Events"])

    for entry in entries:
        f = open(INTENT_DIR + entry, encoding="utf8")
        # print('> ', f)
        json_data = json.load(f)
        # print(entry, '-->', type(json_data),'--> ', json.dumps(json_data, indent = 4, sort_keys=True))
        # print(type(json_data))
        # print(json_data)
        if type(json_data) == dict:
            intent_name = json_data['name']
            input_contexts = ', '.join(json_data['contexts'])
            events = ', '.join([event['name'] for event in json_data['events']])
            if 'responses' in json_data:
                intent_response_messages = json_data['responses'][0]['messages']
                output_contexts = ", ".join([str(ac['name'])+'-'+str(ac['lifespan']) for ac in json_data['responses'][0]['affectedContexts']])
                for msg in intent_response_messages:
                    # print(intent_name, '-->', msg)
                    if 'speech' in msg:
                        writer.writerow([intent_name, msg['speech'][0], input_contexts, output_contexts, events])
                    elif 'payload' in msg:
                        payload = msg['payload']
                        # if 'menuOptions' in payload:
                        #     writer.writerow([intent_name, payload['menuOptions']])
                        writer.writerow([intent_name, payload, input_contexts, output_contexts, events])
                    else:
                        writer.writerow([intent_name, '', input_contexts, output_contexts, events])
                        # print(intent_name,'->',msg['speech'][0])

with open(TRAINING_PHRASES_FILE, 'w', newline='') as file:
    usersay_writer = csv.writer(file)
    usersay_writer.writerow(["Intent Name", "Training Phrases"])

    for entry in entries:
        f = open(INTENT_DIR + entry, encoding="utf8")
        json_data = json.load(f)
        # print('Training: ', type(json_data))
        if type(json_data) == list:
            usersay_intent = entry.replace('_usersays_en.json','')
            multiline_phrases = ''
            for usersay in json_data:
                usersay_data = usersay['data']
                # print(usersay_data)
                tr_phrases = (''.join([words['text'] for words in usersay_data])).strip()
                usersay_writer.writerow([usersay_intent, tr_phrases])
                # multiline_phrases = multiline_phrases + tr_phrases + '\n'
            # print(multiline_phrases)
            # usersay_writer.writerow([usersay_intent, multiline_phrases])