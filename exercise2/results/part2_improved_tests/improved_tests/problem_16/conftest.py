"""Pytest configuration"""
import pytest

def pytest_addoption(parser):
    parser.addoption("--model", action="store", default="gpt4o",
                     help="Model to test (gpt4o/claude)")
    parser.addoption("--strategy", action="store", default="cot",
                     help="Strategy to test")

@pytest.fixture
def model(request):
    return request.config.getoption("--model")

@pytest.fixture
def strategy(request):
    return request.config.getoption("--strategy")
