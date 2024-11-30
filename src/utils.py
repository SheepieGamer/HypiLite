import aiohttp
from fastapi import HTTPException
from fastapi import status
from datetime import datetime
import time

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
            return data.get("name", "not found")

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

async def get_uuid(username: str):
    ts = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}?at={ts}") as resp:
            if resp.status != 200:
                return "not found"
            data = await resp.json()
            uuid = data["id"]
            return uuid

async def get_user(uuid: str, token: str):
    """Get user data from Hypixel API"""
    uuid = uuid.strip("-")

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.hypixel.net/v2/player?key={token}&uuid={uuid}") as resp:
            if resp.status != 200:
                return None
            data = await resp.json()
            if not data.get("success", False):
                return None
            return data


# Bedwars Functions

class BedWarsXP:
    # Constants
    EASY_LEVELS = 4
    EASY_LEVELS_XP = [500, 1000, 2000, 3500]
    EASY_LEVELS_XP_TOTAL = sum(EASY_LEVELS_XP)
    XP_PER_LEVEL = 5000
    XP_PER_PRESTIGE = 96 * XP_PER_LEVEL + EASY_LEVELS_XP_TOTAL
    LEVELS_PER_PRESTIGE = 100
    HIGHEST_PRESTIGE = 10  # Example highest prestige, adjust as necessary.

    @classmethod
    def calculate_star(cls, exp):
        """
        Main method to calculate the BedWars star (level as a float rounded to 3 decimals)
        and prestige for a given XP.
        """
        level = cls.get_level_for_exp(exp)
        prestige = cls.get_prestige_for_exp(exp)
        return level, prestige

    @classmethod
    def get_prestige_for_exp(cls, exp):
        level = cls.get_level_for_exp(exp)
        return cls.get_prestige_for_level(level)

    @classmethod
    def get_prestige_for_level(cls, level):
        prestige = level // cls.LEVELS_PER_PRESTIGE
        return min(prestige, cls.HIGHEST_PRESTIGE)

    @classmethod
    def get_level_for_exp(cls, exp):
        # Calculate full prestiges
        prestiges = exp // cls.XP_PER_PRESTIGE
        level = prestiges * cls.LEVELS_PER_PRESTIGE

        # Remaining XP after accounting for full prestiges
        exp_without_prestiges = exp % cls.XP_PER_PRESTIGE

        # Process easy levels
        for i in range(1, cls.EASY_LEVELS + 1):
            exp_for_easy_level = cls.get_exp_for_level(i)
            if exp_without_prestiges < exp_for_easy_level:
                break
            level += 1
            exp_without_prestiges -= exp_for_easy_level

        # Add fractional levels from standard XP
        level += exp_without_prestiges / cls.XP_PER_LEVEL
        return round(level, 3)  # Round to 3 decimal places

    @classmethod
    def get_exp_for_level(cls, level):
        if level == 0:
            return 0

        respected_level = cls.get_level_respecting_prestige(level)
        if respected_level <= cls.EASY_LEVELS:
            return cls.EASY_LEVELS_XP[respected_level - 1]
        return cls.XP_PER_LEVEL

    @classmethod
    def get_level_respecting_prestige(cls, level):
        if level > cls.HIGHEST_PRESTIGE * cls.LEVELS_PER_PRESTIGE:
            return level - cls.HIGHEST_PRESTIGE * cls.LEVELS_PER_PRESTIGE
        return level % cls.LEVELS_PER_PRESTIGE

    @classmethod
    def get_xp_to_next_level(cls, exp):
        """
        Calculates the amount of XP needed to reach the next level from the current XP.
        """
        current_level = cls.get_level_for_exp(exp)
        next_level = int(current_level) + 1  # Calculate the next whole level
        xp_for_current_level = cls.get_total_xp_for_level(current_level)
        xp_for_next_level = cls.get_total_xp_for_level(next_level)
        return max(0, xp_for_next_level - exp)  # Ensure it's non-negative

    @classmethod
    def get_total_xp_for_level(cls, level):
        """
        Calculates the total cumulative XP required to reach a specific level.
        """
        prestiges = int(level // cls.LEVELS_PER_PRESTIGE)
        levels_within_prestige = int(level % cls.LEVELS_PER_PRESTIGE)
        
        # Total XP from full prestiges
        xp = prestiges * cls.XP_PER_PRESTIGE

        # Add XP for levels within the current prestige
        for i in range(1, levels_within_prestige + 1):
            xp += cls.get_exp_for_level(i)

        # Add fractional XP if level is not an integer
        fractional_level = level - int(level)
        if fractional_level > 0:
            xp += fractional_level * cls.XP_PER_LEVEL

        return xp

    @classmethod
    def get_progress_through_level(cls, exp):
        """
        Calculates how far through their current level the user is as a percentage.
        """
        current_level = cls.get_level_for_exp(exp)
        xp_for_current_level = cls.get_total_xp_for_level(int(current_level))
        xp_for_next_level = cls.get_total_xp_for_level(int(current_level) + 1)

        # Progress percentage
        progress = ((exp - xp_for_current_level) / (xp_for_next_level - xp_for_current_level)) * 100
        return float(round(progress, 4))  # Round to 2 decimal places

def get_level_info(exp):
    level, prestige = BedWarsXP.calculate_star(exp)
    xp_to_next_level = BedWarsXP.get_xp_to_next_level(exp)
    progress_percentage = BedWarsXP.get_progress_through_level(exp)
    return level, prestige, xp_to_next_level, progress_percentage





async def fetch_xp(uuid: str, token: str):
    uuid = uuid.strip("-")
    data = await get_user(uuid, token)
    # if not data or "player" not in data:
    #     return None

    try:
        xp = data["player"]["stats"]["BedWars"]["Experience"]
        return xp
    except KeyError:
        return None
