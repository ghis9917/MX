# MX Assessment

### Requirements

1. Docker

OR

2. Python 3.9+

### Setup Instructions

1. Clone repo and enter folder:

    ```bash
    git clone https://github.com/ghis9917/MX
    cd MX
    ```

2. Setup the `.env` file to include the `OPENAI_API_KEY`:

    ```bash
    OPENAI_API_KEY=<your_key>
    ```

- #### With Docker installed:

    3. Create the docker image:

        ```bash
        docker compose build
        ```

    4. Run the docker image:

        ```bash
        docker run -d -p 8000:8000 mx-image 
        ```

- #### With Python only:

    3. Create virtual env and install all requirements:

        ```bash
        python3 -m venv <venv_name>
        source ./<venv_name>/bin/activate
        pip install -r requirements.txt
        ```

    4. Run the FastAPI server locally:

        ```bash
        uvicorn main:app --host 0.0.0.0 --port 8000
        ```


### API Documentation

The application make 4 endpoints available as required:

- `GET /`: Root path that can be used as healthcheck

- `POST /claims/`: Allows to submit a list of files that belong to a single claim (no batch allowed). Then processes the claim and returns the choice of the agent along with the claim id as saved on the "system" in the following shape:

    ```json
    {
        "id":<uuid4_str>,
        "result":{
            "decision":<decision_str>,
            "explanation":<explanation_str>
            "confidence":<confidence_float>
        }
    }
    ```

- `GET /claims/`: Allows to retrieve all the claims processed by the agent so far and returns the results in the following shape:

    ```json
    [
        {
            "id":<uuid4_str>,
            "result":{
                "decision":<decision_str>,
                "explanation":<explanation_str>
                "confidence":<confidence_float>
            }
        },
        {
            "id":<uuid4_str>,
            "result":{
                "decision":<decision_str>,
                "explanation":<explanation_str>
                "confidence":<confidence_float>
            }
        }
    ]
    ```

- `GET /claims/{claim_id}`: Allows to retrieve a specific claim based on the ID assigned during processing and returns the results in the following shape:

    ```json
    {
        "id":<uuid4_str>,
        "result":{
            "decision":<decision_str>,
            "explanation":<explanation_str>
            "confidence":<confidence_float>
        }
    }
    ```

### Decision-making Logic

- `FastAPI`
- `Pydantic AI`
- `OpenAI`
- `Docker`
- `File System instead of DB`
- `Bonus features (?)`