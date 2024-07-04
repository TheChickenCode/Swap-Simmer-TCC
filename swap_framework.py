from swap_game_data import *
from random import randint, choices
from numpy import random as rd

######################################
# # # # # # Card Chances # # # # # # #
######################################

card_chances:dict = {'swap_body' : 120
                    ,'swap_sex' : 65
                    ,'swap_age' : 50
                    ,'swap_identity' : 65
                    ,'swap_race' : 40
                    ,'change_sex' : 60
                    ,'change_age' : 55
                    ,'change_race' : 20
                    ,'bimbofy' : 10
                    ,'adapt_to_body' : 2.5
                    ,'adapt_to_mind' : 2.5}

bimbo_himbo_ratio: float = 0.9
bimbo_himbo_bool:bool = randint(1, 10) >= 10*bimbo_himbo_ratio

######################################
# # # # # Swapping Functions # # # # # 
######################################

def swap(actor1: PersonObject, actor2: PersonObject, to_swap: list) -> None:
    '''Internal function used as framework for specific-swap swapping functions'''
    for att in to_swap:
        temp_att = getattr(actor1, att)
        setattr(actor1, att, getattr(actor2, att))
        setattr(actor2, att, temp_att)

def get_player2(index:int) -> int:
    '''Internal function used only by swapping functions'''
    while True:
        p2_index = (index + randint(1,8)) % 8
        if p2_index != index: break
    return p2_index

def swap_body(actor:list[PersonObject], index) -> bool:
    p2_index = get_player2(index)
    swap(actor[index], actor[p2_index], ['picture', 'current_age', 'sex', 'current_race'])
    print(f'Swapping bodies between {actor[index].name} and {actor[p2_index].name}')
    return True

def swap_sex(actor:list[PersonObject], index) -> bool: #TODO: Needs both a before and after sex swap
    p2_index = get_player2(index)
    swap(actor[index], actor[p2_index], ['sex'])
    print(f'Swapping sex between {actor[index].name} and {actor[p2_index].name}')
    return True

def swap_age(actor:list[PersonObject], index) -> bool:
    p2_index = get_player2(index)
    swap(actor[index], actor[p2_index], ['current_age'])
    print(f'Swapping ages between {actor[index].name} and {actor[p2_index].name}')
    return True

def swap_identity(actor:list[PersonObject], index) -> bool:
    p2_index = get_player2(index)
    swap(actor[index], actor[p2_index], ['identity', 'age', 'race', 'gender'])
    print(f'Swapping minds between {actor[index].name} and {actor[p2_index].name}')
    return True

def swap_race(actor:list[PersonObject], index) -> bool:
    p2_index = get_player2(index)
    swap(actor[index], actor[p2_index], ['current_race'])
    print(f'Swapping races between {actor[index].name} and {actor[p2_index].name}')
    return True

def change_sex(actor:list[PersonObject], index) -> bool: #TODO: Needs both a before and after sex swap
    if actor[index].sex == 'Male':
        actor[index].sex = 'Female'
    else:
        actor[index].sex = 'Male'
    print(f'Changing {actor[index].name} into a {actor[index].sex}')
    return True

def change_age(actor:list[PersonObject], index) -> bool:
    age_up:bool = randint(1,2) == 2

    age_change_number = round((rd.gamma(1,2)*1.1)%16)
    if age_change_number < 2: age_change_number = 2
    if age_change_number > 16: age_change_number = 16

    if actor[index].current_age >= 25 or (age_up == True and actor[index].current_age <= 25 and randint(1,1) == 1): round((rd.gamma(1,2)*11)%16)

    if age_up == True:
        actor[index].current_age += age_change_number
        print(f'Changing {actor[index].name} age up by {age_change_number} years')
    else:
        actor[index].current_age -= age_change_number
        if actor[index].current_age <= 11:
            actor[index].current_age = 12
            print(f'Changing {actor[index].name} age down to {age_change_number} years')
        else: 
            print(f'Changing {actor[index].name} age down by {age_change_number} years')
    
    return True

def change_race(actor:list[PersonObject], index) -> bool:
    races:list = ['White', 'Black', 'Asian', 'Hispanic']

    while True:
        race_picked = races[randint(0,3)]
        if actor[index].current_race == race_picked:
            continue
        else:
            actor[index].current_race = race_picked
            break
    print(f'Changing {actor[index].name} into a {race_picked} person')
    return True

