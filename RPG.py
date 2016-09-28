from .DeathMatch import DeathMatch
import random

import GEEntity
import GEGlobal
import GEMPGameRules
import GEPlayer
import GEUtil
import GEWeapon
import Utils

# API Version
USING_API = GEGlobal.API_VERSION_1_1_1

# Stats & Money
Level = []
XP = []
StatPoints = []
LevelHealth = []
LevelArmor = []
LevelAttack = []
Money = []

# Combo
Combo = []
ComboTimer = []

# Weapons
CurrentWeapon = []
Weapons = []
Headshot = []

# Loot Suitcase
LootToken = "token_janus"
LootTokenActive = False

# Spectator
Viewing = []

# ----------------------------------------------------------------------------------------------------
# 
# Tables
# 
# ----------------------------------------------------------------------------------------------------

# Weapon List
WeaponList = [
   # Class Name                 Nice Name            Price  Ammo
    
    ("weapon_knife",            "Hunting Knife",     250,   1  ),
    ("weapon_knife_throwing",   "Throwing Knife",    200,   10 ),
    ("weapon_pp7",              "PP7",               100,   100),
    ("weapon_pp7_silenced",     "PP7 (Silenced)",    100,   100),
    ("weapon_dd44",             "DD44",              200,   100),
    ("weapon_klobb",            "Klobb",             100,   100),
    ("weapon_kf7",              "KF7 Soviet",        500,   100),
    ("weapon_zmg",              "ZMG",               1000,  100),
    ("weapon_d5k",              "D5K",               500,   100),
    ("weapon_d5k_silenced",     "D5K (Silenced)",    500,   100),
    ("weapon_phantom",          "Phantom",           750,   100),
    ("weapon_ar33",             "AR-33",             1000,  100),
    ("weapon_rcp90",            "RCP-90",            5000,  100),
    ("weapon_auto_shotgun",     "Automatic Shotgun", 2500,  20 ),
    ("weapon_shotgun",          "Shotgun",           2000,  20 ),
    ("weapon_sniper_rifle",     "Sniper Rifle",      1000,  20 ),
    ("weapon_cmag",             "Cougar Magnum",     2000,  36 ),
    ("weapon_golden_gun",       "Golden Gun",        10000, 10 ),
    ("weapon_silver_pp7",       "Silver PP7",        5000,  100),
    ("weapon_golden_pp7",       "Gold PP7",          50000, 100),
    ("weapon_moonraker",        "Moonraker Laser",   10000, 1  ),
    ("weapon_grenade_launcher", "Grenade Launcher",  7500,  12 ),
    ("weapon_rocket_launcher",  "Rocket Launcher",   5000,  5  ),
    ("weapon_grenade",          "Grenades",          1000,  12 ),
    ("weapon_timedmine",        "Timed Mines",       1000,  10 ),
    ("weapon_proximitymine",    "Proximity Mines",   2000,  10 ),
    ("weapon_remotemine",       "Remote Mines",      2000,  10 )
]

# Weapon Bonuses
WeaponBonus = [
   # Class Name                 Bonus
    
    ("weapon_slappers",         100),
    ("weapon_knife",            100),
    ("weapon_knife_throwing",   200),
    ("weapon_golden_gun",       200),
    ("weapon_grenade_launcher", 50 ),
    ("weapon_rocket_launcher",  50 ),
    ("weapon_grenade",          50 ),
    ("weapon_timedmine",        50 ),
    ("weapon_proximitymine",    50 ),
    ("weapon_remotemine",       50 )
]

# Ammo Amounts
Ammo = [
   # Ammo Name        Nice Name          Price Amount
    
    ("throwingknife", "Throwing Knives", 100,  10 ),
    ("9mm",           "9mm Ammo",        100,  100),
    ("rifle",         "Rifle Ammo",      250,  100),
    ("buckshot",      "Buckshot Ammo",   250,  20 ),
    ("magnum",        "Magnum Ammo",     500,  36 ),
    ("goldenammo",    "Golden Ammo",     1000, 10 ),
    ("shells",        "Grenade Shells",  1000, 12 ),
    ("rockets",       "Rockets",         1000, 5  ),
    ("grenades",      "Grenades",        500,  12 ),
    ("timedmine",     "Timed Mines",     1000, 10 ),
    ("proximitymine", "Proximity Mines", 2000, 10 ),
    ("remotemine",    "Remote Mines",    2000, 10 )
]

