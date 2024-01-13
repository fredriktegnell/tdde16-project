import pandas as pd
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

PREDICTIONS_PATH = 'data/predictions.csv'
MERGED_PATH = 'data/merged_data.csv'

# Load the tokenizers and models
qa_tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
qa_model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")
sentiment_model_path = f"cardiffnlp/twitter-roberta-base-sentiment-latest"

data = pd.read_csv(MERGED_PATH)

# Pipelines
qa_pipeline = pipeline("question-answering", model=qa_model, tokenizer=qa_tokenizer)
sentiment_pipeline = pipeline("sentiment-analysis", model=sentiment_model_path, tokenizer=sentiment_model_path)

predictions = []

counter = 0
for index, row in data.iterrows():
    context = row['Article']

    # Home team
    question_home = f"What do you think about {row['Home_Team']}?"
    answer_home = qa_pipeline({'context': context, 'question': question_home})
    result_home = sentiment_pipeline(answer_home['answer'])[0]['label']

    # Away team
    question_away = f"What do you think about {row['Away_Team']}?"
    answer_away = qa_pipeline({'context': context, 'question': question_away})
    result_away = sentiment_pipeline(answer_away['answer'])[0]['label']

    # Determine the prediction based on sentiment
    if (result_home == "positive" and result_away in ["negative", "neutral"]) or (result_home == "neutral" and result_away == "negative"):
        prediction = "Home Win"
    elif (result_away == "positive" and result_home in ["negative", "neutral"]) or (result_away == "neutral" and result_home == "negative"):
        prediction = "Away Win"
    else:
        prediction = "Draw"

    predictions.append({
        "Home_Team": row['Home_Team'],
        "Away_Team": row['Away_Team'],
        "Prediction": prediction
    })

predictions_df = pd.DataFrame(predictions)
predictions_df.to_csv(PREDICTIONS_PATH, index=False)
