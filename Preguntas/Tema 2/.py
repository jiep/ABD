# -*- coding: utf-8 -*-

from mrjob.job import MRJob

class MRWordFrequencyCount(MRJob):
    
    def mapper(self, _, line):
        