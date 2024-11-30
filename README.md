# INTJ: An LLM based IoT Network Threat Journeyman

## Installation

### Model

- [XD3an/INTJ-Llama-3.1-8b](https://huggingface.co/XD3an/INTJ-Llama-3.1-8b)
    - Fine-Tuning-dataset: [INTJ-QA-2024](https://huggingface.co/datasets/XD3an/INTJ-QA-2024)

## Usage

- Build model
    ```
    ollama create <model_name> -f ./model/Modeilfile
    ```

- Bulid ollama 
    ```
    ollama serve
    ```

- Change the Model name and Base URL in the docker-compose.yml file
    ```
    ...
        environment:
          - model=<model_name>                  # e.g. model=llama3.1:latest
          - model_base_url=<model_base_url>     # e.g. http://host.docker.internal:11434
    ...
    ```

- FastAPI server
    - app/main.py
    ```
    uvicorn main:app --reload --host <host> --port <port>
    ```

- Open WebUI
    - [https://docs.openwebui.com/](https://docs.openwebui.com/)


### docker

- Build
    ```
    docker-compose up --build
    ```