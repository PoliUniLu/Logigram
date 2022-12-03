'''

Logigram is a Python library for drawing logic diagrams.
Logic diagrams are used for visualizing Boolean structures.
LOGIGRAM is a package for visualizing Boolean functions in
disjunctive normal form (DNF). Resulting diagrams will thus consist of
disjunctions of conjunctions of literals.
As inputs and outputs, LOGIGRAM can process either binary or multivalent
factors.

'''

import SchemDraw
import SchemDraw.logic as logic
import SchemDraw.elements as elm
import re
from enum import Enum



# raw input
INPUT_PATTERN2 = re.compile('^([^<\= >]+)(<*\=>*(.+))$')




# clean input
def clean_input(input):
  if isinstance(input,str):
      new_inputs=[''.join(c for c in input if not c.isspace())]
  else:
     new_inputs=[''.join(filter(lambda x: not x.isspace() ,y)) for y in input]
  parsed_functions=[x for x in new_inputs if len(x)!=0]
  return parsed_functions

# implicants from input
def create_implicant_string(input):
 inputs=clean_input(input)
 result=set()
 for f in inputs:

   if INPUT_PATTERN2.match(f) is not None:
      result.update( INPUT_PATTERN2.match(f).group(1).split("+"))
   else:
    pass
 return '+'.join(result)

# variables
def get_the_variabels(f,multi_output=False,multi_value=False):
  if multi_output:
    result=create_implicant_string(f)
  else:
    f_new=clean_input(f)

    if INPUT_PATTERN2.match(f_new[0]) is not None:
      result = INPUT_PATTERN2.match(f_new[0]).group(1)
    else:
      pass
  res=(result.split("+"))
  res_final=set()
  if not multi_value:
    for i in res:
      res_final.update(c.upper() for c in (i.split("*")))
    return sorted(list(res_final))  
  
  else:
    for i in res:
      for j in (i.split("*")):
        res_final.add(j.split("{",1)[0])
    return (sorted(list(res_final)))

# output name
def get_output_label(f):
    functions=clean_input(f)
    res=[]
    for f in functions:
      if INPUT_PATTERN2.match(f) is not None:
        res.append(INPUT_PATTERN2.match(f).group(3))
      else:
        pass
    return res

# multi output > creating functions
def create_multiple_functions(input):
  functions=clean_input(input)
  result=[]
  for f in functions:
    if INPUT_PATTERN2.match(f) is not None:
      result.append(INPUT_PATTERN2.match(f).group(1).split("+"))
  return (result)

def create_implicants_multi_output(f,variables):
    l=len(variables)
    f_new=create_multiple_functions(f)
    all_implicants=dict()
    for ind,i in enumerate(f_new):
      for k in i:
        var_array=k.split("*")
        impl=[True]*l
        for indx,j in enumerate(variables):
          if j.upper() in var_array:
            impl[indx]=True
          elif j.lower() in var_array:
            impl[indx]=False
          else:
            impl[indx]=None
        new_impl=tuple(impl)
        if new_impl in all_implicants.keys():
          all_implicants[new_impl].add(ind)
        else:
          all_implicants[new_impl]={ind}
    
    return all_implicants

def parse_implicant(impl):
  return {m.group(1): int(m.group(2)) for m in
             re.finditer('([A-Z]+)\{([^}]+)\}\*?',impl)}

def create_implicants_multi_value_multi_output(f,variables):
  l=len(variables)
  all_implicants=dict()
  f_new=create_multiple_functions(f)
  for ind,i in enumerate(f_new):
    for j in i:
      impl=parse_implicant(j)
      impl_new=[None]*l
      for indx,k in enumerate(variables):
        if k in impl:
          impl_new[indx]=impl[k]
      k = tuple(impl_new)
      if k in all_implicants.keys():
        all_implicants[k].add(ind)
      else:
        all_implicants[k]={ind}
  return all_implicants



def create_implicants(f,variables):
    f=create_implicant_string(f)
    l=len(variables)
    f_new=f.split('+')
    all_implicants=[]
    for i in f_new:
      impl=[True]*l
      vars_in_impl = set(i.split('*'))
      for indx,j in enumerate(variables):
        if j.upper() in vars_in_impl:
          impl[indx]=True
        elif j.lower() in vars_in_impl:
          impl[indx]=False
        else:
          impl[indx]=None
      all_implicants.append(impl)
   
    return all_implicants




