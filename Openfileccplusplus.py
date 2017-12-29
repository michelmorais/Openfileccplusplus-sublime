import sublime
import sublime_plugin
import sys
import re
import os

def baseName(filename,character):
	if filename.find(character) > -1:
		words2 = filename.split(character)
		return baseName(words2[-1],character)
	return filename

def openFile(line,settings):
	m = re.search('^\s*(?!\/[\/|\*])\s*\#include\s+[<|"](.*)[>|"]', line)
	if m != None and settings.has('dir'):
		filename = m.group(1)
		filename = baseName(filename,'/')
		filename = baseName(filename,'\\')
		folder=sublime.active_window().extract_variables()['folder']
		#print("searching [" + filename + "] in [" + folder + "]")
		if openFromFolder(filename,folder,True) == False:
			folder = settings.get('dir')
			for path in folder:
				openFromFolder(filename,path,False)

def openFromFolder(filename,folder,recursive):
	bfound = False
	for root, dirs, files in os.walk(folder,topdown=True):
		for file in files:
			if file == filename:
				fullfilename = os.path.join(root, file)
				bfound = True
				sublime.active_window().open_file(fullfilename)
		if recursive == False:
			break
				
	return bfound

class openccplusCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		# Walk through each region in the selection
		for region in self.view.sel():
			# Only interested in empty regions, otherwise they may span multiple
			# lines, which doesn't make sense for this command.
			if region.empty():
				# Expand the region to the full line it resides on, excluding the newline
				line = self.view.line(region)
				# Extract the string for the line, and add a newline
				lineContents = self.view.substr(line)
				# Add the text at the beginning of the line
				openFile(lineContents,self.view.settings())

