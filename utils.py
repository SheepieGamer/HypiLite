import aiohttp
from fastapi import HTTPException
from fastapi import status
from datetime import datetime

async def get_rank(uuid: str, data: dict):
    uuid = str(uuid).strip("-")
    if not data or "player" not in data:
        return ""

    player = data["player"]
    
    try:
        if player.get("prefix"):
            prefix = player["prefix"]
            while "§" in prefix:
                idx = prefix.index("§")
                prefix = prefix[:idx] + prefix[idx+2:]
            return prefix.strip().strip("[").strip("]") # example output: "PIG+++", "OWNER"
        if player.get("rank"):
            return player["rank"] # example output: "YOUTUBE"
        
        # MVP++ and MVP+
        if player.get("monthlyPackageRank") == "SUPERSTAR":
            return "MVP++"
        elif player.get("monthlyPackageRank") == "NONE" and player.get("newPackageRank") == "MVP_PLUS":
            return "MVP+"
    except: 
        pass

    # The rest of the ranks
    try:
        rank = player.get("newPackageRank", "")
        if rank == "MVP_PLUS":
            return "MVP+"
        elif rank == "MVP":
            return "MVP"
        elif rank == "VIP_PLUS":
            return "VIP+"
        elif rank == "VIP":
            return "VIP"
    except:
        pass

    return "NONE"

async def get_username(uuid: str) -> str:
    """Convert a Minecraft UUID to username using Mojang API.
    
    Args:
        uuid (str): The UUID to convert (with or without dashes)
    
    Returns:
        str: The username associated with the UUID
        
    Raises:
        HTTPException: If the UUID is invalid or the API request fails
    """
    # Remove dashes from UUID if present
    uuid = str(uuid).replace("-", "")
    
    # Mojang API endpoint
    url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 204:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Player not found"
                )
            elif resp.status == 400:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Invalid UUID format"
                )
            elif resp.status != 200:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Mojang API error"
                )
            
            data = await resp.json()
            return data.get("name", "Unknown")

def format_timestamp(timestamp: int) -> str:
    """Convert a Unix timestamp (milliseconds) to a human-readable date and time.
    
    Args:
        timestamp (int): Unix timestamp in milliseconds
    
    Returns:
        str: Formatted date and time string (e.g., "2023-12-25 15:30:45")
    """
    if not timestamp:
        return "Never"
    try:
        # Convert milliseconds to seconds for datetime
        dt = datetime.fromtimestamp(timestamp / 1000)
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except:
        return "Invalid timestamp"
