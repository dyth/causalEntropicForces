import numpy
import sys
from collections import defaultdict

class Brownian():

    """
    The equation is the following 

    dv = (-v/a) dt + alpha * sqrt(2*b/a*dt)

    alpha is distributed with mean 0 and variance 1.
    """

    def __init__(self, dt, initV = 0.0, runtime = 100.0):
        self.dt =  dt
        self.steps = int(runtime/dt)
        self.dxs = numpy.zeros(self.steps)
        self.time = numpy.zeros(self.steps+1)
        self.pos = numpy.zeros(self.steps+1)
        self.a = 1.0 
        self.b = 1.0
        self.alpha = numpy.random.normal(0.0, 1.0, self.steps)
        self.initV = initV
        self.finalV = 0.0
        self.runtime = runtime

    def reset(self):
        self.__init__(self.dt, self.initV, self.runtime)

    def computeV(self, v, alpha):
        dv = (- (v / self.a) * self.dt) + (alpha * numpy.sqrt(2.0 * self.b / self.a * self.dt))
        return (v + dv)

    def solve(self):
        t = 0.0
        v = self.initV
        for i, a in enumerate(self.alpha):
            t = t + self.dt
            vnew = self.computeV(v, a)
            self.time[i+1] = t
            self.dxs[i] = v * self.dt
            self.pos[i+1] = self.pos[i] + self.dxs[i]
            v = vnew
        self.finalV = v

    def solveMany(self, times = 1):
        """Do the Brownian motion for n times and return the averages of values
        """
        finalV = numpy.zeros(times)
        finalX = numpy.zeros(times)
        for i in range(times):
            self.reset()
            self.solve()
            finalV[i] = self.finalV
            finalX[i] = self.pos[-1]
        return finalX, finalV

def getRMSDisplacement(pos):
    """get root mean squared displacements of a particle """
    return numpy.mean(numpy.square(pos))

def solve_problem1():
    import pylab
    timesteps = [0.1, 0.01, 0.001]
    initV = [0, 10]
    # This is a dictionary with keys as (timestep,initV) and final velocity as
    # values.
    finalvecolicies = defaultdict(list)
    total = 5
    for dt in timesteps:
        for v in initV:
            print("Solving for %s timestep and %s initial velocty" % (dt,v))
            print("++ Generating %s samples" % total)
            pylab.figure()
            for i in range(total):
                a = Brownian(dt, v)
                a.solve()
                finalvecolicies[(dt,v)].append(a.finalV)
                pylab.plot(a.time, a.pos)
            pylab.xlabel("Time: dt is %s" % dt)
            pylab.ylabel("Position when init velocity is %s" % v)
            print("++ Saving plot")
            pylab.savefig("plot_{}dt_{}initv_{}.png".format(int(dt*1000), v, total))

    with open("results_{}.txt".format(total), "w") as f:
        f.write("samples,dt,initv,mean,variance,rms\n")
        for dt, v in finalvecolicies:
            vs = finalvecolicies[(dt, v)]
            f.write("%s,%s,%s,%s,%s,%s\n"%(
                total
                ,dt
                ,v
                ,numpy.mean(vs)
                ,numpy.std(vs)
                ,numpy.sqrt(numpy.mean(numpy.square(vs))))
                )
        print("Problem 1 is solevd")

def solve_problem2():
    import pylab
    print("Solving problem 2")
    rmsXList = []
    simTimeList = []
    displacements = []
    total = 100
    repeat = 20
    for i in range(total):
        runtime = i+1 
        b = Brownian(0.01, 0, runtime = runtime)
        finalX, finalV = b.solveMany(repeat)
        f = numpy.sqrt(numpy.mean(numpy.square(finalX)))
        displacements.append(f)
    pylab.plot(displacements)
    pylab.savefig("{}x{}.png".format(total, repeat))
    pylab.show()



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("USAGE: {} 1|2".format(sys.argv[0]))
        sys.exit()
    if "1" == sys.argv[1]:
        solve_problem1()
    elif "2" == sys.argv[1]:
        solve_problem2()
    else:
        print("USAGE: {} 1|2".format(sys.argv[0]))
        sys.exit()
