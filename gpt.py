import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ.get("GPT_PERSONAL"))

c3_fixed_prompt = \
    [
        {
            "role": "system",
            "content": "You are now an excellent SQL writer, first I'll give you some tips and examples, and I need you to remember the tips, and do not make same mistakes."
        },
        {
            "role": "user",
            "content": """Tips 1: 
            Question: Which A has most number of B?
            Gold SQL: select A from B group by A order by count ( * ) desc limit 1;
            Notice that the Gold SQL doesn't select COUNT(*) because the question only wants to know the A and the number should be only used in ORDER BY clause, there are many questions asks in this way, and I need you to remember this in the the following questions."""
        },
        {
            "role": "assistant",
            "content": "Thank you for the tip! I'll keep in mind that when the question only asks for a certain field, I should not include the COUNT(*) in the SELECT statement, but instead use it in the ORDER BY clause to sort the results based on the count of that field."
        },
        {
            "role": "user",
            "content": """Tips 2: 
            Don't use "IN", "OR", "LEFT JOIN" as it might cause extra results, use "INTERSECT" or "EXCEPT" instead, and remember to use "DISTINCT" or "LIMIT" when necessary.
            For example, 
            Question: Who are the A who have been nominated for both B award and C award?
            Gold SQL should be: select A from X where award = 'B' intersect select A from X where award = 'C';"""
        },
        {
            "role": "assistant",
            "content": "Thank you for the tip! I'll remember to use \"INTERSECT\" or \"EXCEPT\" instead of \"IN\", \"OR\", or \"LEFT JOIN\" when I want to find records that match or don't match across two tables. Additionally, I'll make sure to use \"DISTINCT\" or \"LIMIT\" when necessary to avoid repetitive results or limit the number of results returned."
        },
    ]

c3_generate_sql_prompt = """
### Complete sqlite SQL query only and with no explanation, and do not select extra columns that are not explicitly requested in the query.
### Sqlite SQL tables, with their properties:
#
{database_tables}
{foreign_keys}
### {user_prompt}
SELECT"""

c3_generate_sql_prompt_with_examples = """
### Complete sqlite SQL query only and with no explanation, and do not select extra columns that are not explicitly requested in the query.
### Followings are example user prompts and generated SQL queries. I will ask a similar question and you need to generate an SQL query for it.
{similar_questions}

### Sqlite SQL tables, with their properties:
#
{database_tables}
{foreign_keys}
### Generate the query for the following
Question:
{user_prompt}
Query:
SELECT"""

### FILTER


filter_tables_prompt = """
Given the database schema and question, perform the following actions:
1 - Rank all the tables based on the possibility of being used in the SQL according to the question from
the most relevant to the least relevant, Table or its column that matches more with the question words is
highly relevant and must be placed ahead.
2 - Check whether you consider all the tables.
3 - Output a list object in the order of step 2, Your output should contain all the tables. The format should
be like:
[
"table_1", "table_2", ...
]
Schema:
{database_tables}
Question:
### {user_prompt}

Only output the JSON Array with table names inside it. Do NOT comment.
Related Tables
[
"""

