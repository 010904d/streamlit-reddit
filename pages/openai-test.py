from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key="sk-proj-CRnT8LdeVM8MOutwHiEFT3BlbkFJ8iP4beKjvRpsYQNO7Lm8")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "explain global warming ."}
  ]
)

print(completion.choices[0].message['content'])



