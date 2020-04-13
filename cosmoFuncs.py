#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:46:31 2020

@author: Bharath Saiguhan
"""
import numpy as np
from scipy.constants import pi, c, G
from scipy.integrate import quad


c = c / 1000.0  # get the value of the speed of light in km/s
arcsec = pi / (3600 * 180)  # conversion from " to radians

# Note : We hardcode omega_rad_0 to 4.165e(-5), and omega_k is computed
#        according to omega_k + omega_m + omega_lam + omega_rad_0 = 1
#        We will only input the values of H_0, omega_m and omega_lam.


def convertH(H):
    """
    A helper function to convert a given Hubble's constant value from km/s/Mpc to 1/s

    Arguments
    ---------
    H : float
        A value of the Hubble's constant to convert.

    Returns
    -------
    H_new : float
        Converted value of Hubble's constant, in 1/s

    """
    return(H * 1000 / (3.086e22))


def HubbleDistance(H):
    """
    A helper function to compute the Hubble distance given the current Hubble's constant.

    Arguments
    ---------
    H : float
        A value of the Hubble's constant to use for the calculation

    Returns
    -------
    d_H : float
        Value of the Hubble distance in Mpc
    """
    d_H = c / H
    return d_H


def t(parameters, z_val):
    """
    A function to calculate age of Universe at the given redshift of z_val.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of 1/s)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    t_age : float
        A value for the Age of the Universe (in Gyr) at redshift z = z_val.

    """
    h = parameters[0] * (3.086e22) / 100000  # normalized Hubble's constant
    omega_rad = 4.165e-5 / (h ** 2)
    omega_k = 1 - sum(parameters[1:]) - omega_rad
    def integrand(z): return 1 / ((1 + z) *
                                  (parameters[0] * np.sqrt((parameters[1] + parameters[2] * (1 + z) ** 3 + omega_k * (1 + z) ** 2 + omega_rad * (1 + z) ** 4))))
    t_age = quad(integrand, z_val, np.inf)[0] / (86400 * 365 * 1e9)
    return(t_age)


def lightTravelTime(parameters, z_val):
    """
    A function to calculate the Light Travel Time from redshift z = z_val to z = 0.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of 1/s)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    ltt : float
        The Light Travel Time (in Gyr) corresponding to the Cosmological parameters given, from the redshift z = z_val
        to z = 0.

    """
    ltt = t(parameters, 0.0) - t(parameters, z_val)
    return(ltt)


def comoving_distance_radial(parameters, z_val):
    """
    A function to compute the (radial) comoving distance, given the cosmological parameters and a value
    for redshift.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    d_c : float
        The (Radial) Comoving Distance (in Mpc) corresponding to the Cosmological parameters given, at the redshift z_val.

    """
    h = parameters[0] / 100  # normalized Hubble's constant
    omega_rad = 4.165e-5 / (h ** 2)
    omega_k = 1 - sum(parameters[1:]) - omega_rad

    def denom(z): return 1 / \
        (parameters[0] * np.sqrt((parameters[1] + parameters[2] * (1 + z)
                                  ** 3 + omega_k * (1 + z) ** 2 + omega_rad * (1 + z) ** 4)))
    return(c * quad(denom, 0, z_val)[0])


def comoving_distance_transverse(parameters, z_val):
    """
    A function to compute the (transverse) comoving distance, given the cosmological parameters and a value
    for redshift.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    d_M : float
        The (Transverse) Comoving Distance (in Mpc) corresponding to the Cosmological parameters given, at the redshift z_val.
    """
    h = parameters[0] / 100  # normalized Hubble's constant
    omega_rad = 4.165e-5 / (h ** 2)
    omega_k = 1 - sum(parameters[1:]) - omega_rad
    if omega_k > 0:
        d_M = HubbleDistance(parameters[0]) * (1 / np.sqrt(omega_k)) * np.sinh(np.sqrt(
            omega_k) * comoving_distance_radial(parameters, z_val) / HubbleDistance(parameters[0]))
    elif omega_k == 0:
        d_M = comoving_distance_radial(parameters, z_val)
    else:
        d_M = HubbleDistance(parameters[0]) * (1 / np.sqrt(np.abs(omega_k))) * np.sin(np.sqrt(
            np.abs(omega_k)) * comoving_distance_radial(parameters, z_val) / HubbleDistance(parameters[0]))
    return(d_M)


def comoving_volume(parameters, z_val):
    """
    A function to compute the comoving distance, given the cosmological parameters and a value
    for redshift.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    V_c : float
        The Comoving Volume (in cubic Gpc) corresponding to the Cosmological parameters given, at the redshift z_val.

    """
    d_M = comoving_distance_transverse(parameters, z_val)
    h = parameters[0] / 100  # normalized Hubble's constant
    omega_rad = 4.165e-5 / (h ** 2)
    omega_k = 1 - sum(parameters[1:]) - omega_rad
    if omega_k > 0:
        V_c = (4 * pi * HubbleDistance(parameters[0]) ** 3) / (2 * omega_k) * ((d_M / HubbleDistance(parameters[0])) * np.sqrt(1 + omega_k * np.power(
            d_M / HubbleDistance(parameters[0]), 2)) - 1 / np.sqrt(np.abs(omega_k)) * np.arcsinh(np.sqrt(np.abs(omega_k)) * d_M / HubbleDistance(parameters[0])))
        V_c = V_c / 1e9
    elif omega_k == 0:
        V_c = (4 * pi / 3) * (d_M ** 3) / 1e9
    else:
        V_c = (4 * pi * HubbleDistance(parameters[0]) ** 3) / (2 * omega_k) * ((d_M / HubbleDistance(parameters[0])) * np.sqrt(1 + omega_k * np.power(
            d_M / HubbleDistance(parameters[0]), 2)) - 1 / np.sqrt(np.abs(omega_k)) * np.arcsin(np.sqrt(np.abs(omega_k)) * d_M / HubbleDistance(parameters[0])))
        V_c = V_c / 1e9
    return(V_c)


def angulardiameter_distance(parameters, z_val):
    """
    Function to compute the angular diameter distance, corresponding to a cosmology set by parameters,
    at the redshift z_val.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    d_a : float
        The Angular Diameter Distance (in Mpc) corresponding to the Cosmological parameters given, at the redshift z_val.

    """
    d_M = comoving_distance_transverse(parameters, z_val)
    d_a = d_M / (1 + z_val)
    return(d_a)


def linear_scale(parameters, z_val):
    """
    A function to compute the linear scale, corresponding to an angular size of 1",
    at an angular diameter distance set by the parameters and at the redshift values
    z = z_val.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    scale : float
        The linear scale (in kpc) corresponding to an angular scale of 1", at a distance equal
        to the Angular Diameter Distance for the Cosmological parameters given,
        at the redshift z_val.

    """
    scale = angulardiameter_distance(
        parameters, z_val) * arcsec * 1000  # convert from Mpc to kpc
    return(scale)


def luminosity_distance(parameters, z_val):
    """
    Function to compute the luminosity distance, corresponding to a cosmology set by parameters,
    at the redshift z_val.

    Arguments
    ---------
    parameters : list of length 3
        A list containing the cosmological parameters, with:
        parameter[0] = H_0 (in units of km/s/Mpc)
        parameter[1] = omega_lam_0
        parameter[2] = omega_m_0

    z_val : float
        A value for the redshift.

    Returns
    -------
    d_l : float
        The Luminosity Distance (in Mpc) corresponding to the Cosmological parameters given, at the redshift z_val.

    """
    d_M = comoving_distance_transverse(parameters, z_val)
    d_l = (1 + z_val) * d_M
    return(d_l)
