#!/usr/bin/env python

"""
This program rotates a Square, illustrating the simplest possible
animation.  
The animation is accomplished by registring an idle-callback function,
and incrementing a key parameter in the idle function.
That key parameter (an angle theta in this code) controls how
the display looks.  Redisplay is forced by glutPostRedisplay().
Note that animations should use double-buffering, which requires
initializing that as the display mode, and swapping buffers after
each display is flushed from the pipeline.
This version also draws a circle and the origin to make things
clearer.
"""

#import pydoc #Not used
__author__= "Joseph O'Rourke"
__version__ = "1.0"
__date__= "Sep10"

import sys
from math import *
#import time  #Not used in this version
from OpenGL.GL import *
from OpenGL.GLUT import *

theta = 0.0    # angle around circle for RotSquare center
nsteps = 0

##############################################################################
def RotSquare( angle ):
    """
    Draws a Square rotated by angle out on circle.
    """
    
    glClear(GL_COLOR_BUFFER_BIT)
    
    glColor3f( 0.0, 1.0, 0.0 )     #Green
    arc( 0., 0., 1., 0., 360., 36 )
    glColor3f( 1.0, 1.0, 1.0 )     #White
    MarkOrigin()
    
    glColor3f( 1.0, 0.0, 0.8 )     #Roughly: violet

    glPushMatrix()
    glRotatef( angle, 0.0, 0.0, 1.0 )# Rotate coord system
    glTranslatef( 1.0, 0.0, 0.0 )    # Translate out to circle
    glRectf(-0.5, -0.5, 0.5, 0.5)    # Draw a RotSquare
    glPopMatrix()
    
def arc(x, y, r, a, b, n):
    """
    Draw an arc of a circle.
    a and b are assumed to be in degrees!
    n is the number of points in a full circle.
    """

    glBegin( GL_LINE_STRIP )
    for i in range( n+1 ):
        angdeg = 360. * i / n; 
        angrad = 2 * pi * angdeg / 360.;
        if (angdeg >= a) and (angdeg <= b):
            x = r * cos( angrad );
            y = r * sin( angrad );
            glVertex2f( x, y )
    glEnd()


def MarkOrigin( ):
    """
    Marks a cross at the origin just so we can see it.
    """
    glBegin(GL_LINES)
    glVertex2f( -0.1,0.0 )
    glVertex2f(  0.1,0.0 )
    glVertex2f( 0.0,-0.1 )
    glVertex2f( 0.0, 0.1 )
    glEnd()
    
##############################################################################
def displayGL():
    """
    What to do when the screen is repainted: draw the rectangle.
    """

    global theta
    
    glClear( GL_COLOR_BUFFER_BIT )
    RotSquare( theta )
    glFlush() #Flush the graphics pipeline buffer
    glutSwapBuffers() #For animation
    
def reshapeGL(width,height):
    """
    What to do when the window is resized: reset coord system etc.
    Initial creation of window constitutes a resize.
    """
    
    w = width / float(height)
    h = 1.0
    
    glViewport( 0, 0, width, height )
    glMatrixMode(GL_PROJECTION) #Work on projection matrix
    glLoadIdentity()
    glOrtho(-2.0, 2.0, -2.0, 2.0, -2.0, 2.0) # 4 x 4, origin in center
    # Note: first four numbers are xmin, xmax, ymin, ymax.
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def initializeGL():
    """
    What to do upon first invocation.
    """
    glClearColor(0.0, 0.0, 1.0, 0.0) #blue
        # Turn on antialiasing
##    glHint( GL_LINE_SMOOTH_HINT, GL_NICEST )
##    glEnable ( GL_LINE_SMOOTH )
##    glHint( GL_POLYGON_SMOOTH_HINT, GL_NICEST )
##    glEnable ( GL_POLYGON_SMOOTH )

def idleGL():
    """
    What to do when idle: increment theta
    """

    global theta
    global nsteps
    
    # mod 360 to keep angle in range [0,360).  (Not strictly necessary.)
    nsteps = nsteps + 1
    theta = (theta + 0.05) % 360
    #time.sleep(0.1) # seconds

    glutPostRedisplay() # Force redisplay


##############################################################################
if __name__=='__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE) #Double-buffering for animation

    glutInitWindowPosition(0, 0) #Upperleft corner.
    glutInitWindowSize(500, 500) #500 x 500 pixels
    glutCreateWindow("Rotating Square")
    initializeGL()
    
    glutDisplayFunc(displayGL) #Register display callback
    glutReshapeFunc(reshapeGL) #Register reshape callback
    glutIdleFunc(idleGL)       #Register idle callback
    
    glutMainLoop() #Infinite loop