# ----------------------------------------------------------------------------------------------------
# 
# Constants
# 
# ----------------------------------------------------------------------------------------------------

# General
MAX_PLAYERS = 64
LEVEL_BASE = 100
MONEY_START = 10
COMBO_MAX = 30
LOOT_CHANCE = 5000

# Costs
HEALTH_COST = 1000
ARMOR_COST = 500

# Stat Types
STAT_HEALTH = 1
STAT_ARMOR = 2
STAT_ATTACK = 3

# Stat Rates
HEALTH_START = 100
HEALTH_INCREASE = 50
ARMOR_START = 100
ARMOR_INCREASE = 25
ATTACK_INCREASE = 0.25

# Colors
COLOR_NORMAL =          GEUtil.Color(255, 255, 255, 255)
COLOR_ERROR =           GEUtil.Color(255, 0,   0,   255)
COLOR_XP =              GEUtil.Color(255, 255, 0,   255)
COLOR_MONEY =           GEUtil.Color(32,  255, 32,  255)
COLOR_LOOT =            GEUtil.Color(32,  255, 32,  255)
COLOR_HEALTH =          GEUtil.Color(255, 32,  32,  255)
COLOR_ARMOR =           GEUtil.Color(32,  128, 255, 255)
COLOR_ATTACK =          GEUtil.Color(255, 128, 32,  255)
COLOR_WEAPON =          GEUtil.Color(192, 64,  192, 255)
COLOR_AMMO =            GEUtil.Color(96,  64,  160, 255)

# Channels
CHANNEL_STATS = 1
CHANNEL_WEAPON = 2
CHANNEL_GAIN = 3
CHANNEL_MESSAGE = 4

# Bars
BAR_HEALTH = 1
BAR_ARMOR = 2
BAR_COMBO = 3

