from openai import OpenAI

client = OpenAI()

generate_sql_prompt = """
You are given a database to query and a user prompt. Write a SQL query that answers the user's question.

Keypoints you need to follow:
- Try not to use "IN", "OR", and "LEFT JOIN" keywords in your query.
- Only output the SQL query that fetch the information user asked for inside the database, do not output the results or comment on the SQL you generated.
- If the user prompt contains a specific name in Turkish, translate it to English too (Such as 'ABD' -> 'USA').
- Only use table columns mentioned in database schema, don't use any other columns. Also, only fetch the information user asks for from the set of defined column names. 

In the light of the keypoints above, you are given the following information about the database schema and the user prompt:
Name of the database you will work is {database_name}. Here is the tables in the database with column names:
{database_tables}

The user prompt is given in Turkish, but you should write the SQL query in English. Here is the user prompt:
{user_prompt}

Here is the SQL query you should write:
SELECT"""

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
    def generate_sql_for_promt(database_name, database_tables, user_prompt):
        print(generate_sql_prompt.format(database_name=database_name,
                                         database_tables=database_tables,
                                         user_prompt=user_prompt))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SQL developer translating user prompts to SQL queries.",
                },
                {"role": "user", "content": generate_sql_prompt.format(database_name=database_name,
                                                                       database_tables=database_tables,
                                                                       user_prompt=user_prompt)},
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
