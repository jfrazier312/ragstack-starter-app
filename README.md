# Getting Started

Follow these steps to set up and use this repository:

1. **Clone this repository:** Use the following command to clone this repository to your local machine:

   ```shell
   git clone https://github.com/jfrazier312/ragstack-starter-app.git
   or
   git clone git@github.com:jfrazier312/ragstack-starter-app.git
   ```

2. **Install CookieCutter:** If you haven't already, you'll need to install Cookiecutter. You can find installation instructions [here](https://cookiecutter.readthedocs.io/en/stable/README.html#installation)
3. **Move to your directory**: Navigate to the directory you want your project at.
4. **Run CookieCutter:** 
   ```shell
   cookiecutter /path/to/this/repo
   ```
5. **Create your project:** Follow the prompts to customize your RAG application.
6. **(Recommended) Set up python virtual environment:** Navigate to your project and set up a virtual environment:
   ```shell
   python -m venv test_env
   source test_env/bin/activate
   ```
7. **Install dependencies:**
   ```
   poetry install
   ```
8. **Copy Credentials**: This project uses `dotenv` to load credentials. Create a `.env` file and populate it with your credentials. (You may need to customize this based on your project).
   ```shell
   ASTRA_DB_API_ENDPOINT=...
   ASTRA_DB_APPLICATION_TOKEN=...
   OPENAI_API_KEY=...
   LANGCHAIN_API_KEY=...
   ```
9. **Try it out:** Start your RAG pipeline!
   ```shell
   python your_project/main.py
   ```
