# This file contains all the functions with API calls to openAI
from openai import OpenAI

client = OpenAI()

def generate_random_name_prompt():
    """
    Function that gets a random first name
    """
    completion = client.chat.completions.create(
        # model="gpt-4o-mini",
        model = "gpt-3.5-turbo-0125",
        messages=[
            {"role": "developer", "content": "Give a random first name"}
        ],
        frequency_penalty=1.0,
        temperature=1.0
    )

    return completion.choices[0].message.content

def favorite_food_question_prompt(name):
    """
    Function that returns a question that asks a user with name=<name> what his/her top 3 favorite foods are 

    Parameters:
     - name(str)
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": f"Ask a user called {name} what his or her top 3 favorite foods are"}
        ]
    )

    return completion.choices[0].message.content


def favorite_food_answer_prompt():
    """
    Function that returns the answer from a user when asked about his/her top 3 favorite foods
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": f"You are a user and you have been asked about what are your top 3 favorite foods. Answer it in a short and simple way. Consider that users can be Omnivore, Vegetarian, Vegan, ..."}
        ]
    )

    return completion.choices[0].message.content


def identify_food_prompt(message):
    """
    Function that identifies the food mentioned in the message passed as a parameter

    Parameters:
    - message(str)

    Returns:
    - json with the format: { 'foods' : [food1, food2, food3] }
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": f"Identify the foods mentioned in the text: '{message}. Return your answer in a json format as follows: ['Pasta', 'Pork', 'Apples'] with key='foods' "}
        ],
        frequency_penalty=1.0,
        temperature=1.0,
        response_format = { "type": "json_object" }
    )

    return completion.choices[0].message.content


def identify_food_category_prompt(food):
    """
    Function that identifies the category of the food passed as a parameter

    Parameters:
    - food(str)

    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "developer", "content": 
                f"""Classify the given food into one of the following groups:

                Vegan: Food that can be eaten by Vegan people
                Vegetarian: Food that can be eaten by Vegetarian people
                Omnivore : Food that can be eaten by Omnivore people

                Name the smallest group that can eat the given food.
                
                Your output should be just the group name"""
            },
            {"role": "user", "content": food}
        ],
    )

    return completion.choices[0].message.content
