import argparse
import sys
import os
import subprocess
import glob
import whisper  # Make sure you've run: pip install openai-whisper
from dotenv import load_dotenv
from openai import OpenAI

def download_audio(url):
    output_dir = "yt_audio"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "%(title).50s.%(ext)s")
    command = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", output_path,
        url
    ]
    try:
        subprocess.run(command, check=True)
        print(f"✅ Audio downloaded to {output_dir}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error downloading audio: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Summarize a YouTube video or transcript a text file.")
    parser.add_argument('--url', type=str, help='URL of the YouTube video to summarize')
    parser.add_argument('--file', type=str, help='Path to the text file to summarize')
    args = parser.parse_args()

    load_dotenv() # WRITE THE PATH TO YOUR .env FILE HERE WITH dotenvpath="/path/to/.env"
    client = OpenAI()

    if not args.url and not args.file:
        print("❌ Please provide either a YouTube URL or a text file path.")
        sys.exit(1)
    
    if args.url:
        print(f"🎥 YouTube URL received: {args.url}")
        download_audio(args.url)

        # Find latest downloaded .wav file
        latest_file = sorted(glob.glob("yt_audio/*.wav"), key=os.path.getctime)[-1]

        print("🧠 Transcribing...")
        model = whisper.load_model("base")
        result = model.transcribe(latest_file)
        transcript = result["text"]
        prompt = f"""
        You're a podcast summarizer assistant.
        Summarize the following transcript in 3 short sentences:
        Then extract 5 key takeaway or quotes.
        Then suggest an SEO friendly blog title and 3 relevant hashtags.
        Transcript: {transcript}
        """
        print("✅ Transcription complete.\n")
        print("--- Transcript Preview ---\n")
        print(transcript[:1000] + "..." if len(transcript) > 1000 else transcript)
        print("Sending transcript to OpenAI for summarization...\n")
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.5
        )
        summary = response.choices[0].message.content
        print("✅ Summary received:\n")
        print(summary)

    elif args.file:
        print(f"📄 File path received: {args.file}")
    
    


if __name__ == "__main__":
    main()
