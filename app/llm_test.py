from openai import OpenAI

client = OpenAI()

response = client.responses.create(
        model = "",
        input = "Explain what kafka is in two sentences"
  )

print(responses.output_text)