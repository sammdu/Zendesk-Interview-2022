# Zendesk-Interview-2022
Take-home technical project for Zendesk 2022 summer internship.
* Connect to the Zendesk API
* Request all the tickets for your account
* Display them in a list
* Display individual ticket details
* Page through tickets when more than 25 are returned

Developed using Python, Flask, HTML, CSS, JavaScript, and displays a web-based user interface.

## Prerequisites
### Python
Please use `Python3.9`.
### Packages
The following Python packages are used for this project:
```
certifi==2021.10.8
Flask==2.0.2
Jinja2==3.0.3
mypy==0.910
mypy-extensions==0.4.3
requests==2.26.0
types-Flask==1.1.5
types-Jinja2==2.11.8
types-requests==2.26.1
typing-extensions==4.0.0
urllib3==1.26.7
```
They are also found in [requirements.txt](https://github.com/sammdu/Zendesk-Interview-2022/blob/main/requirements.txt).

## Setup Instructions

### 1. Create a Python virtual environment
```bash
python3.9 -m venv zendesk_test_env
```
Enter the newly created Python virtual environment folder:
```bash
cd zendesk_test_env
```

### 2. Setup the project environment
Clone the project repository from GitHub:
```bash
git clone https://github.com/sammdu/Zendesk-Interview-2022.git
```
Enter the project repository folder:
```bash
cd Zendesk-Interview-2022
```
Activate the Python virtual environment in your terminal:
```bash
source ../bin/activate
```
> After the previous step, you should see the following prompt prepended to your command prompt: `(zendesk_test_env)`, which should be consistent with the Python virtual environment folder name.

Install required Python packages with `pip`:
```bash
pip install -r requirements.txt
```

### 3. Environment variables
Some important configuration parameters are sensitive in nature, therefore not included in the project repository. They need to be supplied via system environment variables.
There are three required environment variables that need to be provided before is is possible to run or test the project:
* `ZENDESK_API_SUBDOMAIN`: subdomain that is prepended to `zendesk.com`, chosen upon Zendesk account setup
    * For example, if your Zendesk Dashboard is accessed at `https://zccuser.zendesk.com/agent/dashboard`, then your subdomain should be `zccuser`
* `ZENDESK_API_EMAIL`: email of the user associated with the Zendesk account
* `ZENDESK_API_TOEKEN`: HTTP Basic Authentication API token generated at the Zendesk Admin Center

Sample configuration:
```
ZENDESK_API_SUBDOMAIN="zccuser"
ZENDESK_API_EMAIL="user@example.com"
ZENDESK_API_TOEKEN="6wiIBWbGkBMo1mRDMuVwkw1EPsNkeUj95PIz2akv"
```

> These environment variables are required before running or testing is possible!

## Seeing the project in action
With an activated virtual environment in the project repository, simply execute the following command to start a Flask development server:
```bash
python3.9 ./run.py
```
This will start a server at [http://127.0.0.1:5000/](http://127.0.0.1:5000/). Visit this address in your browser to see the project in action.

## Testing
### 1. Testing for type violations
In the project repository root, where the `mypy.ini` file is located, simply execute the following command to test for type violations:
```bash
mypy
```

### 2. Unit tests with `pytest`
