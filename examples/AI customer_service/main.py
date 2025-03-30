from openai import OpenAI

client = OpenAI(
  api_key="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"
)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  store=True,
  messages=[
    {"role": "user", "content": "write a haiku about ai"}
  ]
)

print(completion.choices[0].message);
