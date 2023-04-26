# CS 5100 Final Project
# SAGE with GPT

import openai

# this key is for cs5100 final project demo purposes only and will be turned off after April 2023
openai.api_key = "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"

# gpt-3.5-turbo is one of GPT's latest, more reliable and cost-effective models
# tokens determine the length of the response
# temperature determines the randomness of the response
def get_gpt_response(user_input, model='gpt-3.5-turbo', tokens=150, temperature=0.5, api_key=None):

    # this message gets prepended to any requests to the API so it has some context for the response
    # without it, you are asking "vanilla" GPT to respond to a prompt with no context
    system_message = "You are a friendly AI assistant that helps users \
        with their questions and tasks, specifically regarding environmental issues, \
            lifestyle choices, and sustainability practices."

    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
        ]

    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=tokens,
        temperature=temperature,
        n=1
    )

    return response.choices[0].message['content'].strip()

def main():
    print("Welcome to SAGE: Now enhanced with GPT!")
    print("Enter your question: ")
    while True:
        user_input = input("")
        if user_input.lower() == ("quit" or "q"):
            print("Goodbye!")
            break

        gpt_response = get_gpt_response(user_input, api_key=openai.api_key)
        print("SAGE:", gpt_response, "...")
        print("<ask me to continue for more information, or ask a new question.>")
        
    

if __name__ == "__main__":
    main()