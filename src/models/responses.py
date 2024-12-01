from pydantic import BaseModel, Field, create_model
from typing import Dict, List, Optional, Any

class PlayerUUIDData(BaseModel):
    uuid: str
    username: str

class PlayerUUIDResponse(BaseModel):
    success: bool
    data: PlayerUUIDData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "uuid": "0937b604c1ce446a96ff818d752a19f6",
                    "username": "sheepie20"
                }
            }
        }

class GuildMemberInfo(BaseModel):
    uuid: str
    username: str
    joined: int
    joined_pretty: str
    quests: int
    rank: str
    weekly_exp: int
    daily_exp: int
    role: str

class GuildData(BaseModel):
    uuid: str
    username: str
    in_guild: bool
    name: str
    tag: Optional[str]
    tag_color: Optional[str]
    exp: int
    created: int
    created_pretty: str
    quests: int
    joined: int
    joined_pretty: str
    weekly_exp: int
    members: List[GuildMemberInfo]

class GuildResponse(BaseModel):
    success: bool
    data: GuildData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "uuid": "0937b604c1ce446a96ff818d752a19f6",
                    "username": "sheepie20",
                    "in_guild": True,
                    "name": "TheWaffleCult",
                    "tag": "WAFFLE",
                    "tag_color": "GOLD",
                    "exp": 19606242,
                    "created": 1715983620704,
                    "created_pretty": "2024-05-17 22:07:00",
                    "quests": 0,
                    "joined": 1719092290705,
                    "joined_pretty": "2024-06-22 21:38:10",
                    "weekly_exp": 0,
                    "members": [{
                        "uuid": "0937b604c1ce446a96ff818d752a19f6",
                        "username": "sheepie20",
                        "joined": 1719092290705,
                        "joined_pretty": "2024-06-22 21:38:10",
                        "quests": 0,
                        "rank": "Member",
                        "weekly_exp": 0,
                        "daily_exp": 0,
                        "role": "Member"
                    }]
                }
            }
        }

class PlayerImages(BaseModel):
    full_skin_image: str
    three_d_head_image: str = Field(alias="3d_head_image")
    two_d_head_image: str = Field(alias="2d_head_image")
    network_level_image: str

class PlayerProfileData(BaseModel):
    uuid: str
    username: str
    rank: str
    first_login: int
    first_login_pretty: str
    last_login: int
    last_login_pretty: str
    last_logout: int
    last_logout_pretty: str
    exp: int
    network_level: float
    karma: int
    achievement_points: int
    total_rewards: int
    total_daily_rewards: int
    reward_streak: int
    reward_score: int
    reward_high_score: int
    most_recent_game: str
    online: bool
    images: PlayerImages

    class Config:
        allow_population_by_field_name = True

class PlayerProfileResponse(BaseModel):
    success: bool
    data: PlayerProfileData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "uuid": "0937b604c1ce446a96ff818d752a19f6",
                    "username": "sheepie20",
                    "rank": "MVP+",
                    "first_login": 1591626420000,
                    "first_login_pretty": "2020-06-08 14:27:00",
                    "last_login": 1732925161165,
                    "last_login_pretty": "2024-11-30 00:06:01",
                    "last_logout": 1732925713703,
                    "last_logout_pretty": "2024-11-30 00:15:13",
                    "exp": 14533931,
                    "network_level": 105.39,
                    "karma": 2456542,
                    "achievement_points": 4645,
                    "total_rewards": 18,
                    "total_daily_rewards": 10,
                    "reward_streak": 1,
                    "reward_score": 1,
                    "reward_high_score": 6,
                    "most_recent_game": "BEDWARS",
                    "online": False,
                    "images": {
                        "full_skin_image": "https://crafatar.com/renders/body/0937b604c1ce446a96ff818d752a19f6",
                        "3d_head_image": "https://crafatar.com/renders/head/0937b604c1ce446a96ff818d752a19f6",
                        "2d_head_image": "https://crafatar.com/avatars/0937b604c1ce446a96ff818d752a19f6",
                        "network_level_image": "https://gen.plancke.io/exp/sheepie20.png"
                    }
                }
            }
        }

class BedwarsResources(BaseModel):
    tokens: int
    slumber_tickets: int
    slumber_tickets_max: int
    slumber_tickets_total: int

class BedwarsGameModeStats(BaseModel):
    emeralds: int
    diamonds: int
    gold: int
    iron: int
    wins: int
    losses: int
    final_kills: int
    final_deaths: int
    kills: int
    deaths: int
    beds_broken: int
    beds_lost: int
    wlr: float
    kdr: float
    fkdr: float
    bblr: float

class OverallStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"overall_{field}"

class CoreStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"core_{field}"

class EightOneStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_one_{field}"

class EightTwoStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_two_{field}"

class FourThreeStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_three_{field}"

class FourFourStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_{field}"

class TwoFourStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"two_four_{field}"

class FourFourArmedStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_armed_{field}"

class CastleStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"castle_{field}"

class FourFourLuckyStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_lucky_{field}"

class EightTwoLuckyStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_two_lucky_{field}"

class EightTwoRushStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_two_rush_{field}"

class FourFourRushStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_rush_{field}"

class EightTwoSwapStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_two_swap_{field}"

class FourFourSwapStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_swap_{field}"

class EightTwoUltimateStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"eight_two_ultimate_{field}"

class FourFourUltimateStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_ultimate_{field}"

class FourFourUnderworldStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_underworld_{field}"

class FourFourVoidlessStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"four_four_voidless_{field}"

class UltimateStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"ultimate_{field}"

class LuckyStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"lucky_{field}"

class RushStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"rush_{field}"

