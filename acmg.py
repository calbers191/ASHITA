from MyVariant import MyVariant

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

    criteria = []

    ## evaluate BP4/PP3
    fxn_pred = variant.get_functional_predictions()
    if fxn_pred == 'tolerated':
        criteria.append('BP4')
    elif fxn_pred == 'damaging':
        criteria.append('PP3')

    ## evaluate BP1
    if variant.get_bp1() == True:
        criteria.append('BP1')

    ## evaluate PP2
    if variant.get_pp2() == True:
        criteria.append('PP2')

    ## evaluate PM2
    max_MAF = variant.get_max_MAF()
    inheritance_is_AD = variant.inheritance_is_AD()
    if max_MAF == 0:
        criteria.append('PM2')
    elif inheritance_is_AD == False and max_MAF < 0.001:
        criteria.append('PM2')

    ## evaluate BS2
    homozygotes_exist = variant.homozygotes_exist()
    if inheritance_is_AD == True and max_MAF > 0:
        criteria.append('BS2')
    elif inheritance_is_AD == False and homozygotes_exist == True:
        criteria.append('BS2')

    output_file = open('acmg_classifications_%s.txt' % (copath_no), 'a')
    output_file.write('%s\t%s\t%s\t%s\t%s' % (variant.chr, variant.pos, variant.ref, variant.alt, criteria))
    output_file.close()