# Smart Scout: Your AI Shopping Assistant

Smart Scout is an AI-powered web application that helps users extract and understand product information from any e-commerce product page. It uses web scraping, natural language processing, and a conversational interface to answer user queries about products in a friendly, helpful manner.

---

## Features

- **Web Scraping:** Extracts product details from any provided product URL using a headless browser.
- **Content Cleaning:** Removes unnecessary sections (headers, footers, reviews, etc.) and cleans the content for better AI processing.
- **AI-Powered Q&A:** Uses a local LLM (Ollama with Llama 3.1) to answer user questions about the product.
- **Conversational UI:** Chat interface built with Streamlit for easy interaction.
- **Caching:** Efficient response caching for faster repeated queries.

---

## Demo
![Main UI](https://github.com/user-attachments/assets/cad87911-2b70-4dc1-af2d-19bbbb0145e6)
![Flipkart Prodct link](https://github.com/user-attachments/assets/be17f515-f398-4671-b2d4-cd52c8e09a14)
![Scaping the product Data](https://github.com/user-attachments/assets/dc136559-ada1-4159-a06f-6ac12ca7c580)
![Generating Response](https://github.com/user-attachments/assets/5df03500-dd10-4035-8225-3fda1b3ada11)
![Response](https://github.com/user-attachments/assets/75c4ca31-5ba7-4cc5-82dc-a079b32ef545)







---

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/smart-scout.git
cd smart-scout
```

### 2. Install Python Dependencies

Make sure you have Python 3.11+ installed.

```sh
pip install -r requirements.txt
```

### 3. Download Chrome WebDriver

- Download the Chrome WebDriver that matches your installed version of Google Chrome from the official site:  
  [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads)
- Place the downloaded `chromedriver.exe` in the project root directory.

---

## Usage

### 1. Start Ollama with Llama 3.1 Model

Make sure you have [Ollama](https://ollama.com/) installed and running with the `llama3.1` model.

```sh
ollama run llama3.1
```

### 2. Run the Streamlit App

```sh
streamlit run app.py
```

### 3. Using the App

- Enter a product URL from any e-commerce website.
- Click "Go" to scrape and process the product page.
- Ask any question about the product in the chat interface (e.g., "What is the RAM?", "How is the battery life?").
- Reset the chat or scrape a new product as needed.

---

## Project Structure

```
├── app.py                # Streamlit app (main entry point)
├── scrape.py             # Web scraping and content cleaning utilities
├── parse.py              # AI parsing, caching, and response logic
├── requirements.txt      # Python dependencies
└── chromedriver.exe      # Chrome WebDriver (download separately)
```

---

## Requirements

- Python 3.11+
- Google Chrome (latest version recommended)
- Chrome WebDriver ([download here](https://chromedriver.chromium.org/downloads))
- Ollama with Llama 3.1 model ([Ollama installation guide](https://ollama.com/))

---

## Troubleshooting

- **WebDriver Errors:** Ensure `chromedriver.exe` matches your Chrome version and is in the project root.
- **Ollama Connection Errors:** Make sure Ollama is running and the Llama 3.1 model is downloaded.
- **Module Errors:** Double-check all dependencies are installed via `pip install -r requirements.txt`.

---

## License

This project is for educational purposes.

---

## Presentation

- [Read the Project PPT](https://drive.google.com/file/d/1UBdBGgiug4tS57l-F-cIo7inmrFrpF6I/view?usp=sharing)  

---

## Acknowledgements

- [Selenium](https://www.selenium.dev/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [lxml](https://lxml.de/)
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Ollama](https://ollama.com/)
