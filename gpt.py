from openai import OpenAI

client = OpenAI()

generate_sql_prompt = """
You are given an example list of question in plain English and SQL query correspondence. 

{similar_questions}

Use the database schemas given below to construct your SQL schemas.
{database_tables}

Produce an SQL query given the following user question.
Question:
{user_prompt}
Query:

"""

translate_prompt = """
You are given ten sentences in English and is asked to translate them to Turkish.
Don't add any additional information or explanation on your answer, just translate the sentences to Turkish in a list.

Keep the specific names as they are, don't translate them. A good indicator to understand if a name is specific is to check if it is written with capital letters.

An example behaviour we are expecting is:
Given the following sentences in English:
1. I am a student.
2. What is a good way to learn Turkish?
3. What age Mert learned to play table tennis?

You should output the following in Turkish:
1. Ben bir öğrenciyim.
2. Türkçe öğrenmenin iyi bir yolu nedir?
3. "Mert" kaç yaşında masa tenisi oynamayı öğrendi?

Let's begin:
Here are your sentences to translate:
"""


class OpenAIWrapper:
    @staticmethod
    def generate_sql_for_promt(database_name, database_tables, user_prompt, similar_items=[]):
        similar_questions = []
        if similar_items:
            similar_questions = [f"Question:\n{q[1]} \nQuery:\n{q[2]}\n" for q in similar_items]

        """
        print(generate_sql_prompt.format(database_name=database_name,
                                         database_tables=database_tables,
                                         user_prompt=user_prompt,
                                         similar_questions="\n".join(similar_questions))),
        """

        response = client.chat.completions.create(
            model="gpt-4-32k",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SQL developer translating user prompts to SQL queries.",
                },
                {"role": "user", "content": generate_sql_prompt.format(database_name=database_name,
                                                                       database_tables=database_tables,
                                                                       user_prompt=user_prompt,
                                                                       similar_questions="\n".join(similar_questions))},
            ])

        return response.choices[0].message.content

    @staticmethod
    def translate_to_turkish(user_promt_list):
        prompt = translate_prompt
        for i, p in enumerate(user_promt_list):
            prompt += f"{i + 1}. {p}\n"

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a translator, translating English sentences to Turkish.",
                },
                {"role": "user", "content": prompt},
            ])

        return response.choices[0].message.content

    @staticmethod
    def translate_to_english(question):
        prompt = question

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a translator, translating Turksish sentences to English.",
                },
                {"role": "user", "content": prompt},
            ])

        return response.choices[0].message.content
