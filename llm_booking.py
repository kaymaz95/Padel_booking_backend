from openai import OpenAI

client = OpenAI()

response = client.responses.create(
    model="gpt-4.1-mini",
    input="jade wants court 3 at 19:00 for 45 minutes. Summarise this request.",
    max_output_tokens=150,
)

print(response.output_text)