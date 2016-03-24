#!/bin/env python
# -*- encoding: utf-8 -*-

from pyrrd.rrd import RRD
from pyrrd.backend import bindings


class BaseAnalysisClass(object):

    default_options = {}

    def __init__(self, tag, mt_rrd_info, kargs):
        self.rrd_data = {}
        for mt, series_data in mt_rrd_info.items():
            self.load_rrds_from_pathopt(mt, series_data)

        self.tag = tag
        self.kargs = kargs

    def load_rrds_from_pathopt(self, mt, series_data):
        self.rrd_data[mt] = {}

        for k, series_info in series_data.items():
            self.rrd_data[mt][k] = [
                {
                    'data': self.load_rrd(s['filepath'],
                                          s['source'],
                                          self.default_options.get(k, {})),
                    'series': s['series']
                } for s in series_info]

    @classmethod
    def load_rrd(cls, filepath, options, default_options):
        take_param = lambda k: (k, options[k]
                                if k in options else default_options.get(k))
        kargs = dict(map(take_param, ['start', 'end', 'resolution', 'cf']))
        rrd = RRD(filepath, mode='r', backend=bindings)
        rrd_data = rrd.fetch(**kargs)
        return rrd_data.get('42')

    def analysis(self):
        """
        データから、マシンの状態
        * Success = 0
        * Warning = 1
        * Error = 2
        の3つの状態を辞書で返す
        {
            ('localhost', 'localhost'): State.SUCCESS,
            ('machine', 'm1'): State.WARNING,
            ('machine', 'm2'): State.ERROR
            ('machine', 'm3'): State.INFO
        }
        """
        pass

    def make_view(self):
        """
        解析データから、Webページを生成し
        MachineTupleと文字列の辞書で返す
        {
            ('localhost', 'localhost'): '<HTML>~~',
            ('machine', 'm1'):  '<HTML>~~',
            ('machine', 'm2'):  '<HTML>~~'
        }
        """
        pass
