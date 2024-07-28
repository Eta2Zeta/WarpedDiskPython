import numpy as np
import matplotlib.pyplot as plt

h = 6.6261e-34  # Planck's constant (J*s)
c = 3.0e8       # Speed of light (m/s)
k = 1.3806e-23  # Boltzmann's constant (J/K)

def blackbody_spectrum(wavelength, T):
    """
    Calculate the blackbody spectrum using Planck's Law.

    Parameters:
    wavelength (numpy array): Wavelengths in meters.
    T (float): Temperature in Kelvin.

    Returns:
    numpy array: Normalized spectral radiance (W/m^3/sr).
    """

    
    
    # Calculate the spectrum at the upper bound wavelength
    upper_bound_wavelength = wavelength[-1]  # The last element in the wavelength array
    upper_bound_exponent = (h * c) / (upper_bound_wavelength * k * T)
    upper_bound_radiance = (2.0 * h * c**2) / (upper_bound_wavelength**5 * (np.expm1(upper_bound_exponent)))
    

    # Planck's Law
    exponent = (h * c) / (wavelength * k * T)
    normalized_spectral_radiance = (2.0 * h * c**2) / (wavelength**5 * (np.expm1(exponent)))/upper_bound_radiance

    
    return normalized_spectral_radiance

# Define the temperature of the Sun
T_sun = 0.1*1e3*1.6e-19/k  # Temperature in Kelvin

# Define the wavelength range (in meters)
lower = 1e-11
upper = 1e-8
wavelength = np.linspace(lower, upper, 1000)  # 1e-11 to 1e-8 is the wavelength of x-ray

# Calculate the normalized blackbody spectrum
normalized_spectrum = blackbody_spectrum(wavelength, T_sun)

# Plot the normalized spectrum
plt.figure(figsize=(10, 6))
plt.plot(wavelength, normalized_spectrum, color='orange')
plt.title('Normalized Blackbody Spectrum of the Sun')
plt.xlabel('Wavelength (m)')
plt.ylabel('Normalized Spectral Radiance')
plt.grid(True)
plt.xscale('log')  # Use logarithmic scale for x-axis
plt.show()
