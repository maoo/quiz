import pytest
from django.test import Client
from django.urls import reverse
import json
import yaml
import base64
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

# Ensure Django is configured for testing
pytestmark = pytest.mark.django_db

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def sample_yaml_data():
    return {
        "title": "Test Quiz",
        "questions": [
            {
                "question_content": "What is 2+2?",
                "options": ["3", "4", "5"],
                "correct": "4"
            }
        ]
    }

@pytest.fixture
def sample_svg_data():
    return {
        "svg": "<svg width=\"100\" height=\"100\"><rect width=\"100\" height=\"100\" fill=\"blue\"/></svg>"
    }

def test_yaml_to_svg_endpoint(client, sample_yaml_data):
    response = client.post(
        "/api/yaml-to-svg/convert",
        data=json.dumps(sample_yaml_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "svg_content" in data
    assert "svg" in data["svg_content"]

def test_file_utils_endpoint(client):
    test_content = b"Test file content"
    file = SimpleUploadedFile("test.txt", test_content, content_type="text/plain")
    response = client.post("/api/file-utils/process", {"files": file})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "results" in data

def test_svg_to_pdf_endpoint(client, sample_svg_data):
    response = client.post(
        "/api/svg-to-pdf/convert",
        data=json.dumps(sample_svg_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    if data["status"] != "success":
        print("SVG to PDF error:", data)
    assert data["status"] == "success"
    assert "pdf_content" in data
    try:
        base64.b64decode(data["pdf_content"])
    except Exception:
        pytest.fail("PDF content is not valid base64")

def test_yaml_to_markdown_endpoint(client, sample_yaml_data):
    response = client.post(
        "/api/yaml-to-markdown/convert",
        data=json.dumps(sample_yaml_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "markdown_content" in data
    assert "What is 2+2?" in data["markdown_content"]
    assert "1. 3" in data["markdown_content"]
    assert "2. 4" in data["markdown_content"]
    assert "3. 5" in data["markdown_content"]

def test_qr_generator_endpoint(client):
    test_data = {"content": "https://example.com"}
    response = client.post(
        "/api/qr-generator/generate",
        data=json.dumps(test_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    if data["status"] != "success":
        print("QR generator error:", data)
    assert data["status"] == "success"
    assert "qr_content" in data
    try:
        base64.b64decode(data["qr_content"])
    except Exception:
        pytest.fail("QR content is not valid base64")

# Test invalid inputs
def test_invalid_yaml_to_svg_endpoint(client):
    invalid_data = {"invalid": "data"}
    response = client.post(
        "/api/yaml-to-svg/convert",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

def test_invalid_svg_to_pdf_endpoint(client):
    invalid_data = {"svg": "invalid svg content"}
    response = client.post(
        "/api/svg-to-pdf/convert",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

def test_invalid_yaml_to_markdown_endpoint(client):
    invalid_data = {"invalid": "data"}
    response = client.post(
        "/api/yaml-to-markdown/convert",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

def test_invalid_qr_generator_endpoint(client):
    invalid_data = {}
    response = client.post(
        "/api/qr-generator/generate",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data
    invalid_data = {"content": ""}
    response = client.post(
        "/api/qr-generator/generate",
        data=json.dumps(invalid_data),
        content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data

def test_invalid_file_utils_endpoint(client):
    response = client.post("/api/file-utils/process")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "error"
    assert "message" in data
    file = SimpleUploadedFile("test.txt", b"", content_type="text/plain")
    response = client.post("/api/file-utils/process", {"files": file})
    assert response.status_code == 200
    data = response.json()
    if data["status"] != "error":
        print("File utils (empty file) error:", data)
    assert data["status"] == "error"
    assert "message" in data 