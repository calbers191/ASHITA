from MyBrowser import MyBrowser

if __name__ == '__main__':

    ## Command line args from VBA


    ## Open browser and take screenshots
    b = MyBrowser()

    # ## ClinVar missense
    # b.clinvar_missense_nav('SCN5A')
    # b.take_screenshot('clinvar_missense.jpg', 2, 180, 193, 796)
    # b.browser.find_by_text('Missense').click()
    #
    # ## ClinVar P/LP
    # b.clinvar_path_nav('SCN5A')
    # b.take_screenshot('clinvar_plp.jpg', 2, 180, 193, 796)

    # ## HSF
    # b.hsf_nav('SCN5A', 'c.5881C>T', 'ENST00000414099')
    # b.take_screenshot('HSF.jpg', 0, 0, 2000, 2000)

    # ## ExAC
    # b.exac_nav('SCN5A')
    # b.take_screenshot('exac.jpg', 36, 82, 1696, 386)

    # ## OMIM
    # coords = b.omim_nav('SCN5A')
    # b.take_screenshot('OMIM.jpg', )