def create_implicants_multi_value(f,variables):
  f=create_implicant_string(f)
  l=len(variables)
  f_new=f.split('+')
  all_implicants=[]
  for i in f_new:
    impl=parse_implicant(i)
    impl_new=[None]*l
    for indx,j in enumerate(variables):
      if j in impl:
        impl_new[indx]=impl[j]
    all_implicants.append(impl_new)
  return all_implicants

        

def num_of_non_none(arr):
  return 1 if sum(1 for x in arr if x is not None) ==1  else 0

class Implicants:

  def __init__(self,implicant):
    if(isinstance(implicant[0], bool) or
       isinstance(implicant[0], int) or
       implicant[0] is None):
      self.implicant = implicant
      self.outputs = 1
    else:
      self.implicant=implicant[0]
      self.outputs=implicant[1]

  def get_outputs(self):
    return self.outputs


  def get_implicant(self):
    return self.implicant

  def nr_inputs(self):
    nr_inputs=0
    for i in self.implicant:
      if i is not None:
        nr_inputs=nr_inputs+1
    return nr_inputs

  def get_idxs_of_negated(self):
    cur_idx = 1
    res = []
    for x in self.implicant:
      if x is None:
        continue
      if not x:
        res.append(cur_idx)
      cur_idx += 1
    return res 

  def implicant_to_gate(self):  
    return logic.andgate(inputs=self.nr_inputs(),
                          inputnots=self.get_idxs_of_negated())
  


  def is_line(self):
    positive=0
    for i in self.implicant:
      if i is not None:
        positive=positive+1

    if(positive==1):
      return True
    else:
      return False
  
  def is_neg_gate(self):
    return sum(1 for x in self.implicant if self.is_line() and x is False) == 1

class ImplicantsMulti:

  def __init__(self,implicant):
    self.implicant=implicant[0]
    self.outputs=implicant[1]
 
  def get_implicant(self):
    return self.implicant
  
  def get_outputs(self):
    return self.outputs
  
  def nr_inputs(self):
    nr_inputs=0
    for i in self.implicant:
      if i is not None:
        nr_inputs=nr_inputs+1
    return nr_inputs

  def implicant_to_gate(self):  
    return logic.andgate(inputs=self.nr_inputs()) 

  def is_line(self):
    return True if self.nr_inputs()==1 else False


class GateWrapper(Implicants):

  def __init__(self, gate,implicant, multi_value = False):
    Implicants.__init__(self,implicant)
    self.gate = gate
    if multi_value:
      self.set_labels()
  
  def get_output(self):
    return self.gate.out

  def get_input(self, idx):
    return getattr(self.gate, 'in{}'.format(idx))
  
  def get_output_funcs(self):
    return self.outputs
  
  def set_labels(self):
    for i, v in enumerate(filter(lambda x: x is not None, self.implicant)):
      self.gate.add_label(str(v),loc='in{}'.format(i+1), size=7, ofst=0.01)
  
  def map_label_to_input_index(self,label_index):
    if self.implicant[label_index] is None:
      return None
    else:
      k=1
      for i,elm in enumerate(self.implicant):
          if i == label_index:
            return k
          if elm is not None:
            k = k + 1

class OrWrapper():

  def __init__(self,or_gate,multi_value = False, all_gates_in_indxs=None):
    self.or_gate=or_gate
    if multi_value:
      self.set_labels()
    self.all_gates_in_indxs = all_gates_in_indxs

  
  def get_input(self, idx):
    return getattr(self.or_gate, 'in{}'.format(idx))

  def get_all_gates_idx_for_input(self, in_idx):
    return self.all_gates_in_indxs[in_idx]

  def nr_of_inputs(self):
    return len(self.all_gates_in_indxs)
  
  def get_output(self):
    return self.gate.out
  
  


class LineWrapper(Implicants):

  def __init__(self, line,implicant):
    Implicants.__init__(self,implicant)
    self.line = line

  def get_input(self,index):
    if (index != 1):
      raise RuntimeError('Requested ')
    return self.line.start
  
  def get_output(self):
    return self.line.end
  
  def get_output_funcs(self):
    return self.outputs

  def map_label_to_input_index(self,label_index):
    if self.implicant[label_index] is None:
      return None
    return 1

