# Grafana Tempo
This is an example repository to integrate Grafana Tempo with Kafka. You can immediately run the `docker-compose.yml`, which will use the configuration from `tempo.yml`.

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Commands

1. **Clone the repository:**
```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Start the services:**
```docker-compose up -d```


3. **Check the logs to ensure everything is running correctly:**
    ```docker-compose logs -f```

### Configuration
The services are configured using the tempo.yml file, which is referenced in the docker-compose.yml file. You can modify the configuration as needed.