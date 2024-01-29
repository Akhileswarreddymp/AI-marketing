import openai

# Replace 'YOUR_API_KEY' with your actual OpenAI GPT API key
openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):
    # Create a list of messages in the conversation format expected by the Chat API
    messages = [{"role": "user", "content": input_text}]

    # Call the OpenAI Chat API to generate a response
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # You can adjust this parameter as needed
    )

    # Print or return the generated response
    generated_text = response.choices[0].message["content"]
    print(generated_text)
    return generated_text

# Example usage
prompt = "give me code for adding 2 numbers"
input_text = "Hello, how are you?"
get_completion(prompt)
