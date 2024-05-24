
.. _geoclaw_examples_storm_surge_typhoon_mangkhut:

Basic Example of Storm Surge from Typhoon Mangkhut
=================================================

This example contains the data and setup for running a storm surge forecast for
Typhoon Mangkhut.  The example can be run via::

    make all

which should download the necessary topography and storm data, start the 
simulation and plot the results.


The Method to Calculate Radius of Maximum Wind:
We use Complete Radial Structure of the Tropical Cyclone Wind Field in [1] to 
calculate radius of maximum wind because there is no such data for typhoon Mangkhut.

In the paper [1], Outer-Region Structure Model is given by:
\frac{\partial M_{E04}}{\partial r} = \chi\frac{(rV)^2}{{r_0}^2 - r^2}
where V is the azimuthal wind in the boundary layer and chi is given by
chi = \frac{2C_d}{W_{cool}}
C_d is constrained to be a piecewise constant–linear–constant function of V 
whose parameters are optimally estimated directly from the data of [2]. Here only 
consider the simplest case and assume chi = 1.0

In the paper [1], Inner-Region Structure Model is given by:
(\frac{M_{ER11}}{M_m})^{2-(C_k/C_d)} = \frac{2(r/r_m)^2}{2-(C_k/C_d)+(C_k/C_d)(r/r_m)^2}
where
M_m = r_m * V_m + 1/2 * f * {r_m}^2
$C_k$/$C_d$ is the ratio of the exchange coefficients of enthalpy and momentum.
Here only consider the simplest case and assume $C_k$/$C_d$ =1, then inner-region 
structure model is:
\frac{M_{ER11}}{M_m} = \frac{2(r/r_m)^2}{1+(r/r_m)^2}

Seek to merge the solutions of the inner ascending and outer descending regions. 

Mathematically, this merger imposes two constraints that $M$ and its radial 
derivative each be continuous at a merge point, denoted (r_a, V_a). Respective 
constraints are given by:
M_m\frac{2}{(r_m/r_a)^2 + 1} = M_a
M_a\frac{2}{r_a((r_a/r_m)^2 + 1)} = \chi\frac{(r_a V_a)^2}{{r_0}^2 - {r_a}^2}
where M_a = v_a * r_a + 1/2 * f * {r_a}^2 is the angular momentum at the merge 
point and 
M_a = M_{E04}(r_a)
which can be solved by numerical integration of outer-region structure model equation.

Solve following equation set by Newton Method:
f_1(r_m,r_a,v_a)=M_m\frac{2}{(r_m/r_a)^2 + 1} - M_a
f_2(r_m,r_a,v_a)=M_a\frac{2}{r_a((r_a/r_m)^2 + 1)} - \chi\frac{(r_a V_a)^2}{{r_0}^2 - {r_a}^2}
f_3(r_m,r_a,v_a)=M_{E04}(r_a)-M_a


The Method to Find r_0: Function `Find_r0`,
Velocity = 30 knots and its radius for Mangkhut are given. Assume v = 30 knots in the 
outer region structure and substitute v and r into this structure. Then use a loop to 
find proper r_0 which suits outer region structure model.


Reference:
[1] D. R. Chavas, N. Lin, and K. Emanuel, A model for the complete radial structure of the 
tropical cyclone wind field. Part I: Comparison with observed structure. J. Atmos. Sci. 72, 
3647–3662 (2015).
[2] M. Donelan, B. Haus, N. Reul, W. Plant, M. Stiassnie, H. Graber, O. Brown, E. Saltzman, 
On the limiting aerodynamic roughness of the ocean in very strong winds. Geophys. Res. Lett. 31, 
L18306, doi: 10.1029/2004GL019460 (2004).