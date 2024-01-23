import os

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

class OpenAIWrapper:
    @staticmethod
    def generate_sql_for_promt(database_name, database_tables, user_prompt, similar_items=None):
        similar_questions = []
        if similar_items:
            similar_questions = [f"Question:\n{q[1]} \nQuery:\n{q[2]}\n" for q in similar_items]
        else:
            similar_questions = []

        """
        print(generate_sql_prompt.format(database_name=database_name,
                                         database_tables=database_tables,
                                         user_prompt=user_prompt,
                                         similar_questions="\n".join(similar_questions))),
        """


        response = client.chat.completions.create(
            model="gpt-4",
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
