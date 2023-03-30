import random
import pandas as pd
import streamlit as st
import os
import string
import environ
import json

from datetime import datetime
from pathlib import Path
# Initialise environment variables
env = environ.Env()
environ.Env.read_env()


def read_file(path):
    file = open(path, 'r')
    data = file.read()
    file.close()
    return data


def read_json(path):
    return json.loads(read_file(path))


relation_data = read_json("./data_relation.json")
assignment_options = relation_data["assignment_option"]


def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y)).lower()


def tracking_submission_data(assignment_name, _owner, _uploaded_file_name, _folder_str):
    df = pd.DataFrame(
        {
            'Assignment Name': [assignment_name],
            'Owner': [_owner],
            'Filename': [_uploaded_file_name],
            'Submission Date': [datetime.now()],
            'Points': [0],
            'Review Date': [None]
        },
    )
    filepath = Path(f'{_folder_str}/data.csv')
    if filepath.exists():
        df.to_csv(filepath, mode='a', index=False, header=False)
    else:
        df.to_csv(filepath, mode='a', index=False)


def view_submission_data(_folder_str):
    filepath = Path(f'{_folder_str}/data.csv')
    df = pd.read_csv(filepath)
    st.table(df.sort_values(by='Submission Date', ascending=False))


st.set_page_config(page_title="Java Assignment Submission", page_icon="🎓")
st.markdown("# 🎓 Java Assignment Submission")

form = st.form("assignment-form", clear_on_submit=True)
with form:
    assignment_sel = st.selectbox(
        "Select Java Assignment Option", options=assignment_options)
    owner = st.text_input('Owner: (shortname, ex: nduc)', '')
    uploaded_file = st.file_uploader(
        "Choose a zip file", accept_multiple_files=False)  # , type=['zip']
    submitted = st.form_submit_button("Submit")
    if not owner:
        st.error('Owner required')
        st.stop()
    if not uploaded_file:
        st.error('Upload File required')
        st.stop()
    if uploaded_file is not None:
        uploaded_file_name = f'{uploaded_file.name.split(".")[0]}_{random_char(5)}.{uploaded_file.name.split(".")[-1]}'
        folder_str = f'{os.path.abspath(os.getcwd())}/submission/data'
        assignment_str = f'{folder_str}/{assignment_sel}/'
        folder_path = Path(assignment_str)
        save_path = Path(f'{assignment_str}{uploaded_file_name}')
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
        with open(save_path, 'wb') as f:
            f.write(uploaded_file.getvalue())
        if save_path.exists():
            tracking_submission_data(
                assignment_sel, owner, uploaded_file_name, folder_str)
            view_submission_data(folder_str)
            st.success(
                f'Assignment={assignment_sel} - '
                f'Owner={owner} - '
                f'File={uploaded_file_name} is successfully saved!',
                icon="✅"
            )
