from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import aiohttp
import math
from utils import get_rank, get_username, format_timestamp

app = FastAPI(
    docs_url="/swagger_docs",
    redoc_url="/docs",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/api/uuid/{username}")
async def get_uuid(username: str):
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 204:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Player not found"
                )
            elif resp.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Mojang API error"
                )
            
            data = await resp.json()
            return {
                "success": True,
                "data": {
                    "uuid": data.get("id"),
                    "username": data.get("name")
                }
            }

@app.get("/api/profile/{uuid}")
async def get_profile(uuid: str, api_key: str):
    uuid = str(uuid).replace("-", "")
    url = f"https://api.hypixel.net/v2/player?uuid={uuid}"
    headers = {"API-Key": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            data = await resp.json()
            
            if resp.status == 401 or data == {"success": False, "cause": "Invalid API key"}:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key"
                )
            elif resp.status == 422 or data == {"success":False,"cause":"Malformed UUID"}:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid UUID"
                )
            elif resp.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Hypixel API error"
                )

    if not data.get("success", False):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player not found"
        )

    player_data = data.get("player", {})
    if not player_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player data not found"
        )

    # Get player username
    username = await get_username(uuid)
    rank = await get_rank(uuid, data)

    # Get timestamps
    first_login = player_data.get("firstLogin", 0)
    last_login = player_data.get("lastLogin", 0)
    last_logout = player_data.get("lastLogout", 0)
    
    return {
        "success": True,
        "data": {
            "uuid": uuid,
            "username": username,
            "rank": rank,
            "first_login": first_login,
            "first_login_pretty": format_timestamp(first_login),
            "last_login": last_login,
            "last_login_pretty": format_timestamp(last_login),
            "last_logout": last_logout,
            "last_logout_pretty": format_timestamp(last_logout),
            "exp": player_data.get("networkExp", 0),
            "network_level": round((math.sqrt((2 * player_data.get("networkExp", 0)) + 30625) / 50) - 2.5, 2),
            "karma": player_data.get("karma", 0),
            "achievement_points": player_data.get("achievementPoints", 0),
            "total_rewards": player_data.get("totalRewards", 0),
            "total_daily_rewards": player_data.get("totalDailyRewards", 0),
            "reward_streak": player_data.get("rewardStreak", 0),
            "reward_score": player_data.get("rewardScore", 0),
            "reward_high_score": player_data.get("rewardHighScore", 0),
            "most_recent_game": player_data.get("mostRecentGameType", "unknown"),
            "online": player_data.get("lastLogin", 0) > player_data.get("lastLogout", 0),
            "images": {
                "full_skin_image": f"https://crafatar.com/renders/body/{uuid}",
                "3d_head_image": f"https://crafatar.com/renders/head/{uuid}",
                "2d_head_image": f"https://crafatar.com/avatars/{uuid}",
                "network_level_image": f"https://gen.plancke.io/exp/{username}.png",
            }
        }
    }

@app.get("/api/guild/{uuid}")
async def get_guild(uuid: str, api_key: str):
    uuid = str(uuid).replace("-", "")
    url = f"https://api.hypixel.net/v2/guild?player={uuid}"
    headers = {"API-Key": api_key}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            guild_data = await resp.json()
            
            if resp.status == 401 or guild_data == {"success": False, "cause": "Invalid API key"}:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid API key"
                )
            elif resp.status == 422 or guild_data == {"success":False,"cause":"Malformed UUID"}:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid UUID"
                )
            elif resp.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Hypixel API error"
                )

    # Process Guild Data
    guild = guild_data.get("guild")
    if not guild:
        return {
            "success": True,
            "data": {
                "in_guild": False
            }
        }

    # Get player username
    username = await get_username(uuid)

    # Get timestamps
    created = guild.get("created", 0)

    guild_info = {
        "uuid": uuid,
        "username": username,
        "in_guild": True,
        "name": guild.get("name", "not found"),
        "tag": guild.get("tag", "not found"),
        "tag_color": guild.get("tagColor", "not found"),
        "exp": guild.get("exp", 0),
        "created": created,
        "created_pretty": format_timestamp(created)
    }
    
    # Process Guild Members
    guild_members = guild.get("members", [])
    formatted_members = []
    current_member_data = {}

    for member in guild_members:
        member_uuid = member.get("uuid")
        if not member_uuid:
            continue

        # Get member username
        try:
            member_username = await get_username(member_uuid)
        except:
            member_username = "Unknown"

        # Get timestamps
        joined = member.get("joined", 0)

        member_info = {
            "uuid": member_uuid,
            "username": member_username,
            "joined": joined,
            "joined_pretty": format_timestamp(joined),
            "quests": member.get("questParticipation", 0),
            "rank": member.get("rank", "not found"),
            "weekly_exp": member.get("expHistory", {}).get("weekly", 0),
            "daily_exp": member.get("expHistory", {}).get("daily", 0),
            "role": member.get("role", "not found")
        }
        formatted_members.append(member_info)
        
        if member_uuid == uuid:
            current_member_data = member

    # Get timestamps for current member
    joined = current_member_data.get("joined", 0)

    # Add member data to guild info
    guild_info.update({
        "quests": current_member_data.get("quests", 0),
        "joined": joined,
        "joined_pretty": format_timestamp(joined),
        "weekly_exp": current_member_data.get("weekly_exp", 0),
        "daily_exp": current_member_data.get("daily_exp", 0),
        "role": current_member_data.get("role", "not found"),
        "members": formatted_members
    })

    return {
        "success": True,
        "data": guild_info
    }