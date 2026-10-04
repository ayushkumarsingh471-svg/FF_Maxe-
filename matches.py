from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/matches")

class JoinRequest(BaseModel):
    user_id: str
    match_id: str

@router.get("/list")
async def get_matches(request: Request):
    supabase = request.app.state.supabase
    # Saare matches fetch karo UI me dikhane ke liye
    response = supabase.table('matches').select('*').execute()
    return response.data

@router.post("/join")
async def join_match(payload: JoinRequest, request: Request):
    supabase = request.app.state.supabase
    
    try:
        supabase.table('registrations').insert({
            "user_id": payload.user_id,
            "match_id": payload.match_id
        }).execute()
        return {"success": True, "message": "Match successfully join ho gaya!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail="Aapne pehle se join kiya hai ya koi error aayi.")

@router.get("/{match_id}/room-details")
async def get_room_details(match_id: str, user_id: str, request: Request):
    supabase = request.app.state.supabase
    
    # Check karo ki user registrations table me hai ya nahi
    reg = supabase.table('registrations').select('*').eq('match_id', match_id).eq('user_id', user_id).execute()
    
    if not reg.data:
        return {"success": False, "error": "Aapne ye match join nahi kiya hai. ID/Pass hidden hai."}
        
    match = supabase.table('matches').select('room_id, room_password').eq('id', match_id).execute()
    if match.data:
        return {"success": True, "data": match.data[0]}
    
    return {"success": False, "error": "Match nahi mila"}