
# IMPORTS
from project_utils import *
from cobra.io import read_sbml_model 
from cobra.flux_analysis import single_gene_deletion

def main():
    # Loading the model and presenting its summary
    model = read_sbml_model('iYS854.xml')

    # Change model objective function to the one recommended in the article
    model.objective = 'BIOMASS_iYS_reduced'
    model.reactions.get_by_id('BIOMASS_iYS_reduced').upper_bound = 1000

    # Get model essential genes
    with model: # first prepare the medium
        give_essential = model.medium

        give_essential['EX_arg__L_e'] = 10.0
        give_essential['EX_gly_e'] = 10.0
        give_essential['EX_leu__L_e'] = 10.0
        give_essential['EX_pro__L_e'] = 10.0
        give_essential['EX_val__L_e'] = 10.0

        model.medium = give_essential
        deletion_results = single_gene_deletion(model)

    essential_genes_provided = []
    for i in range(len(deletion_results.index)):
        if deletion_results.at[i, 'growth'] < 0.0001 or deletion_results.at[i, 'status'] != 'optimal':
            essential_genes_provided.append(deletion_results.at[i, 'ids'])

    essential_genes = trim(convert_gene_name(essential_genes_provided))
    write_gene_list(essential_genes,'essential_gene_list.txt')

    # Prepare files for BLAST
    prot_gnf, nuc_gnf = write_fasta(essential_genes)

if __name__ == '__main__':
    main()