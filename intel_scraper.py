import argparse



def main():
    parser = argparse.ArgumentParser(description="Scrape and summarize an article from the web")
    parser.add_argument('--url', type=str, required=True, help='URL of the article you want to be scraped')
    args = parser.parse_args()

    print(f"URL received: {args.url}")

    from newspaper import Article

    article = Article(args.url)
    article.download()
    article.parse()

    title = article.title
    text = article.text
    print("\n Article Title: ")
    print(title)
    print("\n--- Article Content Start ---")
    print(text[:500] + "..." if len(text) > 500 else text)
    print("--- Article Content End ---\n")

    from dotenv import load_dotenv
    from openai import OpenAI
    import os

    load_dotenv() # Write the path to your env file here
    client = OpenAI()
    prompt = f"""
    Summarize the following article in 3 sentences. 
    Then extract 5 key insights. 
    hen suggest a short, SEO friendly blog title. 
    Article Title: {title}

    Article content:
    {text}
    """
    print("Sending content to OpenAI API...")
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4,
        max_tokens=500
    )
    summary = response.choices[0].message.content
    print("\n Summary Output:\n")
    print(summary)

    from datetime import datetime
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe_title = "_".join(title.lower().split())[:50]
    output_dir = "summarized_articles"
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{safe_title}_{timestamp}.txt")
    with open(output_path, "w", encoding='utf-8') as f:
        f.write(f" URL: {args.url}\n")
        f.write(f"Title: {title}\n")
        f.write(f"Summary:\n")
        f.write(summary)

    print(f"\nSummary saved to {output_path}")



    



if __name__ == "__main__":
    main()

