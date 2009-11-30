#! /usr/bin/env python

import draw_points
import lcm
from laser_t import laser_t

from math import *

try:
	from OpenGL.GLUT import *
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	print 'ERROR: PyOpenGL not installed properly'
	sys.exit()

isinit = False
points = []
w_size = [500, 500]
#axes = [-20, 20, -20, 20]
#axes = [1 for i in range(0, 4)]
axes = [-1, 1, -1, 1]

def draw_scan(channel, data):
	global points
	global isinit
	msg = laser_t.decode(data)
	rad = [msg.radstep * i + msg.rad0 for i in range(0, msg.nranges)]
	x = [cos(rad[i]) * msg.ranges[i] for i in range(0, msg.nranges)];
	y = [sin(rad[i]) * msg.ranges[i] for i in range(0, msg.nranges)];
	update_axes(x, y)
	points = [[x[i], y[i]] for i in range(0, msg.nranges)];
	glutPostRedisplay()

def update_axes(x, y):
	global axes
	x_min = min(x) - 3
	x_max = max(x) + 3
	y_min = min(y) - 10
	y_max = max(y) + 10
	'''axes[0] = min([x_min, axes[0]])
	axes[1] = max([x_max, axes[1]])
	axes[2] = min([y_min, axes[2]])
	axes[3] = max([y_max, axes[3]])'''
	axes[0] = x_min
	axes[1] = x_max
	axes[2] = y_min
	axes[3] = y_max

def init_graph(idle_func):
	global w_size
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(w_size[0], w_size[1])
	glutInitWindowPosition(100, 100)
	glutCreateWindow('Points')
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glShadeModel(GL_FLAT)
	glutDisplayFunc(display)
	glutIdleFunc(idle_func)
	glutReshapeFunc(reshape)
	glutMainLoop()

def draw_point(point):
    glBegin(GL_POINTS)
    glVertex2f(point[0], point[1])
    glEnd()

def draw_points(points):
    for point in points:
        draw_point(point)

def display():
	global points
	global w_size
	reshape(w_size[0], w_size[1])
	glClear(GL_COLOR_BUFFER_BIT)
#glPushMatrix()
	glColor3f(1.0, 1.0, 1.0)
	glPointSize(3.0)
	draw_points(points)
	glutSwapBuffers()

def reshape(w, h):
	global axes
	w_size = [w, h]
	glViewport(0, 0, w, h)	
	glMatrixMode(GL_PROJECTION)	
	glLoadIdentity()
	glOrtho(axes[0], axes[1], axes[2], axes[3], -1.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

if __name__ == '__main__':
	lc = lcm.LCM()
	subs = lc.subscribe("LASER", draw_scan)
	init_graph(lc.handle)
	lc.unsubscribe(subs)
