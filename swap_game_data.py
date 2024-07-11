MAX_PLAYERS:int = 8 #Don't be fooled, this is mutable
PLAYER_IMAGE_WIDTH:int = 136
PLAYER_IMAGE_HEIGHT:int = 166

PATH_IMAGE_FOLDER:str = 'img\\'
PATH_PLAYER_BG:str = f'{PATH_IMAGE_FOLDER}8624_crumpled_white_paper_texture_by_melemel.png'
PATH_IMG_PRESETS:str = f'{PATH_IMAGE_FOLDER}portraits'
PATH_PLACEHOLDER_AVATAR:str = f'{PATH_IMAGE_FOLDER}vecteezy_illustration-of-human-icon-vector-user-symbol-icon-modern_8442086.jpg'
PATH_TEST_IMAGE:str = f'{PATH_IMAGE_FOLDER}testimg.png'

class PersonObject:
    def __init__(self, id:int , name:str , age:int , sex:str , race:str , path:str) -> None:
        self.id = id
        self.name: str = name
        self.identity: str = name
        self.age: int = age
        self.sex: str = sex
        self.gender: str = sex
        self.race: str = race

        self.current_name: str = name
        #self.current_identity: str = name
        self.current_age: int = age
        #self.current_sex: str = sex
        self.current_gender: str = sex  #aka current_sex
        self.current_race: str = race

        self.original_name: str = name
        self.original_identity: str = name
        self.original_age: int = age
        self.original_sex: str = sex
        self.original_gender: str = sex
        self.original_race: str = race

        self.picture_path:str = path
        self.picture = None

bimboExists: bool = False

#GEORGIA FAMILY
people_georgia = [
    PersonObject(1, 'Georgia', 46, 'Female', 'White', PATH_TEST_IMAGE), #Mom
    PersonObject(2, 'Douglas', 42, 'Male', 'White', PATH_TEST_IMAGE), #Dad
    PersonObject(3, 'Maisy', 20, 'Female', 'White', PATH_TEST_IMAGE),
    PersonObject(4, 'Jackson', 16, 'Male', 'White', '.\\img\\ai_art\\jackson.jpg'),
    PersonObject(5, 'Joel', 1, 'Male', 'White', PATH_TEST_IMAGE), #Maisy 1
]

#CHLOE FAMILY
people_chloe = [
    PersonObject(6, 'Chloe', 46, 'Female', 'White',PATH_TEST_IMAGE), #Mom
    PersonObject(7, 'Thad', 53, 'Male', 'White',PATH_TEST_IMAGE), #Dad
    PersonObject(8, 'Zack', 19, 'Male', 'White',PATH_TEST_IMAGE),
    PersonObject(9, 'Brandon', 17, 'Male', 'White', '.\\img\\ai_art\\brandon.jpg'),
    PersonObject(10, 'Justin', 9, 'Male', 'White',PATH_TEST_IMAGE)
]

#FAITH FAMILY
people_faith = [
    PersonObject(11, 'Faith', 46, 'Female', 'Hispanic', PATH_TEST_IMAGE), #Mom
    PersonObject(12, 'Kevin', 48, 'Male', 'Asian', PATH_TEST_IMAGE), #Dad
    PersonObject(13, 'Theodore', 30, 'Male', 'Hispanic', PATH_TEST_IMAGE),
    PersonObject(14, 'Grace', 30, 'Female', 'Asian', PATH_TEST_IMAGE),
    PersonObject(15, 'Arthur', 22, 'Male', 'Hispanic', PATH_TEST_IMAGE),
    PersonObject(16, 'Samuel', 16, 'Male', 'Hispanic', '.\\img\\ai_art\\samuel.jpg'),
    PersonObject(17, 'Hollie', 11, 'Female', 'White', PATH_TEST_IMAGE), #Theo 1 (White Mother)
    PersonObject(18, 'Peter', 6, 'Male', 'Asian', PATH_TEST_IMAGE), #Grace 1
    PersonObject(19, 'Spencer', 4, 'Male', 'White', PATH_TEST_IMAGE), #Theo 2 (White Mother)
    PersonObject(20, 'Shannon', 3, 'Female', 'Hispanic', PATH_TEST_IMAGE), #Theo 3 (White Mother)
    PersonObject(21, 'Reece', 3, 'Male', 'Hispanic', PATH_TEST_IMAGE), #Arthur 1
    PersonObject(22, 'Charlie', 1, 'Male', 'Hispanic', PATH_TEST_IMAGE), #Arthur 2
    PersonObject(23, 'Henry', 1, 'Male', 'Hispanic', PATH_TEST_IMAGE), #Arthur 3
    PersonObject(24, 'Ben', -1, 'Male', 'White', PATH_TEST_IMAGE) #Theo 4
]

#HANNAH FAMILY
people_hannah = [
    PersonObject(25, 'Hannah', 46, 'Female', 'White', PATH_TEST_IMAGE), #Mom
    PersonObject(26, 'Barry', 36, 'Male', 'White', PATH_TEST_IMAGE), #Dad
    PersonObject(27, 'Thomas', 14, 'Male', 'White', '.\\img\\ai_art\\thomas.jpg')
]

