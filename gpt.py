from openai import OpenAI

client = OpenAI()

prompt = """
You are given a database to query and a user prompt. Write a SQL query that answers the user's question.

Name of the database you will work is {database_name}. The database contains the following tables:
{database_tables}

The user prompt is:
{user_prompt}

Please only output the SQL query that could fetch the information user asked for inside the database, do not output the results or comment on the SQL you generated.
Also, only use table columns mentioned in database schema, don't use any other columns.

SELECT"""


class OpenAIWrapper:
    @staticmethod
    def generate_sql_for_promt(database_name, database_tables, user_prompt):

        print(prompt.format(database_name=database_name,
                            database_tables=database_tables,
                            user_prompt=user_prompt))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an SQL developer translating user prompts to SQL queries.",
                },
                {"role": "user", "content": prompt.format(database_name=database_name,
                                                          database_tables=database_tables,
                                                          user_prompt=user_prompt)},
            ])

        return response.choices[0].message.content
