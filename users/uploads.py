from io import BytesIO
from fastapi import APIRouter, UploadFile, Depends
from core.connect import get_s3_client
from core.config import get_settings
from users.services import insert_user,get_user,get_user_info,get_curr_user
router = APIRouter(prefix='/upload',tags=["upload"])

@router.post("/profile/{user_id}")
async def upload_profile_pic(file:UploadFile, user_id:str, s3=Depends(get_s3_client)):
    settings = get_settings()
    key = f"users/{user_id}/{user_id}.jpg"
    file.file.seek(0)

    # ✅ Use upload_fileobj with ExtraArgs
    s3.upload_fileobj(
        Fileobj=file.file,
        Bucket=settings.get_bucket_name(),
        Key=key,
        ExtraArgs={
            "ContentType": file.content_type
        })
    return {"message": "Profile picture uploaded successfully"}



