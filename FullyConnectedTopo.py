#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
class FullyConnectedTopo(Topo):

  "fully-connected Topo."
  def __init__(self, n=2,**opts):
    # Initialize topology and default options
    Topo.__init__(self,**opts)
    slist = []
    for i in range(n):
        switch = self.addSwitch('s%s' % (i + 1),cls=OVSSwitch)
        host = self.addHost('h%s' % ( i + 1))
        self.addLink(host, switch)
        slist.append(switch)
    for i in range(n):
      for j in range(i+1,n):
          self.addLink(slist[i],slist[j])

def simpleTest():
  "Create and test a simple network"
  m = 4
  topo = FullyConnectedTopo(n=m)
  net = Mininet(topo)
  net.start()
  for i in range(m):
      net.get('s%s'%(i + 1)).cmd('ovs-vsctl set bridge s%s stp-enable=true'%(i+1))

  CLI(net)
  print "Dumping host connections"
  dumpNodeConnections(net.hosts)
  print "Testing network connectivity"
  net.pingAll()
  net.stop()

if __name__ == '__main__':
  # Tell mininet to print useful information
  setLogLevel('info')
  simpleTest()
