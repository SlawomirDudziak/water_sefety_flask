from flask import Flask, flash, render_template, request, redirect, url_for
from OS import app
import os, sys
import sqlite3
# import startdatabase
# import network
# import leak

target = 'networks'

database = "/var/www/app/OS/woda.db"
path = '/var/www/app/OS/networks'
net = 'Net1.inp'

nodes = []
junc = []
pipes = []
f_list = []
i = 0
numer = str(i)
l_pictures = []
det = 'Net1'


@app.after_request
def add_header(response):
  response.cache_control.max_age = 0
  return response


@app.route('/')
def main():
  conn = sqlite3.connect(database)
  return render_template('index.html', title='Home')


@app.route('/home')
def home():
  return render_template('index.html', title='Home')


@app.route('/info')
def info():
  global det
  files = os.listdir(path)
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM nodes")
  data = cur.fetchall()
  return render_template('info.html', files=files, title='Info', data=data, table='nodes',det=det)


@app.route('/tanksinfo')
def tanksinfo():
  global det
  files = os.listdir(path)
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM tanks")
  data = cur.fetchall()
  return render_template('info.html', files=files, title='Info', data=data, table='tanks',det=det)


@app.route('/nodesinfo')
def nodesinfo():
  global det
  files = os.listdir(path)
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM nodes")
  data = cur.fetchall()
  return render_template('info.html', files=files, title='Info', data=data, table='nodes',det=det)


@app.route('/pipesinfo')
def pipesinfo():
  global det
  files = os.listdir(path)
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM pipes")
  data = cur.fetchall()
  return render_template('info.html', files=files, title='Info', data=data, table='pipes',det=det)


@app.route('/pipes-sim')
def pipes_sim():
  global numer
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM pipes_simulation")
  data2 = cur.fetchall()
  return render_template('results.html', title='Simulation', data2=data2, table='pipes sim',numer=numer)


@app.route('/pumps-sim')
def pumps_sim():
  global numer
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM pumps_simulation")
  data2 = cur.fetchall()
  return render_template('results.html', title='Simulation', data2=data2, table='pumps sim',numer=numer)


@app.route('/tanks-sim')
def tanks_sim():
  global numer
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM tanks_simulation")
  data2 = cur.fetchall()
  return render_template('results.html', title='Simulation', data2=data2, table='tanks sim',numer=numer)


@app.route('/junctions-sim')
def junctions_sim():
  global numer
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM junctions_simulation")
  data2 = cur.fetchall()
  return render_template('results.html', title='Simulation', data2=data2, table='junctions sim',numer=numer)


@app.route('/add-model')
def add_model():
  return render_template('add_model.html', title='Add network')


@app.route('/simulation')
def simulation():
  files = os.listdir(path)
  return render_template('simulation.html', title='Simulation', files=files)


@app.route('/choose', methods=['GET', 'POST'])
def choose():
  files = os.listdir(path)
  global net, det
  if request.method == 'POST':
    net = request.form['network']
    net_length = len(net)

    det = net.replace(net[net_length-1], "")
    for x in range(0,3):
      det_length = len(det)
      det = det.replace(det[det_length-1], "")

    # startdatabase.create_db(net)
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pumps")
    data = cur.fetchall()
    return redirect(url_for('info'))
  else:
      flash('Only POST method', 'danger')
  return render_template('info.html', net=net, files=files, title='Info', table='pumps',det=det)


@app.route('/run-sim', methods=['GET', 'POST'])
def run_sim():
  global net, det
  files = os.listdir(path)
  net_length = len(net)
  det = net.replace(net[net_length - 1], "")
  for x in range(0, 3):
    det_length = len(det)
    det = det.replace(det[det_length - 1], "")
  if request.method == 'POST':
    node = request.form['junction']
    sim_time = request.form['sim_time']
    poison_hour = request.form['poison_hour']
    if poison_hour >= sim_time:
      flash('Poison hour must be less than simulation time', 'danger')
      return redirect(url_for('simulation'))
    else:
      if int(sim_time) > 48:
        flash('Select simulation time less than 49 hours', 'danger')
      else:
        if int(sim_time) < 0 or int(poison_hour) < 0:
          flash('Selected time is less than 0!', 'danger')
        else:
          p_h = int(poison_hour)
          sim_time_1 = int(sim_time)
          # pllik.simulation(net, node, sim_time_1, p_h)
          flash('Simulation completed', 'success')
        return redirect(url_for('simulation'))
  return render_template('simulation.html', title='Info', net=net, node=node,sim_time=sim_time,poison_hour=poison_hour,
                         files=files, det=det)


