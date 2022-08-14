from collections import OrderedDict


class Group:
    record_match = []
    table_scores = {}
    ordered_table_scores = []

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
        self.order_result()

        print (
            "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"
            .format('Equipos','Ganados','Empates','Perdidos','A Favor','En Contra', 'Diferencia', 'Puntos')
        )
        print("-" * 120 )

        for team in self.ordered_table_scores:
            key = (team.keys())[0]
            print (
                "{:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15} {:<15}"
                .format(
                    key[0].upper()+key[1:],
                    team[key]['Ganados'], 
                    team[key]['Empates'], 
                    team[key]['Perdidos'],
                    team[key]['A Favor'],
                    team[key]['En Contra'],
                    team[key]['Diferencia'], 
                    team[key]['Puntos']
                )
            )
    
    def order_result(self):

        table_scored_auxiliar = [ 
            [team[0], team[1]['Puntos'], int(team[1]['Diferencia']), team[1]['A Favor'] ] 
            for team in self.table_scores.items()  
        ]
        table_scored_auxiliar = sorted(table_scored_auxiliar, key=lambda x:x[1], reverse=True)
        ordered_name_team = []
        
        for team in table_scored_auxiliar:

            array_aux = filter(lambda x:x[1] == team[1], table_scored_auxiliar)

            if len(array_aux) != 1:
                array_aux = sorted(array_aux, key=lambda x:x[2], reverse=True)

                if len(filter(lambda x:x[2] == team[2], array_aux)) != 1:
                    array_aux = sorted(array_aux, key=lambda x:x[3], reverse=True)
                    
                    if len(filter(lambda x:x[3] == team[3], array_aux)) != 1:
                        print("Ultima tanda de criterios")
                    
            for element in array_aux:
                if not(element[0] in ordered_name_team):
                    ordered_name_team.append(element[0])
            

        for element in ordered_name_team:
            self.ordered_table_scores.append( {element:self.table_scores.get(element)} ) 
        
    def set_statistics_team_winner(self, team_winner, score_winner, score_loser):
        score_team = self.table_scores.get(team_winner)

        #Actualizamos la estadistica del equipo ganador
        score_team.update(  {   "Ganados" : score_team["Ganados"] + 1   }   )
        score_team.update(  {   "A Favor" : score_team["A Favor"] + score_winner    }    )
        score_team.update(  {   "En Contra" : score_team["En Contra"] + score_loser   })
        score_team.update( {   "Diferencia" : self.put_sign_to_diference(score_team["A Favor"], score_team["En Contra"])    })
        score_team.update(  {   "Puntos" : (score_team["Ganados"]*3) + score_team["Empates"]    })

    def set_statistics_team_loser(self, team_loser, score_loser, score_winner):
        score_team = self.table_scores.get(team_loser)

        #Actualizamos la estadistica del equipo perdedor
        score_team.update(  {   "Perdidos" : score_team["Perdidos"] + 1     }   )
        score_team.update(  {   "A Favor" : score_team["A Favor"] + score_loser     }   )
        score_team.update(  {   "En Contra" : score_team["En Contra"] + score_winner   })
        score_team.update( {   "Diferencia" : self.put_sign_to_diference(score_team["A Favor"], score_team["En Contra"])    })
        score_team.update(  {   "Puntos" : (score_team["Ganados"]*3) + score_team["Empates"]    })
    
    def put_sign_to_diference(self, number1, number2):
        return number1-number2 if (number1-number2)<=0 else "+" + str(number1-number2)

    def update_teams_tie(self,team, score1, score2):
        score_team = self.table_scores.get(team)
        score_team.update( {   "Empates" : score_team["Empates"] + 1      })
        score_team.update( {   "A Favor" : score_team["A Favor"] + score1     })
        score_team.update( {   "En Contra" : score_team["En Contra"] + score2     })
        score_team.update( {   "Diferencia" : self.put_sign_to_diference(score_team["A Favor"], score_team["En Contra"])    })
        score_team.update(  {   "Puntos" : score_team["Puntos"] + score_team["Empates"]      })

    def set_statistics_teams_tie(self, team1, score1, team2, score2):
        self.update_teams_tie(team1,score1,score2)
        self.update_teams_tie(team2,score1,score2)

    def generate_statistics(self,arr_match):
        team1, score1 = arr_match[0], arr_match[1]
        team2, score2 = arr_match[2], arr_match[3]
        
        if score1 != score2:
            (team_winner, score_winner) = (team1,score1) if score1>score2 else (team2,score2)
            (team_loser, score_loser) = (team1,score1) if team_winner != team1 else (team2,score2)

            self.set_statistics_team_winner(team_winner, score_winner, score_loser)
            self.set_statistics_team_loser(team_loser, score_loser, score_winner)

        else:
            self.set_statistics_teams_tie( team1, score1, team2, score2)

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


grupo = Group( ["Colombia","Japon","Senegal","Polonia"] )

grupo.match(["Senegal",0,"Colombia",1])
grupo.match(["Japon",0,"Polonia",1])
grupo.match(["Senegal",2,"Japon",2])
grupo.match(["Polonia",0,"Colombia",3])
grupo.match(["Polonia",1,"Senegal",2])
grupo.match(["Colombia",1,"Japon",3])
grupo.result()




