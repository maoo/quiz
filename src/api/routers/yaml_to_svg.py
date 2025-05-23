from ninja import Router, Body
from typing import Any
from src.yaml_to_svg.generate_svg import YAMLToSVG

router = Router()

@router.post("/convert")
def convert_yaml_to_svg_endpoint(request, data: dict = Body(...)):
    """
    Convert YAML data to SVG
    """
    try:
        if not isinstance(data, dict):
            return {"status": "error", "message": "Invalid input data format"}
        
        if "questions" not in data and not any(key in data for key in ["question_content", "options", "correct"]):
            return {"status": "error", "message": "Missing required fields in input data"}
        
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create the expected directory structure
            cards_dir = os.path.join(temp_dir, "cards", "card1")
            os.makedirs(cards_dir)
            # Write content.yaml (top-level question)
            question_data = data["questions"][0] if "questions" in data else data
            yaml_file = os.path.join(cards_dir, "content.yaml")
            with open(yaml_file, "w") as f:
                import yaml
                yaml.dump(question_data, f)
            # Write empty answers.yaml
            answers_file = os.path.join(cards_dir, "answers.yaml")
            with open(answers_file, "w") as f:
                f.write("")
            # Create a minimal valid index.yaml so YAMLToSVG does not fail
            index_file = os.path.join(temp_dir, "index.yaml")
            with open(index_file, "w") as f:
                f.write("title: Test Quiz\n")
            converter = YAMLToSVG([temp_dir])
            converter.process_deck()
            svg_file = os.path.join(cards_dir, "content.svg")
            with open(svg_file, "r") as f:
                svg_content = f.read()
            return {"status": "success", "svg_content": svg_content}
    except Exception as e:
        return {"status": "error", "message": str(e)} 