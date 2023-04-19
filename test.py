import openai
openai.api_key = "Wait_For_Api_Key"

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
        {"role": "system", "content": "You are a helpful assistant in cybersecurity filed."},
        {"role": "user", "content": "What is cybersecurity?"},
    ]
)

response["choices"][0]["message"]

messages=[
        {"role": "system", "content": "You are a helpful assistant in cybersecurity filed."},
        {"role": "user", "content": "What is cybersecurity?"},
    ]

messages.append(response["choices"][0]["message"])

message={"role":"user","content":"What is the math behind cybersecurity expert"}

messages.append(message)

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=messages
)

def chatbot(input):
    messages=[
        {"role": "system", "content": "You are a helpful assistant in cybersecurity filed."},
        {"role": "user", "content": "What is cybersecurity?"},
    ]
    if input:
        message={"role":"user","content":input}
        messages.append(message)
        response = openai.ChatCompletion.create( model="gpt-3.5-turbo", messages=messages)
        reply = response["choices"][0]["message"]["content"]
        return reply