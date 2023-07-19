import os
import openai

# Load your API key from an environment variable or secret management service
openai.api_key = "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"


# The business jargon translation example, but with example names for the example messages
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "HI!"},
    ],
    temperature=0,
)


print(response)

#6051246626:AAGIe-mec1-uanl0MqFLDJdSBJSRuRlN_0w"