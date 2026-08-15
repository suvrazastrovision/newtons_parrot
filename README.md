# Newton's Parrot

Newton's Parrot is a Flask-powered AI voice assistant. It uses Google Gemini to answer questions and Gemini text-to-speech to read the answers aloud in a natural voice.

## Requirements

- Python 3.10 or newer
- A Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey)

## Run locally

1. Clone the repository and enter the project folder:

   ```bash
   git clone https://github.com/suvrazastrovision/newtons_parrot.git
   cd newtons_parrot
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment.

   Windows PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   Git Bash, macOS, or Linux:

   ```bash
   source .venv/Scripts/activate  # Git Bash on Windows
   # source .venv/bin/activate    # macOS or Linux
   ```

4. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root, beside `app.py`:

   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

6. Start the application:

   ```bash
   python app.py
   ```

7. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

## Security

Never commit or share your `.env` file or Gemini API key. The included `.gitignore` prevents `.env` from being added to Git. If a key is exposed, revoke it in Google AI Studio and create a new one.

When deploying the app publicly, store `GEMINI_API_KEY` as a secret environment variable on the hosting platform. Public visitors can consume your Gemini quota through the deployed app, so request limits are recommended.
