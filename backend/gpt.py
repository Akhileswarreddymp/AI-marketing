import openai

openai.api_key = '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'

def get_completion(prompt, model="gpt-3.5-turbo"):

    messages = [{"role": "user", "content": input_text}]


    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, 
    )


    generated_text = response.choices[0].message["content"]
    print(generated_text)
    return generated_text


prompt = "give me code for adding 2 numbers"
input_text = "Hello, how are you?"