class RPG(DeathMatch):
    # ----------------------------------------------------------------------------------------------------
    # 
    # Constructor
    # 
    # ----------------------------------------------------------------------------------------------------
    
    def __init__(self):
        super(RPG, self).__init__()
        
        for i in range(0, MAX_PLAYERS):
            Level.append(0)
            XP.append(0)
            StatPoints.append(0)
            LevelHealth.append(0)
            LevelArmor.append(0)
            LevelAttack.append(0)
            Money.append(0)
            CurrentWeapon.append(-1)
            Weapons.append([])
            Headshot.append(False)
            Combo.append(0)
            ComboTimer.append(0)
            Viewing.append(-1)
    
    # ----------------------------------------------------------------------------------------------------
    # 
    # Functions
    # 
    # ----------------------------------------------------------------------------------------------------

    # Get XP to next Level
    def LevelNext(self, id):
        players = GEMPGameRules.GetNumActivePlayers()
        return int((LEVEL_BASE * players) + ((Level[id] * LEVEL_BASE) * (1.0 + (Level[id] * 0.25))) * players)
    
    # Level Up
    def LevelUp(self, player):
        id = player.GetPlayerID()
        Level[id] += 1
        StatPoints[id] += 1
        GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| is now Level {1}".format(player.GetPlayerName(), Level[id]))
        GEUtil.PlaySoundTo(player, "GEGamePlay.Token_Grab", True)
    
    def IncreaseStat(self, player, type):
        id = player.GetPlayerID()
        
        if StatPoints[id] == 0:
            return
        
        if type == STAT_HEALTH:
            LevelHealth[id] += 1
            player.SetMaxHealth(HEALTH_START + LevelHealth[id] * HEALTH_INCREASE)
            player.SetHealth(player.GetHealth() + HEALTH_INCREASE)
            GEUtil.HudMessage(player, "^rHealth increased!^|", -1, 0.7, COLOR_NORMAL, 2, CHANNEL_MESSAGE)
            self.CreateHUD(player)
        elif type == STAT_ARMOR:
            LevelArmor[id] += 1
            player.SetMaxArmor(ARMOR_START + LevelArmor[id] * ARMOR_INCREASE)
            GEUtil.HudMessage(player, "^iArmor increased!^|", -1, 0.7, COLOR_NORMAL, 2, CHANNEL_MESSAGE)
            self.CreateHUD(player)
        elif type == STAT_ATTACK:
            LevelAttack[id] += 1
            player.SetDamageMultiplier(1.0 + (LevelAttack[id] * ATTACK_INCREASE))
            GEUtil.HudMessage(player, "^dDamage increased!^|", -1, 0.7, COLOR_NORMAL, 2, CHANNEL_MESSAGE)
        
        GEUtil.PlaySoundTo(None, "GEGamePlay.Token_Drop_Enemy", True)
        StatPoints[id] -= 1
    
    # Get current damage of the weapon with Level taken into account
    def GetWeaponDamage(self, player):
        weapon = player.GetActiveWeapon()
        if not weapon:
            return 0
        return weapon.GetDamage() * (1.0 + (LevelAttack[player.GetPlayerID()] * ATTACK_INCREASE))
    
    # Check to make sure you have enough money for a purchase
    def CheckMoney(self, player, amount):
        id = player.GetPlayerID()
        if Money[id] >= amount:
            Money[id] -= amount
            return True
        else:
            GEUtil.HudMessage(player, "Not Enough Money!\n${0} Needed".format(amount), -1, -1, COLOR_ERROR, 2, CHANNEL_MESSAGE)
            GEUtil.PlaySoundTo(player, "HUD.Hint", True)
            return False
    
    # Create HUD
    def CreateHUD(self, player):
        GEUtil.RemoveHudProgressBar(player, BAR_HEALTH)
        GEUtil.RemoveHudProgressBar(player, BAR_ARMOR)
        GEUtil.InitHudProgressBar(player, BAR_HEALTH, "", GEGlobal.HUDPB_SHOWBAR | GEGlobal.HUDPB_VERTICAL, player.GetMaxHealth(), 0.45, 0.78, 10, 50, COLOR_HEALTH, player.GetHealth())
        GEUtil.InitHudProgressBar(player, BAR_ARMOR, "", GEGlobal.HUDPB_SHOWBAR | GEGlobal.HUDPB_VERTICAL, player.GetMaxArmor(), 0.55, 0.78, 10, 50, COLOR_ARMOR, player.GetArmor())
    
    # Gets a new buyable weapon
    def NewCurrentWeapon(self, player):
        id = player.GetPlayerID()
        picked = False
        weapon = -1
        
        # Set to nothing
        CurrentWeapon[id] = -1
        
        # You have all weapons
        if len(Weapons[id]) == len(WeaponList):
            return
        
        # Keep looking for a new weapon the player doesn't have yet
        while not picked:
            picked = True
            weapon = random.randint(0, len(WeaponList) - 1)
            for i in range(0, len(Weapons[id]) - 1):
                if Weapons[id][i] == WeaponList[weapon][0]:
                    picked = False
                    break
        
        # Set new weapon
        CurrentWeapon[id] = weapon
        
    # ----------------------------------------------------------------------------------------------------
    # 
    # Event Hooks
    # 
    # ----------------------------------------------------------------------------------------------------
    
    # Teamplay
    def GetTeamPlay(self):
        return GEGlobal.TEAMPLAY_TOGGLE
    
    # Name
    def GetPrintName(self):
        return "RPG"
    
    # Description
    def GetGameDescription(self):
        return "RPG"

    # Load
    def OnLoadGamePlay(self):
        pass
    
    # Begin Round
    def OnRoundBegin(self):
        super(RPG, self).OnRoundBegin()
        
        # Custom Commands
        for player in Utils.GetPlayers():
            GEUtil.ClientCommand(player, "bind \"F1\" \"say !rpg_buy_health\"")
            GEUtil.ClientCommand(player, "bind \"F2\" \"say !rpg_buy_armor\"")
            GEUtil.ClientCommand(player, "bind \"F3\" \"say !rpg_buy_weapon\"")
            GEUtil.ClientCommand(player, "bind \"F4\" \"say !rpg_buy_ammo\"")
            GEUtil.ClientCommand(player, "bind \"F5\" \"say !rpg_increase_health\"")
            GEUtil.ClientCommand(player, "bind \"F6\" \"say !rpg_increase_armor\"")
            GEUtil.ClientCommand(player, "bind \"F7\" \"say !rpg_increase_attack\"")
        
        # Reset the Loot Briefcase state
        GEMPGameRules.GetTokenMgr().RemoveToken(LootToken)
        GEMPGameRules.GetRadar().DropRadarContact(player)
        LootTokenActive = False
    
    # Spectate
    def OnPlayerObserver(self, player):
        # Remove Bars
        GEUtil.RemoveHudProgressBar(player, BAR_HEALTH)
        GEUtil.RemoveHudProgressBar(player, BAR_ARMOR)
        GEUtil.RemoveHudProgressBar(player, BAR_COMBO)
    
    # Player Spawn
    def OnPlayerSpawn(self, player):
        id = player.GetPlayerID()
        
        # Give XP to new players to bring them up to speed with the current match
        if player.IsInitialSpawn():
            xp = 0
            for i in range(0, len(XP)):
                xp += XP[i]
            xp /= (GEMPGameRules.GetNumActivePlayers() / 2) + 1
            XP[id] = xp
        
        # Help
        if player.IsInitialSpawn():
            help = ""
            help2 = ""
            help += "Press ^lF1^| to buy Health Kit\n"
            help += "Press ^lF2^| to buy Armor Vest\n"
            help += "Press ^lF3^| to buy Weapon\n"
            help += "Press ^lF4^| to buy Ammo for current Weapon\n"
            help2 += "^rLevel Up:^|\n"
            help2 += "Press ^lF5^| to increase Health\n"
            help2 += "Press ^lF6^| to increase Armor\n"
            help2 += "Press ^lF7^| to increase Damage\n"
            GEUtil.HudMessage(player, help, -1, 0.3, COLOR_NORMAL, 5, CHANNEL_MESSAGE)
            GEUtil.HudMessage(player, help2, -1, 0.5, COLOR_NORMAL, 5, CHANNEL_MESSAGE + 1)
        
        # Pick a new buyable weapon
        if not isinstance(player, GEPlayer.CGEBotPlayer):
            self.NewCurrentWeapon(player)
        
        # Set base Money
        if (Money[id] < MONEY_START * Level[id]):
            Money[id] = MONEY_START * Level[id]
        
        # Set initial Health/Armor
        if player.IsInitialSpawn():
            player.SetMaxHealth(HEALTH_START)
            player.SetMaxArmor(ARMOR_START)
        
        # Set Health
        player.SetHealth(player.GetMaxHealth())
        
        # Give bought weapons
        for i in range(0, len(Weapons[id])):
            for j in range(0, len(WeaponList)):
                if Weapons[id][i] in WeaponList[j][0]:
                    weapon, ammo = WeaponList[j][0], WeaponList[j][3]
                    player.GiveNamedWeapon(weapon, ammo, True)
                    break
        
        # Create HUD
        self.CreateHUD(player)
        
        # Create Combo
        GEUtil.InitHudProgressBar(player, BAR_COMBO, "", GEGlobal.HUDPB_SHOWBAR | GEGlobal.HUDPB_VERTICAL, 30, 0.01, 0.4, 10, 100, COLOR_NORMAL, ComboTimer[player.GetPlayerID()])
    
    # Calculate Damage
    def CalculateCustomDamage(self, victim, info, health, armour):
        impact = health + armour
        killer = GEPlayer.ToMPPlayer(info.GetAttacker())
        id = killer.GetPlayerID()
        weapon = GEWeapon.ToGEWeapon(info.GetWeapon())
        if not isinstance(weapon, GEWeapon.CGEWeapon):
            return
        if impact >= 80 * (1.0 + (Level[id] * ATTACK_INCREASE)) and not weapon.IsMeleeWeapon() and not weapon.IsThrownWeapon() and not weapon.IsExplosiveWeapon() and not weapon.GetPrintName().lower() == "#ge_goldengun" and not weapon.GetPrintName().lower() == "#ge_goldpp7": # Dirty hacks, yay!
            Headshot[id] = True
    
    # Killed
    def OnPlayerKilled(self, victim, killer, weapon):
        super(RPG, self).OnPlayerKilled(victim, killer, weapon)
        
        # XP and Money calculations
        victimid = victim.GetPlayerID()
        killerid = killer.GetPlayerID()
        distance = 0
        weapbonus = 0
        combobonus = 0
        headshotbonus = 0
        xp = 0
        money = 0
        bonus = 0
        text = ""
        
        # You killed yourself; lose all your money
        if victim.GetPlayerName() == killer.GetPlayerName():
            Money[killerid] = 0
            Money[victimid] = 0
            return
        
        # Base XP and Money gain
        xp += random.randint(50, 100) + (random.randint(Level[victimid] * 100 / 2, Level[victimid] * 100) / 4)
        money += Money[victimid]
        
        # Bonus - Distance
        distance = int(round(GEUtil.DistanceBetween(killer, victim)))
        if distance > 250:
            distance /= random.randint(4, 8)
            bonus += distance
        else:
            distance = 0
        
        # Bonus - Weapon
        for i in range(0, len(WeaponBonus)):
            if GEWeapon.ToGEWeapon(weapon):
                if GEWeapon.ToGEWeapon(weapon).GetClassname().lower() == WeaponBonus[i][0]:
                    weapbonus = random.randint(WeaponBonus[i][1] / 2, WeaponBonus[i][1])
                    bonus += weapbonus
        
        # Bonus - Combo
        Combo[killerid] += 1
        ComboTimer[killerid] += COMBO_MAX
        if Combo[killerid] > 1:
            combobonus = random.randint(50, 100) * Combo[killerid]
        bonus += combobonus
        
        # Bonus - Headshot
        if Headshot[killerid]:
            headshotbonus = 100 * (Combo[killerid] + 1)
            Headshot[killerid] = False
            bonus += headshotbonus
        
        # Add Bonus to XP and Money
        xp += bonus
        money += bonus
        
        # Create String
        if money > 0:
            text += "^l+${0}\n".format(money)
        if xp > 0:
            text += "^|XP +{0}\n".format(xp)
        if distance > 0:
            text += "^uDistance Bonus: +{0}\n".format(distance)
        if weapbonus > 0:
            text += "^uWeapon Bonus: +{0}\n".format(weapbonus)
        if headshotbonus > 0:
            text += "^uHeadshot Bonus: +{0}\n".format(headshotbonus)
        if Combo[killerid] > 1:
            text += "^uCombo Bonus: +${0}\n".format(combobonus)
        text += "^|"
        
        # Display String
        GEUtil.HudMessage(killer, text, 0.6, 0.8, COLOR_XP, 5, CHANNEL_GAIN)
        
        # Add XP and Money to pool
        XP[killerid] += xp
        Money[killerid] += money
        
        # Reset victim's Money
        Money[victimid] = 0
    
    # Game Loop
    def OnThink(self):
        for player in Utils.GetPlayers():
            id = player.GetPlayerID()
            
            # Return if there's no active players
            if GEMPGameRules.GetNumActivePlayers() == 0:
                return
            
            # Spectator Stat View
            if Viewing[id] != -1:
                for plr in Utils.GetPlayers():
                    if Viewing[id] == plr.GetPlayerID():
                        id = plr.GetPlayerID()
                        GEUtil.HudMessage(player, "^u{0}\n^l${1}\n^|XP: {2}/{3} ({4})\n^dDamage: {5}\n^rHealth: {6}/{7}\n^iArmor: {8}/{9}^|".format(plr.GetPlayerName(), Money[id], XP[id], self.LevelNext(id), Level[id], self.GetWeaponDamage(plr), plr.GetHealth(), plr.GetMaxHealth(), plr.GetArmor(), plr.GetMaxArmor()), 0.01, 0.3, COLOR_XP, 1, CHANNEL_STATS)
                        if CurrentWeapon[id] != -1:
                            GEUtil.HudMessage(player, "{0}\n${1}".format(WeaponList[CurrentWeapon[id]][1], WeaponList[CurrentWeapon[id]][2]), 1.0, 0.3, COLOR_WEAPON, 1, CHANNEL_WEAPON)
                        break
            
            # continue if the player is dead or inactive
            if player.IsDead() or not player.IsActive():
                continue
            
            # Display Money, XP, Stats
            stats = ""
            stats += "^l${0}\n".format(Money[id])
            stats += "^|XP: {0}/{1} ({2})".format(XP[id], self.LevelNext(id), Level[id])
            if StatPoints[id] > 0:
                stats += " [{0}]\n".format(StatPoints[id])
            else:
                stats += "\n"
            stats += "^rHealth: {0}/{1} ({2})\n".format(player.GetHealth(), player.GetMaxHealth(), LevelHealth[id])
            stats += "^iArmor: {0}/{1} ({2})\n".format(player.GetArmor(), player.GetMaxArmor(), LevelArmor[id])
            stats += "^dDamage: {0:g} ({1})".format(self.GetWeaponDamage(player), LevelAttack[id])
            stats += "^|"
            GEUtil.HudMessage(player, stats, 0.01, 0.8, COLOR_XP, 1, CHANNEL_STATS)
            
            # Display current buyable Weapon
            if CurrentWeapon[id] != -1:
                GEUtil.HudMessage(player, "{0}\n${1}".format(WeaponList[CurrentWeapon[id]][1], WeaponList[CurrentWeapon[id]][2]), 1.0, 0, COLOR_WEAPON, 1, CHANNEL_WEAPON)
            
            # Loot Case Token
            global LootTokenActive
            lootnum = random.randint(0, LOOT_CHANCE)
            if lootnum == 0 and not LootTokenActive:
                GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^iA Loot Briefcase has appeared!")
                GEUtil.PlaySoundTo(None, "GEGamePlay.Token_Drop_Friend", True)
                GEMPGameRules.GetTokenMgr().SetupToken(LootToken, limit = 1, respawn_delay = 60.0,
                                    location = GEGlobal.SPAWN_WEAPON | GEGlobal.SPAWN_SPECIALONLY,
                                    glow_color = COLOR_MONEY, glow_dist = 3500,
                                    world_model = "models/weapons/tokens/w_briefcasetoken.mdl",
                                    view_model = "models/weapons/tokens/v_briefcasetoken.mdl",
                                    print_name = "Loot Briefcase")
                LootTokenActive = True
            
            # Loot Briefcase Handling
            if player.HasWeapon(LootToken):
                Money[id] += 1
            
            # Show who has the Loot Case on the Scoreboard
            if player.HasWeapon(LootToken):
                player.SetScoreBoardColor(GEGlobal.SB_COLOR_GOLD)
            else:
                player.SetScoreBoardColor(GEGlobal.SB_COLOR_NORMAL)
            
            # Combo Timer handling
            if ComboTimer[id] > 0:
                ComboTimer[id] -= 1
            if ComboTimer[id] <= 0:
                Combo[id] = 0
            GEUtil.UpdateHudProgressBar(player, BAR_COMBO, ComboTimer[id], "{0}".format(Combo[id]), COLOR_NORMAL)
            
            # Level Checking
            if XP[id] >= self.LevelNext(id):
                self.LevelUp(player)
            
            # HUD Handling
            GEUtil.UpdateHudProgressBar(player, BAR_HEALTH, player.GetHealth())
            GEUtil.UpdateHudProgressBar(player, BAR_ARMOR, player.GetArmor())
    
    # Token Spawn
    def OnTokenSpawned(self, token):
        GEMPGameRules.GetRadar().AddRadarContact(token, GEGlobal.RADAR_TYPE_TOKEN, True, "", COLOR_MONEY)
        GEMPGameRules.GetRadar().SetupObjective(token, GEGlobal.TEAM_NONE, "", "Loot Briefcase", COLOR_LOOT)
    
    # Token Picked Up
    def OnTokenPicked(self, token, player):
        GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| got the Loot Briefcase!".format(player.GetPlayerName()))
        GEUtil.PlaySoundTo(None, "GEGamePlay.Token_Grab", True)
        GEMPGameRules.GetRadar().DropRadarContact(token)
        GEMPGameRules.GetRadar().AddRadarContact(player, GEGlobal.RADAR_TYPE_PLAYER, True, "", COLOR_LOOT)
        GEMPGameRules.GetRadar().SetupObjective(player, GEGlobal.TEAM_NONE, "", "Loot Briefcase", COLOR_LOOT)
    
    # Token Dropped
    def OnTokenDropped(self, token, player):
        GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| dropped the Loot Briefcase!".format(player.GetPlayerName()))
        GEUtil.PlaySoundTo(None, "GEGamePlay.Token_Drop_Enemy", True)
        GEMPGameRules.GetRadar().DropRadarContact(player)
        GEMPGameRules.GetRadar().AddRadarContact(token, GEGlobal.RADAR_TYPE_TOKEN, True, "", COLOR_MONEY)
        GEMPGameRules.GetRadar().SetupObjective(token, GEGlobal.TEAM_NONE, "", "Loot Briefcase", COLOR_LOOT)
    
    # Say / Command
    def OnPlayerSay(self, player, text):
        id = player.GetPlayerID()
        text = text.lower()
        
        # Commands
        if text == "!rpg_buy_health":
            if not player.IsActive() or player.IsDead():
                return True
            if self.CheckMoney(player, HEALTH_COST):
                GEUtil.PlaySoundTo(player, "GEPlayer.Gasp", True)
                GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| bought a Health Kit".format(player.GetPlayerName()))
                player.SetHealth(player.GetMaxHealth())
            return True
        elif text == "!rpg_buy_armor":
            if not player.IsActive() or player.IsDead():
                return True
            if self.CheckMoney(player, ARMOR_COST):
                GEUtil.PlaySoundTo(player, "ArmorVest.Pickup", True)
                GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| bought an Armor Vest".format(player.GetPlayerName()))
                player.SetArmor(player.GetMaxArmor())
            return True
        elif text == "!rpg_buy_weapon":
            if not player.IsActive() or player.IsDead() or CurrentWeapon[id] == -1:
                return True
            weapon = WeaponList[CurrentWeapon[id]]
            if self.CheckMoney(player, weapon[2])and CurrentWeapon[id] != -1:
                if not weapon[0] in Weapons[id]:
                    Weapons[id].append(weapon[0])
                player.GiveNamedWeapon(weapon[0], weapon[3], True)
                self.NewCurrentWeapon(player)
                GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| bought {1}".format(player.GetPlayerName(), weapon[1]))
            return True
        elif text == "!rpg_buy_ammo":
            if not player.IsActive() or player.IsDead():
                return True
            weapon = player.GetActiveWeapon()
            if weapon.GetAmmoCount() < weapon.GetMaxAmmoCount():
                if not weapon.GetPrintName().lower() == "#ge_slapper" and not weapon.GetPrintName().lower() == "#ge_knife":
                    ammotype = player.GetActiveWeapon().GetAmmoType()
                    for i in range(0, len(Ammo)):
                        if Ammo[i][0] == ammotype:
                            if self.CheckMoney(player, Ammo[i][2]):
                                player.GiveAmmo(Ammo[i][0], Ammo[i][3], False)
                                GEUtil.ClientPrint(None, GEGlobal.HUD_PRINTTALK, "^d{0}^| bought {1} (x{2})".format(player.GetPlayerName(), Ammo[i][1], Ammo[i][3]))
                                return True
            return True
        elif text == "!rpg_increase_health":
            self.IncreaseStat(player, STAT_HEALTH)
            return True
        elif text == "!rpg_increase_armor":
            self.IncreaseStat(player, STAT_ARMOR)
            return True
        elif text == "!rpg_increase_attack":
            self.IncreaseStat(player, STAT_ATTACK)
            return True
        elif "!rpg_view_stats" in text:
            if "none" in text:
                Viewing[id] = -1
                GEUtil.ClientPrint(player, GEGlobal.HUD_PRINTTALK, "Reset stat view")
                return True
            for plr in Utils.GetPlayers():
                if plr.GetPlayerName().lower() in text:
                    Viewing[id] = plr.GetPlayerID()
                    GEUtil.ClientPrint(player, GEGlobal.HUD_PRINTTALK, "Now viewing stats of {0}".format(plr.GetPlayerName()))
                    return True
            GEUtil.ClientPrint(player, GEGlobal.HUD_PRINTTALK, "Unknown player name")
            return True
