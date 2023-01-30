import os
import requests

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
    twi_prompt = "give 3 celebrity twitter handles with no name, just starting with @"
    if request.method == "GET":
        response_twi = openai.Completion.create(
                model="text-davinci-003",
                prompt=twi_prompt,
                temperature=0.6,
                max_tokens=1000,
                )

    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
            max_tokens=1000,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result, twi=response_twi.choices[0].text)


def generate_prompt(animal):
    return """
    I want you to create a virtual world idea elevator pitch based on Twitter handle """+animal+"""and sponsored by big brand Twitter handle.
Add the idea of monetization with digital items or NFT.
write it as discussion provocative tweet and include given handle """+animal+""" and big brand twitter handle. All hashtags should be in the very end. Before all hashtags include @x_la_official. Output should not be more than 280 total.
"""
