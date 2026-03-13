# MX Assessment

## Requirements

1. Docker

OR

2. Python 3.9+ (I used Python 3.12)

## Setup Instructions

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


## API Documentation

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

## Benchmark run and performance metrics

Some benchmark results are already available in `./data/benchmarks/` related to various runs the settled around 72% Accuracy in most cases, sometimes reaching 76% or 80%.
These files are simple json files containing for each claim in the benchmark (not ordered by claim number) the expected (aka the choice provided by the assignment as the correct one) and the actual choice, in the format described above by the API documentation.
Notable runs are:

- `./data/benchmarks/run_80%.json`: Best overall out of my tests, slightly more inclined to DENY claims which is good if a conservative model is preferred. Uses a mix of GPT-5.4 and GPT-4o

- `./data/benchmarks/run_76%.json`: Second best overall, similar behavior to the 80% run.
- `./data/benchmarks/run_72%_gpt5_1.json`: Using GPT-5.1, more prone to APPROVE with respect to GPT-5.4 but sill reaching a good level by the standards that this architecture achieved. 

Many runs are provided to demonstrate the model stability in the choices and performance overall.
Should it be needed to verify the validity, the benchmark of the full 25 claims can be run by:

1. Run the project to start the FastAPI server (with either Python or Docker)

2. Make sure that `./data/benchmarks` does not currently contain a plain `run.json`. 
    If there is one, simply rename it or delete it.

3. From the project home, run the following commands:

    ```bash
    source <venv_name>/bin/activate
    cd tests
    python run_full_benchmark.py
    ```

4. Make sure that in `tests/compute_performance_metrics.py` the `RUN` variable corresponds to the run file which scores you want to check, for instance `RUN = "run.json"`.

5. When the run finishes you can visualize the performance of the pipeline on the benchmark but running the following command:

    ```bash
    python compute_performance_metrics.py
    ```


## Decision-making Logic

- #### Why FastAPI?:
    This is the framework I am most comfortable with out of the options allowed by the assignment which also allowed me to be done with this side of the assignment quite quickly.

- #### Why Pydantic AI?:
    With limited prior knowledge in Agentic AI, I decided to take this as a learning opportunity as well and implement the process as a multi-agent system rather than a strictly predefined flow.
    The project uses a main agent with the avility to augment it's context with the Policy file content and 3 tools:
    
    - Description Analysis
    - Supporting Documents Analysis 
    - Fraud Checker

    The first 2 leverage on the FileAnalyser agent which can use the input context provided in the form of either Description file of the claim or list of files for the Supporting documents. It then analyses them one by one to provide a detailed assessment for each.
    The third tool instead, takes care of analysing the supporting file that are in image format to inspect them and find any evidence of fraudulent intent or more simply signs that the files cannot be considered valid and used for the assessment of the claim. 

    Additionally, the file analyser for supporting documents, uses another model to extract the text from the images in order to assess the content of the file itself rather than any potential cosmetic issue.

- #### Why OpenAI?:
    I have often worked with OpenAI apis and models and am therefore more comfortable with them. 
    Having an account already setup and with funds to make use of also drove the decision.

- #### Why Docker?:
    Easily the quickest and safest way to prepare a project to be run on other machines.
    Mind you the current `dockercompose.yml` prepares the image for `linux/amd64` platforms which should be able to run on M1, M2, etc. MacBooks but in case that part can be omitted from the docker compose in order to have the `linux/arm64` version.

- #### Why a File System Storage instead of DB?:
    To keep the development quick and focus on the performances a bit more, I decided to simply store the claim submissions as local folders. Alternatively SQLite3 could have been used but this was much quicker for me to develop.
    
    **N.B.**: In this context, I save each claim as a folder whose name follows the following pattern: `claim_<uuid4>` instead of using an incremental ID. This is to generate a unique id that should likely not generate conflicts in case of parallel processing of claims. This would have been easily avoided with a proper DB.

- #### Bonus features:
    - **Confidence Scoring**: 
        This is a score generated by the agent when providing the response which is defined in the structured output of the mode. Unfortunately as the whole agent runs async and the logprobs are not yet available through pydantic ai run and run_stream methods, I decided to go with this less technical way of determining the model confidence.

    - **Document Processing**:
        The `src/agents/ocr_agent.py` take care of this. When a file is detected as image during the `supporting_docs_analysis` function run, the `extract_text` runs to extract the text and build a text binary document to be passed to the file analysis agent.

    - **Fraud Detection**:
        For this, the `src/agents/fraud_checker.py` agent takes care of analysing the image files as images in order to return an assessment on the validity/fraudulent intent of the file. 
        Especially when using the latest GPT model (5.4) for this agent, the reasoning for the choices highlights this by reporting the cases for instance in which the file contains redact or partially illegible parts.

 
