import sys, os, time
import subprocess
import bashlex
import pyscreenshot
import keyboard
from splinter import Browser
import pyautogui
'''
-------------------------------
    General task functions
-------------------------------
'''

def open_browser():

    b = Browser()
    b.driver.set_window_position(0,0)
    b.driver.set_window_size(1920, 1080)

    return b


def take_screenshot(filename, x1, y1, x2, y2):
    ss = pyscreenshot.grab(bbox=(x1, y1, x2, y2))
    ss.save(filename)


'''
-------------------------------
    Navigation functions
-------------------------------
'''

def gnomad_nav(chrom, pos, ref, alt):
    pass

def dbnsfp_nav(chrom, pos, ref, alt):
    pass

def gerp_nav(chrom, pos, ref, alt):
    pass

def clinvar_missense_nav(browser, gene):

    browser.visit('https://www.ncbi.nlm.nih.gov/clinvar/')
    browser.find_by_id('term').fill(gene)
    browser.find_by_id('search').click()
    browser.find_by_text('Missense').click()


def clinvar_path_nav(browser, gene):

    browser.visit('https://www.ncbi.nlm.nih.gov/clinvar/')
    browser.find_by_id('term').fill(gene)
    browser.find_by_id('search').click()
    browser.find_by_text('Pathogenic').click()
    browser.find_by_text('Likely pathogenic').click()

def hsf_nav(browser, gene, dna_change, transcript):

    browser.visit('http://www.umd.be/HSF3/HSF.shtml')
    browser.driver.find_element_by_xpath("//select[@id='choix_analyse']/option[@value='ssf_batch']").click()
    browser.driver.find_element_by_xpath("//select[@id='choix_bdd']/option[@value='gene_name']").click()
    GeneTextBox = browser.driver.find_element_by_name("champlibre")
    GeneTextBox.click()
    GeneTextBox.send_keys(gene)
    DNAChangeTextBox = browser.driver.find_element_by_name("batch")
    DNAChangeTextBox.click()
    DNAChangeTextBox.send_keys(dna_change)
    Analyze = browser.driver.find_element_by_id("proceed")
    time.sleep(2)
    Analyze.click()
    time.sleep(2)
    try:
        proceed = browser.driver.find_element_by_id("exproceed")
        if proceed.is_displayed and proceed.is_enabled():
            proceed.click()
    except:
        print("Element not visible")

def exac_nav(browser, gene):

    browser.visit('http://exac.broadinstitute.org/')
    browser.find_by_id('home-searchbox-input').fill(gene)


if __name__ == '__main__':

    ## Command line args from VBA


    ## Open browser and take screenshots

    with open_browser() as b:


        # ## ClinVar missense
        # clinvar_missense_nav(b, 'SCN5A')
        # take_screenshot('clinvar_missense.jpg', 2, 180, 193, 796)
        #
        # ## ClinVar P/LP
        # clinvar_path_nav(b, 'SCN5A')
        # take_screenshot('clinvar_plp.jpg', 2, 180, 193, 796)

        ## ExAC
        exac_nav(b, 'SCN5A')
        take_screenshot('exac.jpg', 30, 87, 1185, 389)