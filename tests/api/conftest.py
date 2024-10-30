import sys
import os
from pathlib import Path

# Add src directory to Python path
src_path = str(Path(__file__).parent.parent.parent)
sys.path.append(src_path)

import pytest
from fastapi.testclient import TestClient
from src.fastyr.api.main import app

@pytest.fixture
def client():
    return TestClient(app) 