def print_gates(d,implicants,output_label,color_and,multi_value=False):
  all_gates=[]
  for indx, i in enumerate(implicants.items()
                            if isinstance(implicants, dict)
                            else zip(implicants, [1] * len(implicants))):
    if(multi_value is False):
      impl=Implicants(i)
    else:
      impl=ImplicantsMulti(i)
    # first input >> gate/not/line
    if(indx==0):
      # is not a line >> AND GATE
      if(impl.is_line() is False):
          AND_GATE=d.add(impl.implicant_to_gate(),fill=color_and)
          all_gates.append(GateWrapper(AND_GATE,i,multi_value))
      # is not a line >> NOT GATE
      elif (len(implicants) == 1
            and multi_value is False
            and impl.is_neg_gate()):
          Not_gate = d.add(logic.NOT, d='right', fill='white')
          LINE = d.add(elm.LINE, d='right', l=d.unit)
          LINE.add_label(output_label, ofst=0.3, align=('left', 'bottom'))
          all_gates.append(LineWrapper(Not_gate, i))
      # is a LINE
      else:
        LINE=d.add(elm.LINE,d='right')
        all_gates.append(LineWrapper(LINE,i))
        if len(implicants)==1:
            LINE=d.add(elm.LINE,d='right',l=d.unit)
            LINE.add_label(output_label,ofst=0.3,align=('left','bottom'))
            if(multi_value):
                LINE.add_label('{}'.format( [x for x in i if x is not None][0]),
                                      size=7,ofst=-0.3,align=('left','bottom'))

    else:
      #gate
      if(impl.is_line() is False):
        AND_gate=d.add(impl.implicant_to_gate(),d='right',
                                                anchor='in1',
                                                fill=color_and,
                 xy=[all_gates[-1].get_input(all_gates[-1].nr_inputs())[0],
                     all_gates[-1].get_input(all_gates[-1].nr_inputs())[1]-1.2],

                )
        all_gates.append(GateWrapper(AND_gate,i,multi_value))

      #line after a line  
      elif(impl.is_line() and all_gates[-1].is_line()):
        LINE=d.add(elm.LINE,d='right',
                xy=[all_gates[-1].get_input(all_gates[-1].nr_inputs())[0],
                    all_gates[-1].get_input(all_gates[-1].nr_inputs())[1]-1.2],
                to=[all_gates[-1].get_output()[0],
                    all_gates[-1].get_output()[1]-1.2])
        all_gates.append(LineWrapper(LINE,i))

      #line after a gate
      elif(impl.is_line() and all_gates[-1].is_line() is False):
        LINE=d.add(elm.LINE,r='right',
                xy=[all_gates[-1].get_input(all_gates[-1].nr_inputs())[0],
                    all_gates[-1].get_input(all_gates[-1].nr_inputs())[1]-1.2],
                to=[all_gates[-1].get_output()[0],
                    all_gates[-1].get_input(all_gates[-1].nr_inputs())[1]-1.2])
        all_gates.append(LineWrapper(LINE,i))

  return all_gates

def get_ends_line(labels,all_gates):
  endings=[]
  for indx,l in enumerate(labels):
    for indx2, gate in enumerate(reversed(all_gates)):
      if gate.map_label_to_input_index(indx) is not None:
          endings.append((gate,gate.map_label_to_input_index(indx)))
          break
  return endings



def compare_with_eps(x,y):
  return abs(x-y) < 1e-10


def initial_lines_printing(d,f,labels, all_gates):
  l=len(labels)
  all_lines=[]
  ends=get_ends_line(labels,all_gates)
  for i,line, last_gate in zip(range(len(labels)),labels,reversed(ends)):
    max_len=max([len(labels[i]) for i in range(len(labels))])
    if max_len>1:
      rot=90
    else:
      rot=0
    

    if(i==0):
       L=d.add(elm.LINE,

              xy=[all_gates[0].get_input(1)[0]-0.5,
                  all_gates[0].get_input(1)[1]+0.5],
              to=[ends[-1][0].get_input(ends[-1][1])[0]-0.5,
                  ends[-1][0].get_input(ends[-1][1])[1]])
       L.add_label(labels[l-i-1],loc='rgt',ofst=None, align=None,
                                           rotation=rot,lblsize=0.04)
       all_lines.append(L)
    else:
      L=d.add(elm.LINE,
              xy=[L.start[0]-d.unit*2,L.start[1]],
                  #lftlabel=labels[l-i-1],
               to=[L.start[0]-d.unit*2,
                   last_gate[0].get_input(last_gate[1])[1]])
      L.add_label(labels[l-i-1],loc='rgt',ofst=None, align=None,
                                          rotation=rot,lblsize=0.04)
      all_lines.append(L)
  
  #conecting lines and AND GATES
  for index,i in enumerate(f):
    k=0
    for j_position,j in enumerate(i):
    
      if(j is not None):
        k=k+1
        x=all_gates[index].get_input(k)
        to_x = (all_lines[-(j_position+1)].start[0],x[1])
        LINE=d.add(elm.LINE,d='left', xy=[x[0],x[1]],
              to=to_x)
        if compare_with_eps(LINE.end[1], all_lines[-(j_position+1)].end[1]):
          pass

        else:
          d.add(elm.DOT)

