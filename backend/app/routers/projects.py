from fastapi import APIRouter, UploadFile, File

router = APIRouter(prefix="/projects")

@router.post("/")
def create_project(title: str, manga_type: str):
    return {"title": title, "manga_type": manga_type}

@router.post("/{project_id}/upload")
def upload_file(project_id: int, file: UploadFile = File(...)):
    return {"project_id": project_id, "filename": file.filename}
