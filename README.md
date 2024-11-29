# INTJ: An LLM based IoT Network Threat Journeyman

## Installation

### Model

- [INTJ model](https://huggingface.co/XD3an/Llama-3.1-8b-4bit-IoT-SecConsultant)
    - Fine-Tuning-dataset: [CICIoT2023-fine1](https://huggingface.co/datasets/XD3an/CICIoT2023-fine1)

## Usage

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