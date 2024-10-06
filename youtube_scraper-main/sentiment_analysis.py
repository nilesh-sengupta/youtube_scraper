import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

class SentimentAnalysis:
    def __init__(self, comments):
        self.comments = comments
        self.tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def find_sentiment(self):
        scores = []
        subjectivity = []
        objectivity = []

        for comment in self.comments:
            inputs = self.tokenizer.encode_plus(
                comment,
                add_special_tokens=True,
                return_tensors="pt",
                padding="max_length",
                truncation=True,
                max_length=512,
            )

            inputs.to(self.device)
            outputs = self.model(**inputs)
            logits = outputs.logits
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            sentiment = torch.argmax(probabilities).item()
            sentiment_label = "Positive" if sentiment == 1 else "Negative"

            neutral_probability = probabilities[0, 0].item()
            subjectivity_value = 1 - neutral_probability
            objectivity_value = neutral_probability

            scores.append(sentiment_label)
            subjectivity.append(round(subjectivity_value, 2))
            objectivity.append(round(objectivity_value, 2))

        return scores, subjectivity, objectivity

    def main(self):
        return self.find_sentiment()

if __name__ == "__main__":
    obj = SentimentAnalysis(["This is a standard comment", "This is a test comment"])
    print(obj.main())
