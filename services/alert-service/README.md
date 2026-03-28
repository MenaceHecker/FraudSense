# Alert Service

This service currently targets Python 3.13.

The checked-in dependency pins install cleanly on Python 3.13, while `pydantic==2.9.2` may fail on Python 3.14 because `pydantic-core==2.23.4` can fall back to a source build that is not compatible with Python 3.14.

## Setup

```bash
cd services/alert-service
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