def bimbofy(actor:list[PersonObject], index) -> bool:
    if PersonObject.bimboExists == True: return False
    PersonObject.bimboExists = True

    actor[index].age = actor[index].current_age = 24
    actor[index].race = actor[index].current_race
    if randint(1, 10) >= 10*bimbo_himbo_ratio:
        actor[index].current_name = actor[index].identity = 'Drake'
        actor[index].sex = actor[index].gender = actor[index].current_gender = 'Himbo'
    else:
        actor[index].current_name = actor[index].identity = 'Candy'
        actor[index].sex = actor[index].gender = actor[index].current_gender = 'Bimbo'
    print(f'Making {actor[index].name} really dumb and addicted to sex')
    return True

def adapt_to_body(actor:list[PersonObject], index) -> bool:
    if (actor[index].identity == 'Candy' or 'Drake') and (actor[index].current_name != 'Candy' or 'Drake'):
        PersonObject.bimboExists = True

    actor[index].identity = actor[index].current_name
    actor[index].age = actor[index].current_age
    actor[index].gender = actor[index].sex
    actor[index].race = actor[index].current_race
    print(f'Changing {actor[index].name}\'s mind to more suit their body')
    return True

def adapt_to_mind(actor:list[PersonObject], index) -> bool:
    if (actor[index].current_name == 'Candy' or 'Drake') and (actor[index].identity != 'Candy' or 'Drake'):
        PersonObject.bimboExists = False

    actor[index].current_name = actor[index].identity
    actor[index].current_age = actor[index].age
    actor[index].sex = actor[index].gender
    actor[index].current_race = actor[index].race
    print(f'Changing {actor[index].name}\'s body to more suit their mind')
    return True

def new_default(people_list:list[PersonObject]) -> None:
    for c in people_list:
        people_list[c-1].age
        pass
    #What is new default? Do their name change as well or just their originals reset?

def reset_all(people_list:list[PersonObject]) -> None:
    for c in people_list:
        pass

######################################
# # # # # # TEST FUNCTIONS # # # # # #
######################################

def getelder(people:list[PersonObject]) -> list:
    '''Returns list of people aged 66 and above'''
    elder:list = []
    for person in people:
        if person.age >= 66:
            elder.append(person)
    return elder

def getmiddle_age_adults(people:list[PersonObject]) -> list:
    '''Returns list of people aged from 36 to 65 years old'''
    maa:list = []
    for person in people:
        if 65 >= person.age >= 36:
            maa.append(person)
    return maa

def getyoung_adults(people:list[PersonObject]) -> list:
    '''Returns list of people aged from 19 to 35 years old'''
    ya:list = []
    for person in people:
        if 35 >= person.age >= 19:
            ya.append(person)
    return ya

def getteens(people:list[PersonObject]) -> list:
    '''Returns list of people aged from 13 to 18 years old'''
    teens:list = []
    for person in people:
        if 18 >= person.age >= 13:
            teens.append(person)
    return teens

def getkids(people:list[PersonObject]) -> list:
    '''Returns list of people aged from 6 to 12 years old'''
    kids:list = []
    for person in people:
        if 12 >= person.age >= 6:
            kids.append(person)
    return kids

def getbabies(people:list[PersonObject]) -> list:
    '''Returns list of people aged 5 and below'''
    babies:list = []
    for person in people:
        if 5 >= person.age:
            babies.append(person)
    return babies

#################################

def describe_swap(bodies:list[PersonObject]) -> None:
    '''Prints current situation for every PersonObject in the list'''
    for actor in bodies:
        print(f'{actor.name} thinks they are {actor.identity} a {actor.age} years old {actor.race} {actor.gender} in the body of {actor.current_name}, a {actor.current_age} years old {actor.current_race} {actor.sex}.')

def write_swap(actor:PersonObject) -> str:
    '''Returns a string describing a PersonObject current situation'''
    return f'{actor.name} thinks they are {actor.identity} a {actor.age} years old {actor.race} {actor.gender} in the body of {actor.current_name}, a {actor.current_age} years old {actor.current_race} {actor.sex}.'

def prob_range() -> None:
    '''For sampling probabilities, should be used for debugging after manually changing card values in card_chances{}'''
    probabilities = {key: 0 for key in card_chances}

    for _ in range(1000):
        card = ''.join(choices(population= list(card_chances.keys()),
                   weights= list(card_chances.values()),
                   k=1))
        probabilities[card] += 1

    for key, value in probabilities.items():
        print(f'{key} \t {value}')