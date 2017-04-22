#!/usr/bin/python
# -*- coding: UTF-8 -*-
try:
    import configparser #python 3
except:
    import ConfigParser as configparser #python 2
import os
"""
ConfigParser Support Unicode
https://my.oschina.net/cppblog/blog/384099
http://laochake.iteye.com/blog/443704
http://www.cnblogs.com/zhaoweiwei/p/ConfigParser.html
"""
class Config:
    """ [class] """
    
    def __init__( self, path = None, file = None ):
        """ [construct] """
        if path is None:
            if 'lib' in os.path.abspath(''):
                self.path = os.path.abspath('').replace('lib','')
            else:
                self.path = os.path.abspath('')+'\\'
        else:
            self.path = path
        if file is None:
            if os.path.exists(self.path+'config.ini'):
                self.file = 'config.ini'
            else:
                self.file = file
        else:
            self.file = file
        self.config = self.__readCfg( self.path, self.file )

    def __readCfg( self, path = None, file = None ):
        """ [private] Returns class configparser.ConfigPaser()  . 
            {path} : absolute path of the configuration file
            {file} : file name of the configuration file
        """
        if path is None:
            self.path = self.path
        else:
            self.path = path
        if file is None:
            self.file = self.file
        else:
            self.file = file
        config = configparser.ConfigParser()
        config.read( self.path + self.file, encoding='utf-8-sig')
        return config

    def getCfg( self, section = None ):
        """ [public] Returns dicts , a configuration file info. 
            {section} : None -> all sections info, Not None -> one section info
        """
        sections = self.config.sections()
        if section is not None :
            sections = [section]
        dicts = {}
        for i in sections:
            dicts.setdefault(i)
            for key, value in self.config.items(i):
                if not dicts.get(i) :
                    dicts[i]=dict({key:value})
                else:
                    dicts[i].setdefault(key,value)
        return (dicts[section] if (section is not None) else dicts)

    def showFile( self ):
        """ [public] No Returns, Display a file name of a configuration file  """
        print (self.file)

    def showPath( self ):
        """ [public] No Returns, Display the absolute path of a configuration file  """
        print (self.path)

    def showSections( self ):
        """ [public] No Returns, Display all sections of a configuration file  """
        print (self.config.sections())

    def showSectionsInfo( self, section = None ):
        """ [public] No Returns, Display all sections of a configuration file  """
        dicts = self.getCfg()
        for i in sorted(dicts.keys()):  
            print ('['+i+']')
            for key, value in sorted(dicts[i].items()):
                print(key,'=',value)
            print ('')                              
            if section is not None:
                break

# def test(): 
#     cfg = Config()  
#     cfg.showSections() 
#     cfg.showSectionsInfo()

# if __name__ == '__main__':
#     test()