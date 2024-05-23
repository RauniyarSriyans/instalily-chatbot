```
Please ignore all commented lines of code as multiple approaches were tried 
to meet the objectives of the project. The codebase isn't clean as of now and further 
updates will be made in the future to make it more readable and maintainable.

To run this project locally, please follow the instructions below:
```

# Clone the repository

```bash
git clone [reporitory_url]
```

# Activate virtual environment

```bash
source .instalily/bin/activate
```

# Install the backend requirements

```bash
cd backend
pip install -r requirements.txt
```

# Install the frontend requirements

```bash
cd frontend
npm install
```

# Run the backend server

```bash
cd backend
make server-dev
```

# Run the frontend

```bash
cd frontend
npm start
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.
```

# Backend API Endpoints

```bash
Open [http://localhost:8000](http://localhost:8000) to interact with the API.

To scrape data for a particular model, use the following endpoint:
/scrape/model/{model_number}

To scrape data for a particular part, use the following endpoint:
/scrape/part/{partselect_number}
```

# To run the scrapper via the command line

Use the following commands to run the individual scrappers via the command line:

# 1. Scrape All Models and Parts [Caution: This will take a long time to run. Please do not run this command unless you have a lot of time and your processor can handle it.]

```bash
cd partselect
scrapy crawl all_models_parts
```

# 2. Scrape Individual Model

```bash
cd partselect
scrapy crawl model -a model_number={{model_number}}
The output will be saved in the 'out/models/' folder inside backend directory. The name of the file should match {{model_number}}.jsonl.
```

# 3. Scrape Individual Part

```bash
cd partselect
scrapy crawl part_details -a partselect_number={{partselect_number}}
The output will be saved in the 'out/parts/' folder inside backend directory. The name of the file should match {{partselect_number}}.jsonl.
```