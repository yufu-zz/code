#! /usr/bin/env python

import sys
import time

try:
	from OpenGL.GLUT import *
	from OpenGL.GL import *
	from OpenGL.GLU import *
except:
	print 'ERROR: PyOpenGL not installed properly'
	sys.exit()

a_range = [20.0, 20.0] # axis range
w_size = [500, 500] #Initial window size

def init():
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
	glutInitWindowSize(w_size[0], w_size[1])
	glutInitWindowPosition(100, 100)
	glutCreateWindow('Points')
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glShadeModel(GL_FLAT)

def draw_point(point):
	glBegin(GL_POINTS)
	glVertex2f(point[0], point[1])
	glEnd()

def draw_points(points):
	for point in points:
		draw_point(point)

def display():
	points = [[i, -i+20] for i in range(0, 21)]
	points.append([0, 0])
	glClear(GL_COLOR_BUFFER_BIT)
	glPushMatrix()
	glColor3f(1.0, 1.0, 1.0)
	glPointSize(3.0)
	draw_points(points)
	points = [[i, 0] for i in range(0, 21)]
	draw_points(points)
	glutSwapBuffers()

def reshape(w, h):
	w_size = [w, h]
	glViewport(0, 0, w, h)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
#glOrtho(-w_size[0]/a_range[0]/4, w_size[0]/a_range[0]/4, \
#			-w_size[1]/a_range[1]/4, w_size[1]/a_range[1]/4, -1.0, 1.0)
	glOrtho(-20, 20, -20, 20, -1.0, 1.0)
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()

if __name__ == '__main__':
	init()
	glutDisplayFunc(display)
	glutReshapeFunc(reshape)
#	glutMouseFunc(mouse)
	glutMainLoop()
