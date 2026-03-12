import os
import json
import requests
import time
from openai import OpenAI

OPENAI_API_KEY = "your-openai-api-key-here" # Replace with your actual API key
client = OpenAI(api_key=OPENAI_API_KEY)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# API base URLs
COINGECKO_BASE = "https://api.coingecko.com/api/v3"
CURRENCY_BASE = "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies"


# Crypto and currency functions 

# Function to get current price of a cryptocurrency in USD, EUR, GBP
def get_crypto_price(coin):
    coin = coin.lower().strip()
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd,eur,gbp&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find price for '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    info = data[coin]
    return (
        f"{coin.title()} Price:\n"
        f"- USD: ${info['usd']:,.2f}\n"
        f"- EUR: €{info['eur']:,.2f}\n"
        f"- GBP: £{info['gbp']:,.2f}\n"
    )


# Function to get top 10 cryptocurrencies 
def get_top_cryptos():
    url = f"{COINGECKO_BASE}/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=10&page=1"
    response = requests.get(url)
    data = response.json()
    
    if not data:
        return "Couldn't fetch top cryptocurrencies."
    
    results = []
    for i, coin in enumerate(data, 1):
        change = coin.get('price_change_percentage_24h', 0) or 0
        results.append(f"{i}. {coin['name']} ({coin['symbol'].upper()}): ${coin['current_price']:,.2f} ({change:+.2f}%)")
    
    return "Top 10 Cryptocurrencies:\n" + "\n".join(results)


# Function to get trending cryptocurrencies
def get_trending_cryptos():
    url = f"{COINGECKO_BASE}/search/trending"
    response = requests.get(url)
    data = response.json()
    
    if not data or "coins" not in data:
        return "Couldn't fetch trending cryptocurrencies."
    
    results = []
    for item in data["coins"][:7]:
        coin = item["item"]
        results.append(f"- {coin['name']} ({coin['symbol']})")
    
    return "Trending Cryptocurrencies:\n" + "\n".join(results)