filter_columns_prompt = """
Given the database tables and question, perform the following actions:
1 - Rank the columns in each table based on the possibility of being used in the SQL, Column that
matches more with the question words or the foreign key is highly relevant and must be placed ahead.
You should output them in the order of the most relevant to the least relevant.
Explain why you choose each column.
2 - Output a JSON object that contains all the columns in each table according to your explanation. The
format should be like:
{{
"table_1": ["column_1", "column_2", ......],
"table_2": ["column_1", "column_2", ......],
"table_3": ["column_1", "column_2", ......],
......
}}
Only output the JSON object with table names and column names inside it. Don't comment on why.
Schema:
{database_tables}
Foreign keys:
{foreign_keys}
Question:
### {user_prompt}

Only output the JSON object with table names and column names inside it. Do NOT comment.
Related Tables with columns:
{{
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



MODEL = 'gpt-4'  # "gpt-4"  # "gpt-3.5-turbo"

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
    def generate_sql_for_prompt_c3(database_name, database_tables, foreign_keys, user_prompt, N=20):
        database_tables = '# ' + database_tables.replace('\n', '\n# ')
        foreign_keys = '# ' + foreign_keys.replace('\n', '\n# ')

        print("Generate sql main query:")
        print(c3_generate_sql_prompt.format(database_name=database_name,
                                            database_tables=database_tables,
                                            foreign_keys=foreign_keys,
                                            user_prompt=user_prompt))

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.75,
            messages=[
                *c3_fixed_prompt,
                {"role": "user", "content": c3_generate_sql_prompt.format(database_name=database_name,
                                                                          database_tables=database_tables,
                                                                          foreign_keys=foreign_keys,
                                                                          user_prompt=user_prompt)},
            ],
            n=N)

        responses = []
        for i in range(N):
            responses.append(
                'SELECT ' + ' '
                .join(response.choices[i].message.content
                      .replace('\n', ' ').split())
            )

        return responses

    @staticmethod
    def generate_sql_for_prompt_c3_with_examples(database_name, database_tables, foreign_keys, user_prompt, similar_items, N=20):
        database_tables = '# ' + database_tables.replace('\n', '\n# ')
        foreign_keys = '# ' + foreign_keys.replace('\n', '\n# ')

        similar_questions = [f"Question:\n{q[1]} \nQuery:\n{q[2]}\n" for q in similar_items]
        similar_questions = "\n".join(similar_questions)

        print("Generate sql main query:")
        print(c3_generate_sql_prompt.format(database_name=database_name,
                                            database_tables=database_tables,
                                            foreign_keys=foreign_keys,
                                            user_prompt=user_prompt))

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.75,
            messages=[
                *c3_fixed_prompt,
                {"role": "user", "content": c3_generate_sql_prompt_with_examples.format(database_name=database_name,
                                                                                        database_tables=database_tables,
                                                                                        foreign_keys=foreign_keys,
                                                                                        user_prompt=user_prompt,
                                                                                        similar_questions=similar_questions)},
            ],
            n=N)

        responses = []
        for i in range(N):
            responses.append(
                'SELECT ' + ' '
                .join(response.choices[i].message.content
                      .replace('\n', ' ').split())
            )

        return responses

    @staticmethod
    def filter_related_tables(database_name, database_tables, user_prompt, N=10):
        database_tables = '# ' + database_tables.replace('\n', '\n# ')


        print("Filtering related tables:")
        print( filter_tables_prompt.format(database_tables=database_tables,
                                                                        user_prompt=user_prompt))


        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.75,
            messages=[
                {
                    "role": "system",
                    "content": "You are now an excellent SQL writer, deciding related tables of the given user prompts and only outputing JSON."
                },
                {"role": "user", "content": filter_tables_prompt.format(database_tables=database_tables,
                                                                        user_prompt=user_prompt)},
            ],
            n=N)

        responses = []
        for i in range(N):
            print(response.choices[i].message.content)
            responses.append('[ '+ response.choices[i].message.content)
        return responses


    @staticmethod
    def filter_related_columns(database_name, database_tables, foreign_keys, user_prompt, N=10):
        database_tables = '# ' + database_tables.replace('\n', '\n# ')
        foreign_keys = '# ' + foreign_keys.replace('\n', '\n# ')

        """
        print("Filtering related columns:")
        print(filter_columns_prompt.format(database_tables=database_tables,
                                           foreign_keys=foreign_keys,
                                           user_prompt=user_prompt))
        """

        response = client.chat.completions.create(
            model=MODEL,
            temperature=0.75,
            messages=[
                {
                    "role": "system",
                    "content": "You are now an excellent SQL writer, deciding related tables and their columns of the given user prompts."
                },
                {"role": "user", "content": filter_columns_prompt.format(database_tables=database_tables,
                                                                         foreign_keys=foreign_keys,
                                                                         user_prompt=user_prompt)},
            ],
            n=N)

        responses = []
        for i in range(N):
            print(response.choices[i].message.content)
            responses.append('{ ' + response.choices[i].message.content)
        return responses

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