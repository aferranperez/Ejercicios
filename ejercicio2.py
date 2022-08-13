
class Group:

    def __init__(self, arr_team):
        #Constructor
        validation,error = self.validate_constructor(arr_team)

        if validation and not(error):
            self.team1 = arr_team[0]
            self.team2 = arr_team[1]
            self.team3 = arr_team[2]
            self.team4 = arr_team[3]
        else:
            raise Exception(error)

    
    def match(self, arr_match):
        
        validation, error = self.validate_format_match(arr_match)
        if validation and not(error):
            print("Todo OK")
        else:
            raise Exception(error)


    def validate_constructor(self,arr_team):
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
                try:
                    validation = False if not(element.isalpha()) else True
                except AttributeError:
                    validation = False
                finally:
                    if not(validation):break
            else:
                #Cuando estamos en las posiciones impares del array (Score de los equipos)
                try:
                    validation = False if not(element.isnumeric()) else True
                except AttributeError:
                    validation = False
                finally:
                    if not(validation):break
                
        error = None if validation else 'Formato incorrecto, para registrar partido.'
        return validation,error


arr_team = ["Colombia","Japon","Senegal","Polonia"]
arr_match = ["Colombia",2,"Japon",3]

grupo = Group( arr_team )
print(grupo.team1)
#grupo.match(arr_match)

for index,element in enumerate(arr_team):
    print(index%2)
