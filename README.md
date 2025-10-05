# API Sports - NFL Data Client

A comprehensive Python client for accessing NFL (American Football) data from the API-Sports service. This library provides a clean interface to fetch NFL data including teams, players, games, standings, statistics, injuries, and betting odds with built-in caching and rate limiting.

## Features

- **Complete NFL API Coverage**: Access to all NFL endpoints including seasons, leagues, teams, players, games, standings, statistics, injuries, and odds
- **Intelligent Caching**: Built-in caching system to reduce API calls and improve performance
- **Rate Limiting**: Automatic rate limiting to respect API limits and prevent throttling
- **Error Handling**: Comprehensive error handling for HTTP errors, authentication issues, and API failures
- **Easy Integration**: Simple, intuitive API design for easy integration into other projects

## Project Structure

```
api_sports/
├── __init__.py          # Package initialization and main exports
├── base_api.py          # Base API class with core functionality
├── cache.py             # Caching system for API responses
├── nfl_api.py           # NFL-specific API methods and endpoints
└── README.md           # This documentation
```

## Component Overview

### 1. Cache System (`cache.py`)

The caching system provides intelligent storage of API responses to minimize API calls and improve performance.

**Key Features:**
- **File-based Storage**: Uses JSON files for persistent caching
- **TTL Support**: Configurable expiration time (default: 1 hour)
- **Automatic Cleanup**: Removes expired entries automatically
- **Statistics Tracking**: Provides cache hit/miss statistics

**Configuration:**
- `cache_file`: Path to cache file (default: 'cache.json')
- `expire_seconds`: Cache expiration time in seconds (default: 3600)

**Methods:**
- `get(key)`: Retrieve cached data if available and not expired
- `set(key, data)`: Store data in cache with timestamp
- `is_cached(key)`: Check if data exists in cache and is valid
- `get_stats()`: Get cache performance statistics

### 2. Base API (`base_api.py`)

The base API class provides core functionality for all API interactions including authentication, rate limiting, and error handling.

**Key Features:**
- **Authentication**: Handles API key authentication automatically
- **Rate Limiting**: Enforces minimum intervals between requests (default: 1 second)
- **Error Handling**: Comprehensive HTTP error handling (401, 403, 429, etc.)
- **Response Processing**: Automatic JSON parsing and metadata addition
- **Cache Integration**: Seamless integration with the caching system

