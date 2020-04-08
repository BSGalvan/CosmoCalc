#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:46:31 2020

@author: Bharath Saiguhan
"""

# Have to write code for the following :
# 1. Age at redshift z = 0 (Done)
# 2. Age at redshift z = z_user (Done)
# 3. Light Travel time = 1. - 2. (Done)
# 4. Comoving Radial Distance = 3. * c (in Mpc) (Done)
# 5. Comoving Volume within redshift z = 4.** 3 (in cubic Gpc) (Done)
# 6. Angular Size Distance (in Mpc) (Done)
# 7. Scale factor (kpc / arcsec) (Done)
# 8. Luminosity distance (in Mpc) (Done)

import numpy as np
from scipy.constants import pi
from astropy.constants import c, G
from scipy.integrate import quad

c = c.value / 1000.0  # get the value of the speed of light in km/s
G = G.value  # get the value of the Universal Gravitational Constant
arcsec = pi / (3600 * 180)  # conversion from " to radians

# Note : We assume that omega_k_0 = 0.0, and omega_rad_0 is too small, such that
#        it can be safely neglected as well. We will only input the values of
#        H_0, omega_m and omega_lam


def convertH(H):
    """
    A function to convert a given Hubble's constant value from km/s/Mpc to 1/s

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


def t(parameters, z_val):
    """
    A function to calculate age of Universe at the given redshift of z_val.

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
    t_age : float
        A value for the Age of the Universe (in Gyr) at redshift z = z_val.

    """
    def integrand(z): return 1 / ((1 + z) *
                                  (parameters[0] * np.sqrt((parameters[1] + parameters[2] * (1 + z) ** 3))))
    t_age = quad(integrand, z_val, np.inf)[0] / (86400 * 365 * 1e9)
    return(t_age)


def lightTravelTime(parameters, z_val):
    """
    A function to calculate the Light Travel Time from redshift z = z_val to z = 0.

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
    ltt : float
        The Light Travel Time (in Gyr) corresponding to the Cosmological parameters given, from the redshift z = z_val
        to z = 0.

    """
    ltt = t(parameters, 0.0) - t(parameters, z_val)
    return(ltt)


def comoving_distance(parameters, z_val):
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
    d_c : float
        The Comoving Distance (in Mpc) corresponding to the Cosmological parameters given, at the redshift z_val.

    """
    def denom(z): return 1 / \
        (parameters[0] * np.sqrt((parameters[1] + parameters[2] * (1 + z) ** 3)))
    return(c * quad(denom, 0, z_val)[0])


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
    d_c = comoving_distance(parameters, z_val)
    # convert from cubic Mpc to cubic Gpc.
    V_c = (4 * pi / 3) * (d_c ** 3) / 1e9
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
    d_c = comoving_distance(parameters, z_val)
    d_a = d_c / (1 + z_val)
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
    d_c = comoving_distance(parameters, z_val)
    d_l = (1 + z_val) * d_c
    return(d_l)
