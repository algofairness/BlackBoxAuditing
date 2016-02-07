
class SparseList(list):
  def __init__(self, default=0):
    self.default = default
    self.vals = {}
    self.size = 0
  def __setitem__(self, index, value):
    if self.default != value:
      self.vals[index] = value
    self.size += 1
  def __len__(self):
    return self.size
  def __getitem__(self, index):
    try:
      return self.vals[index]
    except (KeyError, IndexError):
      return self.default
  def __repr__(self):
    return "<SparseList {}>".format(self.vals)
  def append(self, val):
    self[self.size] = val
  def sort(self):
    values = sorted(self.vals.values())
    self.vals = {}
    old_size = self.size
    self.size = 0

    need_to_add_default = True
    for value in values:
      if need_to_add_default and self.default < value:
          self.size += (old_size - len(values))
          need_to_add_default = False
      self.append(value)

def test():
  l = SparseList(default=0)
  l.append(0)
  l.append(0)
  l.append(-1)
  l.append(2)

  print "SparseList size correct?", len(l) == 4
  print "SparseList accessed correctly?", l[0]==0 and l[2]==-1 and l[3] == 2

  l.sort()
  print "Sorted SparseList size correct?", len(l) == 4
  print "Sorted SparseList accessed correct?", l[0] == -1 and l[1]==0 and l[3] == 2

  l.append(100)
  l.append(-100)
  l.sort()
  print "Resorted SparseList size correct?", len(l) == 6
  print "Resorted SparseList accessed correct?",  l[0] == -100 and l[5]==100


if __name__=="__main__":
  test()

