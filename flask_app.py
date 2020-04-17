#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:46:31 2020

@author: Bharath Saiguhan
"""

from flask import Flask, render_template, request
import pandas as pd
import cosmoFuncs as cf

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    error_red = error_h = error_m = error_vac = ""
    if request.method == "POST":
        z_user = None
        H = None
        Omega_m = None
        Omega_vac = None
        form_inputs = request.form
        results = {}
        # print(form_inputs)
        try:
            z_user = float(form_inputs['redshift'])
        except:
            error_red += "{!r} is not a number! Enter a valid redshift.".format(
                form_inputs['redshift'])
        try:
            H = float(form_inputs['hubblepar'])
        except:
            error_h += "{!r} is not a number! Enter a valid value for the Hubble parameter.".format(
                form_inputs['hubblepar'])
        try:
            Omega_m = float(form_inputs['omega_m'])
        except:
            error_m += "{!r} is not a number! Enter a valid value for mass density.".format(
                form_inputs['omega_m'])
        if len(error_red) != 0 or len(error_m) != 0 or len(error_h) != 0:
            return render_template("home.html", error_1=error_red, error_2=error_h, error_3=error_m, error_4=error_vac)
        if len(error_red) == 0 and len(error_m) == 0 and len(error_h) == 0 and z_user is not None and H is not None and Omega_m is not None:
            z_user = -1 * z_user if z_user < 0 else z_user
            if request.form['submit_button'] == "Flat":
                params = [H, 1 - Omega_m, Omega_m]
                if (cf.t(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], 0.0) < 1):
                    results['Age of Universe (at z = 0) [in Myr]'] = "{:.3f}".format(cf.t(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], 0.0) * 1000)
                else:
                    results['Age of Universe (at z = 0) [in Gyr]'] = "{:.3f}".format(cf.t(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], 0.0))

                if (cf.t([cf.convertH(H), 1 - Omega_m, Omega_m], z_user) < 1):
                    results['Age of Universe (at z = {redshift:.3f}) [in Myr]'.format(
                        redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), 1 - Omega_m, Omega_m], z_user) * 1000)
                else:
                    results['Age of Universe (at z = {redshift:.3f}) [in Gyr]'.format(
                        redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), 1 - Omega_m, Omega_m], z_user))

                if (cf.lightTravelTime(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], z_user) < 1):
                    results['Light Travel Time [in Myr]'] = "{:.3f}".format(cf.lightTravelTime(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], z_user) * 1000)
                else:
                    results['Light Travel Time [in Gyr]'] = "{:.3f}".format(cf.lightTravelTime(
                        [cf.convertH(H), 1 - Omega_m, Omega_m], z_user))

                if (cf.comoving_distance_radial(
                        params, z_user) < 1):
                    results['Comoving Distance [in kpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                        params, z_user) * 1000)
                else:
                    results['Comoving Distance [in Mpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                        params, z_user))

                if (cf.comoving_volume(
                        params, z_user) < 1):
                    results['Comoving Volume [in cubic Mpc]'] = "{:.3f}".format(cf.comoving_volume(
                        params, z_user) * 1e9)
                else:
                    results['Comoving Volume [in cubic Gpc]'] = "{:.3f}".format(cf.comoving_volume(
                        params, z_user))

                if(cf.angulardiameter_distance(
                        params, z_user) < 1):
                    results['Angular Diameter Distance [in kpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                        params, z_user) * 1000)
                else:
                    results['Angular Diameter Distance [in Mpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                        params, z_user))

                if (format(cf.linear_scale(
                        params, z_user) < 1)):
                    results['Angular Scale [in pc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                        params, z_user) * 1000)
                else:
                    results['Angular Scale [in kpc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                        params, z_user))

                if (cf.luminosity_distance(
                        params, z_user) < 1):
                    results['Luminosity Distance [in kpc]'] = "{:.3f}".format(cf.luminosity_distance(
                        params, z_user) * 1000)
                else:
                    results['Luminosity Distance [in Mpc]'] = "{:.3f}".format(cf.luminosity_distance(
                        params, z_user))

                results_df = pd.DataFrame.from_dict(
                    results, orient='index', columns=['Values'])
                results_table = results_df.to_html(classes="results")
                return render_template("home.html", table=results_table, rs=str(z_user), hpar=str(H), om=str(Omega_m), de=str(params[1]))
            elif request.form['submit_button'] == "Open":
                params = [H, 0.0, Omega_m]
                if (cf.t(
                        [cf.convertH(H), 0.0, Omega_m], 0.0) < 1):
                    results['Age of Universe (at z = 0) [in Myr]'] = "{:.3f}".format(cf.t(
                        [cf.convertH(H), 0.0, Omega_m], 0.0) * 1e3)
                else:
                    results['Age of Universe (at z = 0) [in Gyr]'] = "{:.3f}".format(cf.t(
                        [cf.convertH(H), 0.0, Omega_m], 0.0))

                if (cf.t([cf.convertH(H), 0.0, Omega_m], z_user) < 1):
                    results['Age of Universe (at z = {redshift:.3f}) [in Myr]'.format(
                        redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), 0.0, Omega_m], z_user) * 1e3)
                else:
                    results['Age of Universe (at z = {redshift:.3f}) [in Gyr]'.format(
                        redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), 0.0, Omega_m], z_user))

                if (cf.lightTravelTime(
                        [cf.convertH(H), 0.0, Omega_m], z_user) < 1):
                    results['Light Travel Time [in Myr]'] = "{:.3f}".format(cf.lightTravelTime(
                        [cf.convertH(H), 0.0, Omega_m], z_user) * 1000)
                else:
                    results['Light Travel Time [in Gyr]'] = "{:.3f}".format(cf.lightTravelTime(
                        [cf.convertH(H), 0.0, Omega_m], z_user))

                if (cf.comoving_distance_radial(
                        params, z_user) < 1):
                    results['Comoving Distance [in kpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                        params, z_user) * 1e3)
                else:
                    results['Comoving Distance [in Mpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                        params, z_user))

                if (cf.comoving_volume(
                        params, z_user) < 1):
                    results['Comoving Volume [in cubic Mpc]'] = "{:.3f}".format(cf.comoving_volume(
                        params, z_user) * 1e9)
                else:
                    results['Comoving Volume [in cubic Gpc]'] = "{:.3f}".format(cf.comoving_volume(
                        params, z_user))

                if (cf.angulardiameter_distance(
                        params, z_user) < 1):
                    results['Angular Diameter Distance [in Mpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                        params, z_user) * 1e3)
                else:
                    results['Angular Diameter Distance [in Gpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                        params, z_user))

                if (cf.linear_scale(
                        params, z_user) < 1):
                    results['Angular Scale [in pc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                        params, z_user) * 1e3)
                else:
                    results['Angular Scale [in kpc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                        params, z_user))

                if (cf.luminosity_distance(
                        params, z_user) < 1):
                    results['Luminosity Distance [in kpc]'] = "{:.3f}".format(cf.luminosity_distance(
                        params, z_user) * 1e3)
                else:
                    results['Luminosity Distance [in Mpc]'] = "{:.3f}".format(cf.luminosity_distance(
                        params, z_user))

                results_df = pd.DataFrame.from_dict(
                    results, orient='index', columns=['Values'])
                results_table = results_df.to_html(classes="results")
                return render_template("home.html", table=results_table, rs=str(z_user), hpar=str(H), om=str(Omega_m), de=str(params[1]))
            elif request.form['submit_button'] == "General":
                try:
                    Omega_vac = float(form_inputs['omega_vac'])
                except:
                    error_vac += "{!r} is not a number! Enter valid value for dark energy density.".format(
                        form_inputs['omega_vac'])
                if len(error_red) != 0 or len(error_m) != 0 or len(error_h) != 0 or len(error_vac) != 0:
                    return render_template("home.html", error_1=error_red, error_2=error_h, error_3=error_m, error_4=error_vac)
                if len(error_red) == 0 and len(error_m) == 0 and len(error_h) == 0 and len(error_vac) == 0 and Omega_vac is not None:
                    params = [H, Omega_vac, Omega_m]
                    if (cf.t(
                            [cf.convertH(H), Omega_vac, Omega_m], 0.0) < 1):
                        results['Age of Universe (at z = 0) [in Myr]'] = "{:.3f}".format(cf.t(
                            [cf.convertH(H), Omega_vac, Omega_m], 0.0) * 1e3)
                    else:
                        results['Age of Universe (at z = 0) [in Gyr]'] = "{:.3f}".format(cf.t(
                            [cf.convertH(H), Omega_vac, Omega_m], 0.0))

                    if (cf.t([cf.convertH(H), Omega_vac, Omega_m], z_user) < 1):
                        results['Age of Universe (at z = {redshift:.3f}) [in Myr]'.format(
                            redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), Omega_vac, Omega_m], z_user) * 1e3)
                    else:
                        results['Age of Universe (at z = {redshift:.3f}) [in Gyr]'.format(
                            redshift=z_user)] = "{:.3f}".format(cf.t([cf.convertH(H), Omega_vac, Omega_m], z_user))

                    if(cf.lightTravelTime(
                            [cf.convertH(H), Omega_vac, Omega_m], z_user) < 1):
                        results['Light Travel Time [in Myr]'] = "{:.3f}".format(cf.lightTravelTime(
                            [cf.convertH(H), Omega_vac, Omega_m], z_user) * 1e3)
                    else:
                        results['Light Travel Time [in Gyr]'] = "{:.3f}".format(cf.lightTravelTime(
                            [cf.convertH(H), Omega_vac, Omega_m], z_user))

                    if(cf.comoving_distance_radial(
                            params, z_user) < 1):
                        results['Comoving Distance [in kpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                            params, z_user) * 1e3)
                    else:
                        results['Comoving Distance [in Mpc]'] = "{:.3f}".format(cf.comoving_distance_radial(
                            params, z_user))

                    if(cf.comoving_volume(
                            params, z_user) < 1):
                        results['Comoving Volume [in cubic Mpc]'] = "{:.3f}".format(cf.comoving_volume(
                            params, z_user) * 1e9)
                    else:
                        results['Comoving Volume [in cubic Gpc]'] = "{:.3f}".format(cf.comoving_volume(
                            params, z_user))

                    if(cf.angulardiameter_distance(
                            params, z_user) < 1):
                        results['Angular Diameter Distance [in kpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                            params, z_user) * 1e3)
                    else:
                        results['Angular Diameter Distance [in Mpc]'] = "{:.3f}".format(cf.angulardiameter_distance(
                            params, z_user))

                    if(cf.linear_scale(
                            params, z_user) < 1):
                        results['Angular Scale [in pc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                            params, z_user) * 1e3)
                    else:
                        results['Angular Scale [in kpc/\'\']'] = "{:.3f}".format(cf.linear_scale(
                            params, z_user))

                    if(cf.luminosity_distance(
                            params, z_user) < 1):
                        results['Luminosity Distance [in kpc]'] = "{:.3f}".format(cf.luminosity_distance(
                            params, z_user) * 1e3)
                    else:
                        results['Luminosity Distance [in Mpc]'] = "{:.3f}".format(cf.luminosity_distance(
                            params, z_user))

                    results_df = pd.DataFrame.from_dict(
                        results, orient='index', columns=['Values'])
                    results_table = results_df.to_html(classes="results")
                    return render_template("home.html", table=results_table, rs=str(z_user), hpar=str(H), om=str(Omega_m), de=str(params[1]))
    if request.method == "GET":
        return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == '__main__':
    app.run(debug=True)
