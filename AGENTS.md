# Discord Bot Architecture

This document describes the cog-based architecture of the Discord Clash of Clans bot. It provides context for LLMs working on the codebase to understand the role-based permission system and how components interact.

## Architecture Overview

The bot uses Discord.py's **cog system** to organize functionality by role-based permissions. Each cog handles commands for specific Clash of Clans roles, with a base framework enforcing consistent permission checking.

## Role Hierarchy

The bot recognizes these Discord roles (defined in `base_cog.py`):
1. **admin** - Server administrators 
2. **leader** - Clan leaders
3. **coleader** - Clan co-leaders  
4. **elder** - Clan elders
5. **member** - Clan members
6. **foreigner** - Unverified users (default for new Discord members)

## Current Cog Implementation

### `BaseCog` (`base_cog.py`)
**Purpose**: Abstract base class for all cogs
**Key Features**:
- Defines the `Role` enum with all supported roles
- Enforces permission checking via abstract `cog_check()` method
- Requires error handling via abstract `cog_command_error()` method
- Provides basic `ping` command

**Usage**: All cogs must inherit from `BaseCog` and implement the required abstract methods.

### `AdminCog` (`admin.py`)
**Purpose**: Administrative commands and server setup
**Permissions**: `admin` role only (or bot owners)
**Key Features**:
- Only cog currently loaded in `main.py`
- Handles new guild setup with `on_guild_join` event
- Permission check allows DMs for bot owners
- Uses `CocClient` for API integration

**Commands**: `setup_bot` (incomplete implementation)

### `DMCog` (`foreigner.py`) 
**Purpose**: New member onboarding and verification
**Key Features**:
- **Automatic onboarding**: Assigns "foreigner" role to new members
- **Verification flow**: Guides users through CoC account linking via DM
- **Visual guides**: Sends screenshots showing how to find API tokens
- **Role assignment**: Updates Discord roles based on verified CoC clan rank
- **Cleanup**: Handles member departures

**Commands**:
- `setup <nickname> <token>` - Verify by CoC nickname
- `setup_tag <player_tag> <token>` - Verify by player tag

**Interaction Flow**:
1. User joins Discord → `on_member_join` → assign "foreigner" role
2. Send DM with setup instructions and visual guides
3. User provides CoC credentials via DM commands
4. Verify with CoC API via `CocClient`
5. Update Discord role, nickname, and announce to clan

### `ColeaderCog` (`coleader.py`)
**Purpose**: Leadership commands 
**Status**: **Has bug** - imports `Rol` instead of `Role`
**Permissions**: `leader` and `coleader` roles
**Note**: Not currently loaded in `main.py`

### Missing Implementations
- `elder.py` - Empty file
- `member.py` - Empty file

## API Integration

### `CocClient` (`api/coc.py`)
**Purpose**: Clash of Clans API wrapper
**Key Methods**:
- `get_clan_members(clan_tag)` - Fetch clan roster
- `post_verify_player(player_tag, token)` - Verify user tokens
- `get_player(player_tag)` - Get player details
- Error handling for invalid tags, server errors

**Usage**: Instantiated in cogs that need CoC API access

## How Components Interact

1. **Permission Flow**: `BaseCog.cog_check()` → role validation → command execution
2. **Verification Flow**: `DMCog` events → `CocClient` API calls → role updates
3. **Error Handling**: Each cog implements `cog_command_error()` for consistent error responses

## Development Guidelines

### Adding New Cogs
1. Inherit from `BaseCog`
2. Implement required abstract methods
3. Define `allowed_roles` list
4. Add to `main.py` cogs list to load

### Permission Pattern
```python
def cog_check(self, ctx: commands.Context) -> bool:
    if isinstance(ctx.author, Member):
        return any(role.name in self.allowed_roles for role in ctx.author.roles)
    return False  # or handle DM permissions
```

### API Integration Pattern
```python
def __init__(self, bot):
    self.bot = bot
    self.coc_client = CocClient()
```

## Current Issues to Address

1. `ColeaderCog` has import bug (`Rol` vs `Role`)
2. `elder.py` and `member.py` are empty
3. Only `AdminCog` is loaded in `main.py`
4. Missing complete implementations for leadership and member functionality