def set_label_on_orinput(or_gate,f):
 labels=[]
 for i,elm in enumerate(f):
   Implicant=Implicants(elm)
   if Implicant.is_line():
      labels.extend([(x,i+1) for x in Implicant.implicant if x is not None])

 for i in labels:
   or_gate.add_label(str(i[0]),loc='in{}'.format(i[1]),size=7,
                                            ofst=0.01,align=('left','bottom'))


def or_lines(d,f,all_gates,output_label,color_or,multi_value=False):
  l_implicants=len(f)
  if(l_implicants>1):
    if(multi_value):
       gate_or = logic.orgate(inputs=l_implicants)
    else:
      neg_indexes=[i+1 for i in range(len(all_gates))
                   if all_gates[i].is_neg_gate()]
      gate_or = logic.orgate(inputs=l_implicants,inputnots=neg_indexes)
    len_half=l_implicants//2
    if (l_implicants%2==1):
      GATE_OR=d.add(gate_or,d='right',anchor='out',fill=color_or,
        xy=[all_gates[0].get_output()[0]+1.1*l_implicants,
            all_gates[l_implicants//2].get_output()[1]])
      if(multi_value):
        set_label_on_orinput(GATE_OR,f)
      Out_line=d.add(elm.LINE, d='right', l=d.unit/4)
      Out_line.add_label(label=output_label,ofst=0.3,align=('left','bottom'))
     
     #print the mid line firt
      d.add(elm.LINE,d='right',
            xy=[all_gates[len_half].get_output()[0],
                all_gates[len_half].get_output()[1]],
            to=(getattr(GATE_OR,'in'+'{}'.format(len_half))[0],
                getattr(GATE_OR,'in'+'{}'.format(len_half))[1]))
    else:
      GATE_OR=d.add(gate_or,d='right',anchor='out', fill= color_or,
        xy=[all_gates[0].get_output()[0]+l_implicants+1,
          (all_gates[l_implicants//2-1].get_output()[1]+
           all_gates[l_implicants//2].get_output()[1])/2])
      if(multi_value):
        set_label_on_orinput(GATE_OR,f)

      Out_line=d.add(elm.LINE, d='right', l=d.unit/4)
      Out_line.add_label(label=output_label,ofst=0.3,align=('left','bottom'))

    j=0
    all_gates_reverse=[x for x in reversed(all_gates)]
    up=1
    down=l_implicants
    for i in zip(all_gates[:l_implicants//2],
                 all_gates_reverse[:l_implicants//2]):
      j=j+1.5
      L_left=d.add(elm.LINE,d='right',l=l_implicants-j,
                   xy=[i[0].get_output()[0],
                       i[0].get_output()[1]])
      L_down=d.add(elm.LINE,d='down',
                   to=(L_left.end[0],getattr(GATE_OR,'in'+'{}'.format(up))[1]))
      L_final=d.add(elm.LINE,d='right',
                   to=getattr(GATE_OR,'in'+'{}'.format(up)))
      L_left2=d.add(elm.LINE,d='right',l=l_implicants-j,
                    xy=[i[1].get_output()[0],
                        i[1].get_output()[1]])
      L_up=d.add(elm.LINE,d='up',
                 to=(L_left2.end[0],getattr(GATE_OR,'in'+'{}'.format(down))[1]))
      L_final2=d.add(elm.LINE,d='right',
                     to=getattr(GATE_OR,'in'+'{}'.format(down)))   
      up=up+1
      down=down-1


class LineWrapper2:

  def __init__(self, line):
    self.line = line

  def get(self, *args, **kwargs):
    return self.line.get(*args, **kwargs)

  def add_label(self, *args, **kwargs):
    return self.line.add_label(*args, **kwargs)

  def __getitem__(self, x):
    return self.line[x]

  def __iter__(self):
    return iter(self.line)

  def __getattr__(self, name):
    if name == 'in1':
      return self.line.start
    elif name == 'out':
      return self.line.end
    return self.__getattribute__(name)

def print_ors(d,inputs,all_gates, labels,color_or):
 
  max_len=max([len(labels[i]) for i in range(len(labels))])
  if max_len>3:
      rot=90
  else:
      rot=0 
  all_ors=[]
  func_idxs = set()
  for x in inputs.values():
    func_idxs.update(x)
  nr_ors=len(func_idxs)
  for j in range(nr_ors):
   neg_indexes = []
   out_idx = 1
   for i, gate in enumerate(all_gates):
     if j not in gate.get_output_funcs():
       continue
     if gate.is_neg_gate():
       neg_indexes.append(out_idx)
     out_idx+=1
   nr_of_inputs=sum(1 for x in all_gates if j in x.get_output_funcs())
   all_gates_in_idxs = [i for i,gate in enumerate(all_gates) if
                        j in gate.get_output_funcs()]
   if nr_of_inputs == 1:
     if len(neg_indexes) == 1:
       gate_or = logic.NOT
       GATE_OR=LineWrapper2(d.add(gate_or,d='up',anchor='out',fill=color_or,
          xy=[all_gates[0].get_output()[0]+j*4*d.unit+2,
            (all_gates[0].get_output()[1]+ 6*d.unit
             )]))
       GATE_OR.add_label(labels[j], loc='out',ofst=None, align=None,
                                              rotation=rot,lblsize=0.04)
     else:
     # Change this
       gate_or = elm.LINE #logic.orgate(nr_of_inputs,inputnots=neg_indexes)
       GATE_OR=LineWrapper2(d.add(gate_or,d='up',fill=color_or,
          xy=[all_gates[0].get_output()[0]+j*4*d.unit+2,
            (all_gates[0].get_output()[1]+ 6*d.unit
             )]))
       GATE_OR.add_label(labels[j], loc='rgt',ofst=None, align=None,
                                              rotation=rot,lblsize=0.04)
   else:
     gate_or = logic.orgate(nr_of_inputs,inputnots=neg_indexes)
     GATE_OR=d.add(gate_or,d='up',anchor='out',fill=color_or,
          xy=[all_gates[0].get_output()[0]+j*6*d.unit+2,
            (all_gates[0].get_output()[1]+ 6*d.unit
             )])
     GATE_OR.add_label(labels[j], loc='out',ofst=0.5, align=None,
                                            rotation=rot,lblsize=0.04)
   all_ors.append(OrWrapper(GATE_OR, all_gates_in_indxs=all_gates_in_idxs))
  return all_ors

def add_line_after_ands(d,all_ors,all_gates,multi_value):

  line_ends = [0]*len(all_gates)
  for gate_or in all_ors:
     for i in range(gate_or.nr_of_inputs()):
        in_coords = gate_or.get_input(i+1)
        gate_idx = gate_or.get_all_gates_idx_for_input(i)
        line_ends[gate_idx] = max(line_ends[gate_idx], in_coords[0])
  
  for gate_or in all_ors:
    for i in range(gate_or.nr_of_inputs()):
      in_coords = gate_or.get_input(i+1)
      gate_idx = gate_or.get_all_gates_idx_for_input(i)
      out_coords = all_gates[gate_idx].get_output()
      Line=d.add(elm.LINE, d='down', xy=in_coords, to=[in_coords[0],
                                                       out_coords[1]])
      if all_gates[gate_idx].is_line() and multi_value:
        label = [x for x in all_gates[gate_idx].implicant if x is not None][0]
        Line.add_label(str(label),loc='rgt',size=7,
                                  ofst=0.1,align=('left','bottom'))
      if in_coords[0] == line_ends[gate_idx]:
        d.add(elm.LINE, d='right', xy=out_coords,
                        to=[in_coords[0], out_coords[1]])
      else:
        d.add(elm.DOT)
      


def draw_boolean_func(f, variables,output_label,multi_value,multi_output,
                      color_or,color_and):
  d = SchemDraw.Drawing(unit=.5)
  all_gates = print_gates(d, f,output_label,color_and,multi_value)
  initial_lines_printing(d, f, variables, all_gates)
  if not multi_output:
    or_lines(d,f,all_gates,output_label,color_or,multi_value)
  else:
    all_ors=print_ors(d,f,all_gates, output_label,color_or)
    add_line_after_ands(d,all_ors,all_gates,multi_value)
  return d



PATTERN11 = re.compile('^(([A-Z]+|[a-z]+)((\+|\*)([A-Z]+|[a-z]+))*)'
                       '(<*\=>*[A-Za-z0-9-\{-\}-,]+)$')
PATTERN22 = re.compile(r'^(([A-Z]+\{[0-9]+\})((\+|\*)([A-Z]+\{[0-9]+\}))*)'
                       r'(<*\=>*[A-Za-z0-9-\{-\}-,]+)$')



class Mode(Enum):
  BOOLEAN_MODE = 1
  MULTI_VALUE_MODE = 2
  INVALID = 3
  MULTI_OUTPUT = 4
  MUTLI_VALUE_MULTI_OUT =5


def get_mode(input):
    if isinstance(input,str):
        new_inputs=[''.join(c for c in input if not c.isspace())]
    else:
        new_inputs=[''.join(filter(lambda x: not x.isspace(),y)) for y in input]
    res=[x for x in new_inputs if len(x)!=0]
    if all(PATTERN11.match(s) is not None for s in res):
        if len(res)>1:
            return Mode.MULTI_OUTPUT
        else:
            return Mode.BOOLEAN_MODE

    elif all(PATTERN22.match(s) is not None for s in res):
        if len(res)>1:
          return  Mode.MUTLI_VALUE_MULTI_OUT
        else:
          return Mode.MULTI_VALUE_MODE

    else:
        return Mode.INVALID


def replace_quote(match):
    text = match.group()
    if '\'' in text:

        return text.replace('\'', '')
    else:
        return text.upper()


def prime_to_nonprime(input):
    regex = re.compile('([a-z-0-9]+\'*)')
    new_input = []
    for elm in input:
        onset, offset = elm.split('=')
        if ('\'' not in elm):
            new_onset = onset.upper()
        else:
            new_onset = regex.sub(replace_quote, onset)
        new_input.append(new_onset+"="+offset)
    return new_input


"""

Drawing of a boolean expression.

Parameters

----------

input : string
    A boolean function in DNF form in the expected binary or the
    multivalue format.

color_or : string
    The name of the color of OR gates.

color_and : string
    The name of the color of AND gates.

notation : string
    Possible values - prime, nonprime.
    Differentiating between 2 possible 
    variable notations.
    
"""

def draw_schem(input,color_or = 'lightblue',color_and = 'lemonchiffon',
               notation='case_based', showplot=True):
    if notation =='prime':
        input= prime_to_nonprime(input)
    mode = get_mode(input)
    if mode==Mode.BOOLEAN_MODE:
      variables=get_the_variabels(input)
      if notation == 'prime':
          variables=[x.lower() for x in variables]
      output_label=get_output_label(input)
      f_filtered = ''.join(c for c in input if not c.isspace())    
      f=create_implicants(f_filtered,variables)
      multi_value=False
      multi_output=False
    elif mode==Mode.MULTI_VALUE_MODE:
      output_label=get_output_label(input)
      variables=get_the_variabels(input,multi_value=True)
      f=create_implicants_multi_value(input,variables)
      multi_value=True
      multi_output=False
    elif mode== Mode.MULTI_OUTPUT:
      output_label=get_output_label(input)
      variables=get_the_variabels(input,multi_output=True)
      if notation =='prime':
          variables=[x.lower() for x in variables]
      f=create_implicants_multi_output(input,variables)
      multi_value=False
      multi_output=True
    elif mode== Mode.MUTLI_VALUE_MULTI_OUT:
      output_label=get_output_label(input)
      variables=get_the_variabels(input,multi_output=True,multi_value=True)
      f=create_implicants_multi_value_multi_output(input,variables)
      multi_value=True
      multi_output=True
    else:
      raise RuntimeError('Unsupported input entered.')
      
    if not multi_output:
      f.sort(key=num_of_non_none)
    d=draw_boolean_func(f,variables,output_label,multi_value,
                        multi_output,color_or,color_and)
    d.draw(showframe=False, showplot=False)
    f=d.fig

    return f

def save_figure(f,file_name,file_format,dpi=72):
    f.savefig(file_name+"."+file_format,bbox_inches='tight',dpi=dpi)

if __name__ == '__main__':
        

    f= draw_schem(["a'<=>D"],color_or = 'red',color_and = 'Blue',
                  notation='prime')