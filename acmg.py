from MyVariant import MyVariant
import sys

if __name__ == '__main__':

    ## Command line args
    # copath_no = sys.argv[1]
    # chr = sys.argv[2]
    # pos = sys.argv[3]
    # ref = sys.argv[4]
    # alt = sys.argv[5]
    # gene = sys.argv[6]
    # transcript_id = sys.argv[7]
    # c_dot = sys.argv[8]

    copath_no = 'M18-10000'
    chr = '17'
    pos = '72281284'
    ref = 'C'
    alt = 'T'
    gene = 'DNAI2'
    transcript_id = 'ENST00000414099'
    c_dot = 'c.5881A>T'
    mimNumber = '605483'

    variant = MyVariant(chr, pos, ref, alt, gene, transcript_id, c_dot, mimNumber)

    ## evaluate BP4/PP3
    fxn_pred = variant.get_functional_predictions()
    if fxn_pred == 'tolerated':
        print('BP4')
    elif fxn_pred == 'damaging':
        print('PP3')

    ## evaluate BP1
    if variant.get_bp1() == True:
        print('BP1')

    ## evaluate PP2
    if variant.get_pp2() == True:
        print('PP2')

    ## evaluate PM2
    max_MAF = variant.get_max_MAF()
    inheritance_is_AD = variant.inheritance_is_AD()
    if max_MAF == 0:
        print('PM2')
    elif inheritance_is_AD == False and max_MAF < 0.001:
        print('PM2')

    ## evaluate BS2
    homozygotes_exist = variant.homozygotes_exist()
    if inheritance_is_AD == True and max_MAF > 0:
        print('BS2')
    elif inheritance_is_AD == False and homozygotes_exist == True:
        print('BS2')


    