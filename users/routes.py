from fastapi import APIRouter,Depends,Form,Request,Cookie,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,HTMLResponse,Response
from core.database import get_db,setting
from users.models import Userinfo
from users.schemas import RequestUser,ResponseUser,UserinfoCreate,UserinfoUpdate,DescriptionUpdate
from users.services import insert_user,get_user,get_user_info,get_curr_user,create_userinfo,update_userinfo,get_user_data
from fastapi.templating import Jinja2Templates
import requests
from botocore.exceptions import ClientError
import httpx

from core.connect import get_s3_client
s3=get_s3_client()
templates = Jinja2Templates(directory="templates")
router=APIRouter(tags=["Users"],prefix="/users")

 

@router.post("/createuser")
async def createuser(
    request: Request,
    firstname: str = Form(...),
    lastname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Build SQL user object
    user_data = RequestUser(
        firstname=firstname,
        lastname=lastname,
        email=email,
        password=password
    )
    new_user = insert_user(data=user_data, db=db)

    # Prepare payload for notification
    data = {
        "user_name": firstname,
        "to": email,
        "type": "email",
        "template_key": "welcome"
    }

    # 🔗 Call Neo4j API endpoint
    async with httpx.AsyncClient() as client:
        neo4j_res = await client.post(
            "http://127.0.0.1:8003/create_user_no_sql",
            json={"username": firstname, "email": email}
        )

        # 🔗 Try notification service, but ignore errors
        try:
            await client.post(
                "http://127.0.0.1:8080/notification/send_notfication",
                json=data
            )
        except httpx.RequestError as e:
            # Log the error but don’t break the flow
            print(f"Notification service unreachable: {e}")

    # Handle only Neo4j response
    if neo4j_res.status_code == 200:
        return JSONResponse(
            status_code=201,
            content={"message": f"User {new_user} account created successfully in SQL + Neo4j"}
        )
    else:
        return JSONResponse(
            status_code=500,
            content={"error": f"Neo4j failed with status {neo4j_res.status_code}"}
        )

@router.get("/{user_id}/description")
def get_description(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Userinfo).filter(Userinfo.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"description": user.about or ""}

# 🔹 2. Edit description
@router.put("/{user_id}/description")
def update_description(user_id: int, update: DescriptionUpdate, db: Session = Depends(get_db)):
    user = db.query(Userinfo).filter(Userinfo.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.about= update.description
    db.commit()
    db.refresh(user)
    return {"message": "Description updated successfully", "description": user.about}

@router.get("/profile", response_class=HTMLResponse)
def profile(request: Request, curr_user: int = Depends(get_curr_user), db: Session = Depends(get_db)):
    user = get_user_info(curr_user, db)
    access_token = request.cookies.get("access_token")
    refresh_token = request.cookies.get("refresh_token")
     
    user_data = ResponseUser.from_orm(user).dict()

    return templates.TemplateResponse("profile.html", {
        "request": request,
        "access": access_token,
        "refresh": refresh_token,
        "user_info": user_data,
        "user_id": curr_user
    },headers={
            "Cache-Control": "no-cache, no-store, must-revalidate",
            "Pragma": "no-cache",
            "Expires": "0",
        })

# @router.get("/get_avatar/{data}")
# def avatar(data:int,db: Session = Depends(get_db)):
#     user = get_user_data(data, db)
     
     
#     return user

@router.get("/get_data")
def avatar(request:Request,data:int,db: Session = Depends(get_db)):
    user = get_user_data(data, db)
     
     
    return user

@router.post("/get_data")
def avatar(request:Request,data:int,db: Session = Depends(get_db)):
    return {"hello"}

@router.get("/profile2")
def profile(request: Request, curr_user: int = Depends(get_curr_user), db: Session = Depends(get_db)):
  user = get_user_info(curr_user, db)
  return JSONResponse(content={
      "access": request.cookies.get("access_token"),
      "refresh": request.cookies.get("refresh_token"),
      "user_info": ResponseUser.from_orm(user).dict(),
      "user_id": curr_user
  })

# @router.get("/profile", response_class=HTMLResponse)
# def profile(request:Request,curr_user:int= Depends(get_curr_user),db:Session=Depends(get_db)):
    

    
#     key = f"users/{curr_user}/profile.jpg"

#     # ✅ Generate presigned URL
#     url = s3.generate_presigned_url(
#         ClientMethod='get_object',
#         Params={
#             'Bucket': setting.get_bucket_name(),
#             'Key': key
#         },
#         ExpiresIn=3600  # URL valid for 1 hour
#     )

     
    
#     user=get_user_info(curr_user,db)
#     access_token = request.cookies.get("access_token")
#     refresh_token = request.cookies.get("refresh_token")
     
#     user_data = ResponseUser.from_orm(user).dict()

#     return templates.TemplateResponse("profile.html", {
#         "request": request,
#         "access": access_token,
#         "refresh": refresh_token,
#         "user_info": user_data,
#         "user_id":curr_user,
#         "profile_url":url
#     })
 
@router.get("/{user_id}/profile-pic")
def get_profile_pic(user_id: int):
    key = f"users/{user_id}/{user_id}.jpg"
    try:
        obj = s3.get_object(Bucket=setting.get_bucket_name(), Key=key)
        return Response(
            content=obj["Body"].read(),
            media_type="image/jpeg",
            headers={"Cache-Control": "public, max-age=86400"}  # cache for 1 day
        )
    except ClientError as e:
        if e.response['Error']['Code'] == "NoSuchKey":
            # ✅ Continue gracefully: return a default placeholder image
            with open("static/volume.png", "rb") as f:
                return Response(
                    content=f.read(),
                    media_type="image/jpeg",
                    headers={"Cache-Control": "public, max-age=86400"})
 
@router.post("/userinfo")
def insert_userinfo(data: UserinfoCreate):
    print(data)
    # user_inffo=create_userinfo(data,db)
    return {"user_data":"user_inffo"}

# @router.put("/userinfo")
# def modify_userinfo(data: UserinfoUpdate, db: Session = Depends(get_db)):
#     updated = update_userinfo(db, curr_user, data)
#     if not updated:
#         raise HTTPException(status_code=404, detail="Userinfo not found")
#     return updated
