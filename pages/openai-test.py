from openai import OpenAI

# Initialize the client with your API key
client = OpenAI(api_key="***")

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "explain global warming ."}
  ]
)

print(completion.choices[0].message['content'])



