# RAG-Pipeline

This project implements a Retrieval Augmented Generation (RAG) pipeline using Ollama for language model inference and Weaviate as a vector database. The setup allows for efficient data retrieval and processing, leveraging the capabilities of both tools.

![image](https://github.com/user-attachments/assets/a7fde28e-d795-4e17-814a-42707b3c1260)

## Prerequisites

Before you begin, ensure you have the following applications and libraries installed:

### Ollama
- **Download Ollama**: [Ollama Download Page](https://ollama.com/download)
- **Pull Models**:
  - Use the command `ollama pull {model}` to download the desired language model.
  - Use the command `ollama pull {embed model}` to download the embedding model.

### Weaviate
- **Quickstart Guide**: [Weaviate Quickstart](https://weaviate.io/developers/weaviate/quickstart)
- **Install Weaviate Client**:
  ```bash
  pip install -U weaviate-client

### Docker
- **Quickstart Guide**: [Docker Download Page](https://docs.docker.com/desktop/install/linux-install/)
- **Quickstart Guide**: [Weaviate Docker Quickstart](https://weaviate.io/developers/weaviate/installation/docker-compose)