#LILY FAMILY
people_lily = [
    PersonObject(28, 'Lily', 46, 'Female', 'Black', PATH_TEST_IMAGE), #Mom
    PersonObject(29, 'Mark', 38, 'Male', 'Black', PATH_TEST_IMAGE), #Dad 1
    PersonObject(30, 'Scott', 48, 'Male', 'White', PATH_TEST_IMAGE), #Dad 2
    PersonObject(31, 'Scarlett', 14, 'Female', 'Black', '.\\img\\ai_art\\scarlett.jpg'), #Mark
    PersonObject(32, 'Emma', 12, 'Female', 'White', PATH_TEST_IMAGE) #Scott
]

#TIFFANY FAMILY
people_tiffany = [
    PersonObject(33, 'Tiffany', 42, 'Female', 'White', PATH_TEST_IMAGE), #Mom
    PersonObject(34, 'Steven', 42, 'Male', 'White', PATH_TEST_IMAGE), #Dad
    PersonObject(35, 'Tyler', 29, 'Male', 'White', PATH_TEST_IMAGE),
    PersonObject(36, 'Jack', 23, 'Male', 'White', PATH_TEST_IMAGE),
    PersonObject(37, 'Maya', 21, 'Female', 'White', PATH_TEST_IMAGE),
    PersonObject(38, 'Zeke', 19, 'Male', 'White', PATH_TEST_IMAGE),
    PersonObject(39, 'Evan', 19, 'Male', 'White', PATH_TEST_IMAGE),
    PersonObject(40, 'Liza', 15, 'Female', 'White', '.\\img\\ai_art\\liza.jpg'),
    PersonObject(41, 'Estella', 15, 'Female', 'White', '.\\img\\ai_art\\estella.jpg'),
    PersonObject(42, 'Sophie', 11, 'Female', 'White', PATH_TEST_IMAGE), #Tyler 1
    PersonObject(43, 'Zoe', 9, 'Female', 'White', PATH_TEST_IMAGE), #Tyler 2
    PersonObject(44, 'Leah', 5, 'Female', 'White', PATH_TEST_IMAGE), #Tyler 3
    PersonObject(45, 'Samantha', 3, 'Female', 'White', PATH_TEST_IMAGE), #Tyler 4
    PersonObject(46, 'Sarah', 1, 'Female', 'White', PATH_TEST_IMAGE), #Jackson 1
    PersonObject(47, 'Katie', 0, 'Female', 'White', PATH_TEST_IMAGE), #Jackson 2
]

people_tiffany[0].current_age = 46

#BRITANNY AND LEXI FAMILY
people_bri_lexi = [
    PersonObject(48, 'Brittany', 46, 'Female', 'Hispanic', PATH_TEST_IMAGE), #Mom 1
    PersonObject(49, 'Lexi', 46, 'Female', 'White', PATH_TEST_IMAGE), #Mom 2
    PersonObject(50, 'Cindy', 24, 'Female', 'Black', PATH_TEST_IMAGE), #Adopted
    PersonObject(51, 'Darrel', 14, 'Male', "Black", '.\\img\\ai_art\\darrel.jpg'), #Britanny with unknown father
    PersonObject(52, 'Alexa', 3, 'Female', 'Black', PATH_TEST_IMAGE), #Cindy 1
    PersonObject(53, 'Bree', 2, 'Female', 'White', PATH_TEST_IMAGE) #Cindy 2
]

#presets:list = ['Maisy', 'Zack', 'Theodore', 'Grace', 'Arthur', 'Tyler', 'Jack', 'Maya', 'Zeke', 'Evan', 'Cindy']
presets:list = [ #Will eventually become a YAML file that constructs this
    ('Maisy', 20, 'Female', 'White', 'img\\testimg.png'), 
    ('Zack', 19, 'Male', 'White', 'img\\testimg.png'), 
    ('Theodore', 30, 'Male', 'Hispanic', 'img\\testimg.png'), 
    ('Grace', 30, 'Female', 'Asian', 'img\\testimg.png'), 
    ('Arthur', 22, 'Male', 'Hispanic', 'img\\testimg.png'), 
    ('Tyler', 29, 'Male', 'White', 'img\\testimg.png'), 
    ('Jack', 23, 'Male', 'White', 'img\\testimg.png'), 
    ('Maya', 21, 'Female', 'White', 'img\\testimg.png'), 
    ('Zeke', 19, 'Male', 'White', 'img\\testimg.png'), 
    ('Evan', 19, 'Male', 'White', 'img\\testimg.png'), 
    ('Cindy', 24, 'Female', 'Black', 'img\\testimg.png')
]
presets_dict:dict[str,int] = {x[0]: i for i, x in enumerate(presets)} #Later change it to simple data to reduce necessary computation
everyone:list[PersonObject] = people_georgia + people_chloe + people_faith + people_hannah + people_lily + people_tiffany + people_bri_lexi

#TODO: Build list from YAML and add to it if user types a different one, check case sensitivity
races:list = ['White', 'Black', 'Asian', 'Hispanic']

def person_get_help() -> None: #wtf is this name
    p_ids:list = [3, 8, 13, 14, 15, 35, 36, 37, 38, 39, 50]
    for person in everyone:
        if person.id in p_ids:
            person_data:tuple = (person.name, person.age, person.gender, person.race, person.picture_path)
            presets.append(person_data)