Road Accident Root Cause Analysis (mABC)
==========================================

Overview:
---------
This project implements a modular multi-agent pipeline for performing root cause analysis on road accident descriptions. The system leverages OpenAI’s reasoning models to analyze the input text and determine the most likely accident cause—along with a confidence score—using a structured chain-of-thought approach. The pipeline is designed to be efficient and provide clear, interpretable outputs.

Main Agents:
------------
1. Agent 1 – Translation to English:
   - Translates the accident description from Portuguese to English using a translation API.

2. Agent 2 – Text Improvement:
   - Improves the translated text by replacing generic terms with more technical terminology related to road safety and safety engineering.

3. Agent 3 – Accident Classifier (with Reasoning):
   - This is the core of the pipeline.
   - Process:
     a. The improved text is sent to the OpenAI Chat API using a reasoning model (e.g., GPT-4-turbo or another available reasoning model) to generate a semantic analysis.
     b. The model is instructed via a chain-of-thought prompt to explain its reasoning step by step and then to select the accident cause that best fits the description from the following list:
        - Driver distraction
        - Speeding
        - Driving under the influence of alcohol or drugs
        - Disregard for traffic rules
        - Fatigue and drowsiness
        - Lack of vehicle maintenance
        - Adverse weather conditions
        - Inadequate infrastructure
        - Aggressive behavior
        - Lack of experience
        - Inadequate use of safety equipment
        - Animals on the road
        - Visibility issues
        - Disregard for right of way
        - Improper lane usage
        - Lack of attention to pedestrians and cyclists
        - Driver health issues
        - Pedestrian inattention
        - Others
     c. The model returns a chain-of-thought explanation, the "Selected Cause", and a "Score" (a confidence level between 0 and 1).
   
4. Agent 4 – Translation to Brazilian Portuguese:
   - Translates the selected accident cause from English to Brazilian Portuguese using a predefined mapping.

File Structure:
---------------
mABC_RoadAccident_Analysis/
├── agents/
│     ├── __init__.py
│     ├── agent1_translate.py         (Translates input text to English)
│     ├── agent2_improve.py            (Improves the translated text using technical terms)
│     ├── agent3_classify.py           (Classifies the accident using reasoning)
│     └── agent4_translate.py          (Translates the root cause to Brazilian Portuguese)
├── utils/
│     ├── __init__.py
│     ├── translation.py               (Functions for text translation)
│     ├── text_improvement.py          (Functions to improve the translated text)
│     └── token_count.py               (Optional: Functions to count tokens using tiktoken)
├── config.py                        (Reads the OpenAI API key from environment variables or a .env file)
├── streamlit_app.py                 (Streamlit interface for user input and displaying results)
├── requirements.txt                 (Project dependencies)
└── README.txt                       (This file)

How It Works:
-------------
1. Input and Translation:
   - The user enters an accident description in Portuguese via the Streamlit interface.
   - Agent 1 translates the description to English.

2. Text Improvement:
   - Agent 2 refines the translated text by incorporating domain-specific details, replacing general terms with technical terminology related to road safety.

3. Semantic Classification Using Reasoning (Agent 3):
   - The improved text is sent to the OpenAI Chat API using a reasoning model (such as GPT-4-turbo) with a chain-of-thought prompt.
   - The prompt instructs the model to explain its reasoning step by step and then select the accident cause that best matches the description from a predefined list.
   - The model returns its detailed reasoning, the selected cause (in English), and a confidence score (0 to 1).

4. Translation of the Root Cause:
   - Agent 4 translates the selected cause from English to Brazilian Portuguese using a fixed mapping to ensure consistency.

5. Displaying Results:
   - The Streamlit app displays:
     - The full reasoning output (chain-of-thought).
     - The extracted results: the selected cause in English, its translation to Brazilian Portuguese, and the confidence score.
     - (Optional) Token usage information can also be displayed.
     - A "Clear Data" button is available to reset the session for new input.

Running the Application:
------------------------
1. Initialize the project with uv:
   uv init mABC_RoadAccident_Analysis
   cd mABC_RoadAccident_Analysis
   uv install -r requirements.txt

2. Configure your API key:
   - Create a .env file in the project root with:
     OPENAI_API_KEY=sk-xxx
   (Ensure .env is in your .gitignore)

3. Run the Streamlit app:
   uv run streamlit run streamlit_app.py
   (This starts the app on port 8501 and opens it in your browser)

4. Expose via ngrok (Optional):
   - Configure ngrok with your AuthToken:
     ngrok config add-authtoken YOUR_NGROK_AUTH_TOKEN
   - Start a secured tunnel with basic authentication:
     ngrok http 8501 --basic-auth="admin:minhasenha"
   - Share the generated URL; users will be prompted for authentication.

Dependencies:
-------------
- streamlit: For building the web interface.
- openai: For accessing OpenAI’s reasoning API.
- numpy: For any vector operations (if needed).
- tiktoken (optional): For token counting.
- Additional packages as listed in requirements.txt.

License:
--------
This project is licensed under the terms specified in the LICENSE file.

Happy Analyzing!
