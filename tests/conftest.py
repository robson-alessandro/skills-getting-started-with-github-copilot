import pytest
import copy
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide TestClient for API testing"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a clean state before each test"""
    # Store original state
    original_activities = copy.deepcopy(activities)
    
    # Clear and reset for test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
    
    yield
    
    # Restore original state after test
    activities.clear()
    activities.update(copy.deepcopy(original_activities))
