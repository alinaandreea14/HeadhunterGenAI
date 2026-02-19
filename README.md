🕵️‍♂️ GenAI Headhunter Assistant

GenAI Headhunter is a Streamlit-based intelligence tool designed for a better view of the job descriptions. It automates the task of parsing job URLs, extracting technical requirement and calculating a "Quality Score" to determine the clarity and viability of a job posting.

## ✨ Key Features

🔗 Smart URL Scraping: Uses BeautifulSoup4 to extract clean data from job boards and company career pages.

🧠 LLM Analysis: Use Groq to summarize roles and identify core responsibilities.

🛠️ Tech Stack Extraction: Automatically identifies and badges programming languages, frameworks, and infrastructure tools.

📊 Quality Scoring: A 0-100 score based on JD completeness, salary transparency, and role clarity.

🚩 Red Flag Detection: Instant alerts for red flags.

📦 Structured Data: Powered by Pydantic for strict data validation and type safety.

## 🛠️ Installation & Setup
1. Clone the Repository
```
git clone https://github.com/alinaandreea14/HeadhunterGenAI.git
cd HeadhunterGenAI
```
2. Configure Environment Variables
Create a .env file in the root directory and add your API keys:
```
GROQ_API_KEY=your_key_here
```
3. Create an environment
```
python3 -m .venv venv
```
5. Install Dependencies
```
pip install -r requirements.txt
```
4. Run the App
```
streamlit run job_analyzer.py
```
## 📖 How It Works
* Input: Paste a URL from LinkedIn, Glassdoor, or any company career page.
* Processing: The app fetches the HTML and process the structured text with the AI model.
* Output: role title, company name, salary range and location.
* Score: A 0-100 rating of the Job Description.
* Tech Stack: A clean list of required technologies.
* Red Flags: Critical warnings ("toxicity" "vague", "unrealistic").

## 🎨 Deploy
```
https://headhunter-gen-ai.streamlit.app
```

## 🤝 Contributing
Contributions are welcome! If you have ideas for new features, feel free to open an issue or submit a pull request.
