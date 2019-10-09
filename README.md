# Parameter Selection for the Functionally Assembled Terrestrial Ecosystem Simulator (FATES)

### Summary
Numerical models that simulate tropical forest ecosystem dynamics, such as the Functionally Assembled Terrestrial Ecosystem Simulator (FATES), have been proposed as a way to improve climate change projections. However, parameterizing these complex, process-based models is challenging due to their numerous and interconnected non-linear relationships. This code identifies three high-performing FATES parameter sets by quantitatively evaluating the performance of nearly 300 simulations, each run with a unique parameter set, against observations at a tropical forest test site.

<br>

### Contents
This repository contains several files used in the parameter selection analysis.

'fates_parameter_selection.ipynb' is the main analysis file. This is file contains an introduction, the analysis, and a summary of results.

The 'ps_functions' folder contains several modules that define functions used in the main analysis code.

The 'data' folder conatins data in used in the analysis that is publicly available. Some data sets used in this analysis require special permission to use, or are not yet publicly available, and are therefore not included here.

<br>

### Further Information
__Details of the parameter ensemble and analysis:__

Kovenock, M. (2019). Ecosystem and large-scale climate impacts of plant leaf dynamics (Doctoral dissertation). Chapter 4: "Within-canopy gradient of specific leaf area improves simulation of tropical forest structure and functioning in a demographic vegetation model." http://hdl.handle.net/1773/44061

<br>

__Details of the Functionally Assembled Ecosystem Simulator (FATES):__

GitHub code repository: <br>
https://github.com/NGEET/fates

Fisher, R. A., Koven, C. D., Anderegg, W. R., Christoffersen, B. O., Dietze, M. C., Farrior, C. E., et al. (2018). Vegetation demographics in Earth System Models: A review of progress and priorities. Global Change Biology, 24(1), 35–54. https://doi.org/10.1111/gcb.13910
