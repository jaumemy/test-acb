import requests

from django.db import transaction

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import MatchEvent
from .serializers import MatchEventSerializer


endpoint = "https://api2.acb.com/api/v1/openapilive/PlayByPlay/matchevents"
token = (
    "H4sIAAAAAAAAA32Ry3aqMBSG36iLi7qOw4oFk9PEQyohZEYilkCirIMF5OkbOmiVQUdZ+/bv798pbrAUkVR7BUEyAhcr0IIzWcoArEDdMBrA9VNxg"
    "5BPiQqp1wDGnEGTp/009MIZD4sd0dIsSxFMw7ATUaL2ulWxN7jZGV2poTegehuvrzKiTp7iRniL7zxhoZuzTZl5uhPKTTkD055Q+qTkkR6Pka4y9q"
    "NDTDjyu/hg6zxdVnkajq+UazmZ0Bstz7gT5j5HGhmtx4MPa9s/34dyxvUj41LL22OdMOxkqdXxSZN5d9r10BwNDS2v5Vh/zPg8ntD6W9OhwzHVvfD"
    "nPU033ZFHL495uinlmTTcsv/q5Yshmc+2GdNB8fXWs32wK3a4Ej7UMx8JT13LBy3LvUdsNXDDjf2P2X3YW6+EgQZUlwEf6gXeIgdvk4W9my52z2pf"
    "AReNcY8q1KPte4+CXtn/cub9p/jJef7j/Xvf/j150Sag6C1ctS41qVe3p6Fml5U4gf/xdecli8sn/TA0Eb8CAAA="
)


class PbpLeanView(APIView):

    def get(self, request, game_id):

        matchevent_qs = MatchEvent.objects.filter(game_id=game_id)

        if matchevent_qs.exists():
            print("MatchEvent exists")
            result = Response(MatchEventSerializer(matchevent_qs, many=True).data)

        else:
            print("MatchEvent does not exist")
            try:
                headers = {
                    "Authorization": f"Bearer {token}"
                }
                params = {
                    "idMatch": game_id
                }
                response = requests.get(endpoint, headers=headers, params=params)

                if response:
                    with transaction.atomic():
                        for el in response.json():
                            MatchEvent.objects.create(
                                game_id=el.get("id_match"),
                                team_id=el.get("team").get("id_team_denomination") if el.get("team") else None,
                                player_license_id=el.get("id_license"),
                                action_time=el.get("crono"),
                                action_type=el.get("id_playbyplaytype")
                            )

                    matchevent_qs = MatchEvent.objects.filter(game_id=game_id)
                    result = Response(MatchEventSerializer(matchevent_qs, many=True).data)

                else:
                    result = Response({"info": "No data found"})

            except Exception as e:
                print("Error: ", e)
                result = Response({"error": str(e)}, status=500)

        return result


class GameLeadersView(APIView):

    def get(self, request, game_id):

        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "idMatch": game_id
        }
        response = requests.get(endpoint, headers=headers, params=params)

        team_leaders_dict = {
            "home_team": {},
            "away_team": {}
        }

        for el in response.json():

            try:
                team = "home_team" if el.get("local") else "away_team"
                player_dict = {
                    "name": el.get("license").get("licenseAbbrev"),
                    "points": el.get("statistics").get("points"),
                    "rebounds": el.get("statistics").get("total_rebound"),
                }
                team_leaders_dict[team][el.get("id_license")] = player_dict

            except AttributeError:
                pass

        home_team_leaders = sorted(
            team_leaders_dict["home_team"].items(),
            key=lambda x: (x[1]["points"], x[1]["rebounds"]),
            reverse=True
        )
        away_team_leaders = sorted(
            team_leaders_dict["away_team"].items(),
            key=lambda x: (x[1]["points"], x[1]["rebounds"]),
            reverse=True
        )

        return Response({
            "home_team_leaders": home_team_leaders,
            "away_team_leaders": away_team_leaders
        })


class GameBiggestLeadView(APIView):

    def get(self, request, game_id):

        headers = {
            "Authorization": f"Bearer {token}"
        }
        params = {
            "idMatch": game_id
        }
        response = requests.get(endpoint, headers=headers, params=params)

        result = {
            "home_team": 0,
            "away_team": 0
        }

        for el in response.json():
            diff = el.get("score_local") - el.get("score_visitor")
            result["home_team"] = max(result["home_team"], diff)
            result["away_team"] = max(result["away_team"], -diff)

        return Response(result)