**Configuration:**
- `api_key`: Your API-Sports API key (required)
- `base_url`: API base URL (https://v1.american-football.api-sports.io)
- `min_request_interval`: Minimum time between requests (default: 1.0 seconds)

**Response Format:**
All API responses include metadata:
```python
{
    "data": ...,              # Original API response data
    "from_cache": boolean,    # Whether data came from cache
    "status_code": int,       # HTTP status code
    "endpoint": str,          # API endpoint called
    "params": dict           # Parameters used in request
}
```

### 3. NFL API (`nfl_api.py`)

The NFL API class extends the base API to provide sport-specific methods for accessing NFL data.

**Available Endpoints:**

#### League & Season Data
- `get_timezone()` - Get available timezones
- `get_seasons()` - Get all available seasons
- `get_leagues(season=None)` - Get leagues with optional season filter

#### Team Data
- `get_teams(league=None, season=None, name=None, code=None, search=None)` - Get team information

#### Player Data
- `get_players(season=None, team=None, id=None, name=None, search=None)` - Get player information
- `get_players_statistics(league=None, season=None, id=None, team=None)` - Get player season statistics

#### Game Data
- `get_games(league=None, season=None, date=None, timezone=None, id=None, live=None, team=None)` - Get game information
- `get_games_events(id=None)` - Get game events and plays
- `get_games_statistics(id=None)` - Get team game statistics
- `get_games_players_statistics(id=None, group=None, team=None, player=None)` - Get player game statistics

#### Standings
- `get_standings(league=None, season=None)` - Get league standings
- `get_standings_conferences(league=None, season=None)` - Get available conferences
- `get_standings_divisions(league=None, season=None)` - Get available divisions

#### Injuries
- `get_injuries(team=None, date=None, player=None)` - Get current injury reports

#### Betting Odds
- `get_odds(game=None, bookmaker=None, bet=None)` - Get betting odds
- `get_bets()` - Get available bet types
- `get_bookmakers()` - Get available bookmakers

## Installation

### Prerequisites

- Python 3.7+
- API-Sports API key (sign up at https://api-sports.io/)

### Install Dependencies

```bash
pip install requests
```

### Setup

1. Clone or download this project
2. Place it in your project directory or install as a package
3. Ensure you have a valid API-Sports API key

## Usage

### Basic Usage

```python
from api_sports import NFLAPI

# Initialize the API client
api = NFLAPI(api_key="your_api_key_here")

# Get available seasons
seasons = api.get_seasons()
print(seasons)

# Get teams for a specific league and season
teams = api.get_teams(league=1, season=2023)
print(teams)

# Get games for a specific date
games = api.get_games(date="2023-09-10")
print(games)
```

### Advanced Usage with Parameters

```python
from api_sports import NFLAPI

api = NFLAPI(api_key="your_api_key_here")

# Get players with search functionality
players = api.get_players(search="Tom Brady")

# Get player statistics for a specific season
player_stats = api.get_players_statistics(
    id=123,  # Player ID
    season=2023,
    league=1
)

# Get games with timezone support
games = api.get_games(
    league=1,
    season=2023,
    timezone="America/New_York"
)

# Get betting odds for a specific game
odds = api.get_odds(game=45678)  # Game ID
```

### Working with Cache

```python
from api_sports import NFLAPI

api = NFLAPI(api_key="your_api_key_here")

# Check cache statistics
cache_stats = api.cache.get_stats()
print(f"Cache hit rate: {cache_stats['hit_rate']:.2%}")

# Make a request (will be cached on first call)
teams = api.get_teams(league=1, season=2023)
print(f"From cache: {teams['from_cache']}")  # False

# Make the same request again (will come from cache)
teams_again = api.get_teams(league=1, season=2023)
print(f"From cache: {teams_again['from_cache']}")  # True
```

### Error Handling

```python
from api_sports import NFLAPI

api = NFLAPI(api_key="invalid_key")

# This will return an error response instead of raising an exception
response = api.get_seasons()
if 'error' in response:
    print(f"Error: {response['error']}")
    print(f"Status Code: {response['status_code']}")
```

## Integration in Other Projects

### As a Local Module

1. **Copy the `api_sports` directory** to your project root
2. **Import and use** in your code:

```python
from api_sports import NFLAPI

class MyNFLApp:
    def __init__(self, api_key):
        self.api = NFLAPI(api_key)
    
    def get_team_roster(self, team_id, season):
        """Get complete team roster with player statistics"""
        players = self.api.get_players(team=team_id, season=season)
        
        if 'error' in players:
            return None
        
        roster = []
        for player in players.get('response', []):
            stats = self.api.get_players_statistics(
                id=player['id'],
                season=season
            )
            roster.append({
                'player': player,
                'statistics': stats.get('response', [])
            })
        
        return roster
```

### As a Package (Recommended)

1. **Install the package**:

```bash
pip install -e .
```

2. **Use in any project**:

```python
from api_sports import NFLAPI

# Your NFL-powered application
api = NFLAPI(api_key="your_key")
```

### Example: NFL Dashboard Application

```python
from api_sports import NFLAPI
import json

class NFLDashboard:
    def __init__(self, api_key):
        self.api = NFLAPI(api_key)
    
    def get_weekly_summary(self, week_date):
        """Get comprehensive weekly game summary"""
        games = self.api.get_games(date=week_date)
        
        if 'error' in games:
            return {"error": games['error']}
        
        summary = {
            "date": week_date,
            "total_games": len(games.get('response', [])),
            "games": []
        }
        
        for game in games.get('response', []):
            game_details = {
                "id": game['id'],
                "teams": {
                    "home": game['teams']['home']['name'],
                    "away": game['teams']['away']['name']
                },
                "score": {
                    "home": game['scores']['home'],
                    "away": game['scores']['away']
                },
                "status": game['status']['long']
            }
            
            # Add game statistics if available
            stats = self.api.get_games_statistics(id=game['id'])
            if 'error' not in stats:
                game_details['statistics'] = stats.get('response', [])
            
            summary['games'].append(game_details)
        
        return summary
    
    def export_to_json(self, data, filename):
        """Export data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

# Usage
dashboard = NFLDashboard(api_key="your_api_key")
weekly_data = dashboard.get_weekly_summary("2023-09-10")
dashboard.export_to_json(weekly_data, "nfl_week_1_summary.json")
```

## Configuration Options

### Custom Cache Settings

```python
from api_sports import NFLAPI, Cache

# Custom cache with 2-hour expiration
custom_cache = Cache(expire_seconds=7200, cache_file="nfl_cache.json")
api = NFLAPI(api_key="your_key")
api.cache = custom_cache
```

### Custom Rate Limiting

```python
from api_sports import NFLAPI

api = NFLAPI(api_key="your_key")
api.min_request_interval = 2.0  # 2 seconds between requests
```

## API Key Setup

1. **Sign up** at https://api-sports.io/
2. **Get your API key** from the dashboard
3. **Choose the appropriate subscription plan** for your needs
4. **Replace `"your_api_key_here"`** with your actual API key

## Rate Limits and Quotas

- **Free Tier**: Limited requests per day
- **Paid Tiers**: Higher limits and additional features
- **Automatic Rate Limiting**: Built-in protection against exceeding limits
- **Cache Optimization**: Reduces actual API calls significantly

## Error Reference

Common HTTP status codes and their meanings:

- **200**: Success
- **401**: Authentication failed - Invalid API key
- **403**: Access forbidden - Check API subscription plan
- **429**: Rate limit exceeded - Too many requests
- **500+**: Server errors - Try again later

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Support

For issues related to:
- **API-Sports Service**: https://api-sports.io/contact
- **This Library**: Create an issue in the repository

## Changelog

### Version 1.0.0
- Initial release
- Complete NFL API coverage
- Built-in caching system
- Rate limiting and error handling
- Comprehensive documentation
