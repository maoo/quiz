from ninja import Router, File
from src.file_utils import get_question_folders, get_deck_folders

router = Router()

@router.post("/process")
def process_files_endpoint(request):
    """
    Process multiple files
    """
    try:
        files = request.FILES.getlist("files")
        if not files:
            return {"status": "error", "message": "No files provided"}
        
        import tempfile
        import os
        with tempfile.TemporaryDirectory() as temp_dir:
            file_paths = []
            for file in files:
                # Check for empty file content
                file.seek(0, os.SEEK_END)
                size = file.tell()
                file.seek(0)
                if size == 0:
                    return {"status": "error", "message": "Empty file provided"}
                file_path = os.path.join(temp_dir, file.name)
                with open(file_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                file_paths.append(file_path)
            deck_folders = get_deck_folders(file_paths)
            question_folders = get_question_folders(deck_folders)
            return {
                "status": "success",
                "results": {
                    "deck_folders": deck_folders,
                    "question_folders": question_folders
                }
            }
    except Exception as e:
        return {"status": "error", "message": str(e)} 