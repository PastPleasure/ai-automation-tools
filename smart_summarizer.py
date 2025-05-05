import argparse
import os
from dotenv import load_dotenv
import openai
from openai import OpenAI




def main():
    load_dotenv() # Write the path to your env file here
    client = OpenAI()
    parser = argparse.ArgumentParser(description="Summarize a text file")
    parser.add_argument('--input_file', type=str, required=True, help='Path to the input text file')
    args = parser.parse_args()
    print(f"File path reveived: {args.input_file}")
    with open(args.input_file, 'r', encoding='utf-8') as file:
        text = file.read()
    print("\n--- File Content Start ---")
    print(text)
    print("--- File Content End ---\n")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize this text in 5 clear bullet points:\n\n" + text}
        ],
        temperature=0.5,
        max_tokens=500
    )

    summary = response.choices[0].message.content

    output_file = "summary_output.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
    print(f"\n Summary saved to {output_file}")
    print("Summary preview:\n")
    print(summary)


if __name__ == "__main__":
    main()

