# Config Structure
```json
{
    "postgresql": {
        "host": "IP",
        "port": 5432,
        "dbname": "DB",
        "user": "postgres",
        "password": "PASS"
    },
    "evm_wallets": ["0x0000000000000000000000000000000000000000"],
    "solana_wallets": ["0x0000000000000000000000000000000000000000"],
    "zapper": {
        "api_key": "ZAPPER_API_KEY"
    },
    "bybit": {
        "api_key": "BYBIT_API_KEY",
        "api_secret": "BYBIT_API_SECRET"
    },
    "prices": ["BTCUSDT", "ETHUSDT", "ENAUSDT"],
}
```

# Deployment
Build for target
```
docker build . -t portfolio-tracker --platform linux/amd64
```

Push to artifact registry
```
docker push <LOCATION>-docker.pkg.dev/<PROJECT>/portfolio-tracker/portfolio-tracker:<VER>
```

Pull from registry on VM
```
docker pull <LOCATION>-docker.pkg.dev/<PROJECT>/portfolio-tracker/portfolio-tracker:<VER>
```

Run
```
docker run -d --name portfolio-tracker --restart always <LOCATION>-docker.pkg.dev/<PROJECT>/portfolio-tracker/portfolio-tracker:<VER>
```

## Debugging
- Ensure you have configured gcloud auth with google for the right region on both push and pull ends using `gcloud auth configure-docker <LOCATION>-docker.pkg.dev`
- Ensure the service account on the GCP VM has access to pull from artifact registry. To do this, enable use of all service APIs in the VM settings and give the service account the artifact registry writer role.