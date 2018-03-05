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


    def take_screenshot(self, filename, x1, y1, x2, y2):
        ss = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
        ss.save(filename)

    '''
    -------------------------------
        Navigation functions
    -------------------------------
    '''

    def gnomad_nav(self, chrom, pos, ref, alt):
        pass

    def dbnsfp_nav(self, chrom, pos, ref, alt):
        pass

    def gerp_nav(self, chrom, pos, ref, alt):
        pass

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

    def hsf_nav(self, gene, dna_change, transcript):

        self.browser.visit('http://www.umd.be/HSF3/HSF.shtml')
        self.browser.driver.find_element_by_xpath("//select[@id='choix_analyse']/option[@value='ssf_batch']").click()
        self.browser.driver.find_element_by_xpath("//select[@id='choix_bdd']/option[@value='gene_name']").click()
        GeneTextBox = self.browser.driver.find_element_by_name("champlibre")
        GeneTextBox.click()
        GeneTextBox.send_keys(gene)
        DNAChangeTextBox = self.browser.driver.find_element_by_name("batch")
        DNAChangeTextBox.click()
        DNAChangeTextBox.send_keys(dna_change)
        Analyze = self.browser.driver.find_element_by_id("proceed")
        time.sleep(2)
        Analyze.click()
        time.sleep(2)
        try:
            proceed = self.browser.driver.find_element_by_id("exproceed")
            if proceed.is_displayed and proceed.is_enabled():
                proceed.click()
        except:
            print("Element not visible")

    def exac_nav(self, gene):

        self.browser.visit('http://exac.broadinstitute.org/')
        self.browser.find_by_id('home-searchbox-input').fill(gene)
        
        ## Press enter with selenium
        self.browser.driver.find_element_by_id('home-searchbox-input').send_keys(Keys.RETURN)
        
        ## Sleep 1 second until 'gene' contained in URL
        while re.search('gene', self.browser.url) is None:
            time.sleep(1)
        
        time.sleep(5)

    def omim_nav(self, gene):
        self.browser.visit('http://omim.org/')
        time.sleep(5)
        self.browser.find_by_xpath('/html/body/div[2]/div[4]/div/div/div[1]/button').click()
        self.browser.find_by_id('entrySearch').fill(gene)
        self.browser.find_by_id('omimSearchSubmit').click()
        self.browser.find_by_text(gene).click()
        element = self.browser.find_by_xpath("/html/body/div[2]/div[4]/div[1]/div[2]/div[3]/div[5]/div/table").first

        return {'width': element['offsetWidth'], 'height': element['offsetHeight']}
