from .base_api import BaseAPI

class NFLAPI(BaseAPI):
    """
    NFL API Client for accessing American Football data from API-Sports.
    
    This class provides methods to interact with various NFL endpoints including
    seasons, leagues, teams, players, games, standings, injuries, odds, and statistics.
    
    The API-Sports NFL API provides comprehensive coverage of American football data
    including historical and current season information, team statistics, player data,
    game results, standings, injuries, and betting odds.
    
    Attributes:
        api_key (str): Your API-Sports API key for authentication
        base_url (str): Base URL for the API-Sports NFL endpoints
        cache (Cache): Caching mechanism for API responses
    
    Example:
        >>> api = NFLAPI(api_key="your_api_key")
        >>> seasons = api.get_seasons()
        >>> teams = api.get_teams(league=1, season=2023)
    """
    
    def get_timezone(self):
        """
        Returns list of timezone set that can be used in endpoint games.
        
        This endpoint provides all available timezone options that can be used as 
        parameters in the games endpoint. Timezones are used to display game times
        in the user's preferred local time instead of UTC.
        
        This endpoint does not require any parameters.
        
        Returns:
            dict: API response containing list of available timezones
        """
        return self._get("/timezone")

    def get_seasons(self):
        """
        Return list of all available seasons for all competitions.
        
        All seasons are only 4-digit keys, so for a league whose season is 2018-2019 
        season in API will be 2018. All seasons can be used in other endpoints as filters.
        
        This endpoint does not require any parameters.
        
        Returns:
            dict: API response containing list of available seasons
        """
        return self._get("/seasons")

    def get_leagues(self, season=None):
        """
        Return list of all available competitions.
        
        The league id are unique in API and competitions keep it across all seasons.
        This endpoint contains a field named coverage that indicates for each season 
        of a competition data that are available.
        
        Query Parameters:
            season (int, optional): Default: "YYYY". The season of league
            current (str, optional): Enum: "true" "false"
        
        Returns:
            dict: API response containing list of available leagues
        """
        params = {}
        if season:
            params['season'] = season
        return self._get("/leagues", params=params)

    def get_teams(self, league=None, season=None, name=None, code=None, search=None):
        """
        Return a set of data about teams.
        
        The team id are unique in API and teams keep it among all competitions 
        in which they participate. This endpoint requires at least one parameter.
        This endpoint is updated every day.
        
        Query Parameters:
            id (int): The id of team
            league (int): A valid League id
            season (int): A valid season
            name (str): The name of team
            code (str): The code of team
            search (str, >=3 chars): The name of team
        
        Returns:
            dict: API response containing team data
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        if name:
            params['name'] = name
        if code:
            params['code'] = code
        if search:
            params['search'] = search
        return self._get("/teams", params=params)

    def get_players(self, season=None, team=None, id=None, name=None, search=None):
        """
        Return a set of data about players.
        
        The players id are unique in API and keep it among all competitions 
        in which they participate. Not all data is available for all players.
        This endpoint requires at least one parameter. This endpoint is updated every day.
        
        Query Parameters:
            id (int): The id of player
            name (str): The name of player
            team (int): The id of team
            season (int, default: "YYYY"): The season
            search (str, >=3 chars): The name of player
        
        Returns:
            dict: API response containing player data
        """
        params = {}
        if season:
            params['season'] = season
        if team:
            params['team'] = team
        if id:
            params['id'] = id
        if name:
            params['name'] = name
        if search:
            params['search'] = search
        return self._get("/players", params=params)

    def get_injuries(self, team=None, date=None, player=None):
        """
        Return list of injured players.
        
        There is no preserved history, only currently injured players appear in this endpoint.
        This endpoint requires at least one parameter (player or team).
        This endpoint is updated every hour.
        
        Query Parameters:
            player (int): The id of player
            team (int): The id of team
            date (str): A valid date
        
        Returns:
            dict: API response containing injuries data
        """
        params = {}
        if team:
            params['team'] = team
        if date:
            params['date'] = date
        if player:
            params['player'] = player
        return self._get("/injuries", params=params)

    def get_games(self, league=None, season=None, date=None, timezone=None, id=None, live=None, team=None):
        """
        Return list of games according to given parameters.
        
        For all requests to games you can add query parameter timezone to your request 
        in order to retrieve list of games in the time zone of your choice like 
        "Europe/London". In case timezone is not recognized, empty or is not part 
        of the endpoint timezone list, UTC value will be applied by default.
        
        Available Status:
            NS : Not Started
            Q1 : First Quarter (In Play)
            Q2 : Second Quarter (In Play)
            Q3 : Third Quarter (In Play)
            Q4 : Fourth Quarter (In Play)
            OT : Overtime (In Play)
            HT : Halftime (In Play)
            FT : Finished (Game Finished)
            AOT : After Over Time (Game Finished)
            CANC : Cancelled (Game cancelled and not rescheduled)
            PST : Postponed (Game postponed and waiting for a new game date)
        
        This endpoint requires at least one of these parameters: id, date, league, team, live, h2h.
        Games are updated every 30 seconds.
        
        Query Parameters:
            id (int): The id of game
            date (str, default: "YYYY-MM-DD"): A valid date
            league (int): The id of league
            season (int, default: "YYYY"): The season of league
            team (int): The id of team
            h2h (str, default: "id-id"): Two teams Ids (example: h2h=2-3)
            live (str, default: "all"): Value: "all" (example: live=live=all)
            timezone (str): A valid timezone
        
        Returns:
            dict: API response containing games data
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        if date:
            params['date'] = date
        if timezone:
            params['timezone'] = timezone
        if id:
            params['id'] = id
        if live:
            params['live'] = live
        if team:
            params['team'] = team
        return self._get("/games", params=params)

    def get_standings(self, league=None, season=None):
        """
        Return standings of a competition in relation to a given season.
        
        To know list of available conferences or divisions you have to use 
        endpoint standings/conferences or standings/divisions.
        This endpoint requires at least two parameters: league and season.
        This endpoint is updated every hour.
        
        Query Parameters:
            league (int, required): The id of league
            season (int, required, default: "YYYY"): The season of league
            team (int): The id of team
            conference (str): A valid conference
            division (str): A valid division
        
        Returns:
            dict: API response containing standings data
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        return self._get("/standings", params=params)

    def get_odds(self, game=None, bookmaker=None, bet=None):
        """
        Return list of available odds for games.
        
        We provide pre-match odds between 1 and 7 days before game.
        We keep a 7-day history (The availability of odds may vary according 
        to games, seasons and bookmakers). This endpoint requires at least 
        one of these parameters: game. Odds are updated four times a day.
        
        Query Parameters:
            game (int, required): The id of game
            bookmaker (int): The id of bookmaker
            bet (int): The id of bet
        
        Returns:
            dict: API response containing odds data
        """
        params = {}
        if game:
            params['game'] = game
        if bookmaker:
            params['bookmaker'] = bookmaker
        if bet:
            params['bet'] = bet
        return self._get("/odds", params=params)

    def get_players_statistics(self, league=None, season=None, id=None, team=None):
        """
        Return statistics of a player for whole season.
        
        The statistics of players are different depending on positions they occupy 
        in formation, so they are grouped into different groups.
        
        Available Groups:
            Defense, Kicking, Passing, Punting, Receiving, Returning, Rushing, Scoring
        
        Data for this endpoint start from 2022 season.
        This endpoint requires at least two parameters: id or team and season.
        This endpoint is updated every day.
        
        Query Parameters:
            id (int): The id of player
            team (int): The id of team
            season (int, required, >=3 chars, default: "YYYY"): The season
            league (int): The id of league
        
        Returns:
            dict: API response containing player statistics
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        if id:
            params['id'] = id
        if team:
            params['team'] = team
        return self._get("/players/statistics", params=params)

    def get_games_events(self, id=None):
        """
        Return list of events for one game id.
        
        This endpoint requires at least one parameter.
        This endpoint is updated every 30 seconds.
        
        Query Parameters:
            id (int, required): The id of game
        
        Returns:
            dict: API response containing game events
        """
        params = {}
        if id:
            params['id'] = id
        return self._get("/games/events", params=params)

    def get_games_statistics(self, id=None):
        """
        Return team statistics from a game id.
        
        This endpoint requires the id parameter (not game).
        This endpoint is updated every 30 seconds.
        
        Query Parameters:
            id (int, required): The id of game
        
        Returns:
            dict: API response containing game team statistics
        """
        params = {}
        if id:
            params['id'] = id
        return self._get("/games/statistics/teams", params=params)

    def get_games_players_statistics(self, id=None, group=None, team=None, player=None):
        """
        Return players statistics from a game id.
        
        The statistics of players are different depending on positions they occupy 
        in formation, so they are grouped into different groups.
        
        Available Groups:
            defensive, fumbles, interceptions, kick_returns, kicking, passing, 
            punt_returns, punting, receiving, rushing
        
        This endpoint requires at least one parameter.
        This endpoint is updated every 30 seconds.
        
        Query Parameters:
            id (int, required): The id of game
            group (str): Enum: "defensive" "fumbles" "interceptions" "kick_returns" "kicking" "passing" "punt_returns" "punting" "receiving" "rushing"
            team (int): The id of team
            player (int): The id of player
        
        Returns:
            dict: API response containing game player statistics
        """
        params = {}
        if id:
            params['id'] = id
        if group:
            params['group'] = group
        if team:
            params['team'] = team
        if player:
            params['player'] = player
        return self._get("/games/statistics/players", params=params)

    def get_standings_conferences(self, league=None, season=None):
        """
        Return list of available conferences for standings.
        
        To know list of available conferences you have to use this endpoint.
        This endpoint requires at least two parameters: league and season.
        This endpoint is updated every hour.
        
        Query Parameters:
            league (int, required): The id of league
            season (int, required, default: "YYYY"): The season of league
        
        Returns:
            dict: API response containing conferences data
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        return self._get("/standings/conferences", params=params)

    def get_standings_divisions(self, league=None, season=None):
        """
        Return list of available divisions for standings.
        
        To know list of available divisions you have to use this endpoint.
        This endpoint requires at least two parameters: league and season.
        This endpoint is updated every hour.
        
        Query Parameters:
            league (int, required): The id of league
            season (int, required, default: "YYYY"): The season of league
        
        Returns:
            dict: API response containing divisions data
        """
        params = {}
        if league:
            params['league'] = league
        if season:
            params['season'] = season
        return self._get("/standings/divisions", params=params)

    def get_bets(self):
        """
        Return list of available bet types.
        
        This endpoint provides all available bet types that can be used in odds endpoint.
        This endpoint does not require any parameters.
        
        Returns:
            dict: API response containing bet types data
        """
        return self._get("/odds/bets")

    def get_bookmakers(self):
        """
        Return list of available bookmakers.
        
        This endpoint provides all available bookmakers that can be used in odds endpoint.
        This endpoint does not require any parameters.
        
        Returns:
            dict: API response containing bookmakers data
        """
        return self._get("/odds/bookmakers")

    