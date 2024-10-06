import requests
import pandas as pd
import json
import time
import re




class gpt:
    def __init__(self, comments):
        self.comments = comments

    def main(self):
        results = []
        output_file = "sentiment_results.json"

        headers = {
            'Authorization': "Bearer pk-EMGOyzlqnEgyIlFwvrgAcNsXYDXNovLuCGWdgjsuJUEZnSGB",
            'Content-Type': 'application/json',
        }

        try:
            for comment in self.comments:
                prompt = "Human: Answer in positive/ negative/ neutral : What is the sentiment of :" + comment + "?\nAI:",
                json_data = {
                    'model': 'pai-001-light-beta',
                    "max_tokens": 300,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a helpful assistant"
                        },
                        {
                            "role": "user",
                            "content": "Please categorize the sentiment of the following comment as 'positive,' 'negative,' 'neutral,' or 'mixed' in one word: " + comment
                        }
                    ],
                    "usage": {
                        "completion_tokens": 1,
                    }
                }

                response = requests.post('https://api.pawan.krd/v1/chat/completions', headers=headers, json=json_data)
                print(response)
                output = response.json()['choices'][0]['message']['content'].split()[0].strip('.,!?;:"\'()[]{}')
                result = {
                    "comment": comment,
                    "output": output
                }
                results.append(result)
                time.sleep(5)

        except:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            print("Incomplete results written to", output_file)

        else:
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=4)
            print("Results written to", output_file)
        data_sentiment = pd.read_json('sentiment_results.json')
        return data_sentiment['output']

if __name__=='__main__':
    obj = gpt(["This is a standard comment", "This is a test comment"])
    print(obj.main())