@app.route('/run-leak', methods=['GET', 'POST'])
def run_leak_sim():
  global net, det
  files = os.listdir(path)
  net_length = len(net)
  det = net.replace(net[net_length - 1], "")
  for x in range(0, 3):
    det_length = len(det)
    det = det.replace(det[det_length - 1], "")
  if request.method == 'POST':
    pipe = request.form['pipe']
    sim_time = request.form['sim_time']
    leak_hour = request.form['leak_hour']
    if leak_hour >= sim_time:
      flash('Leak hour must be less than simulation time', 'danger')
      return redirect(url_for('leak_sim'))
    else:
      if int(sim_time) > 48:
        flash('Select simulation time less than 49 hours', 'danger')
      else:
        if int(sim_time) < 0 or int(leak_hour) < 0:
          flash('Selected time is less than 0!', 'danger')
        else:
          p_h = int(leak_hour)
          sim_time_1 = int(sim_time)
          leak.simulation(net, pipe, sim_time_1, p_h)
          flash('Simulation completed', 'success')
        return redirect(url_for('leak_sim'))
  return render_template('run_sim_leak.html', title='Info', net=net, pipe=pipe,sim_time=sim_time,leak_hour=leak_hour,
                         files=files, det=det)


@app.route('/choose-junction', methods=['GET', 'POST'])
def choose_junction():
  global net
  if request.method == 'POST':
    net = request.form['network']
    # startdatabase.create_db(net)
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM junctions")
    junc_db = cur.fetchall()
    junc_count = len(junc_db)
    i = 0
    junc = []
    while i < junc_count:
      junc.append(junc_db[i][1])
      i = i + 1
  return render_template('run_sim.html', title='Choose junc', junc=junc, net=net)


@app.route('/leak-sim', methods=['GET', 'POST'])
def leak_sim():
  global net, det, pipes
  if request.method == 'POST':
    net = request.form['network']
    # startdatabase.create_db(net)
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("SELECT * FROM pipes")
    pipes_db = cur.fetchall()
    pipes_count = len(pipes_db)
    i = 0
    pipes = []
    while i < pipes_count:
      pipes.append(pipes_db[i][1])
      i = i + 1
  return render_template('run_sim_leak.html', title='Choose pipe', pipes=pipes, net=net, det=det)


@app.route('/choose-pipe')
def choose_pipe():
  files = os.listdir(path)
  return render_template('choose_pipe.html', title='Simulation', files=files)


@app.route('/results')
def results():
  global f_list, numer
  pics = '/var/www/app/OS/static/img'
  l_pics = os.listdir(pics)
  for pic in l_pics:
    l_pictures.append('static/img/'+pic)
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM junctions_simulation")
  data2 = cur.fetchall()
  return render_template('results.html', title='Results', data2=data2, table='junctions sim', f_list=f_list,
                         l_pictures=l_pictures, numer=numer)


@app.route('/contact')
def contact():
  return render_template('contact.html', title='Contact')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
  if request.method == 'POST':
    global det
    n = len(os.listdir('/var/www/app/OS/networks'))
    x = str(n+1)

    f = request.files['file']
    filename = 'Net' + x + '.inp'
    destination = "/".join([target, filename])
    f.save(destination)
    # network.save_network('/var/www/app/OS/networks/'+filename, x)
    flash('Plik '+filename+' sent successfully', 'success')
  return render_template('add_model.html', title='Add network', n=n, x=x, det=det)


@app.route('/report')
def report():
  global det
  # conn = sqlite3.connect(database)
  # cur = conn.cursor()
  # cur.executescript("""
                # CREATE TABLE IF NOT EXISTS reports (
                    # simulation_time DECIMAL NOT NULL,
            		# link varchar(250) NOT NULL
                # )""")
  # cur.executescript("""
                # CREATE TABLE IF NOT EXISTS junctions_simulation (
                    # simulation_time DECIMAL NOT NULL,
            		# junction_name archar(250) NOT NULL,
                    # chemical_concenentraction DECIMAL NOT NULL,
            		# demand DECIMAL NOT NULL,
            		# pressure DECIMAL NOT NULL,
            		# head DECIMAL NOT NULL,
                    # FOREIGN KEY(junction_name) REFERENCES nodes(name_nodes)
                # )""")
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM reports")
  report = cur.fetchall()

  # conn = sqlite3.connect(database)
  # cur = conn.cursor()
  # cur.execute("SELECT * FROM junctions_simulation")
  # data2 = cur.fetchall()
  return render_template('report.html', title='Report', report=report, det=det)


@app.route('/report-links')
def report_links():
  return redirect(url_for('report'))


@app.route('/report-nodes')
def report_nodes():
  global det
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.executescript("""
                  CREATE TABLE IF NOT EXISTS reports (
                      simulation_time DECIMAL NOT NULL,
              		link varchar(250) NOT NULL
                  )""")
  cur.executescript("""
                  CREATE TABLE IF NOT EXISTS junctions_simulation (
                      simulation_time DECIMAL NOT NULL,
              		junction_name archar(250) NOT NULL,
                      chemical_concenentraction DECIMAL NOT NULL,
              		demand DECIMAL NOT NULL,
              		pressure DECIMAL NOT NULL,
              		head DECIMAL NOT NULL,
                      FOREIGN KEY(junction_name) REFERENCES nodes(name_nodes)
                  )""")
  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM reports")
  report = cur.fetchall()

  conn = sqlite3.connect(database)
  cur = conn.cursor()
  cur.execute("SELECT * FROM junctions_simulation")
  data2 = cur.fetchall()
  return render_template('report.html', title='Report', report=report, det=det, data2=data2, nnodes='true')
