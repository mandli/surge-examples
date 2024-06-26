# Boundary/Storm Interaction Example

This example explores what may happen if a storm gets too close or crosses a
boundary of the domain.  In general it is not desirable to let a storm get too
close so this example also provides some tools to explore the problem as
well. 

The additional boundary conditions are implemented in the local file
`bc2amr.f90` file and modify only the incoming momentum flux by a factor
$\alpha_{\text{bc}}$ so it decays in time.  Possible values of 
$\alpha_{\text{bc}}$
 - $\alpha_{\text{bc}} = 0$: no flux, always set it to zero
 - $0 < \alpha_{\text{bc}} < 1$: Decaying value of the incoming flux
 - $\alpha_{\text{bc}}=1$: zero-order extrapolation

The additional scripts `run_tests.py` and `plot_comparison.py` will run a number
of values for $\alpha_{\text{bc}}$ and plot comparisons between the gauges.