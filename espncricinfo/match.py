import json
import pdb
import requests
import pandas as pd
from bs4 import BeautifulSoup
from espncricinfo.exceptions import MatchNotFoundError, NoScorecardError

class Match(object):

    def __init__(self, match_id):
        self.match_id = match_id
        self.match_url = "http://www.espncricinfo.com/matches/engine/match/{0}.html".format(str(match_id))
        self.json_url = "http://www.espncricinfo.com/matches/engine/match/{0}.json".format(str(match_id))
        self.json = self.get_json()
        self.html = self.get_html()
        self.comms_json = self.get_comms_json()
        if self.json:
            self.__unicode__ = self._description()
            self.status = self._status()
            self.match_class = self._match_class()
            self.season = self._season()
            self.description = self._description()
            self.legacy_scorecard_url = self._legacy_scorecard_url()
            self.series = self._series()
            self.series_name = self._series_name()
            self.series_id = self._series_id()
            self.event_url = "http://core.espnuk.org/v2/sports/cricket/leagues/{0}/events/{1}".format(str(self.series_id), str(match_id))
            self.details_url = self._details_url()
            self.officials = self._officials()
            self.current_summary = self._current_summary()
            self.present_datetime_local = self._present_datetime_local()
            self.present_datetime_gmt = self._present_datetime_gmt()
            self.start_datetime_local = self._start_datetime_local()
            self.start_datetime_gmt = self._start_datetime_gmt()
            self.cancelled_match = self._cancelled_match()
            self.rain_rule = self._rain_rule()
            self.date = self._date()
            self.continent = self._continent()
            self.town_area = self._town_area()
            self.town_name = self._town_name()
            self.town_id = self._town_id()
            self.weather_location_code = self._weather_location_code()
            self.match_title = self._match_title()
            self.result = self._result()
            self.ground_id = self._ground_id()
            self.ground_name = self._ground_name()
            self.lighting = self._lighting()
            self.followon = self._followon()
            self.scheduled_overs = self._scheduled_overs()
            self.innings_list = self._innings_list()
            self.innings = self._innings()
            self.latest_batting = self._latest_batting()
            self.latest_bowling = self._latest_bowling()
            self.latest_innings = self._latest_innings()
            self.latest_innings_fow = self._latest_innings_fow()
            self.team_1 = self._team_1()
            self.team_1_id = self._team_1_id()
            self.team_1_abbreviation = self._team_1_abbreviation()
            self.team_1_players = self._team_1_players()
            self.team_1_innings = self._team_1_innings()
            self.team_1_run_rate = self._team_1_run_rate()
            self.team_1_overs_batted = self._team_1_overs_batted()
            self.team_1_batting_result = self._team_1_batting_result()
            self.team_2 = self._team_2()
            self.team_2_id = self._team_2_id()
            self.team_2_abbreviation = self._team_2_abbreviation()
            self.team_2_players = self._team_2_players()
            self.team_2_innings = self._team_2_innings()
            self.team_2_run_rate = self._team_2_run_rate()
            self.team_2_overs_batted = self._team_2_overs_batted()
            self.team_2_batting_result = self._team_2_batting_result()
            self.home_team = self._home_team()
            self.batting_first = self._batting_first()
            self.match_winner = self._match_winner()
            self.toss_winner = self._toss_winner()
            self.toss_decision = self._toss_decision()
            self.toss_decision_name = self._toss_decision_name()
            self.toss_choice_team_id = self._toss_choice_team_id()
            self.toss_winner_team_id = self._toss_winner_team_id()
            self.espn_api_url = self._espn_api_url()
            # from comms_json
            self.rosters = self._rosters()
            self.scorecard_summary = self._scorecard_summary()
            self.full_scorecard = self._full_scorecard()
            self.game_state = self._game_state()
            self.all_innings = self._all_innings()
            self.all_partnerships = self._all_partnerships()
            self.close_of_play = self._close_of_play()
            self.hawkeye_source = self._hawkeye_source()


    def get_json(self):
        r = requests.get(self.json_url)
        if r.status_code == 404:
            raise MatchNotFoundError
        elif 'Scorecard not yet available' in r.text:
            raise NoScorecardError
        else:
            return r.json()

    def get_html(self):
        r = requests.get(self.match_url)
        if r.status_code == 404:
            raise MatchNotFoundError
        else:
            return BeautifulSoup(r.text, 'html.parser')

    def match_json(self):
        return self.json['match']

    def get_comms_json(self):
        try:
            text = self.html.find_all('script')[11].get_text().replace("\n", " ").replace('window.__INITIAL_STATE__ =','').replace('&dagger;','wk').replace('&amp;','').replace('wkts;','wkts,').replace('wkt;','wkt,').strip().replace('};', "}};").split('};')[0]
            return json.loads(text)
        except:
            return None

    def _espn_api_url(self):
        return "http://site.api.espn.com/apis/site/v2/sports/cricket/{0}/summary?event={1}".format(self.series_id, self.match_id)

    def _legacy_scorecard_url(self):
        return "http://static.espncricinfo.com"+self.match_json()['legacy_url']

    def _details_url(self, page=1, number=1000):
        return self.event_url+"/competitions/{0}/details?page_size={1}&page={2}".format(str(self.match_id), str(number), str(page))

    def __str__(self):
        return self.json['description']

    def __unicode__(self):
        return self.json['description']

    def _status(self):
        return self.match_json()['match_status']

    def _match_class(self):
        if self.match_json()['international_class_card'] != "":
            return self.match_json()['international_class_card']
        else:
            return self.match_json()['general_class_card']

    def _season(self):
        return self.match_json()['season']

    def _description(self):
        return self.json['description']

    def _series(self):
        return self.json['series']

    def _series_name(self):
        try:
            return self.json['series'][-1]['series_name']
        except:
            return None

    def _series_id(self):
        return self.json['series'][-1]['core_recreation_id']

    def _officials(self):
        return self.json['official']

    # live matches only
    def _current_summary(self):
        if 'current_summary' in self.match_json().keys():
            return self.match_json()['current_summary']

    def _present_datetime_local(self):
        return self.match_json()['present_datetime_local']

    def _present_datetime_gmt(self):
        return self.match_json()['present_datetime_gmt']

    def _start_datetime_local(self):
        return self.match_json()['start_datetime_local']

    def _start_datetime_gmt(self):
        return self.match_json()['start_datetime_gmt']

    def _cancelled_match(self):
        if self.match_json()['cancelled_match'] == 'N':
            return False
        else:
            return True

    def _rain_rule(self):
        if self.match_json()['rain_rule'] == "1":
            return self.match_json()['rain_rule_name']
        else:
            return None

    def _date(self):
        return self.match_json()['start_date_raw']

    def _continent(self):
        return self.match_json()['continent_name']

    def _town_area(self):
        return self.match_json()['town_area']

    def _town_name(self):
        return self.match_json()['town_name']

    def _town_id(self):
        return self.match_json()['town_id']

    def _weather_location_code(self):
        return self.match_json()['weather_location_code']

    def _match_title(self):
        return self.match_json()['cms_match_title']

    def _result(self):
        return self.json['live']['status']

    def _ground_id(self):
        return self.match_json()['ground_id']

    def _ground_name(self):
        return self.match_json()['ground_name']

    def _lighting(self):
        return self.match_json()['floodlit_name']

    def _followon(self):
        if self.match_json()['followon'] == '1':
            return True
        else:
            return False

    def _scheduled_overs(self):
        return int(self.match_json()['scheduled_overs'])

    def _innings_list(self):
        try:
            return self.json['centre']['common']['innings_list']
        except:
            return None

    def _innings(self):
        return self.json['innings']

    def _latest_batting(self):
        try:
            return self.json['centre']['common']['batting']
        except:
            return None

    def _latest_bowling(self):
        try:
            return self.json['centre']['common']['bowling']
        except:
            return None

    def _latest_innings(self):
        try:
            return self.json['centre']['common']['innings']
        except:
            return None

    def _latest_innings_fow(self):
        if 'fow' in self.json['centre'].keys():
            return self.json['centre']['fow']
        else:
            return None

    def _team_1(self):
        return self.json['team'][0]

    def _team_1_id(self):
        return self._team_1()['team_id']

    def _team_1_abbreviation(self):
        return self._team_1()['team_abbreviation']

    def _team_1_players(self):
        return self._team_1()['player']

    def _team_1_innings(self):
        return [inn for inn in self.json['innings'] if inn['batting_team_id'] == self._team_1_id()][0]

    def _team_1_run_rate(self):
        if self._team_1_innings()['run_rate'] == None:
            return None
        else:
            return float(self._team_1_innings()['run_rate'])

    def _team_1_overs_batted(self):
        return float(self._team_1_innings()['overs'])

    def _team_1_batting_result(self):
        return self._team_1_innings()['event_name']

    def _team_2(self):
        return self.json['team'][1]

    def _team_2_id(self):
        return self._team_2()['team_id']

    def _team_2_abbreviation(self):
        return self._team_2()['team_abbreviation']

    def _team_2_players(self):
        return self._team_2()['player']

    def _team_2_innings(self):
        return [inn for inn in self.json['innings'] if inn['batting_team_id'] == self._team_2_id()][0]

    def _team_2_run_rate(self):
        if self._team_2_innings()['run_rate'] == None:
            return None
        else:
            return float(self._team_2_innings()['run_rate'])

    def _team_2_overs_batted(self):
        return float(self._team_2_innings()['overs'])

    def _team_2_batting_result(self):
        return self._team_2_innings()['event_name']

    def _home_team(self):
        if self._team_1_id() == self.match_json()['home_team_id']:
            return self._team_1_abbreviation()
        else:
            return self._team_2_abbreviation()

    def _batting_first(self):
        if self._team_1_id() == self.match_json()['batting_first_team_id']:
            return self._team_1_abbreviation()
        else:
            return self._team_2_abbreviation()

    def _match_winner(self):
        if self._team_1_id() == self.match_json()['winner_team_id']:
            return self._team_1_abbreviation()
        else:
            return self._team_2_abbreviation()

    def _toss_winner(self):
        if self._team_1_id() == self.match_json()['toss_winner_team_id']:
            return self._team_1_id()
        else:
            return self._team_2_id()

    def _toss_decision(self):
        return self.match_json()['toss_decision']

    def _toss_decision_name(self):
        return self.match_json()['toss_decision_name']

    def _toss_choice_team_id(self):
        return self.match_json()['toss_choice_team_id']

    def _toss_winner_team_id(self):
        return self.match_json()['toss_winner_team_id']

    # comms_json methods

    def _rosters(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['rosters']
        else:
            return None

    def _scorecard_summary(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecardSummary']
        else:
            return None

    def _full_scorecard(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']
        else:
            return None

    def _game_state(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['gameStateClass']
        else:
            return None

    def _all_innings(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['allInnings']
        else:
            return None

    def _all_partnerships(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['statistics']['allPartnerships']
        else:
            return None

    def _close_of_play(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['closeOfPlay']['cop']
        else:
            return None

    def _hawkeye_source(self):
        if self.comms_json:
            return self.comms_json['gamePackage']['hawkEye']['hawkEyeSrc']
        else:
            return None

    def batsmen(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['batsmen']
        else:
            return None

    def bowlers(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['bowlers']
        else:
            return None

    def did_not_bat(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['didNotBat']
        else:
            return None

    def absent(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['absent']
        else:
            return None

    def extras(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['extras']
        else:
            return None

    def fows(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['scorecard']['innings'][str(innings)]['fows']
        else:
            return None

    def partnerships(self, innings):
        if self.comms_json:
            return self.comms_json['gamePackage']['statistics']['pshipByInnings'][int(innings)-1]['data']
        else:
            return None

    def flatten(js):
        return pd.DataFrame(js).set_index(['text','name']).squeeze()

    def url_to_id(url):
        i_d = url.split('/')[-1].split('.')[0]
        return i_d

    def get_overs_in_match(self):
        x1 = Match(self.match_id).html
        x2 = json.loads(x1.find_all('script')[13].get_text().replace("\n", " ").replace('window.__INITIAL_STATE__ =','').replace('&dagger;','wk').replace('&amp;','').replace('wkts;','wkts,').replace('wkt;','wkt,').strip().replace('};', "}};").split('};')[0])
        try:
            temp = x2['gamePackage']['scorecard']['innings']['1']['total']
            inn1overs = float(temp.split('(')[1].split(' ')[0])
        except:
            inn1overs = 0
            pass

        try:
            temp = x2['gamePackage']['scorecard']['innings']['2']['total']
            inn2overs = float(temp.split('(')[1].split(' ')[0])
        except:
            inn2overs = 0
            pass

        try:
            temp = x2['gamePackage']['scorecard']['innings']['3']['total']
            inn3overs = float(temp.split('(')[1].split(' ')[0])
        except:
            inn3overs = 0
            pass

        try:
            temp = x2['gamePackage']['scorecard']['innings']['4']['total']
            inn4overs = float(temp.split('(')[1].split(' ')[0])
        except:
            inn4overs = 0
            pass

        totalovers = inn1overs + inn2overs + inn3overs + inn4overs

        return totalovers

    def get_batcards(self):
        df = pd.DataFrame()
        x1 = Match(self.match_id).html
        x2 = json.loads(x1.find_all('script')[13].get_text().replace("\n", " ").replace('window.__INITIAL_STATE__ =','').replace('&dagger;','wk').replace('&amp;','').replace('wkts;','wkts,').replace('wkt;','wkt,').strip().replace('};', "}};").split('};')[0])
        try:
            df1bat = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['1']['batsmen'])
            d1title = x2['gamePackage']['scorecard']['innings']['1']['title']
            df1bat['Team'] = d1title.split(' ')[0]
            inn1_bat = pd.concat([df1bat.drop(['captain','commentary', 'stats','hasVideoId','trackingName'], axis=1), df1bat.stats.apply(Match.flatten)], axis=1)
            inn1_bat['PlayerID'] = inn1_bat['href'].apply(lambda x: Match.url_to_id(x))
            inn1_bat = inn1_bat.drop(['href'], axis=1)
            inn1_bat.columns =  ['fullname','not_out','name','role','runningOver','runningScore','how_out','team','runs','balls','minutes','fours','sixes','sr','id']
            inn1_bat = inn1_bat[['id','fullname','name','runs','how_out','balls','minutes','fours','sixes','sr','runningOver','runningScore','team','not_out']]
            inn1_bat = inn1_bat.to_dict(orient='records')
        except:
            inn1_bat = None
            pass

        try:
            df2bat = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['2']['batsmen'])
            d2title = x2['gamePackage']['scorecard']['innings']['2']['title']
            df2bat['Team'] = d2title.split(' ')[0]
            inn2_bat = pd.concat([df2bat.drop(['captain','commentary', 'stats','hasVideoId','trackingName'], axis=1), df2bat.stats.apply(Match.flatten)], axis=1)
            inn2_bat['PlayerID'] = inn2_bat['href'].apply(lambda x: Match.url_to_id(x))
            inn2_bat = inn2_bat.drop(['href'], axis=1)
            inn2_bat.columns =  ['fullname','not_out','name','role','runningOver','runningScore','how_out','team','runs','balls','minutes','fours','sixes','sr','id']
            inn2_bat = inn2_bat[['id','fullname','name','runs','how_out','balls','minutes','fours','sixes','sr','runningOver','runningScore','team','not_out']]
            inn2_bat = inn2_bat.to_dict(orient='records')
        except:
            inn2_bat = None
            pass

        try:
            df3bat = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['3']['batsmen'])
            d3title = x2['gamePackage']['scorecard']['innings']['3']['title']
            df3bat['Team'] = d3title.split(' ')[0]
            inn3_bat = pd.concat([df3bat.drop(['captain','commentary', 'stats','hasVideoId','trackingName'], axis=1), df3bat.stats.apply(Match.flatten)], axis=1)
            inn3_bat['PlayerID'] = inn3_bat['href'].apply(lambda x: Match.url_to_id(x))
            inn3_bat = inn3_bat.drop(['href'], axis=1)
            inn3_bat.columns =  ['fullname','not_out','name','role','runningOver','runningScore','how_out','team','runs','balls','minutes','fours','sixes','sr','id']
            inn3_bat = inn3_bat[['id','fullname','name','runs','how_out','balls','minutes','fours','sixes','sr','runningOver','runningScore','team','not_out']]
            inn3_bat = inn3_bat.to_dict(orient='records')
        except:
            inn3_bat = None
            pass

        try:
            df4bat = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['4']['batsmen'])
            d4title = x2['gamePackage']['scorecard']['innings']['4']['title']
            df4bat['Team'] = d4title.split(' ')[0]
            inn4_bat = pd.concat([df4bat.drop(['captain','commentary', 'stats','hasVideoId','trackingName'], axis=1), df4bat.stats.apply(Match.flatten)], axis=1)
            inn4_bat['PlayerID'] = inn4_bat['href'].apply(lambda x: Match.url_to_id(x))
            inn4_bat = inn4_bat.drop(['href'], axis=1)
            inn4_bat.columns = ['fullname','not_out','name','role','runningOver','runningScore','how_out','team','runs','balls','minutes','fours','sixes','sr','id']
            inn4_bat = inn4_bat[['id','fullname','name','runs','how_out','balls','minutes','fours','sixes','sr','runningOver','runningScore','team','not_out']]
            inn4_bat = inn4_bat.to_dict(orient='records')
        except:
            inn4_bat = None
            pass
        
        return(inn1_bat, inn2_bat, inn3_bat, inn4_bat)

    def get_bowlcards(self):
        df = pd.DataFrame()
        x1 = Match(self.match_id).html
        x2 = json.loads(x1.find_all('script')[13].get_text().replace("\n", " ").replace('window.__INITIAL_STATE__ =','').replace('&dagger;','wk').replace('&amp;','').replace('wkts;','wkts,').replace('wkt;','wkt,').strip().replace('};', "}};").split('};')[0])
        try:
            df1bowl = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['1']['bowlers'])
            d1title = x2['gamePackage']['scorecard']['innings']['1']['title']
            inn1_bowl = pd.concat([df1bowl.drop(['captain','stats','hasVideoId','trackingName'], axis=1),df1bowl.stats.apply(Match.flatten)], axis=1)
            inn1_bowl['PlayerID'] = inn1_bowl['href'].apply(lambda x: Match.url_to_id(x))
            inn1_bowl = inn1_bowl.drop(['href'], axis=1)
            inn1_bowl.columns = ['fullname','name','role','overs','maidens','runs','wickets','economy','wides','nballs','id']
            inn1_bowl = inn1_bowl[['id','fullname','name','overs','maidens','runs','wickets','economy','wides','nballs','role']]
            inn1_bowl = inn1_bowl.to_dict(orient='records')
        except:
            inn1_bowl = None
            pass

        try:
            df2bowl = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['2']['bowlers'])
            d2title = x2['gamePackage']['scorecard']['innings']['2']['title']
            inn2_bowl = pd.concat([df2bowl.drop(['captain','stats','hasVideoId','trackingName'], axis=1),df2bowl.stats.apply(Match.flatten)], axis=1)
            inn2_bowl['PlayerID'] = inn2_bowl['href'].apply(lambda x: Match.url_to_id(x))
            inn2_bowl = inn2_bowl.drop(['href'], axis=1)
            inn2_bowl.columns = ['fullname','name','role','overs','maidens','runs','wickets','economy','wides','nballs','id']
            inn2_bowl = inn2_bowl[['id','fullname','name','overs','maidens','runs','wickets','economy','wides','nballs','role']]
            inn2_bowl = inn2_bowl.to_dict(orient='records')
        except:
            inn2_bowl = None
            pass

        try:
            df3bowl = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['3']['bowlers'])
            d3title = x2['gamePackage']['scorecard']['innings']['3']['title']
            inn3_bowl = pd.concat([df3bowl.drop(['captain','stats','hasVideoId','trackingName'], axis=1),df3bowl.stats.apply(Match.flatten)], axis=1)
            inn3_bowl['PlayerID'] = inn3_bowl['href'].apply(lambda x: Match.url_to_id(x))
            inn3_bowl = inn3_bowl.drop(['href'], axis=1)
            inn3_bowl.columns = ['fullname','name','role','overs','maidens','runs','wickets','economy','wides','nballs','id']
            inn3_bowl = inn3_bowl[['id','fullname','name','overs','maidens','runs','wickets','economy','wides','nballs','role']]
            inn3_bowl = inn3_bowl.to_dict(orient='records')
        except:
            inn3_bowl = None
            pass

        try:
            df4bowl = pd.DataFrame(x2['gamePackage']['scorecard']['innings']['4']['bowlers'])
            d4title = x2['gamePackage']['scorecard']['innings']['4']['title']
            inn4_bowl = pd.concat([df4bowl.drop(['captain','stats','hasVideoId','trackingName'], axis=1),df4bowl.stats.apply(Match.flatten)], axis=1)
            inn4_bowl['PlayerID'] = inn4_bowl['href'].apply(lambda x: Match.url_to_id(x))
            inn4_bowl = inn4_bowl.drop(['href'], axis=1)
            inn4_bowl.columns = ['fullname','name','role','overs','maidens','runs','wickets','economy','wides','nballs','id']
            inn4_bowl = inn4_bowl[['id','fullname','name','overs','maidens','runs','wickets','economy','wides','nballs','role']]
            inn4_bowl = inn4_bowl.to_dict(orient='records')
        except:
            inn4_bowl = None
            pass

        return(inn1_bowl, inn2_bowl, inn3_bowl, inn4_bowl)



    @staticmethod
    def get_recent_matches(date=None):
        if date:
            url = "http://www.espncricinfo.com/ci/engine/match/index.html?date=%sview=week" % date
        else:
            url = "http://www.espncricinfo.com/ci/engine/match/index.html?view=week"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        return [x['href'].split('/',4)[4].split('.')[0] for x in soup.findAll('a', href=True, text='Scorecard')]
