from fastapi import APIRouter,Depends,UploadFile,Request,File,HTTPException
from core.connect import get_bucket_client,setting
import subprocess
import os
import tempfile
import requests

router=APIRouter(prefix="/upload",tags=["uploads"])
 

@router.post("/profile/{user_id}")
def upload_profile_pic(user_id:str,file:UploadFile = File(...),s3=Depends(get_bucket_client)):

     
    if not user_id:
        raise HTTPException(status_code=402, detail="No user_id cookie found")
    key = f"users/{user_id}/profile.jpg"
    file.file.seek(0)

    # ✅ Use upload_fileobj with ExtraArgs
    s3.upload_fileobj(
        Fileobj=file.file,
        Bucket=setting.get_bucket_name(),
        Key=key,
        ExtraArgs={
            "ContentType": file.content_type
        })

    return {"Profile pic Uploaded":"Successfully"}




@router.get("/profile/{user_id}")
def get_profile_pic(user_id:int,s3=Depends(get_bucket_client)):
     
    key = f"users/{user_id}/profile.jpg"

    # ✅ Generate presigned URL
    url = s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': setting.get_bucket_name(),
            'Key': key
        },
        ExpiresIn=3600  # URL valid for 1 hour
    )

    return {"url": url}

def generate_manifest(output_dir: str, manifest_path: str, target_duration: int = 10):
    chunk_files = sorted([
        f for f in os.listdir(output_dir)
        if f.endswith(".ts")
    ])

    with open(manifest_path, "w") as m3u8:
        m3u8.write("#EXTM3U\n")
        m3u8.write("#EXT-X-VERSION:3\n")
        m3u8.write(f"#EXT-X-TARGETDURATION:{target_duration}\n")
        m3u8.write("#EXT-X-MEDIA-SEQUENCE:0\n")

        for chunk in chunk_files:
            m3u8.write(f"#EXTINF:{target_duration}.0,\n")
            m3u8.write(f"{chunk}\n")

        m3u8.write("#EXT-X-ENDLIST\n")




@router.post("/upload-chunk/{user_id}")
async def upload_user_video(request:Request,user_id:int):
    headers = request.headers
    video_id = headers["X-Video-ID"]
    chunk_index = headers["X-Chunk-Index"]
    chunk = await request.body()

    # Forward to compression microservice
    requests.post(
         
        "http://localhost:8080/compress-chunk",
        headers={
            "X-Video-ID": video_id,
            "X-Chunk-Index": chunk_index,
            "user_id":str(user_id)
        },
        data=chunk
    )

    return {"status": "chunk forwarded"}

 

@router.get("/videos/{user_id}")
def list_user_videos(user_id: int, s3=Depends(get_bucket_client)):
     
    prefix = f"users/{user_id}/videos/"

    response = s3.list_objects_v2(
        Bucket=setting.get_bucket_name(),
        Prefix=prefix
    )

    # Extract keys and generate presigned URLs
    video_urls = []
    for obj in response.get("Contents", []):
        key = obj["Key"]
        url = s3.generate_presigned_url(
            ClientMethod='get_object',
            Params={'Bucket': setting.get_bucket_name(), 'Key': key},
            ExpiresIn=3600
        )
        video_urls.append({"filename": key.split("/")[-1], "url": url})

    return {"videos": video_urls}
