import argparse
import re

version = '1.0.0'

##Make a UI

parser = argparse.ArgumentParser(prog='''Convert Museq vcf to counts''',
                                 description = '''Generates the tumour_counts from vcf generated by titan_preprocess component
                                                 of MutationSeq''')

parser.add_argument("-i","--infile", 
                    required = True, 
                    help= '''The vcf files generated by museq''')

parser.add_argument("-o","--outfile", 
                    required = True, 
                    help="The path to the counts file")

parser.add_argument("--positions_file",
                    default = None,
                    help="If provided, all positions that aren't in the file will be filtered out.")
args = parser.parse_args()


class transformVcfCounts(object):
    def __init__(self):
        self.args = args
        self.outfile = open(self.args.outfile, 'w')

        #write header
        self.outfile.write('chr\tposition\tref\trefCount\tNref\tNrefCount\n')
        
    def read_ref_positions(self):
        if not self.args.positions_file:
            return

        ref_pos = set()
        freader = open(self.args.positions_file)
        for line in freader:
           line = line.strip().split(':')

           ref_pos.add(tuple(line))

        return ref_pos

    def main(self, ref_pos):
        infile_stream = open(self.args.infile)
        for line in infile_stream:
            if line[0] == '#':
                continue
            line = line.strip().split()
            chrom = line[0]
            pos  = line[1]
            ref = line[3]
            tr = re.split(';|=',line[7])[3]
            ta = re.split(';|=',line[7])[5]
            #ndp = re.split(';|=',line[7])[13]
            
            if ref_pos and (chrom, pos) in ref_pos:
                continue

            outstr = '\t'.join([chrom,pos,ref,tr,'X',ta]) + '\n'
            self.outfile.write(outstr)
        self.outfile.close()
        infile_stream.close()
        
#---------------------------------------------
#  Main Program
#---------------------------------------------
if __name__ == '__main__':
    vcf_to_counts = transformVcfCounts()
    ref_pos = vcf_to_counts.read_ref_positions()
    vcf_to_counts.main(ref_pos)
    
