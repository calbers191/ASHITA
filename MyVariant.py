import requests
from MyBrowser import MyBrowser


class MyVariant():

    def __init__(self, chr, pos, ref, alt, gene, transcript_id, c_dot, mimNumber):
        self.chr = chr
        self.pos = pos
        self.ref = ref
        self.alt = alt
        self.gene = gene
        self.transcript_id = transcript_id
        self.c_dot = c_dot
        self.mimNumber = mimNumber


    def get_functional_predictions(self):

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token aF31n1tErNi#yVp%j5@j2dL7Pws#xTYSZ8&b64@e'}
        params = {'add-all-data': 1}
        r = requests.get('https://api.varsome.com/lookup/' + self.chr + "-" + self.pos + "-" + self.ref + "-" + self.alt, params=params, headers=headers)

        tolerated = 0
        damaging = 0
        predictions_available = 0

        ## get raw predictions from VarSome API
        try:
            mutation_taster = r.json()['dbnsfp'][0]['mutationtaster_pred'][0]
            if mutation_taster == 'D':
                damaging += 1
            elif mutation_taster == 'N':
                tolerated += 1
            predictions_available += 1
        except:
            mutation_taster = None

        try:
            mutation_assessor = r.json()['dbnsfp'][0]['mutationassessor_pred'][0]
            if mutation_assessor == 'D' or mutation_assessor == 'H':
                damaging += 1
                predictions_available += 1
            elif mutation_assessor == 'N' or mutation_assessor == 'L':
                tolerated += 1
                predictions_available += 1
        except:
            mutation_assessor = None

        try:
            fathmm = r.json()['dbnsfp'][0]['fathmm_pred'][0]
            if fathmm == 'D':
                damaging += 1
            elif fathmm == 'T':
                tolerated += 1
            predictions_available += 1
        except:
            fathmm = None

        try:
            fathmmMKL = r.json()['dbnsfp'][0]['fathmm_mkl_coding_pred'][0]
            if fathmmMKL == 'D':
                damaging += 1
            elif fathmmMKL == 'N':
                tolerated += 1
            predictions_available += 1
        except:
            fathmmMKL = None

        try:
            metaSVM = r.json()['dbnsfp'][0]['metasvm_pred'][0]
            if metaSVM == 'D':
                damaging  += 1
            elif metaSVM == 'T':
                tolerated += 1
            predictions_available += 1
        except:
            metaSVM = None

        try:
            metalR = r.json()['dbnsfp'][0]['metalr_pred'][0]
            if metalR == 'D':
                damaging  += 1
            elif metalR == 'T':
                tolerated += 1
            predictions_available += 1
        except:
            metalR = None

        try:
            provean = r.json()['dbnsfp'][0]['provean_pred'][0]
            if provean == 'D':
                damaging += 1
            elif provean == 'N':
                tolerated += 1
            predictions_available += 1
        except:
            provean = None

        try:
            LRT = r.json()['dbnsfp'][0]['lrt_pred'][0]
            if LRT == 'D':
                damaging += 1
            elif LRT == 'N':
                tolerated += 1
            predictions_available += 1
        except:
            LRT = None

        try:
            sift = r.json()['dbnsfp'][0]['sift_prediction']
            if sift == 'Damaging':
                damaging += 1
                predictions_available += 1
            elif sift == 'Tolerated':
                tolerated += 1
                predictions_available += 1
        except:
            sift = None

        try:
            gerp = r.json()['gerp'][0]['gerp_rs'][0]
            if gerp > 2:
                damaging += 1
            else:
                tolerated += 1
            predictions_available += 1
        except:
            gerp = None

        #print (tolerated, damaging, predictions_available)

        if tolerated > 6:
            return 'tolerated'
        elif damaging > 6:
            return 'damaging'
        else:
            return 'conflicting'


    ## returns true if less than 10% of total missense variants are benign in ClinVar
    def get_pp2(self):

        b = MyBrowser(head=False)
        b.clinvar_missense_nav(self.gene)

        total_missense = b.browser.find_by_xpath('//*[@id="_molConseq"]/li/ul/li[2]/span').value
        total_missense = int(total_missense[1:][:-1])

        benign_missense = b.browser.find_by_xpath('//*[@id="_Properties"]/li/ul/li[2]/span').value
        benign_missense = int(benign_missense[1:][:-1])

        likely_benign_missense = b.browser.find_by_xpath('//*[@id="_Properties"]/li/ul/li[3]/span').value
        likely_benign_missense = int(likely_benign_missense[1:][:-1])

        if (likely_benign_missense + benign_missense) / total_missense < 0.1:
            return True
        else:
            return False


    ## returns true if greater than 90% of pathogenic/likely pathogenic alterations are LOF (frameshift, nonsense, splice site) in ClinVar
    def get_bp1(self):

        b = MyBrowser(head=False)
        b.clinvar_path_nav(self.gene)

        frameshift = b.browser.find_by_xpath('//*[@id="_molConseq"]/li/ul/li[1]/span').value
        frameshift = int(frameshift[1:][:-1])

        missense = b.browser.find_by_xpath('//*[@id="_molConseq"]/li/ul/li[2]/span').value
        missense = int(missense[1:][:-1])

        nonsense = b.browser.find_by_xpath('//*[@id="_molConseq"]/li/ul/li[3]/span').value
        nonsense = int(nonsense[1:][:-1])

        splice_site = b.browser.find_by_xpath('//*[@id="_molConseq"]/li/ul/li[4]/span').value
        splice_site = int(splice_site[1:][:-1])

        if (frameshift + nonsense + splice_site) / (frameshift + missense + nonsense + splice_site) > 0.9:
            return True
        else:
            return False


    ## returns True if any related disease is autosomal dominant in OMIM gene-phenotype relationship table
    def inheritance_is_AD(self):

        apiKey = "PP_ZMQE7SGyxZxXV4baBYQ"
        params = {'mimNumber': self.mimNumber, 'include': 'all', 'format': 'json', 'apiKey': apiKey}
        url = "https://api.omim.org/api/entry"
        r = requests.get(url, params=params)

        if r.ok:
            entry = r.json()['omim']['entryList'][0]['entry']
            if 'geneMap' in entry:
                genemap = entry['geneMap']
                if 'phenotypeMapList' in genemap:
                    inheritance_list = []
                    for phenotype in genemap['phenotypeMapList']:
                        inheritance_list.append(phenotype['phenotypeMap']['phenotypeInheritance'])
                    if 'Autosomal dominant' in inheritance_list:
                        return True
                    else:
                        return False
                else:
                    return 'no OMIM disease'
            else:
                return 'no genemap'
        else:
            return 'request failed'

    ## returns max minor allele frequency of any sub-population in gnomAD genomes or exomes
    def get_max_MAF(self):

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token aF31n1tErNi#yVp%j5@j2dL7Pws#xTYSZ8&b64@e'}
        params = {'add-all-data': 1}
        r = requests.get('https://api.varsome.com/lookup/' + self.chr + "-" + self.pos + "-" + self.ref + "-" + self.alt, params=params, headers=headers)

        max_MAF = 0
        maf_list = []

        if 'gnomad_exomes' in r.json():
            maf_list.append(r.json()['gnomad_exomes'][0]['af_afr'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_amr'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_asj'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_eas'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_fin'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_nfe'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_oth'])
            maf_list.append(r.json()['gnomad_exomes'][0]['af_sas'])

        if 'gnomad_genomes' in r.json():
            maf_list.append(r.json()['gnomad_genomes'][0]['af_afr'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_amr'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_asj'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_eas'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_fin'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_nfe'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_oth'])
            maf_list.append(r.json()['gnomad_genomes'][0]['af_sas'])

        for maf in maf_list:
            if maf > max_MAF:
                max_MAF = maf

        return max_MAF


    ## returns true if any homozygotes exist in gnomAD genomes or exomes
    def homozygotes_exist(self):

        headers = {'Content-Type': 'application/json',
                   'Authorization': 'Token aF31n1tErNi#yVp%j5@j2dL7Pws#xTYSZ8&b64@e'}
        params = {'add-all-data': 1}
        r = requests.get(
            'https://api.varsome.com/lookup/' + self.chr + "-" + self.pos + "-" + self.ref + "-" + self.alt,
            params=params, headers=headers)

        population_list = []

        if 'gnomad_exomes' in r.json():
            population_list.append(r.json()['gnomad_exomes'][0]['hom_afr'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_amr'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_asj'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_eas'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_fin'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_nfe'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_oth'])
            population_list.append(r.json()['gnomad_exomes'][0]['hom_sas'])

        if 'gnomad_genomes' in r.json():
            population_list.append(r.json()['gnomad_genomes'][0]['hom_afr'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_amr'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_asj'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_eas'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_fin'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_nfe'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_oth'])
            population_list.append(r.json()['gnomad_genomes'][0]['hom_sas'])

        for pop in population_list:
            if pop != 0:
                return True
        return False