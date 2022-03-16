Each folder named like a date (YYYYmmddHHMM) has a case study and it's name after eruption start time.

  * `201208061200` - Historical case study for eruption starting at 2012-08-06T12:00 UTC
  * `202107150000` - Operational case study for eruption starting at 2021-07-15T00:00 UTC

Each case study folder has :
  - `input` folder with the eruption source parameters, sampled with Latin Hyspercube technique, used to configure each HYSPLIT run.
  - `output` folder with the HYSPLIT modelling results processed to cumulative deposited ash thickness netcdf file.



