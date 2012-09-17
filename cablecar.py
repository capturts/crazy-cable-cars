#!/usr/bin/env python

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

class Car(object):
	def __init__(self, path, loop=False, auto=False):
		self.path=path
		self.loop=loop
		self.auto=auto
		if self.auto==True:
			self.dir=1
		else:
			self.dir=0 # -1 = back, 0 = stop, 1 = onwards
		self.x=self.path[0][0]
		self.y=self.path[0][1]
		self.fwd_x=0
		self.fwd_y=0
		self.rev_x=-0
		self.rev_y=-0
		self.node=0
		self.win=False
		self.lives=5
		self.getVectors()
	
	def move(self):
		if self.dir<0:
			# going backwards...
			change_x=self.rev_x
			change_y=self.rev_y
		elif self.dir>0:
			# forwards...
			change_x=self.fwd_x
			change_y=self.fwd_y
		else:
			change_x=0
			change_y=0
		self.x=self.x+change_x
		self.y=self.y+change_y
		self.getVectors()

	def getVectors(self):
		try:
			self.node=self.path.index((self.x, self.y))

			# we are on a node
			if self.node==len(self.path)-1:
				# We are at the end
				if self.auto==True:
					self.dir=-1
				else:
					self.fwd_x=0
					self.fwd_y=0
					self.rev_x=0
					self.rev_y=0
					self.win=True
			else:
				if self.node==0:
					if self.auto==True:
						self.dir=1
					else:
						self.rev_x=0
						self.rev_y=0
				else:
					diff_x=self.path[self.node-1][0]-self.path[self.node][0]
					diff_y=self.path[self.node-1][1]-self.path[self.node][1]
					self.rev_x=float(diff_x)/20
					self.rev_y=float(diff_y)/20

				# forward
				diff_x=self.path[self.node+1][0]-self.path[self.node][0]
				diff_y=self.path[self.node+1][1]-self.path[self.node][1]
				self.fwd_x=float(diff_x)/20
				self.fwd_y=float(diff_y)/20

		except ValueError:
			# we are between nodes
			if self.dir>0:
				#forward motion
				self.rev_x=-self.fwd_x
				self.rev_y=-self.fwd_y
			elif self.dir<0:
				#backward motion
				self.fwd_x=-self.rev_x
				self.fwd_y=-self.rev_y
