
# IMPORTS
from project_utils import *
import json

# CONSTANTS
BLASTP_RESULTS = 'blastp_results_web.xml'
BLASTN_RESULTS = 'blastn_results_web.xml'
EMAIL_BRENDA = "sysbioproject@gmail.com"
PASSWORD_BRENDA = 'brendavalidation'

# DOMAIN FUNCTIONS

def main():

    # Use blast results to  filter our targets
    protein_targets = filter_drug_targets(BLASTP_RESULTS)
    gene_targets = filter_drug_targets(BLASTN_RESULTS)
    write_gene_list(protein_targets,'protein_targets.txt')
    write_gene_list(gene_targets,'gene_targets.txt')

    # Only consider drug targets present in both protein and gene targets
    drug_targets = [x for x in protein_targets if x in gene_targets]

    ec_numbers = {}
    for gene in drug_targets:
        ec_n = get_ec_numbers(gene)
        if ec_n != 'not_found' and ec_n != 'no_ec_numbers':
            ec_numbers[gene] = ec_n
        
    inhibitors = clean_up_inhibs(get_all_inhibitors(ec_numbers,EMAIL_BRENDA,PASSWORD_BRENDA))
    
    write_drug_bank_fasta(inhibitors)

    return inhibitors

if __name__ == '__main__':
    inhibitors = main()
    print('List of inhibitors: ')
    print(json.dumps(inhibitors, indent=4))
    

