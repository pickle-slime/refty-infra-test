#### Setup

Clone repo

```bash
git clone https://github.com/pickle-slime/refty-infra-test.git 
```

Create and activate virtual environment. Download all dependencies

```bash
cd refty-infra-test
python -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

Populate .env file with data. You can use any repo you have access to.

```bash
REPOSITORY_FORK=refty-infra-test
REPOSITORY_BRANCH=main
GITHUB_TOKEN=your_token
GITHUB_USERNAME=your_username
```

Go to the src/ direcotry and run the application.

```bash
cd src
python main.py
```

Now you can open http://localhost:8000/docs to check out endpoints
