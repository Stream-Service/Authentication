from fastapi import APIRouter,Depends,Form,Request,Cookie,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse,HTMLResponse,Response
from core.database import get_db,setting
from users.models import Userinfo,User
from users.schemas import RequestUser,ResponseUser,UserinfoCreate,UserinfoUpdate,DescriptionUpdate,VerifyOtpSchema,Forgot_Details
from users.services import insert_user,get_user,get_user_info,get_curr_user,create_userinfo,update_userinfo,get_user_data,get_hash_password,get_pass_hash
from fastapi.templating import Jinja2Templates
import requests
import secrets
from botocore.exceptions import ClientError
import httpx
import random
import string
import json
from core.config import get_settings

setting=get_settings()
from kafka import KafkaProducer
from redis import Redis
from core.connect import get_s3_client
s3=get_s3_client()
templates = Jinja2Templates(directory="templates")
router=APIRouter(tags=["Users"],prefix="/auth/users")

 
res = Redis(
    host=setting.REDIS_SERVERS, 
    port=setting.REDIS_PORT, 
    decode_responses=True,
    socket_timeout=5,          # 5 seconds max to try connecting
    socket_connect_timeout=5,  # 5 seconds max for the initial handshake
    retry_on_timeout=True      # Try one more time if it fails
)
producer = KafkaProducer(
    bootstrap_servers=[setting.KAFKA_BOOTSTRAP_SERVERS],
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

 

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

    # Send event to Kafka for Neo4j user creation
    kafka_event = {
        "action": "create_user",
        "username": f"{firstname} {lastname}",
        "email": email,
        "user_id": new_user.user_id
    }
    producer.send('create_db_user', value=kafka_event)
     

    return JSONResponse(
            status_code=201,
            content={"user_name":firstname,"email":email}
        )



# @app.post("/auth/register/send-otp")
# def create_user(User_details: UserSignUp,db:Session = Depends(get_db)):
#     user=db.query(User).filter(User.email==User_details.email).first()
     
#     if user:
#         raise HTTPException(status_code=400, detail="User Already Exists")

#     otp = str(random.randint(1000, 9999))
    

#     # Save flattened data
#     temp_data = {
#         "otp": otp,
#         "firstname": User_details.firstname,
#         "lastname": User_details.lastname,
#         "email": User_details.email,
#         "phone": User_details.phone,
#         "password": User_details.password
#     }
    
#     print(f"GENERATED OTP: {otp}", flush=True)
#     # Save to Redis (expires in 300s)
#     res.set(User_details.email, json.dumps(temp_data), ex=300)
#     print(f"GENERA OTP: {otp}", flush=True)
#     # --- FIX 1: Structure payload correctly for Router ---
#     kafka_payload = {
#         "event_type": "CHECK_OTP",
#         "data": temp_data # Router expects 'data' key
#     }
#     producer.send('user_events', value=kafka_payload)
    
#     return {"message": "OTP Sent Successfully, Please Check Your Email"}



# @app.post("/auth/register/verify-otp")
# def register_verify_otp(payload: VerifyOtpSchema,db:Session = Depends(get_db)):
#     stored_data_json = res.get(payload.email)
    
#     if not stored_data_json:
#         raise HTTPException(status_code=400, detail="Invalid OTP or Time Expired")
    
#     stored_data = json.loads(stored_data_json)

#     if stored_data["otp"] != payload.otp:
#         raise HTTPException(status_code=400, detail="Invalid OTP")
    
#     # --- FIX 2: stored_data IS the user info, no ["user_info"] key ---
#     new_user_info = stored_data
    
#     user_id = random.randint(1, 10000)
#     new_user_info["User_id"] = user_id
    
#     # Remove OTP from final user record
#     del new_user_info["otp"]
    
#     new_password=get_pass_hash(new_user_info["password"])
#     new_user=User(user_id=user_id,firstname=new_user_info["firstname"],lastname=new_user_info["lastname"],
#          email=new_user_info["email"],phone=new_user_info["phone"],password=new_password)
    
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     res.delete(payload.email)

#     # --- FIX 3: Match Topic and Event Type to Router ---
#     event_data = {
#         "event_type": "USER_CREATED", # Matches Router TEMPLATE_MAP
#         "data": {
#             "firstname": new_user_info["firstname"],
#             "email": new_user_info["email"],
#             "phone": new_user_info.get("phone")
#         }
#     }
    
#     # Send to 'user.events' (Router listens here), not 'platform_notifications'
#     producer.send('user_events', value=event_data)
#     producer.flush() 

#     return {"message": "User created successfully", "user_id": user_id}

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





@router.post("/forgot_password")
def forgot_password(forgot_details:Forgot_Details,db:Session = Depends(get_db)):
    user=db.query(User).filter(User.email==forgot_details.email).first()
     
    if not user:
        raise HTTPException(status_code=400, detail="User does not Exists")

    otp = str(random.randint(1000, 9999))
    print(f"GENERATED OTP: {otp}", flush=True)

    # Save flattened data
    temp_data = {
        "otp": otp,
         "email": forgot_details.email,
         "firstname":"string"
         
    }
     
     
    res.set(forgot_details.email, json.dumps(temp_data), ex=300)

     
    kafka_payload = {
        "event_type": "FORGOT_PASSWORD",
        "data": temp_data # Router expects 'data' key
    }
    producer.send('user_events', value=kafka_payload)
    
    return {"message": "OTP Sent Successfully, Please Check Your Email"}



@router.post("/forgot/verify-otp")
def verify_otp(payload: VerifyOtpSchema,db:Session=Depends(get_db)):
    stored_data_json = res.get(payload.email)
    
    if not stored_data_json:
        raise HTTPException(status_code=400, detail="Invalid OTP or Time Expired")
    
    stored_data = json.loads(stored_data_json)
    print(stored_data)

    if stored_data["otp"] != payload.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    
    
    # Generate random password
    alphabet = string.ascii_letters + string.digits
    new_password = ''.join(secrets.choice(alphabet) for i in range(12))
    print(f'New Password is: {new_password}',flush=True)
    
    # FIXED: Update user password in database
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.password = get_pass_hash(new_password)
    db.commit()
     
     
    
     
     
    res.delete(payload.email)

    # --- FIX 3: Match Topic and Event Type to Router ---
    event_data = {
        "event_type": "NEW_PASSWORD", # Matches Router TEMPLATE_MAP
        "data": {
            "firstname":  stored_data['firstname'],
            "email":  stored_data['email'],
            "new_password":new_password
             
        }
    }
    
    # Send to 'user.events' (Router listens here), not 'platform_notifications'
    producer.send('user_events', value=event_data)
    producer.flush() 

    return {"Status": "Password updated and Sent"}
