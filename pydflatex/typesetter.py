#!/usr/bin/env python

import subprocess
import datetime
import os

from .processor import Processor, LaTeXError

class Typesetter(Processor):
	"""
	Typeset a TeX file.
	Options:
		- halt_on_errors
		- xetex
	"""

	defaults = Processor.defaults.copy()
	defaults.update({
			'halt_on_errors': True,
			'xetex': False,
			})

	def engine(self):
		return ['pdflatex','xelatex'][self.options['xetex']]

	def arguments(self):
		"""
		Arguments to the (pdf|xe)latex command.
		"""
		args = [self.engine(),
				'-8bit',
				'-no-mktex=pk',
				'-interaction=batchmode',
				'-synctex=1',
				'-output-directory=.tmp'
				]
		if self.options['halt_on_errors']:
			args.insert(-1, '-halt-on-error')
		return args

	def typeset(self, full_path, file_base):
		"""
		Typeset one given file.
		"""
		# make sure that the file exists
		if not os.path.exists(full_path):
			raise LaTeXError('File {0} not found'.format(full_path))
		# run pdflatex
		os.system("mkdir -p .tmp")
		now = datetime.datetime.now().strftime('%Y-%m-%d %H.%M.%S')
		self.logger.message("\t[{now}] {engine} {file}".format(engine=self.engine(), file=full_path, now=now))
		arguments = self.arguments()
		# append file name
		arguments.append(full_path)
		self.logger.debug("\n"+" ".join(arguments)+"\n")
		output = subprocess.Popen(arguments, stdout=subprocess.PIPE).communicate()[0]
		self.logger.message(output.splitlines()[0].decode('utf8'))
		os.system("mv \"" + os.path.join(".tmp", file_base + os.path.extsep + "pdf") + "\"  .")