# LLM Evaluation 

This is a **Unit Test** evaluation for a crypto-currency chatbot. Unit tests are the first level of LLM evaluation - they're fast, low-cost tests that verify the model is calling the correct functions for different types of queries.

## Requirements

Install the dependencies:

```
pip install openai requests 
```

You will also need an OpenAI API key. Get one at https://platform.openai.com/api-keys


## How to Run

1. Open `evaluation.py` and replace the placeholder with your OpenAI API key:

```python
OPENAI_API_KEY = "your-openai-api-key-here"
```

2. Run the script:

```
python evaluation.py
```

## How It Works

The evaluation script sends test queries to the LLM and checks which function it decides to call. The LLM never sees the expected answer, it only receives the query and must choose the appropriate tool on its own.

1. Test cases are loaded from `test_cases.json`.
2. Each query is sent to GPT-4o-mini with the same tools available in the chatbot.
3. The script captures which function the model called.
4. It then executes the actual API call to verify the function works.
5. Results are compared against expected functions and logged.


The script outputs a report `test_results.json` showing each test's query, expected vs actual function, the arguments passed, and the live API response. A summary at the end shows overall accuracy.

## APIs Used

Both APIs are free and require no API key.

- **CoinGecko API** (Cryptocurrency data)

  Full docs: https://www.coingecko.com/en/api/documentation

- **Currency Exchange API** (Fiat currency data)

  Supports 150+ currencies including USD, EUR, GBP, NGN, JPY, CNY.

  Source: https://github.com/fawazahmed0/exchange-api
