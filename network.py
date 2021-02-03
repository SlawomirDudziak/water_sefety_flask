def save_network(net, n):
  import wntr
  import matplotlib.pyplot as plt

  inp_file = net

  wn = wntr.network.WaterNetworkModel(inp_file)
  wntr.graphics.plot_network(wn, title='Nodes', node_size=0, node_labels=True)
  fig = plt.gcf()
  fig.savefig('/var/www/app/OS/static/networks_info/Net' + n + 'nodes.png', dpi=200)
  plt.clf()

  wntr.graphics.plot_network(wn, title='Links', node_size=0, link_labels=True)
  fig = plt.gcf()
  fig.savefig('/var/www/app/OS/static/networks_info/Net' + n + 'links.png', dpi=200)
  plt.clf()