#!/usr/bin/env python
# coding: UTF-8
from __future__ import division

import os
import time

from .processor import Processor, LaTeXError
from .typesetter import Typesetter
from .open_pdf import OpenPdf
from .log_processor import LogProcessor
from .cleaner import Cleaner

class Runner(Processor):

	defaults = {
		'typesetting': True,
		'log_parsing': True,
		'open_after': False,
	}

	@classmethod
	def paths(self, tex_path):
		"""
		Figure out useful paths from the tex_path, and make sure that extension is tex.
		For tex_path = path/to/file.tex, or path/to/file we get
		base: path/to
		file_base: file
		root: path/to/file
		full_path: path/to/file.tex
		"""
		# find out the directory where the file is
		base, file_name = os.path.split(tex_path)
		file_base, file_ext = os.path.splitext(file_name)
		# setup the TEXINPUTS variable
		os.environ['TEXINPUTS'] = base + ':'
		# find out the name of the file to compile
		root, file_ext = os.path.splitext(tex_path)
		if file_ext[1:]:
			if file_ext[1:] != 'tex':
				raise LaTeXError("Wrong extension for {0}".format(tex_path))
			else:
				full_path = tex_path
		else:
			full_path = root + os.path.extsep + 'tex'
		return {'base':base, 'file_base':file_base, 'root':root, 'full_path':full_path}

	def prepare(self, tex_path=None):
		if tex_path is None:
			tex_path = self.tex_path
		paths = self.paths(tex_path)
		return tex_path, paths

	def typeset(self, full_path, file_base):
		time_start = time.time()
		typesetter = Typesetter(logger=self.logger, options=self.options)
		typesetter.typeset(full_path, file_base)
		time_end = time.time()
		return time_end - time_start

	def process_log(self, base, file_base):
		log_processor = LogProcessor(logger=self.logger, options=self.options)
		log_file_path = log_processor.log_file_path(base, file_base)
		error = log_processor.process_log(log_file_path)
		return error

	def clean(self, base, file_base):
		cleaner = Cleaner(logger=self.logger, options=self.options)
		cleaner.handle_aux(base, file_base)

	def open_pdf(self, root):
		opener = OpenPdf(logger=self.logger, options=self.options)
		opener.open_pdf(root)

	def run(self, tex_path=None):
		"""
		Compile the current tex file.
		"""
		tex_path, paths = self.prepare(tex_path)

		full_path = paths['full_path']

		if self.options['typesetting']:
			time_diff = self.typeset(full_path, paths['file_base'])
			success_message = 'Typesetting of "{name}" completed in {time:.1f}s.'.format(name=full_path, time=(time_diff))

		if self.options['log_parsing']:
			# Parse log
			error = self.process_log(paths['base'], paths['file_base'])
			if error and self.options['halt_on_errors']:
				raise LaTeXError(error.get('text'))

		if self.options['typesetting']:
			# Print success message
			self.logger.success(success_message)
			# Post process
			#self.clean(paths['base'], paths['file_base'])
			# Open pdf
			if self.options['open_after']:
				self.open_pdf(paths['root'])

