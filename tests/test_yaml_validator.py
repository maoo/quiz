import pytest
from pathlib import Path
from src.yaml_validator.validator import (
    validate_yaml,
    validate_yaml_file,
    YAMLValidationError,
    load_yaml,
    load_schema
)

@pytest.fixture
def valid_yaml_content():
    return """
    title: Test Quiz
    description: A test quiz
    difficulty: medium
    cards:
      - id: "1"
        question: What is 2+2?
        answer: "4"
    """

@pytest.fixture
def invalid_yaml_content():
    return """
    title: Test Quiz
    description: A test quiz
    difficulty: medium
    cards:
      - id: 1
        question: What is 2+2?
        # Missing answer field
    """

@pytest.fixture
def schema_file(tmp_path):
    schema = {
        "type": "object",
        "required": ["title", "description", "difficulty", "cards"],
        "properties": {
            "title": {"type": "string"},
            "description": {"type": "string"},
            "difficulty": {"type": "string", "enum": ["easy", "medium", "hard"]},
            "cards": {
                "type": "array",
                "items": {
                    "type": "object",
                    "required": ["id", "question", "answer"],
                    "properties": {
                        "id": {"type": "string"},
                        "question": {"type": "string"},
                        "answer": {"type": "string"}
                    }
                }
            }
        }
    }
    
    schema_path = tmp_path / "schema.yaml"
    with open(schema_path, "w") as f:
        import yaml
        yaml.dump(schema, f)
    return schema_path

@pytest.fixture
def yaml_file(tmp_path, valid_yaml_content):
    yaml_path = tmp_path / "content.yaml"
    with open(yaml_path, "w") as f:
        f.write(valid_yaml_content)
    return yaml_path

def test_load_yaml_valid():
    """Test loading valid YAML content."""
    content = """
    title: Test
    value: 42
    """
    result = load_yaml(content)
    assert result["title"] == "Test"
    assert result["value"] == 42

def test_load_yaml_invalid():
    """Test loading invalid YAML content."""
    content = """
    title: Test
    value: 42
    - invalid: yaml
    """
    with pytest.raises(YAMLValidationError):
        load_yaml(content)

def test_load_schema_valid(schema_file):
    """Test loading valid schema file."""
    schema = load_schema(schema_file)
    assert "type" in schema
    assert "properties" in schema

def test_load_schema_invalid(tmp_path):
    """Test loading invalid schema file."""
    invalid_schema = tmp_path / "invalid.yaml"
    with open(invalid_schema, "w") as f:
        f.write("invalid: yaml: content")
    
    with pytest.raises(YAMLValidationError):
        load_schema(invalid_schema)

def test_validate_yaml_valid(valid_yaml_content, schema_file):
    """Test validating valid YAML content."""
    assert validate_yaml(valid_yaml_content, schema_file) is True

def test_validate_yaml_invalid(invalid_yaml_content, schema_file):
    """Test validating invalid YAML content."""
    with pytest.raises(YAMLValidationError):
        validate_yaml(invalid_yaml_content, schema_file)

def test_validate_yaml_file_valid(yaml_file, schema_file):
    """Test validating valid YAML file."""
    assert validate_yaml_file(yaml_file, schema_file) is True

def test_validate_yaml_file_invalid(tmp_path, schema_file):
    """Test validating non-existent YAML file."""
    with pytest.raises(YAMLValidationError):
        validate_yaml_file(tmp_path / "nonexistent.yaml", schema_file)

def test_validate_yaml_with_dict(valid_yaml_content, schema_file):
    """Test validating YAML content as dict."""
    import yaml
    content_dict = yaml.safe_load(valid_yaml_content)
    assert validate_yaml(content_dict, schema_file) is True

def test_validate_yaml_with_invalid_schema_path():
    """Test validating with non-existent schema file."""
    with pytest.raises(YAMLValidationError):
        validate_yaml("title: Test", "nonexistent_schema.yaml") 