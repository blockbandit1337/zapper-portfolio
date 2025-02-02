# Zapper + Bybit 
Portfolio Tracker
Small Python service to capture a historic snapshot of your Zapper and Bybit portfolios. 

# Config Structure
Create a config.json in the root, with the following config setup.
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

# Database Structure
For the service to run properly, it requires two tables in your databass, prices and balances

## Prices Table
```
CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    pair VARCHAR(20) NOT NULL,
    base_currency VARCHAR(10) NOT NULL,
    quote_currency VARCHAR(10) NOT NULL,
    price DECIMAL(18, 8) NOT NULL,
    snapshot_time TIMESTAMP NOT NULL,
    UNIQUE (pair, snapshot_time) -- Ensure no duplicate entries for the same pair and timestamp
);
```

## Balances table
```
CREATE TABLE balances (
    id SERIAL PRIMARY KEY,
    snapshot_time TIMESTAMP NOT NULL,
    source VARCHAR(255) NOT NULL,
    usd_value DECIMAL(18, 2) NOT NULL
);
```


## Debugging
- Ensure you have configured gcloud auth with google for the right region on both push and pull ends using `gcloud auth configure-docker <LOCATION>-docker.pkg.dev`
- Ensure the service account on the GCP VM has access to pull from artifact registry. To do this, enable use of all service APIs in the VM settings and give the service account the artifact registry writer role.