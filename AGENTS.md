# Discord Bot Agents

This document describes the various agents and automated systems within the Discord Clash of Clans bot. The bot operates using a role-based agent system where different components act autonomously to manage clan operations and Discord server interactions.

## Overview

The bot implements a hierarchical agent system based on Clash of Clans roles, where each agent (cog) has specific permissions and responsibilities. These agents work together to automate clan management, member verification, and Discord server moderation.

## Role-Based Agent Hierarchy

The bot recognizes the following role hierarchy, from highest to lowest privilege:

1. **Admin** - Server administrators with full access
2. **Leader** - Clan leaders with management privileges  
3. **Coleader** - Clan co-leaders with limited management privileges
4. **Elder** - Trusted clan members with moderate privileges
5. **Member** - Regular clan members
6. **Foreigner** - Unverified users (default role for new Discord members)

## Agent Types

### 1. Administrative Agent (`AdminCog`)

**Role**: Server and bot administration
**Permissions**: Full access to all bot functions
**Responsibilities**:
- Bot configuration and management
- System administration commands
- Override permissions for special cases

**Allowed Roles**: Admin

### 2. Leadership Agent (`ColeaderCog`) 

**Role**: Clan leadership and management
**Permissions**: Clan management functions
**Responsibilities**:
- Clan member management
- Leadership-specific commands
- Coordination between leaders

**Allowed Roles**: Leader, Coleader

### 3. Member Verification Agent (`DMCog`)

**Role**: Automated member onboarding and verification
**Permissions**: Role assignment and member verification
**Responsibilities**:
- **Automatic Member Onboarding**: When new users join the Discord server, automatically assigns the "foreigner" role
- **Verification Process**: Guides new members through Clash of Clans account verification
- **Account Linking**: Verifies Clash of Clans accounts using the official API
- **Role Assignment**: Automatically assigns appropriate Discord roles based on verified Clash of Clans clan rank
- **Member Departure**: Handles cleanup when members leave the server

**Key Automated Behaviors**:
- Sends welcome DM with setup instructions to new Discord members
- Provides visual guides for finding Clash of Clans API tokens
- Validates clan membership through API calls
- Updates Discord nicknames to match Clash of Clans names
- Announces new verified members in general chat

**Commands**:
- `!setup <nickname> <token>` - Verify account by Clash of Clans nickname
- `!setup_tag <player_tag> <token>` - Verify account by player tag

### 4. Base Agent Framework (`BaseCog`)

**Role**: Foundation for all other agents
**Permissions**: Basic bot functionality
**Responsibilities**:
- Permission checking system
- Error handling framework
- Common functionality shared across agents
- Health check (`ping` command)

## API Integration Agents

### Clash of Clans API Agent (`CocClient`)

**Role**: External API communication
**Responsibilities**:
- Fetch clan member data
- Verify player tokens
- Validate clan membership
- Handle API rate limiting and errors

**Key Functions**:
- Player verification
- Clan member enumeration
- Token validation
- Error handling for API failures

## Security and Permissions

### Permission System

Each agent implements role-based access control:
- Commands are restricted based on Discord role hierarchy
- Permission checks occur before command execution
- Failed permission checks are logged and reported

### Verification Process

The verification agent implements a secure multi-step process:
1. New member joins Discord → automatically assigned "foreigner" role
2. Member provides Clash of Clans nickname/tag and API token via DM
3. Bot verifies token authenticity with Clash of Clans API
4. Bot confirms clan membership
5. Bot assigns appropriate Discord role based on clan rank
6. Bot updates Discord nickname to match game name
7. Bot announces successful verification to the clan

## Error Handling and Logging

All agents implement comprehensive error handling:
- Failed API calls are logged and handled gracefully
- Permission violations are logged for security monitoring
- Invalid verification attempts are tracked
- System errors are reported to administrators

## Configuration

Agents are configured through:
- `secrets.toml` - API keys and sensitive configuration
- Role-based permission matrices
- Clan-specific settings (clan tag, server channels)

## Extensibility

The agent system is designed for extensibility:
- New agents can inherit from `BaseCog` 
- Role-based permissions are automatically enforced
- Modular design allows selective agent activation
- Clear separation of concerns between agents

## Monitoring and Maintenance

- All agent activities are logged for monitoring
- Health checks available through ping commands
- Error tracking for debugging and maintenance
- Performance monitoring for API interactions