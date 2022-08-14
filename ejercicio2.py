
class Group:
    record_match = []
    table_scores = {}

    def __init__(self, arr_team):
        #Constructor
        validation,error = self.validate_constructor(arr_team)

        if validation and not(error):
            self.teams = arr_team[0], arr_team[1], arr_team[2], arr_team[3]
            
            for team in self.teams:
                self.table_scores[team.lower()] = {
                    "Ganados" : 0,
                    "Empates" : 0,
                    "Perdidos" : 0,
                    "A Favor" : 0,
                    "En Contra" : 0,
                    "Diferencia" : 0,
                    "Puntos" : 0
                }
        else:
            raise Exception(error)

    def match(self, arr_match):

        validation, error = self.validate_format_match(arr_match)

        if validation and not(error):
            validation, error = self.validate_in_record_match(arr_match)
            if validation and not(error):
                arr_match[0] = arr_match[0].lower()
                arr_match[2] = arr_match[2].lower()
                self.record_match.append(tuple(arr_match))
                self.generate_statistics(arr_match)
            else:
                raise Exception(error)
        else:
            raise Exception(error)
    
    def result(self):
        print(self.table_scores)

    def set_statistics_team_winner(self, team_winner, score_winner, score_loser):
        score_team = self.table_scores.get(team_winner)

        #Actualizamos la estadistica del equipo ganador
        score_team.update(  {   "Ganados" : score_team["Ganados"] + 1   }   )
        score_team.update(  {   "A Favor" : score_team["A Favor"] + score_winner    }    )
        score_team.update(  {   "En Contra" : score_team["En Contra"] + score_loser   })
        score_team.update(  {   "Diferencia" : score_team["A Favor"] - score_team["En Contra"]  }   )
        score_team.update(  {   "Puntos" : (score_team["Ganados"]*3) + score_team["Empates"]    })

    def set_statistics_team_loser(self, team_loser, score_loser, score_winner):
        score_team = self.table_scores.get(team_loser)

        #Actualizamos la estadistica del equipo perdedor
        score_team.update(  {   "Perdidos" : score_team["Perdidos"] + 1     }   )
        score_team.update(  {   "A Favor" : score_team["A Favor"] + score_loser     }   )
        score_team.update(  {   "En Contra" : score_team["En Contra"] + score_winner   })
        score_team.update(  {   "Diferencia" : score_team["A Favor"] - score_team["En Contra"]  }   )
        score_team.update(  {   "Puntos" : (score_team["Ganados"]*3) + score_team["Empates"]    })
    
    def generate_statistics(self,arr_match):
        team1, score1 = arr_match[0], arr_match[1]
        team2, score2 = arr_match[2], arr_match[3]
        
        if score1 != score2:
            (team_winner, score_winner) = (team1,score1) if score1>score2 else (team2,score2)
            (team_loser, score_loser) = (team1,score1) if team_winner != team1 else (team2,score2)

            self.set_statistics_team_winner(team_winner, score_winner, score_loser)
            self.set_statistics_team_loser(team_loser, score_loser, score_winner)

        else:
            print("Hay empate")

    def validate_constructor(self,arr_team):
        arr_team = set(arr_team)

        if len(arr_team) != 4:
            error = "Cantidad incorrecta de equipos en el Grupo."
            return False,error

        for elemt in arr_team:
            try:
                validation = False if not(elemt.isalpha()) else True
            except AttributeError:
                #Error que lanza python si element es un tipo de dato diferente de (str)
                validation = False
            finally:
                if not(validation):break

        error = None if validation else 'Formato incorrecto en el nombre de los Equipos.'
        return validation,error

    def validate_format_match(self,arr_match):
        if len(arr_match) != 4:
            error = "Cantidad incorrecta de parametros para registrar partido."
            return False,error
        
        for index, element in enumerate(arr_match):
            if not(index%2):
                #Cuando estamos en las posiciones par del array (Nombre de los equipos)
                if not(type(element) == str) or not(element in self.teams):
                    validation = False
                    break
                if index == 2:
                    if (arr_match[0]).lower() == (arr_match[2]).lower():
                        validation = False
                        break
                try:
                    validation = False if not(str(element).isalpha()) else True
                except AttributeError:
                    validation = False
                finally:
                    if not(validation):break
            else:
                #Cuando estamos en las posiciones impares del array (Score de los equipos)
                if not(type(element) == int):
                    validation = False
                    break
                try:
                    validation = False if not(str(element).isdigit()) else True
                except AttributeError:
                    validation = False
                finally:
                    if not(validation):break
                
        error = None if validation else 'Formato incorrecto, para registrar partido.'
        return validation,error

    def validate_in_record_match(self,arr_match):
        validation = True

        for match in self.record_match:
            if ( (arr_match[0]).lower() in match ) and ( (arr_match[2]).lower() in match ):
                validation = False
                break
        
        error = None if validation else 'Estos equipos ya han jugado.'
        return validation, error


arr_team = ["Colombia","Japon","Senegal","Polonia"]
arr_match = ["Colombia",2,"Senegal",3]
arr_match1 = ["Japon",2,"Senegal",3]


grupo = Group( arr_team )

grupo.match(arr_match)
grupo.match(arr_match1)
grupo.result()
# print(grupo.record_match)
#print(grupo.table_scores)
# print(grupo.teams)