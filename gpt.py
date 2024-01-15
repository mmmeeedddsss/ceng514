from openai import OpenAI

client = OpenAI()

generate_sql_prompt = """
You are given a list of question in plain English and SQL query correspondence. 

Question: 
What are the country codes of countries where people use languages other than English?
Query: 
SELECT DISTINCT CountryCode FROM countrylanguage WHERE LANGUAGE != "English"

Question: 
What are the names and birth dates of people, ordered by their names in alphabetical order?
Query: 
SELECT Name ,  Birth_Date FROM people ORDER BY Name ASC

Question: 
What are the first names of all players, and their total ranking points?
Query: 
SELECT sum(ranking_points) ,  T1.first_name FROM players AS T1 JOIN rankings AS T2 ON T1.player_id  =  T2.player_id GROUP BY T1.first_name

Question: 
What are the names of documents that use templates with the code BK?
Query: 
SELECT T2.document_name FROM Templates AS T1 JOIN Documents AS T2 ON T1.template_id  =  T2.template_id WHERE T1.template_type_code  =  "BK"

Question: 
Give the name, year of independence, and surface area of the country that has the lowest population.
Query: 
SELECT Name ,  SurfaceArea ,  IndepYear FROM country ORDER BY Population LIMIT 1

Question: 
What other details can you tell me about students in reverse alphabetical order?
Query: 
SELECT other_student_details FROM Students ORDER BY other_student_details DESC

Question: 
What is the earliest date of a transcript release, and what details can you tell me?
Query: 
SELECT transcript_date ,  other_details FROM Transcripts ORDER BY transcript_date ASC LIMIT 1

Question: 
What are the names of cities in Europe for which English is not the official language?
Query: 
SELECT DISTINCT T2.Name FROM country AS T1 JOIN city AS T2 ON T2.CountryCode  =  T1.Code WHERE T1.Continent  =  'Europe' AND T1.Name NOT IN (SELECT T3.Name FROM country AS T3 JOIN countrylanguage AS T4 ON T3.Code  =  T4.CountryCode WHERE T4.IsOfficial  =  'T' AND T4.Language  =  'English')

Question: 
What is the name and capacity for the stadium with the highest average attendance?
Query: 
SELECT name ,  capacity FROM stadium ORDER BY average DESC LIMIT 1

Question:
What are the publishers who have published a book in both 1989 and 1990?
Query:
"SELECT publisher FROM book_club WHERE YEAR  =  1989 INTERSECT SELECT publisher FROM book_club WHERE YEAR  =  1990"

Question: 
How many courses are there?
Query: 
SELECT count(*) FROM Courses

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
    def generate_sql_for_promt(database_name, database_tables, user_prompt):
        """
        print(generate_sql_prompt.format(database_name=database_name,
                                         database_tables=database_tables,
                                         user_prompt=user_prompt))
        """

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
