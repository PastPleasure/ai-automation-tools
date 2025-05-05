import argparse
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI

def main():
    parser = argparse.ArgumentParser(description="Generate a polite reply to a customer email")
    parser.add_argument('--input_file', type=str, required=True, help='Path to the customer email .txt file')
    args = parser.parse_args()

    print(f"Email file received: {args.input_file}")

    with open(args.input_file, 'r', encoding='utf-8') as file:
        email_text = file.read()

    print("\n--- Email Content Start ---\n")
    print(email_text)
    print("--- Email Content End ---\n")

    load_dotenv() # Write the path to your env file here
    client = OpenAI() 
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a polite and professional email assistant."},
            {"role": "user", "content": "Draft a professional but friendly reply to this customer email:\n\n" + email_text}  
        ],
        temperature=0.5,
        max_tokens=500
    )
    reply = response.choices[0].message.content

    output_file = "email_reply.txt"
    with open(output_file, "w", encoding='utf-8') as f:
        f.write(reply)
    print(f"\n--- Generated Reply Start ---\n")
    print(reply)
    print("--- Generated Reply End ---\n")
    print(f"\nReply saved to {output_file}")



if __name__ == "__main__":
    main()
