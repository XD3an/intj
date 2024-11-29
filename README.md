# INTJ: An LLM based IoT Network Threat Journeyman

## Installation

### Model

- [INTJ model](https://huggingface.co/XD3an/Llama-3.1-8b-4bit-IoT-SecConsultant)
    - Fine-Tuning-dataset: [CICIoT2023-fine1](https://huggingface.co/datasets/XD3an/CICIoT2023-fine1)

## Usage

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