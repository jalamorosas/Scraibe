# Scribe
## An AI note taking tool

## Installation
- Clone this github repository to your device
- In the terminal, cd to the repository and create and activate a virtual environment
  - Create the virtual environment: ```python -m venv myenv```
  - Activate the virtual environment
    - Windows: ```myenv\Scripts\activate```
    - macOS/Linux: ```source myenv/bin/activate```
  - Once activated, your terminal prompt will look like this: ```(myenv) user@hostname:path/to/your/directory$```
- Create an OpenAI API Key and set up billing
  - Navigate to the [OpenAI Website](https://openai.com) and either log in if you have an account or sign up if you don't
  - Navigate to the API section
    - After logging in, click the API selection to navigate to OpenAI's API section
    - Click the lock icon that says API Keys in the left menu
  - Generate an API Key
    - Click on the "Create new secret key" button to generate a new API key
    - In the box that pops up, enter a name for your key then click the "Create secret key" button
    - Copy your generated secret key and paste it in a secure place. YOU WON'T BE ABLE TO RETRIEVE IT AGAIN
    - This API key is for you only. DO NOT SHARE IT WITH ANYONE
  - Set up billing
    - In the left menu, click settings, then click billing, then click Payment methods
    - Click Add payment method and enter your credit card and billing details. Submit once you've entered your information
    - On the top menu, click Overview, then click "Add to credit balance"
    - In the Amount to add entry, choose the amount of money you would like to add to your balance then click continue
- Back in the terminal, verify that your virtual environment is activated then export your API key (replace "your-api-key-here" with your actual API key)
  - macOS/Linux: ```export OPENAI_API_KEY=your-api-key-here```
  - Windows
    - Command Prompt: ```set OPENAI_API_KEY=your-api-key-here```
    - PowerShell: ```$env:OPENAI_API_KEY = "your-api-key-here"```
- Install the requirements with pip: ```pip install -r requirements.txt```
## How to use Scribe
- Run the code: ```python scribe.py```
- In the dropdown menus on the left, choose what large language model you want to use and the type of file you want to save the notes to
- On the right, either click the Record button to record audio of a lecture or the Upload button to choose a file to upload
- Once processing is finished, a Text or Markdown file will save to your repository folder
