from MyBrowser import MyBrowser
import os, sys

if __name__ == '__main__':

    ## Command line args from VBA
    # copath_no = sys.argv[1]
    # chr = sys.argv[2]
    # pos = sys.argv[3]
    # ref = sys.argv[4]
    # alt = sys.argv[5]
    # gene = sys.argv[6]
    # transcript_id = sys.argv[7]
    # c_dot = sys.argv[8]

    copath_no = 'M18-10000'
    chr = '1'
    pos = '155209685'
    ref = 'G'
    alt = 'A'
    gene = 'SCN5A'
    transcript_id = 'ENST00000414099'
    c_dot = 'c.5881A>T'

    patient_path = 'screenshots\\' + copath_no
    variant_path = gene + '_' + chr + '_' + pos + '_' + alt + '_' + ref
    screenshot_path = patient_path + '\\' + variant_path

    ## Make directories for patient and variant if they don't already exist
    if not os.path.exists(patient_path):
        os.makedirs(patient_path)
    if not os.path.exists(screenshot_path):
        os.makedirs(screenshot_path)

    ## Open browser and take screenshots
    b = MyBrowser()

    # # gnomAD
    # b.gnomad_nav(chr, pos, ref, alt)
    # b.take_screenshot(screenshot_path, 'gnomAD.jpg', 350, 200, 1600, 900)
    #
    # # dbNSFP
    # b.dbnsfp_nav(chr, pos, ref, alt)
    # b.take_screenshot(screenshot_path, 'dbNSFP.jpg', 270, 170, 670, 1000)
    #
    # # GERP
    # b.gerp_nav(chr, pos, ref, alt)
    # b.take_screenshot(screenshot_path, 'GERP.jpg', 270, 170, 1170, 600)
    #
    # ## ClinVar missense
    # b.clinvar_missense_nav(gene)
    # b.take_screenshot(screenshot_path, 'clinvar_missense.jpg', 5, 290, 193, 886)
    # ## Unclick missense
    # b.browser.find_by_text('Missense').click()
    #
    # ## ClinVar P/LP
    # b.clinvar_path_nav(gene)
    # b.take_screenshot(screenshot_path, 'clinvar_plp.jpg', 5, 290, 193, 886)
    #
    # ## ExAC
    # b.exac_nav(gene)
    # b.take_screenshot(screenshot_path, 'exac.jpg', 36, 200, 1750, 500)

    ## HSF
    b.hsf_nav(c_dot, transcript_id)
    b.take_screenshot(screenshot_path, 'HSF.jpg', 0, 0, 2000, 2000)

    # ## OMIM
    # coords = b.omim_nav('ANKRD11')
    # b.take_screenshot(screenshot_path, 'OMIM.jpg', coords['xCoord'], coords['yCoord'], coords['xCoord'] + coords['width'], coords['yCoord'] + coords['height'])
