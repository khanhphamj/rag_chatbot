# Customer Product Consultation Chatbot 🤖✨

Welcome to the **Customer Product Consultation Chatbot** project—a sophisticated AI-driven solution designed to provide personalized product advice and customer support. This chatbot integrates with top-tier LLM providers (like OpenAI, Gemini, and others) and utilizes function calling to interact with your product database in real time.

---

## Table of Contents 📑

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Roadmap](#roadmap)
- [Contact](#contact)

---

## Overview 🌟

The Customer Product Consultation Chatbot is built to enhance customer interactions by delivering intelligent, context-aware product recommendations. Whether you’re in e-commerce, retail, or another industry, this solution adapts to your business needs with its robust integration of advanced LLM APIs and direct database communication.

---

## Features 🚀

- **Multi-Provider Integration:** Seamlessly connect with various LLM APIs (e.g., OpenAI, Gemini) to leverage state-of-the-art AI models.
- **Function Calling:** Directly interface with your product database to retrieve, update, and manage product information dynamically.
- **Modular Design:** A well-organized codebase that facilitates scalability and ease of maintenance.
- **Real-Time Performance:** Optimized for quick response times to ensure a smooth user experience.
- **Customizable Workflow:** Tailor the chatbot's behavior to match your business processes and product catalog.
- **Secure Operations:** Emphasizes best practices in API key management and database security.

---

## Architecture 🏗️

The project is structured into several key modules:

- **Core Engine:** Orchestrates API requests, function calls, and overall chatbot logic.
- **API Integration Layer:** Manages communication with multiple LLM providers to generate context-aware responses.
- **Database Module:** Handles interactions with the product database, ensuring data integrity and fast lookups.
- **Utility Functions:** Contains helper functions for error handling, logging, and data validation.
- **User Interface:** Provides a simple and intuitive interface for both customers and administrators.

This modular architecture ensures that each component is independent, making it easier to extend or modify parts of the system without impacting the overall functionality.

---

## Installation 🛠️

Follow these steps to set up the project on your local machine:

1. **Install Poetry:**  
   Install Poetry, a dependency management tool for Python.

   ```bash
   pip install poetry
    ```
2. **Intialize Project:**  
    Set up the project environment with Poetry.
   ```bash
   poetry init
   ```
3. **Install Dependencies:**  
    Install the required dependencies for the project.
   ```bash
   poetry install
   ```

## Usage 💡

After installing the project, you can start the chatbot service using the following command:

```bash
python main.py
```

Customization Options

- **API Providers: Add your API keys for OpenAI, Gemini, etc., in the configuration file.

- **Database Connection: Configure database credentials in .env.

- **Function Definitions: Adjust function calling scripts in /functions.

## Configuration ⚙️

- **API Keys:** Securely store them in `.env`.
- **Database Settings:** Configure connection parameters (host, port, username, password).
- **Logging & Error Handling:** Adjust logging settings to monitor chatbot performance.
- **Environment Variables:** Use different configs for dev, testing, and production.

## Roadmap 🗺️

### Planned Features

1. **Knowledge Graph Integration**:
    - **Objective**: Enhance the chatbot's ability to understand and provide more accurate responses by integrating a knowledge graph.
    - **Technology**: Use Neo4j for the knowledge graph database.
    - **Steps**:
        1. Set up a Neo4j database.
        2. Define the schema for the knowledge graph.
        3. Integrate Neo4j with the chatbot.
        4. Develop functions to query the knowledge graph.
        5. Update the chatbot logic to utilize the knowledge graph for responses.

2. **Multi-Language Support**:
    - **Objective**: Enable the chatbot to support multiple languages to cater to a broader audience.
    - **Steps**:
        1. Identify the target languages.
        2. Implement language detection.
        3. Integrate translation APIs (e.g., Google Translate).
        4. Localize the chatbot responses.
        5. Test the chatbot in different languages to ensure accuracy and fluency.

## Contact 📧

For questions or feedback, please reach out to the project maintainers: phukhanh1903@gmail.com

## Video Demo 🎥

https://github.com/user-attachments/assets/de15a1d6-67df-44e1-9ef6-c6cd6c55d67a
