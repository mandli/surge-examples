#!/usr/bin/env python

import os
import datetime

import numpy as np
import matplotlib.pyplot as plt

import batch.batch
import clawpack.pyclaw.gauges
import clawpack.geoclaw.surge.plot as surgeplot

days2seconds = lambda days: days * 60.0**2 * 24.0

class BoundaryJob(batch.batch.Job):
    r""""""

    def __init__(self, test_type, alpha=1.0, base_path='./'):

        super(BoundaryJob, self).__init__()

        self.type = "boundary_tests"
        self.name = ""
        self.prefix = f"{test_type}_{str(int(alpha * 1e4)).zfill(5)}"
        self.executable = "xgeoclaw"

        # Create base data object
        import setrun
        self.rundata = setrun.setrun()

        if test_type.lower() == "extrap":
            self.rundata.clawdata.bc_lower[0] = 'extrap'
            self.rundata.clawdata.bc_upper[0] = 'extrap'
            self.rundata.clawdata.bc_lower[1] = 'extrap'
            self.rundata.clawdata.bc_upper[1] = 'extrap'
            self.rundata.bc_test_data.alpha_bc = 1.0
        elif test_type.lower() == 'test':
            self.rundata.clawdata.bc_lower[0] = 'extrap'
            self.rundata.clawdata.bc_upper[0] = 'user'
            self.rundata.clawdata.bc_lower[1] = 'extrap'
            self.rundata.clawdata.bc_upper[1] = 'extrap'
            self.rundata.bc_test_data.alpha_bc = alpha
        elif test_type.lower() == 'wall':
            self.rundata.clawdata.bc_lower[0] = 'wall'
            self.rundata.clawdata.bc_upper[0] = 'wall'
            self.rundata.clawdata.bc_lower[1] = 'wall'
            self.rundata.clawdata.bc_upper[1] = 'wall'
            self.rundata.bc_test_data.alpha_bc = 0.0
        else:
            raise ValueError(f"Unknown boundary test type {test_type}")

    def __str__(self):
        output = super(BoundaryJob, self).__str__()
        output += "\n  Name: %s" % self.name
        output += "\n  config: x_bcs = (%s, %s)" % (self.rundata.clawdata.bc_lower[0],
                                                    self.rundata.clawdata.bc_upper[0])
        output += "\n          y_bcs = (%s, %s)" % (self.rundata.clawdata.bc_lower[1],
                                                    self.rundata.clawdata.bc_upper[1])
        output += "\n  alpha_bc = %s" % self.rundata.bc_test_data.alpha_bc
        return output


    def write_data_objects(self):
        r""""""

        # Write out all data files
        super(BoundaryJob, self).write_data_objects()


def plot_gauge(gauge_num, controller):
    
    fig, ax = plt.subplots()

    for job in controller.jobs:
        path = os.path.join(controller.base_path, job.type, 
                                                  f"{job.prefix}_output")
        gauge = clawpack.pyclaw.gauges.GaugeSolution(gauge_id=gauge_num, 
                                                     path=path)
        print(job.rundata.clawdata.bc_upper[0])
        if job.rundata.clawdata.bc_upper[0] == 'wall':
            kwargs = {"color": 'black', "label": "wall"}
        elif job.rundata.clawdata.bc_upper[0] == 'user':
            if job.rundata.bc_test_data.alpha_bc == 0.0:
                kwargs = {"color": 'blue', 
                          "marker": ".", 
                          "label": "zero momentum"}
            else:
                kwargs = {"color": 'lightgray', "label": None}
        elif job.rundata.clawdata.bc_upper[0] == 'extrap':
            kwargs = {"color": 'red', "label": "extrap"}
        else:
            raise ValueError("Invalid test type.")
        ax.plot(surgeplot.sec2days(gauge.t), gauge.q[3, :], **kwargs)

    ax.set_title('Station %s' % gauge_num)
    ax.set_xlim([-1, 3])
    ax.set_xlabel('Days relative to landfall')
    t_labels = [-1, 0, 1, 2, 3]
    ax.set_xticks(t_labels)
    ax.set_xticklabels([r"${}$".format(x) for x in t_labels])
    # ax.set_ylim([-0.25, 1.0])
    ax.legend()

    return fig


if __name__ == '__main__':

    jobs = []
    alphas = [0.000, 0.100, 0.200, 0.250, 0.300, 0.400, 0.500, 0.600, 0.700, 
              0.750, 0.800, 0.900, 0.950, 0.955, 0.960, 0.965, 0.970, 0.975, 
              0.980, 0.985, 0.990, 0.995]
    jobs.append(BoundaryJob('wall'))
    jobs.append(BoundaryJob('extrap'))
    for alpha in alphas:
        jobs.append(BoundaryJob('test', alpha=alpha))
    
    controller = batch.batch.BatchController(jobs)
    controller.plot = False
    controller.wait = True
    print(controller)
    controller.run()

    figs = []
    for gauge_num in range(3):
        file_name = f"comparison_{gauge_num}.pdf"
        figs.append(plot_gauge(gauge_num, controller))
        figs[-1].savefig(os.path.join(os.getcwd(), file_name))
    plt.show()