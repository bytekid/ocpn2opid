import sys
import json
import getopt

from opid import OPID

def print_pnml(opid, outdir, outname):
  with open(outdir + outname + ".pnml", "w") as f:
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write(opid.to_pnml().toprettyxml())
    f.close()


usage = "ocpn2opid.py [-R <relationpairs>]"

def process_args(argv):
  relations = None
  try:
    opts, args = getopt.getopt(argv,"R:")
  except getopt.GetoptError:
    print(usage)
    sys.exit(2)
  for (opt, arg) in opts:
    if opt == "-R":
      relations = arg
    else:
      print(usage)
      sys.exit()
  return relations

def parse_relations(relstr):
  def fail():
    print("Unexpected format of relations string, expected [(m1:o1),...,(mn:on)]")
    sys.exit(2)

  if not (relstr[0] == "[" and relstr[-1] == "]"):
    fail()
  relpairs = relstr[1:-1].split(",")
  rels = []
  for p in relpairs:
    if not (p[0] == "(" and p[-1] == ")"):
      fail()
    otypes = p[1:-1].split(":")
    if len(otypes) != 2:
      fail()
    rels.append(tuple(otypes))
  return rels


def run(input, relations, outdir="./", outname = "out"):
  with open(input, "r") as ifile:
    ocpn = json.loads(ifile.read())
    opid = OPID.from_ocpn_json(ocpn)
  if relations:
    opid.add_many_to_one_syncs(parse_relations(relations))
  opid.to_dot(outdir, outname)
  print_pnml(opid, outdir, outname)


if __name__ == "__main__":
  if len(sys.argv) < 2:
    print(usage)
    sys.exit(2)
  relations = process_args(sys.argv[1:-1])
  input = sys.argv[-1]
  run(input, relations)
  

