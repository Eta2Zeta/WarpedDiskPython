# This is Hongyu Zhang's Python adaption of R. C. Hickox's accretion disk model

This version is translated by ChatGPT and then modified by Hongyu Zhang to try to make it work. 

## Organization of the program

The program is run from the main.py file. 

### Output
The output main directory is specified in the main.py file and the scrip will generate a par.dat file in the main output directory, specifying the parameters of the entire run. There will also be subdirectories in the main directory that is from each individual run. 

#### Naming 
### Directory Naming Convention Documentation

Each simulation run is stored in a uniquely named directory, constructed to encode key parameters for easy identification and reproducibility. The directory names follow the format (shown as an example):

```
000obsm05tin00tout90tw130th00bm1_00bm2_60lng180
```

Here’s a breakdown of each component:

- **`000`**: A three-digit, zero-padded counter that uniquely identifies each run (e.g., `000`, `001`, `002`).
- **`obsm05`**: Encodes the observer's elevation angle. Positive angles are zero-padded (e.g., `obs05` for `5` degrees), while negative angles are prefixed with 'm' (e.g., `obsm05` for `-5` degrees).
- **`tin00`**: Represents the inner disk tilt angle in degrees, zero-padded to two digits (e.g., `tin00` for `0` degrees).
- **`tout90`**: Represents the outer disk tilt angle in degrees, zero-padded to two digits (e.g., `tout90` for `90` degrees).
- **`tw130`**: Encodes the phase offset angle in degrees. Positive angles are zero-padded (e.g., `tw130` for `130` degrees), while negative angles are prefixed with 'm' (e.g., `tw_m130` for `-130` degrees).
- **`th00`**: Encodes the theta angle in degrees, zero-padded to two digits (e.g., `th00` for `0` degrees).
- **`bm1_00bm2_60`**: Represents the beam angles. Positive angles are zero-padded and prefixed with 'bm1' or 'bm2' (e.g., `bm1_00bm2_60` for `0` and `60` degrees respectively). Negative angles are indicated with 'm' (e.g., `bm1_m40bm2_60` for `-40` degrees).
- **`lng180`**: Encodes the longitude angle in degrees, zero-padded to three digits (e.g., `lng180` for `180` degrees).

There is this paper parameter in the function `dtmpspec(xv, yv, zv, labs, T, Tmax, Tmin, side, ph, phio, obselev, paper, fast, diskv, diskvf, plot):`. I am pretty sure it is for "paper-ready plots. 

I will just delete it to make the program more elegant. 