# Function to convert currency from one currency to another
def convert_currency(amount, from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.lower().strip()
    
    url = f"{CURRENCY_BASE}/{from_curr}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    data = response.json()
    rates = data.get(from_curr, {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    rate = rates[to_curr]
    converted = amount * rate
    
    return (
        f"Currency Conversion:\n"
        f"- {amount:,.2f} {from_currency.upper()} = {converted:,.2f} {to_currency.upper()}\n"
        f"- Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"
    )


# Function to get exchange rate between two currencies
def get_exchange_rate(from_currency, to_currency):
    from_curr = from_currency.lower().strip()
    to_curr = to_currency.lower().strip()
    
    url = f"{CURRENCY_BASE}/{from_curr}.json"
    response = requests.get(url)
    
    if response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    data = response.json()
    rates = data.get(from_curr, {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    rate = rates[to_curr]
    return f"Exchange Rate: 1 {from_currency.upper()} = {rate:.4f} {to_currency.upper()}"


# Function to convert cryptocurrency to currency
def crypto_to_fiat(crypto_amount, coin, to_currency):
    coin = coin.lower().strip()
    to_curr = to_currency.lower().strip()
    
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find crypto '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    crypto_price_usd = data[coin]["usd"]
    usd_value = crypto_amount * crypto_price_usd
    
    if to_curr == "usd":
        return (
            f"Conversion: {crypto_amount} {coin.upper()} to USD\n"
            f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
            f"- Value: ${usd_value:,.2f} USD"
        )
    
    rate_url = f"{CURRENCY_BASE}/usd.json"
    rate_response = requests.get(rate_url)
    
    if rate_response.status_code != 200:
        return "Couldn't fetch exchange rates."
    
    rate_data = rate_response.json()
    rates = rate_data.get("usd", {})
    
    if to_curr not in rates:
        return f"Couldn't find currency '{to_currency.upper()}'."
    
    usd_to_fiat_rate = rates[to_curr]
    fiat_value = usd_value * usd_to_fiat_rate
    
    return (
        f"Conversion: {crypto_amount} {coin.upper()} to {to_currency.upper()}\n"
        f"- {coin.upper()} price: ${crypto_price_usd:,.2f} USD\n"
        f"- Value in {to_currency.upper()}: {fiat_value:,.2f}"
    )


# Function to convert currency to cryptocurrency
def fiat_to_crypto(fiat_amount, from_currency, coin):
    coin = coin.lower().strip()
    from_curr = from_currency.lower().strip()
    
    url = f"{COINGECKO_BASE}/simple/price?ids={coin}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    
    if not data or coin not in data:
        return f"Couldn't find crypto '{coin}'. Try bitcoin, ethereum, solana, etc."
    
    crypto_price_usd = data[coin]["usd"]
    
    if from_curr == "usd":
        crypto_amount = fiat_amount / crypto_price_usd
        return (
            f"Conversion: ${fiat_amount:,.2f} USD to {coin.upper()}\n"
            f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
            f"- You get: {crypto_amount:.6f} {coin.upper()}"
        )
    
    rate_url = f"{CURRENCY_BASE}/{from_curr}.json"
    rate_response = requests.get(rate_url)
    
    if rate_response.status_code != 200:
        return f"Couldn't find currency '{from_currency.upper()}'."
    
    rate_data = rate_response.json()
    rates = rate_data.get(from_curr, {})
    
    if "usd" not in rates:
        return "Couldn't convert to USD."
    
    fiat_to_usd_rate = rates["usd"]
    usd_value = fiat_amount * fiat_to_usd_rate
    crypto_amount = usd_value / crypto_price_usd
    
    return (
        f"Conversion: {fiat_amount:,.2f} {from_currency.upper()} to {coin.upper()}\n"
        f"- {from_currency.upper()} in USD: ${usd_value:,.2f}\n"
        f"- {coin.upper()} price: ${crypto_price_usd:,.2f}\n"
        f"- You get: {crypto_amount:.6f} {coin.upper()}"
    )

# Map function names to functions
available_functions = {
    "get_crypto_price": get_crypto_price,
    "get_top_cryptos": get_top_cryptos,
    "get_trending_cryptos": get_trending_cryptos,
    "convert_currency": convert_currency,
    "get_exchange_rate": get_exchange_rate,
    "crypto_to_fiat": crypto_to_fiat,
    "fiat_to_crypto": fiat_to_crypto
}


# Tool definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_crypto_price",
            "description": "Get current price of a cryptocurrency in USD, EUR, GBP. Use when user asks about crypto prices.",
            "parameters": {
                "type": "object",
                "properties": {
                    "coin": {"type": "string", "description": "Cryptocurrency name like bitcoin, ethereum, solana"}
                },
                "required": ["coin"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_cryptos",
            "description": "Get top 10 cryptocurrencies by market cap. Use when user asks about top or biggest cryptos.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_trending_cryptos",
            "description": "Get trending cryptocurrencies right now. Use when user asks what's hot or trending.",
            "parameters": {"type": "object", "properties": {}}
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert fiat currency to another fiat currency. Use for USD to EUR, NGN to GBP, etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number", "description": "Amount to convert"},
                    "from_currency": {"type": "string", "description": "Source currency code like USD, EUR, NGN"},
                    "to_currency": {"type": "string", "description": "Target currency code like USD, EUR, NGN"}
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "Get exchange rate between two fiat currencies. Use when user just wants the rate.",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string", "description": "Source currency code"},
                    "to_currency": {"type": "string", "description": "Target currency code"}
                },
                "required": ["from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "crypto_to_fiat",
            "description": "Convert cryptocurrency to any fiat currency. Use when user wants to convert BTC/ETH/etc to NGN/USD/EUR/etc.",
            "parameters": {
                "type": "object",
                "properties": {
                    "crypto_amount": {"type": "number", "description": "Amount of cryptocurrency"},
                    "coin": {"type": "string", "description": "Cryptocurrency name like bitcoin, ethereum, solana"},
                    "to_currency": {"type": "string", "description": "Target fiat currency code like NGN, USD, EUR"}
                },
                "required": ["crypto_amount", "coin", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "fiat_to_crypto",
            "description": "Convert fiat currency to cryptocurrency. Use when user wants to know how much BTC/ETH they can get for their NGN/USD/EUR.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fiat_amount": {"type": "number", "description": "Amount of fiat currency"},
                    "from_currency": {"type": "string", "description": "Source fiat currency code like NGN, USD, EUR"},
                    "coin": {"type": "string", "description": "Target cryptocurrency like bitcoin, ethereum, solana"}
                },
                "required": ["fiat_amount", "from_currency", "coin"]
            }
        }
    }
]



# Evaluation Logic

def run_chatbot_query(query):
    """Send query to LLM, execute the function, return results."""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful financial assistant. Use the available tools to help users with crypto prices and currency conversions."},
            {"role": "user", "content": query}
        ],
        tools=tools,
        tool_choice="auto",
        temperature=0
    )
    
    reply = response.choices[0].message
    
    if not reply.tool_calls:
        return {
            "function_called": None,
            "arguments": {},
            "api_response": "No function was called"
        }
    
    tool_call = reply.tool_calls[0]
    func_name = tool_call.function.name
    func_args = json.loads(tool_call.function.arguments)
    
    # Call the actual function
    if func_name in available_functions:
        func = available_functions[func_name]
        if func_args:
            api_result = func(**func_args)
        else:
            api_result = func()
    else:
        api_result = f"Unknown function: {func_name}"
    
    return {
        "function_called": func_name,
        "arguments": func_args,
        "api_response": api_result
    }


def load_test_cases():
    filepath = os.path.join(SCRIPT_DIR, "test_cases.json")
    with open(filepath, "r") as f:
        return json.load(f)



if __name__ == "__main__":
    test_cases = load_test_cases()
    results = []
    passed = 0
    
    print("\nCRYPTO CHATBOT - EVALUATION REPORT")
    
    for i, test in enumerate(test_cases, 1):
        query = test["query"]
        expected = test["expected_function"]
        
        print(f"\n Test {i}/{len(test_cases)} ")
        print(f"Query: \"{query}\"")

        
        try:
            result = run_chatbot_query(query)
            actual = result["function_called"]
            
            print(f"API Response:")
            print(result["api_response"])
            
            print(f"\nExpected Function: {expected}")
            print(f"Actual Function:   {actual}")

            
            if actual == expected:
                print(f"\nResult: PASS")
                passed += 1
                status = "PASS"
            else:
                print(f"\nResult: FAIL (wrong function)")
                status = "FAIL"
            
            results.append({
                "query": query,
                "expected": expected,
                "actual": actual,
                "arguments": result["arguments"],
                "api_response": result["api_response"],
                "status": status
            })
            
        except Exception as e:
            print(f"Result: ERROR - {e}")
            results.append({
                "query": query,
                "expected": expected,
                "actual": "ERROR",
                "error": str(e),
                "status": "ERROR"
            })
            
        time.sleep(2)
    
    # Summary
    total = len(test_cases)
    accuracy = (passed / total) * 100
    
    print("\nSUMMARY")
    print(f"Total Tests:  {total}")
    print(f"Passed:       {passed}")
    print(f"Failed:       {total - passed}")
    print(f"Accuracy:     {accuracy:.1f}%")

    
    # Save results
    report = {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "accuracy": accuracy,
        "results": results
    }
    
    results_path = os.path.join(SCRIPT_DIR, "test_results.json")
    with open(results_path, "w") as f:
        json.dump(report, f, indent=2)
    
    print(f"\nDetailed results saved to test_results.json")