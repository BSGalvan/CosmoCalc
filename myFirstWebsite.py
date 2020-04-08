#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:46:31 2020

@author: Bharath Saiguhan
"""

from flask import Flask, render_template, request
import pandas as pd
import cosmoFuncs as cF

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    errors = ""
    if request.method == "POST":
        z_user = None
        H = None
        Omega_m = None
        form_inputs = request.form
        results = {}
        # print(form_inputs)
        try:
            z_user = float(form_inputs['redshift'])
        except:
            errors += "{!r} is not a number! \n".format(
                form_inputs['redshift'])
        try:
            H = float(form_inputs['hubblepar'])
        except:
            errors += "{!r} is not a number! \n".format(
                form_inputs['hubblepar'])
        try:
            Omega_m = float(form_inputs['omega_m'])
        except:
            errors += "{!r} is not a number! \n".format(form_inputs['omega_m'])
        if len(errors) != 0 :
            return render_template("home.html", errors = errors)
        if len(errors) == 0 and z_user is not None and H is not None and Omega_m is not None:
            params = [cF.convertH(H), 1 - Omega_m, Omega_m]
            results['t_0'] = cF.t(params, 0.0)
            results['t_z'] = cF.t(params, z_user)
            results['LTT'] = cF.lightTravelTime(params, z_user)
            results['d_c'] = cF.comoving_distance(params, z_user)
            results['V_c'] = cF.comoving_volume(params, z_user)
            results['d_a'] = cF.angulardiameter_distance(params, z_user)
            results['ang_scale'] = cF.linear_scale(params, z_user)
            results['d_l'] = cF.luminosity_distance(params, z_user)
            results_df = pd.DataFrame.from_dict(results, orient='index')
            results_table = results_df.to_html(classes="results")
            return render_template("home.html", table=results_table)
    if request.method == "GET":
        return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
