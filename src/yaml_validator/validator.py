"""
YAML Validator Module

This module provides functionality to validate YAML content against JSON Schema specifications.
It uses jsonschema for validation and handles both YAML and JSON Schema formats.
"""

from typing import Dict, Any, Union
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError
import json

class YAMLValidationError(Exception):
    """Custom exception for YAML validation errors."""
    pass

def load_yaml(content: Union[str, Dict[str, Any]]) -> Dict[str, Any]:
    """
    Load YAML content from string or dict.
    
    Args:
        content: YAML content as string or dict
        
    Returns:
        Dict[str, Any]: Parsed YAML content
        
    Raises:
        YAMLValidationError: If content cannot be parsed as YAML
    """
    try:
        if isinstance(content, str):
            return yaml.safe_load(content)
        return content
    except yaml.YAMLError as e:
        raise YAMLValidationError(f"Invalid YAML content: {str(e)}")

def load_schema(schema_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load JSON Schema from file.
    
    Args:
        schema_path: Path to the schema file (YAML or JSON)
        
    Returns:
        Dict[str, Any]: Parsed schema
        
    Raises:
        YAMLValidationError: If schema file cannot be read or parsed
    """
    try:
        with open(schema_path, 'r') as f:
            if str(schema_path).endswith('.json'):
                return json.load(f)
            return yaml.safe_load(f)
    except (FileNotFoundError, json.JSONDecodeError, yaml.YAMLError) as e:
        raise YAMLValidationError(f"Failed to load schema: {str(e)}")

def validate_yaml(content: Union[str, Dict[str, Any]], schema_path: Union[str, Path]) -> bool:
    """
    Validate YAML content against a JSON Schema.
    
    Args:
        content: YAML content to validate (string or dict)
        schema_path: Path to the schema file
        
    Returns:
        bool: True if validation succeeds
        
    Raises:
        YAMLValidationError: If validation fails or if content/schema cannot be parsed
    """
    try:
        # Load and parse the content
        yaml_content = load_yaml(content)
        
        # Load and parse the schema
        schema = load_schema(schema_path)
        
        # Validate content against schema
        validate(instance=yaml_content, schema=schema)
        return True
        
    except ValidationError as e:
        raise YAMLValidationError(f"Validation failed: {str(e)}")
    except Exception as e:
        raise YAMLValidationError(f"Validation error: {str(e)}")

def validate_yaml_file(content_path: Union[str, Path], schema_path: Union[str, Path]) -> bool:
    """
    Validate a YAML file against a JSON Schema.
    
    Args:
        content_path: Path to the YAML file to validate
        schema_path: Path to the schema file
        
    Returns:
        bool: True if validation succeeds
        
    Raises:
        YAMLValidationError: If validation fails or if files cannot be read/parsed
    """
    try:
        with open(content_path, 'r') as f:
            content = f.read()
        return validate_yaml(content, schema_path)
    except FileNotFoundError as e:
        raise YAMLValidationError(f"Content file not found: {str(e)}")
    except Exception as e:
        raise YAMLValidationError(f"Validation error: {str(e)}") 