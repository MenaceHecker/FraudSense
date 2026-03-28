# Risk Service

This service currently targets Python 3.13.

`pydantic==2.9.2` installs cleanly on Python 3.13, but fails on Python 3.14 because `pydantic-core==2.23.4` falls back to a source build and its bundled `PyO3` version does not support Python 3.14.

## Setup

```bash
cd services/risk-service
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
