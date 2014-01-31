"""
Module written by Niklaus Johner (niklaus.johner@a3.epfl.ch) 01.2013
This module contains functions for reading and writing files
"""
from ost import *
import math

__all__=('ReadMissingResiduesFromPDB','ReadSymmetryFromPDB','ParsePDBForCubicPhase',\
             'ReadUnitCellFromPDB','WriteListOfListsInLines','WriteListOfListsInColumns',\
             'WriteFloatList','ReadFloatListFile','ReadFile')

def ReadMissingResiduesFromPDB(filename):
  file=open(filename,'r')
  missing_res_list=[]
  flag=False
  for l in file:
    if l.startswith('REMARK 465   M RES C SSSEQI'):
      flag=True
      continue
    if not flag:continue
    if not l.startswith('REMARK 465'):
      flag=False
      continue
    s=l.split()
    try:missing_res_list.append((s[3],int(s[4]),s[2]))
    except:print 'could not add residue for line:',l
  return missing_res_list
  
def ReadSymmetryFromPDB(file):
  file.seek(0)
  search_string='SMTRY1'
  transformation_list=[]
  for line in file:
    sl=line.split()
    if sl[0]=='ATOM': break
    try:
      if (sl[0]=='REMARK' and sl[1]=='290' and sl[2]==search_string):
        i=int(search_string[-1])
        if i==1:
          a=[]
        for j,el in enumerate(sl[4:8]):
          a.append(float(el))
        search_string=search_string[:-1]+str(i+1)
        if i==3:
          a.extend([0.0,0.0,0.0,1.0])
          transformation_list.append(geom.Mat4(a[0],a[1],a[2],a[3],a[4],a[5],a[6],a[7],a[8],a[9],a[10],a[11],a[12],a[13],a[14],a[15]))
          search_string=search_string[:-1]+str(1)
      else: continue
    except: continue
  return transformation_list
  
def ParsePDBForCubicPhase(file):
  file.seek(0)
  search_lines=['REMARK','280']
  search_strings=['LIPIDIC MESOPHASE','LIPIDIC CUBIC PHASE','LIPID CUBIC PHASE']
  flag=0
  file_string=''
  for line in file:
    sl=line.split()
    if sl[0]=='ATOM': break
    try:
      flag2=0
      for i,el in enumerate(search_lines):
        if sl[i]!=el:flag2=1
      if flag2: continue
      if len(sl)==2:
        flag+=1
        continue
      if flag==2:
        for el in sl[2:]:
          file_string+=' '+el
    except:continue
  #sl=file_string.split(', ')
  for el in search_strings:
    #if el in sl:
    if el in file_string:
      return True
  return False

def ReadUnitCellFromPDB(file):
  file.seek(0)
  search_string='CRYST1'
  flag=0
  for line in file:
    if not line[:6]==search_string:
      continue
    sl=line.split()
    print 'Cryst1 found:',sl
    uc=sl[1:7]
    for i,el in enumerate(uc):
      if i<3:
        uc[i]=float(el)
      else:
        uc[i]=float(el)*math.pi/180
    return uc
  return 'na'
  
def WriteListOfListsInLines(column_titles,ll,filename,separator=','):  
  f=open(filename,'w')
  f.write(separator.join(column_titles)+'\n')
  for l in ll:
    f.write(separator.join([str(el) for el in l])+'\n')
  f.close()
  return

def WriteListOfListsInColumns(column_titles,ll,filename,separator=','):  
  f=open(filename,'w')
  f.write(separator.join(column_titles)+'\n')
  for i in range(len(ll[0])):
    l=[str(el[i]) for el in ll]
    f.write(separator.join(l)+'\n')
  f.close()
  return

def WriteFloatList(fl,filename,separator=',',column_title=None):
  f=open(filename,'w')
  if column_title:f.write(column_title+'\n')
  for el in fl:
    f.write(str(el)+'\n')
  f.close()
  return


def ReadFloatListFile(filename,separator=',',column_titles=True):
  float_list_dict={}
  f=open(filename,'r')
  titles=f.next().rstrip()
  titles=titles.split(separator)
  if column_titles:
    for el in titles:float_list_dict[el]=FloatList()
  else:
    for i in range(len(titles)):float_list_dict[i]=FloatList()
    titles=range(len(titles))
    f.seek(0)
  for l in f:
    sl=l.split(separator)
    for el,title in zip(sl,titles):float_list_dict[title].append(float(el))
  return float_list_dict
  
def ReadFile(filename,format,separator=',',column_titles=True):
  float_list_dict={}
  f=open(filename,'r')
  if column_titles:
    titles=f.next().rstrip()
    titles=titles.split(separator)
  else:titles=range(len(format))
  for el in titles:float_list_dict[el]=[]
  for l in f:
    sl=l.split(separator)
    for el,title in zip(sl,titles):float_list_dict[title].append(el)
  for title,f in zip(titles,format):
    if f in ['float','f']:float_list_dict[title]=FloatList([float(el) for el in float_list_dict[title]])
    if f in ['int','i']:float_list_dict[title]=IntList([int(el) for el in float_list_dict[title]])
  return float_list_dict
