import sys, os, time, re
import pyscreenshot
from selenium.webdriver.common.keys import Keys
from splinter import Browser

class MyBrowser():
    def __init__(self):
        self.browser = self.open_browser()

    '''
    -------------------------------
        General task functions
    -------------------------------
    '''

    @staticmethod
    def open_browser():

        b = Browser()
        b.driver.set_window_position(0,0)
        b.driver.set_window_size(1920, 1080)

        return b


    def take_screenshot(self, filepath, filename, x1, y1, x2, y2):
        ss = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        ss.save(filepath + '\\' + filename)

    '''
    -------------------------------
        Navigation functions
    -------------------------------
    '''

    def gnomad_nav(self, chrom, pos, ref, alt):
        self.browser.visit('http://gnomad.broadinstitute.org/variant/' + chrom + '-' + pos + '-' + ref + '-' + alt)

    def dbnsfp_nav(self, chrom, pos, ref, alt):
        self.browser.visit('https://varsome.com/variant/hg19/' + chrom + '-' + pos + '-' + ref + '-' + alt)
        self.browser.find_by_id('agree').click()
        self.browser.find_by_text('Proceed ').click()
        time.sleep(4)
        self.browser.find_by_text('DONE').click()
        self.browser.find_by_text('dbNSFP ').click()
        time.sleep(2)

    def gerp_nav(self, chrom, pos, ref, alt):
        self.browser.find_by_text('Gerp ').click()
        time.sleep(2)

    def clinvar_missense_nav(self, gene):

        self.browser.visit('https://www.ncbi.nlm.nih.gov/clinvar/')
        self.browser.find_by_id('term').fill(gene)
        self.browser.find_by_id('search').click()
        self.browser.find_by_text('Missense').click()


    def clinvar_path_nav(self, gene):

        self.browser.visit('https://www.ncbi.nlm.nih.gov/clinvar/')
        self.browser.find_by_id('term').fill(gene)
        self.browser.find_by_id('search').click()
        self.browser.find_by_text('Pathogenic').click()
        self.browser.find_by_text('Likely pathogenic').click()

    def hsf_nav(self, dna_change, transcript_id):

        self.browser.visit('http://www.umd.be/HSF3/HSF.shtml')
        self.browser.driver.find_element_by_xpath("//select[@id='choix_analyse']/option[@value='ssf_batch']").click()
        self.browser.driver.find_element_by_xpath("//select[@id='choix_bdd']/option[@value='transcript_id']").click()
        self.browser.driver.find_element_by_name("champlibre").send_keys(transcript_id)
        self.browser.driver.find_element_by_name("batch").send_keys(dna_change)
        self.browser.driver.find_element_by_id("proceed").click()
        self.browser.driver.execute_script("document.body.style.zoom='75%'")

    def exac_nav(self, gene):

        self.browser.visit('http://exac.broadinstitute.org/')
        self.browser.find_by_id('home-searchbox-input').fill(gene)
        
        ## Press enter with selenium
        self.browser.driver.find_element_by_id('home-searchbox-input').send_keys(Keys.RETURN)
        
        ## Sleep 1 second until 'gene' contained in URL
        while re.search('gene', self.browser.url) is None:
            time.sleep(1)
        
        time.sleep(5)


    ## Returns width/height of phenotype table
    def omim_nav(self, gene):
        self.browser.visit('http://omim.org/')
        time.sleep(5)
        self.browser.find_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/button').click()
        self.browser.find_by_id('entrySearch').fill(gene)
        time.sleep(2)
        self.browser.find_by_id('omimSearchSubmit').click()
        self.browser.find_by_text(gene).click()
        element = self.browser.driver.find_element_by_xpath("/html/body/div[2]/div[4]/div[1]/div[2]/div[3]/div[5]/div/table")
        print (element.location, element.size)
        return {'xCoord': element.location['x'], 'yCoord': element.location['y'] + 70, 'height': element.size['height'] + 50, 'width': element.size['width']}