class SwapStats(BedwarsGameModeStats):
    class Config:
        alias_generator = lambda field: f"swap_{field}"

class BedwarsStats(BaseModel):
    overall: Optional[OverallStats] = None
    core: Optional[CoreStats] = None
    eight_one: Optional[EightOneStats] = None
    eight_two: Optional[EightTwoStats] = None
    four_three: Optional[FourThreeStats] = None
    four_four: Optional[FourFourStats] = None
    two_four: Optional[TwoFourStats] = None
    four_four_armed: Optional[FourFourArmedStats] = None
    castle: Optional[CastleStats] = None
    four_four_lucky: Optional[FourFourLuckyStats] = None
    eight_two_lucky: Optional[EightTwoLuckyStats] = None
    eight_two_rush: Optional[EightTwoRushStats] = None
    four_four_rush: Optional[FourFourRushStats] = None
    eight_two_swap: Optional[EightTwoSwapStats] = None
    four_four_swap: Optional[FourFourSwapStats] = None
    eight_two_ultimate: Optional[EightTwoUltimateStats] = None
    four_four_ultimate: Optional[FourFourUltimateStats] = None
    four_four_underworld: Optional[FourFourUnderworldStats] = None
    four_four_voidless: Optional[FourFourVoidlessStats] = None
    ultimate: Optional[UltimateStats] = None
    lucky: Optional[LuckyStats] = None
    rush: Optional[RushStats] = None
    swap: Optional[SwapStats] = None

    class Config:
        json_schema_extra = {
            "example": {
                "overall": {
                    "emeralds": 3711,
                    "diamonds": 12764,
                    "gold": 90182,
                    "iron": 675401,
                    "wins": 520,
                    "losses": 2521,
                    "final_kills": 2157,
                    "final_deaths": 2518,
                    "kills": 5284,
                    "deaths": 9925,
                    "beds_broken": 1433,
                    "beds_lost": 2547,
                    "wlr": 0.21,
                    "kdr": 0.53,
                    "fkdr": 0.86,
                    "bblr": 0.56
                },
                "core": {
                    "emeralds": 3678,
                    "diamonds": 12748,
                    "gold": 88632,
                    "iron": 653675,
                    "wins": 403,
                    "losses": 2499,
                    "final_kills": 2043,
                    "final_deaths": 2491,
                    "kills": 5002,
                    "deaths": 9548,
                    "beds_broken": 1401,
                    "beds_lost": 2520,
                    "wlr": 0.16,
                    "kdr": 0.52,
                    "fkdr": 0.82,
                    "bblr": 0.56
                },
                "eight_one": {
                    "emeralds": 549,
                    "diamonds": 2511,
                    "gold": 15682,
                    "iron": 128322,
                    "wins": 77,
                    "losses": 399,
                    "final_kills": 509,
                    "final_deaths": 398,
                    "kills": 658,
                    "deaths": 1153,
                    "beds_broken": 567,
                    "beds_lost": 425,
                    "wlr": 0.19,
                    "kdr": 0.57,
                    "fkdr": 1.28,
                    "bblr": 1.33
                }
            }
        }

class BedwarsData(BaseModel):
    uuid: str
    username: str
    xp: int
    level: float
    prestige: int
    next_level: int
    xp_to_next_level: int
    progress_to_next_level_percentage: int
    resources: BedwarsResources
    stats: BedwarsStats

class BedwarsResponse(BaseModel):
    success: bool
    data: BedwarsData

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": {
                    "uuid": "0937b604c1ce446a96ff818d752a19f6",
                    "username": "sheepie20",
                    "xp": 1025150,
                    "level": 212.83,
                    "prestige": 2,
                    "next_level": 213,
                    "xp_to_next_level": 850,
                    "progress_to_next_level_percentage": 83,
                    "resources": {
                        "tokens": 1101235,
                        "slumber_tickets": 8221,
                        "slumber_tickets_max": 100000,
                        "slumber_tickets_total": 81439
                    },
                    "stats": {
                        "overall": {
                            "emeralds": 3711,
                            "diamonds": 12764,
                            "gold": 90182,
                            "iron": 675401,
                            "wins": 520,
                            "losses": 2521,
                            "final_kills": 2157,
                            "final_deaths": 2518,
                            "kills": 5284,
                            "deaths": 9925,
                            "beds_broken": 1433,
                            "beds_lost": 2547,
                            "wlr": 0.21,
                            "kdr": 0.53,
                            "fkdr": 0.86,
                            "bblr": 0.56
                        },
                        "core": {
                            "emeralds": 3678,
                            "diamonds": 12748,
                            "gold": 88632,
                            "iron": 653675,
                            "wins": 403,
                            "losses": 2499,
                            "final_kills": 2043,
                            "final_deaths": 2491,
                            "kills": 5002,
                            "deaths": 9548,
                            "beds_broken": 1401,
                            "beds_lost": 2520,
                            "wlr": 0.16,
                            "kdr": 0.52,
                            "fkdr": 0.82,
                            "bblr": 0.56
                        },
                        "eight_one": {
                            "emeralds": 549,
                            "diamonds": 2511,
                            "gold": 15682,
                            "iron": 128322,
                            "wins": 77,
                            "losses": 399,
                            "final_kills": 509,
                            "final_deaths": 398,
                            "kills": 658,
                            "deaths": 1153,
                            "beds_broken": 567,
                            "beds_lost": 425,
                            "wlr": 0.19,
                            "kdr": 0.57,
                            "fkdr": 1.28,
                            "bblr": 1.33
                        }
                    }
                }
            }
        }

class ErrorResponse(BaseModel):
    detail: str

    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Player not found"
            }
        }
