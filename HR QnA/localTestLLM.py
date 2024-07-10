import requests

def call_llama2(prompt):
    # Replace PORT_NUMBER with the actual port number llama2 is running on
    url = "http://13.202.32.27:11434/api/generate"
    payload = {
        "model": "llama3:8b",
        # "prompt": prompt
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx errors

        # Try to parse the response as JSON
        try:
            result = response.json()
            if "error" in result:
                print(f"Error from llama2: {result['error']}")
                return None
            answer = result.get("answer", "No answer found")
            return answer
        except ValueError as e:
            print(f"Error parsing response JSON: {e}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error calling llama2: {e}")
        return None


# Example usage:
prompt = "hi"
answer = call_llama2(prompt)
if answer:
    print(f"Answer: {answer}")
