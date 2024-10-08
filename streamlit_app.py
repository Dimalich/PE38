import os
import openai
import streamlit as st
from hh_parser import get_job_description, get_candidate_info

client = openai.Client(
    api_key=os.getenv("OPENAI_API_KEY")
)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу.
Потом представь результат в виде оценки от 1 до 10.
Всегда давай ответы только на русском языке.
""".strip()

def request_gpt(system_prompt, user_prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1000,
        temperature=0,
    )
    return response.choices[0].message.content

st.title("CV Scoring App")

job_description_url = st.text_area("Введите описание вакансии или ссылку на вакансию", key="job_description")
cv_url = st.text_area("Введите резюме или ссылку на резюме", key="cv")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        if job_description_url.startswith("http"):
            job_description = get_job_description(job_description_url)
        else:
            job_description = job_description_url
        
        if cv_url.startswith("http"):
            cv_text = get_candidate_info(cv_url)
        else:
            cv_text = cv_url

        user_prompt = f"# ВАКАНСИЯ\n{job_description}\n\n# РЕЗЮМЕ\n{cv_text}"
        response = request_gpt(SYSTEM_PROMPT, user_prompt)
    st.write(response)
