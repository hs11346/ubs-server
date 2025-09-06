import numpy as np
from scipy.interpolate import UnivariateSpline
import matplotlib.pyplot as plt

def fill_missing_values(data_list, smoothing_param=1.0, plot_result=True):
    """
    Fill missing values in a list of numbers using a smoothing spline.
    
    Additional improvements:
      - Clip predicted values to lie within the known data range.
      - Replace non-finite predictions (nan or inf) with linear interpolation.
    
    Parameters:
        data_list (list): List of numbers with missing entries represented as None.
        smoothing_param (float): Smoothing factor for the spline; s=0 gives an exact interpolation.
        plot_result (bool): If True, a plot is generated showing the interpolation.
    
    Returns:
        list: A list with missing values filled using spline interpolation (with safe estimates).
    """
    # 1. Convert the input list with None values to an array with np.nan
    data = np.array([np.nan if x is None else x for x in data_list], dtype=float)
    N = len(data)
    x = np.arange(N)
    
    # 2. Extract known (non-missing) data
    mask = ~np.isnan(data)
    if np.sum(mask) < 2:
        raise ValueError("Insufficient known data points for interpolation.")
    
    x_known = x[mask]
    y_known = data[mask]
    
    # 3. Fit the smoothing spline using the known data
    spline = UnivariateSpline(x_known, y_known, s=smoothing_param)
    
    # 4. Interpolate missing values
    data_interp = data.copy()
    missing_indices = np.where(np.isnan(data))[0]
    interp_vals = spline(missing_indices)
    
    # Prevent explosion: Clip predictions to within the range of known data.
    y_min, y_max = np.nanmin(y_known), np.nanmax(y_known)
    interp_vals = np.clip(interp_vals, y_min, y_max)
    
    # Check for non-finite values in the predictions: Replace with linear interpolation if needed.
    non_finite = ~np.isfinite(interp_vals)
    if np.any(non_finite):
        # Create a linear interpolation of the known values to fall back on.
        linear_interp = np.interp(missing_indices[non_finite], x_known, y_known)
        interp_vals[non_finite] = linear_interp
    
    # Assign the safe interpolated values into the array.
    data_interp[missing_indices] = interp_vals
    
    # (Optional) Ensure that the known values remain unchanged.
    data_interp[mask] = data[mask]
    
    # 5. Visualization (if enabled)
    if plot_result:
        plt.figure(figsize=(10, 5))
        plt.plot(x, data_interp, label='Spline Interpolation', color='C0')
        plt.scatter(x[mask], data[mask], label='Known Data', color='C1', s=20)
        plt.scatter(missing_indices, interp_vals, label='Interpolated Points', color='C2', s=20)
        plt.legend()
        plt.xlabel('Index')
        plt.ylabel('Value')
        plt.title('Spline Interpolation Filling Missing Data (With Safe Predictions)')
        plt.show()
    
    # Verify that known data are unchanged
    unchanged = np.allclose(data_interp[mask], data[mask], equal_nan=True)
    print("Known data unchanged:", unchanged)
    
    # Convert the numpy array back to a list and return
    return data_interp.tolist()


# ---------------------------------------
# Example usage:
# ---------------------------------------
if __name__ == "__main__":
    # Create an example list with 1000 numbers and insert None values randomly.
    N = 1000
    x = np.arange(N)
    # Create a smooth, noisy signal.
    true = np.sin(2 * np.pi * x / 100) + np.log(x/np.sin(x))
    data = true + 2.1 * np.random.randn(N)
    data = data.tolist()
    
    # Replace approximately 100 indices with None to simulate missing data.
    num_missing = 100
    nan_indices = np.random.choice(N, size=num_missing, replace=False)
    for idx in nan_indices:
        data[idx] = None

    # Fill missing values using the function.
    filled_data = fill_missing_values(data, smoothing_param=1, plot_result=True)