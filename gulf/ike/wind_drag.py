#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

w = np.linspace(0,60,1000)

def direction(velocity):

    # if unit_vector[1] == 0.0:
    #     if unit_vector[0] > 0:
    #         theta = 0.5 * np.pi
    #     else:
    #         theta = 1.5 * np.pi
    # else:
    theta = np.arctan2(velocity[1],velocity[0])

    return theta

def left(w):
    b = 18.7 * (0.0018 - 0.00075) / (0.0020 - 0.00075) 
    return (0.00075 + (0.0020 - 0.00075) / 18.7 * w) * (w < b) + \
            0.0018 * (b <= w) * (w < 25.0) + \
           (0.0018 + (0.0045 - 0.0018) /  5.0 * (w - 25.0)) * (25.0 <= w) * (w < 30.0) + \
           (0.0045 + (0.0010 - 0.0045) / 15.0 * (w - 30.0)) * (30.0 <= w) * (w < 45.0) + \
           (0.0010 * (45.0 <= w))

def right(w):
    return (0.00075 + (0.0020 - 0.00075) / 18.7 * w) * (w < 18.7) + \
            0.002 * (18.7 <= w) * (w < 35.0) + \
           (0.00200 + (0.003 - 0.0020) / 10.0 * (w - 35.0)) * (35.0 <= w) * (w < 45.0) + \
            0.003 * (45.0 < w)

def rear(w):
    return (0.00075 + (0.0020 - 0.00075) / 18.7 * w) * (w < 18.7) + \
            0.002 * (18.7 <= w) * (w < 35.0) + \
           (0.00200 + (0.0010 - 0.00200) / 10.0 * (w - 35.0)) * (35.0 <= w) * (w < 45.0) + \
            0.001 * (45.0 < w)

# Sector test
fig = plt.figure()
axes = fig.add_subplot(111)
axes.plot(w,left(w),'r',label="Left")
axes.plot(w,right(w),'b',label="Right")
axes.plot(w,rear(w),'k',label="Rear")
axes.legend()
axes.set_xlabel("Wind Speed (m/s)")
axes.set_ylabel(r"$C_d$")
axes.set_xlim([0,60])
axes.set_ylim([0.0,0.0045])
axes.grid(True)
xticks = [0, 18.7, 25, 30, 35, 45]
yticks = [0.00075, 0.001, 0.0018, 0.002, 0.003, 0.0045]
axes.set_xticks(xticks)
axes.set_xticklabels(xticks)
axes.set_yticks(yticks)
axes.set_yticklabels(yticks)

# Direction test
# fig = plt.figure()
# tests = [[2.0,0.0],[1.0,2.0],[0.0,1.0],[-2.0,0.5],[-1.0,0.0],[-1.,-1.],[0.0,-1.0],[0.4,-1.5]]
# for (i,test) in enumerate(tests):
#     print "Test = %s" % test
#     theta = direction(test)

#     axes = fig.add_subplot(2,int(len(tests)/2),i+1)
#     axes.plot([0.0,np.cos(theta)],[0.0,np.sin(theta)],'b')
#     axes.plot([0.0,test[0]],[0.0,test[1]],'k--')
#     axes.set_xlim([-2,2])
#     axes.set_ylim([-2,2])
#     axes.grid(True)

# plt.show()

# Sector ranges
hurricane_directions = [1.5*np.pi,0.25*np.pi]
psi = np.linspace(0,2.0*np.pi,314)
fig = plt.figure()
for (i,theta) in enumerate(hurricane_directions):
    phi = (theta > psi) * (2*np.pi - theta + psi) + (theta <= psi) * (psi-theta)

    axes = fig.add_subplot(2,int(len(hurricane_directions)/2),i+1)
    axes.plot(psi,phi)
    axes.plot(np.ones(100)*theta,np.linspace(0,2*np.pi,100),'k-')
    axes.set_title(r'$\theta = %s \pi$' % str(theta%np.pi))

    axes.set_xticks([i*0.25*np.pi for i in range(9)])
    axes.set_xticklabels(['0',r'$1/4 \pi$',r'$1/2 \pi$',r'$3/4 \pi$',r'$\pi$',r'$5/4 \pi$',r'$3/2 \pi$',r'$7/4 \pi$',r'$2 \pi$'])
    axes.set_xlim([0,2*np.pi])

    axes.set_yticks([i*0.25*np.pi for i in range(9)])
    axes.set_yticklabels(['0',r'$1/4 \pi$',r'$1/2 \pi$',r'$3/4 \pi$',r'$\pi$',r'$5/4 \pi$',r'$3/2 \pi$',r'$7/4 \pi$',r'$2 \pi$'])
    axes.set_ylim([0,2*np.pi])

plt.show()